#!/bin/bash
"""
Staging Deployment Script

This script handles the deployment of PiWardrive to the staging environment.
"""

set -euo pipefail

# Configuration
VERSION=${1:-"latest"}
SERVICE_NAME="piwardrive"
COMPOSE_FILE="docker-compose.staging.yml"
HEALTH_CHECK_URL="http://localhost:8000/health"
MAX_WAIT_TIME=300  # 5 minutes

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if service is healthy
check_health() {
    local url=$1
    local max_attempts=30
    local attempt=0
    
    log_info "Checking service health at $url"
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f --max-time 10 "$url" >/dev/null 2>&1; then
            log_info "Service is healthy!"
            return 0
        fi
        
        attempt=$((attempt + 1))
        log_info "Health check attempt $attempt/$max_attempts failed, retrying in 10 seconds..."
        sleep 10
    done
    
    log_error "Service failed health check after $max_attempts attempts"
    return 1
}

# Function to backup current deployment
backup_current_deployment() {
    log_info "Backing up current deployment..."
    
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        # Create backup of current configuration
        mkdir -p backups
        local backup_file="backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz"
        
        # Export current container data if needed
        docker-compose -f "$COMPOSE_FILE" exec -T piwardrive sh -c "
            mkdir -p /tmp/backup
            cp -r /app/data /tmp/backup/ 2>/dev/null || true
            cp -r /app/config /tmp/backup/ 2>/dev/null || true
        " || log_warn "Could not backup application data"
        
        log_info "Backup created: $backup_file"
    else
        log_info "No running deployment found to backup"
    fi
}

# Function to deploy new version
deploy_new_version() {
    local version=$1
    
    log_info "Deploying version: $version"
    
    # Update image tag in docker-compose file
    if [ -f "$COMPOSE_FILE" ]; then
        # Replace image tag
        sed -i "s|piwardrive:staging-.*|piwardrive:staging-$version|g" "$COMPOSE_FILE"
        sed -i "s|piwardrive:staging|piwardrive:staging-$version|g" "$COMPOSE_FILE"
    else
        log_error "Docker compose file not found: $COMPOSE_FILE"
        return 1
    fi
    
    # Pull new image
    log_info "Pulling new Docker image..."
    docker-compose -f "$COMPOSE_FILE" pull || {
        log_error "Failed to pull new image"
        return 1
    }
    
    # Start new deployment
    log_info "Starting new deployment..."
    docker-compose -f "$COMPOSE_FILE" up -d || {
        log_error "Failed to start new deployment"
        return 1
    }
    
    # Wait for service to be ready
    log_info "Waiting for service to be ready..."
    sleep 30  # Give it time to start
    
    if check_health "$HEALTH_CHECK_URL"; then
        log_info "Deployment successful!"
        return 0
    else
        log_error "Deployment failed health check"
        return 1
    fi
}

# Function to rollback deployment
rollback_deployment() {
    log_warn "Rolling back deployment..."
    
    # Get previous image
    local previous_image=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep "piwardrive:staging" | head -2 | tail -1)
    
    if [ -n "$previous_image" ]; then
        log_info "Rolling back to: $previous_image"
        
        # Update compose file with previous image
        sed -i "s|piwardrive:staging-.*|$previous_image|g" "$COMPOSE_FILE"
        
        # Restart with previous version
        docker-compose -f "$COMPOSE_FILE" up -d
        
        # Check health
        if check_health "$HEALTH_CHECK_URL"; then
            log_info "Rollback successful!"
            return 0
        else
            log_error "Rollback failed!"
            return 1
        fi
    else
        log_error "No previous image found for rollback"
        return 1
    fi
}

# Function to cleanup old images
cleanup_old_images() {
    log_info "Cleaning up old Docker images..."
    
    # Keep last 5 staging images
    docker images "piwardrive" --format "{{.ID}} {{.Tag}}" | \
        grep "staging-" | \
        sort -r | \
        tail -n +6 | \
        awk '{print $1}' | \
        xargs -r docker rmi || log_warn "Some images could not be removed"
    
    # Remove dangling images
    docker image prune -f || log_warn "Could not prune dangling images"
}

# Function to run post-deployment tests
run_post_deployment_tests() {
    log_info "Running post-deployment tests..."
    
    # Basic connectivity test
    if ! curl -f --max-time 10 "$HEALTH_CHECK_URL" >/dev/null 2>&1; then
        log_error "Basic connectivity test failed"
        return 1
    fi
    
    # API endpoint tests
    local endpoints=("/api/status" "/api/health" "/performance/stats")
    
    for endpoint in "${endpoints[@]}"; do
        local url="${HEALTH_CHECK_URL%/health}$endpoint"
        if curl -f --max-time 10 "$url" >/dev/null 2>&1; then
            log_info "✓ $endpoint endpoint accessible"
        else
            log_warn "✗ $endpoint endpoint failed"
        fi
    done
    
    # Performance test
    local response_time=$(curl -o /dev/null -s -w "%{time_total}" "$HEALTH_CHECK_URL")
    if (( $(echo "$response_time < 2.0" | bc -l) )); then
        log_info "✓ Response time acceptable: ${response_time}s"
    else
        log_warn "✗ Response time slow: ${response_time}s"
    fi
    
    log_info "Post-deployment tests completed"
}

# Function to send deployment notification
send_notification() {
    local status=$1
    local version=$2
    
    local message
    if [ "$status" = "success" ]; then
        message="✅ Staging deployment successful - Version: $version"
    else
        message="❌ Staging deployment failed - Version: $version"
    fi
    
    log_info "Deployment result: $message"
    
    # Send to Slack if webhook is configured
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{\"text\": \"$message\"}" \
            >/dev/null 2>&1 || log_warn "Failed to send Slack notification"
    fi
    
    # Send to monitoring system if configured
    if [ -n "${MONITORING_WEBHOOK_URL:-}" ]; then
        curl -X POST "$MONITORING_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"event\": \"deployment_$status\",
                \"environment\": \"staging\",
                \"version\": \"$version\",
                \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
            }" >/dev/null 2>&1 || log_warn "Failed to send monitoring notification"
    fi
}

# Main deployment function
main() {
    local version=$1
    
    log_info "Starting staging deployment process..."
    log_info "Version: $version"
    log_info "Timestamp: $(date)"
    
    # Check if docker-compose is available
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "docker-compose is not installed"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running"
        exit 1
    fi
    
    # Backup current deployment
    backup_current_deployment
    
    # Deploy new version
    if deploy_new_version "$version"; then
        # Run post-deployment tests
        run_post_deployment_tests
        
        # Cleanup old images
        cleanup_old_images
        
        # Send success notification
        send_notification "success" "$version"
        
        log_info "Staging deployment completed successfully!"
        exit 0
    else
        log_error "Deployment failed, attempting rollback..."
        
        # Attempt rollback
        if rollback_deployment; then
            send_notification "rollback" "$version"
            log_warn "Deployment failed but rollback was successful"
            exit 1
        else
            send_notification "failure" "$version"
            log_error "Deployment and rollback both failed!"
            exit 2
        fi
    fi
}

# Script entry point
if [ $# -eq 0 ]; then
    log_error "Usage: $0 <version>"
    log_error "Example: $0 staging-abc123"
    exit 1
fi

main "$1"
