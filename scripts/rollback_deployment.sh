#!/bin/bash
# Rollback Deployment Script for PiWardrive
# This script handles automated rollback to previous versions

set -euo pipefail

# Configuration
PREVIOUS_VERSION="${1:-}"
ROLLBACK_TIMEOUT=300
HEALTH_CHECK_URL="http://localhost:8080/health"
BACKUP_DIR="/opt/piwardrive/backups"
LOG_FILE="/var/log/piwardrive/rollback.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1"
    echo -e "${GREEN}$message${NC}"
    echo "$message" >> "$LOG_FILE"
}

log_warn() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1"
    echo -e "${YELLOW}$message${NC}"
    echo "$message" >> "$LOG_FILE"
}

log_error() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1"
    echo -e "${RED}$message${NC}"
    echo "$message" >> "$LOG_FILE"
}

# Health check function
health_check() {
    local url=$1
    local max_attempts=30
    local attempt=0
    
    log_info "Performing health check on $url"
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f -s --max-time 5 "$url" > /dev/null 2>&1; then
            log_info "Health check passed"
            return 0
        fi
        
        attempt=$((attempt + 1))
        log_warn "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 5
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Get current version
get_current_version() {
    if docker ps | grep -q piwardrive; then
        docker inspect piwardrive | jq -r '.[0].Config.Labels["version"]' 2>/dev/null || echo "unknown"
    else
        echo "no-service"
    fi
}

# Get available versions for rollback
get_available_versions() {
    log_info "Available versions for rollback:"
    
    # Check Docker images
    echo "Docker images:"
    docker images piwardrive --format "table {{.Tag}}\t{{.CreatedAt}}" | head -10
    
    # Check backup directory
    if [ -d "$BACKUP_DIR" ]; then
        echo -e "\nBackup versions:"
        ls -la "$BACKUP_DIR" | grep -E "piwardrive-.*\.tar\.gz$" | tail -10
    fi
}

# Backup current state before rollback
backup_current_state() {
    log_info "Creating backup of current state"
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
    
    # Get current version
    local current_version=$(get_current_version)
    local backup_file="$BACKUP_DIR/piwardrive-pre-rollback-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    # Export current Docker image
    if [ "$current_version" != "no-service" ]; then
        docker save piwardrive:latest | gzip > "$backup_file"
        log_info "Current state backed up to $backup_file"
    fi
    
    # Backup configuration
    if [ -f "docker-compose.yml" ]; then
        cp docker-compose.yml "$BACKUP_DIR/docker-compose-$(date +%Y%m%d-%H%M%S).yml"
    fi
    
    # Backup environment variables
    if [ -f ".env" ]; then
        cp .env "$BACKUP_DIR/.env-$(date +%Y%m%d-%H%M%S)"
    fi
}

# Rollback using Docker image
rollback_docker() {
    local version=$1
    
    log_info "Rolling back to Docker image version: $version"
    
    # Stop current service
    log_info "Stopping current service"
    docker-compose down --timeout 30
    
    # Pull or use existing image
    if docker image inspect "piwardrive:$version" &> /dev/null; then
        log_info "Using existing Docker image: piwardrive:$version"
    else
        log_info "Pulling Docker image: piwardrive:$version"
        if ! docker pull "piwardrive:$version"; then
            log_error "Failed to pull Docker image: piwardrive:$version"
            return 1
        fi
    fi
    
    # Update docker-compose.yml to use specific version
    if [ -f "docker-compose.yml" ]; then
        sed -i.bak "s|image: piwardrive:.*|image: piwardrive:$version|g" docker-compose.yml
        log_info "Updated docker-compose.yml to use version $version"
    fi
    
    # Start service with rollback version
    log_info "Starting service with rollback version"
    docker-compose up -d
    
    # Wait for service to start
    sleep 15
    
    # Health check
    if health_check "$HEALTH_CHECK_URL"; then
        log_info "Rollback successful - service is healthy"
        return 0
    else
        log_error "Rollback failed - service is not healthy"
        return 1
    fi
}

# Rollback using Kubernetes (if applicable)
rollback_kubernetes() {
    local version=$1
    
    log_info "Rolling back Kubernetes deployment to version: $version"
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        return 1
    fi
    
    # Rollback deployment
    if kubectl set image deployment/piwardrive piwardrive="piwardrive:$version"; then
        log_info "Kubernetes deployment image updated"
    else
        log_error "Failed to update Kubernetes deployment image"
        return 1
    fi
    
    # Wait for rollback to complete
    if kubectl rollout status deployment/piwardrive --timeout=300s; then
        log_info "Kubernetes rollback completed"
    else
        log_error "Kubernetes rollback failed or timed out"
        return 1
    fi
    
    # Verify rollback
    local service_url="http://$(kubectl get service piwardrive -o jsonpath='{.spec.clusterIP}')/health"
    if health_check "$service_url"; then
        log_info "Kubernetes rollback successful - service is healthy"
        return 0
    else
        log_error "Kubernetes rollback failed - service is not healthy"
        return 1
    fi
}

# Emergency rollback (uses last known good backup)
emergency_rollback() {
    log_warn "Initiating emergency rollback"
    
    # Find latest backup
    local latest_backup=$(ls -t "$BACKUP_DIR"/piwardrive-*.tar.gz 2>/dev/null | head -1)
    
    if [ -z "$latest_backup" ]; then
        log_error "No backup found for emergency rollback"
        return 1
    fi
    
    log_info "Using emergency backup: $latest_backup"
    
    # Stop current service
    docker-compose down --timeout 30 || true
    
    # Load backup image
    docker load < "$latest_backup"
    
    # Start service
    docker-compose up -d
    
    # Wait and check health
    sleep 15
    if health_check "$HEALTH_CHECK_URL"; then
        log_info "Emergency rollback successful"
        return 0
    else
        log_error "Emergency rollback failed"
        return 1
    fi
}

# Send notification
send_notification() {
    local status=$1
    local version=$2
    
    # Slack notification
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        local message
        if [ "$status" = "success" ]; then
            message="✅ Rollback to version $version completed successfully"
        else
            message="❌ Rollback to version $version failed"
        fi
        
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{\"text\": \"$message\"}" || true
    fi
    
    # Email notification (if configured)
    if [ -n "${EMAIL_RECIPIENT:-}" ] && command -v mail &> /dev/null; then
        local subject="PiWardrive Rollback $status"
        local body="Rollback to version $version $status at $(date)"
        echo "$body" | mail -s "$subject" "$EMAIL_RECIPIENT" || true
    fi
}

# Main rollback function
main() {
    log_info "Starting rollback process"
    
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Check if version is provided
    if [ -z "$PREVIOUS_VERSION" ]; then
        log_error "No version specified for rollback"
        echo "Usage: $0 <version>"
        echo "Available versions:"
        get_available_versions
        exit 1
    fi
    
    # Special handling for emergency rollback
    if [ "$PREVIOUS_VERSION" = "emergency" ]; then
        if emergency_rollback; then
            send_notification "success" "emergency"
            log_info "Emergency rollback completed"
            exit 0
        else
            send_notification "failed" "emergency"
            log_error "Emergency rollback failed"
            exit 1
        fi
    fi
    
    # Backup current state
    backup_current_state
    
    # Determine rollback method
    local rollback_success=false
    
    # Try Docker rollback first
    if rollback_docker "$PREVIOUS_VERSION"; then
        rollback_success=true
    # Try Kubernetes rollback if Docker fails
    elif command -v kubectl &> /dev/null; then
        log_warn "Docker rollback failed, trying Kubernetes rollback"
        if rollback_kubernetes "$PREVIOUS_VERSION"; then
            rollback_success=true
        fi
    fi
    
    # Report results
    if [ "$rollback_success" = true ]; then
        send_notification "success" "$PREVIOUS_VERSION"
        log_info "Rollback to version $PREVIOUS_VERSION completed successfully"
        exit 0
    else
        send_notification "failed" "$PREVIOUS_VERSION"
        log_error "Rollback to version $PREVIOUS_VERSION failed"
        
        # Offer emergency rollback
        read -p "Would you like to attempt emergency rollback? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            emergency_rollback
        fi
        
        exit 1
    fi
}

# Trap signals for cleanup
trap 'log_error "Rollback interrupted"; exit 1' INT TERM

# Run main function
main "$@"
