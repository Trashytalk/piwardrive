#!/bin/bash
# Blue-Green Deployment Script for PiWardrive
# This script implements zero-downtime deployment using blue-green strategy

set -euo pipefail

# Configuration
DEPLOYMENT_TAG="${1:-latest}"
BLUE_SERVICE="piwardrive-blue"
GREEN_SERVICE="piwardrive-green"
LOAD_BALANCER="piwardrive-lb"
HEALTH_CHECK_URL="http://localhost:8080/health"
TIMEOUT=300
ROLLBACK_TIMEOUT=60

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

# Check if service is running
is_service_running() {
    local service_name=$1
    if docker-compose ps | grep -q "$service_name.*Up"; then
        return 0
    else
        return 1
    fi
}

# Health check function
health_check() {
    local service_url=$1
    local max_attempts=30
    local attempt=0
    
    log_info "Performing health check on $service_url"
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f -s --max-time 5 "$service_url" > /dev/null 2>&1; then
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

# Determine current active service
get_active_service() {
    if is_service_running "$BLUE_SERVICE"; then
        echo "blue"
    elif is_service_running "$GREEN_SERVICE"; then
        echo "green"
    else
        echo "none"
    fi
}

# Switch traffic to specified service
switch_traffic() {
    local target_service=$1
    local target_color=$2
    
    log_info "Switching traffic to $target_color environment"
    
    # Update load balancer configuration
    if [ "$target_color" = "blue" ]; then
        export ACTIVE_SERVICE="$BLUE_SERVICE"
        export ACTIVE_PORT=8080
    else
        export ACTIVE_SERVICE="$GREEN_SERVICE"
        export ACTIVE_PORT=8081
    fi
    
    # Update load balancer
    envsubst < docker-compose.lb.template.yml > docker-compose.lb.yml
    docker-compose -f docker-compose.lb.yml up -d "$LOAD_BALANCER"
    
    # Wait for load balancer to update
    sleep 10
    
    # Verify traffic switch
    if health_check "$HEALTH_CHECK_URL"; then
        log_info "Traffic successfully switched to $target_color"
        return 0
    else
        log_error "Failed to switch traffic to $target_color"
        return 1
    fi
}

# Deploy to inactive environment
deploy_to_inactive() {
    local inactive_service=$1
    local inactive_color=$2
    
    log_info "Deploying new version to $inactive_color environment"
    
    # Stop inactive service
    docker-compose stop "$inactive_service" 2>/dev/null || true
    docker-compose rm -f "$inactive_service" 2>/dev/null || true
    
    # Pull new image
    docker pull "piwardrive:$DEPLOYMENT_TAG"
    
    # Start inactive service with new image
    if [ "$inactive_color" = "blue" ]; then
        export SERVICE_IMAGE="piwardrive:$DEPLOYMENT_TAG"
        export SERVICE_PORT=8080
        docker-compose -f docker-compose.blue.yml up -d "$BLUE_SERVICE"
    else
        export SERVICE_IMAGE="piwardrive:$DEPLOYMENT_TAG"
        export SERVICE_PORT=8081
        docker-compose -f docker-compose.green.yml up -d "$GREEN_SERVICE"
    fi
    
    # Wait for service to start
    sleep 15
    
    # Health check on inactive service
    local inactive_url="http://localhost:${SERVICE_PORT}/health"
    if health_check "$inactive_url"; then
        log_info "New deployment is healthy on $inactive_color"
        return 0
    else
        log_error "New deployment failed health check on $inactive_color"
        return 1
    fi
}

# Rollback function
rollback() {
    local rollback_service=$1
    local rollback_color=$2
    
    log_warn "Initiating rollback to $rollback_color environment"
    
    if switch_traffic "$rollback_service" "$rollback_color"; then
        log_info "Rollback completed successfully"
        return 0
    else
        log_error "Rollback failed"
        return 1
    fi
}

# Main deployment function
main() {
    log_info "Starting blue-green deployment with tag: $DEPLOYMENT_TAG"
    
    # Check if Docker and docker-compose are available
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Determine current active service
    local active_service=$(get_active_service)
    
    if [ "$active_service" = "none" ]; then
        log_info "No active service found, starting initial deployment"
        # Initial deployment to blue
        if deploy_to_inactive "$BLUE_SERVICE" "blue"; then
            switch_traffic "$BLUE_SERVICE" "blue"
        else
            log_error "Initial deployment failed"
            exit 1
        fi
    else
        log_info "Current active service: $active_service"
        
        # Determine inactive service
        local inactive_service
        local inactive_color
        if [ "$active_service" = "blue" ]; then
            inactive_service="$GREEN_SERVICE"
            inactive_color="green"
        else
            inactive_service="$BLUE_SERVICE"
            inactive_color="blue"
        fi
        
        log_info "Deploying to inactive environment: $inactive_color"
        
        # Deploy to inactive environment
        if deploy_to_inactive "$inactive_service" "$inactive_color"; then
            # Switch traffic to new deployment
            if switch_traffic "$inactive_service" "$inactive_color"; then
                log_info "Deployment successful"
                
                # Stop old service after successful deployment
                local old_service
                if [ "$inactive_color" = "blue" ]; then
                    old_service="$GREEN_SERVICE"
                else
                    old_service="$BLUE_SERVICE"
                fi
                
                log_info "Stopping old service: $old_service"
                docker-compose stop "$old_service"
                
            else
                log_error "Failed to switch traffic, initiating rollback"
                rollback "$active_service" "$active_service"
                exit 1
            fi
        else
            log_error "Deployment to inactive environment failed"
            exit 1
        fi
    fi
    
    log_info "Blue-green deployment completed successfully"
}

# Trap signals for cleanup
trap 'log_error "Deployment interrupted"; exit 1' INT TERM

# Run main function
main "$@"
