# PiWardrive Docker Deployment Guide

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Images](#docker-images)
- [Single Container Deployment](#single-container-deployment)
- [Multi-Container Deployment](#multi-container-deployment)
- [Raspberry Pi Deployment](#raspberry-pi-deployment)
- [Production Deployment](#production-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Configuration Management](#configuration-management)
- [Data Persistence](#data-persistence)
- [Networking](#networking)
- [Security](#security)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

## Overview

PiWardrive supports multiple Docker deployment strategies to accommodate different use cases, from single-device deployments to distributed multi-node clusters. This guide covers all deployment scenarios with complete configuration examples.

### Deployment Options

- **All-in-One Container**: Single container with all services
- **Multi-Container**: Separate containers for API, database, and services  
- **Kubernetes**: Cloud-native orchestration with auto-scaling
- **Docker Swarm**: Multi-node container orchestration
- **Raspberry Pi**: ARM-optimized containers for edge deployment

```mermaid
graph TB
    A[Docker Deployment Options] --> B[All-in-One Container]
    A --> C[Multi-Container Setup]
    A --> D[Kubernetes Cluster]
    A --> E[Docker Swarm]
    A --> F[Raspberry Pi Edge]
    
    B --> B1[Single Container<br/>All Services]
    B --> B2[SQLite Database<br/>Local Storage]
    B --> B3[Quick Setup<br/>Development]
    
    C --> C1[API Container]
    C --> C2[Database Container]
    C --> C3[Redis Cache]
    C --> C4[Grafana Dashboard]
    
    D --> D1[Pod Orchestration]
    D --> D2[Auto-scaling]
    D --> D3[Load Balancing]
    D --> D4[Service Discovery]
    
    E --> E1[Multi-node Cluster]
    E --> E2[Container Orchestration]
    E --> E3[High Availability]
    E --> E4[Rolling Updates]
    
    F --> F1[ARM64 Containers]
    F --> F2[Low Resource Usage]
    F --> F3[Edge Computing]
    F --> F4[Offline Capability]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#ffebee
```

## Prerequisites

### System Requirements

**Minimum Requirements:**
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB RAM (4GB recommended)
- 16GB storage (32GB recommended)
- Linux kernel with Wi-Fi monitor mode support

**For Raspberry Pi:**
- Raspberry Pi 3B+ or newer
- Raspberry Pi OS Lite (64-bit recommended)
- External Wi-Fi adapter with monitor mode support

### Software Installation

#### Docker Engine Installation

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Raspberry Pi OS:**
```bash
# Install Docker using convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Reboot to ensure all changes take effect
sudo reboot
```

#### Verify Installation

```bash
# Check Docker version
docker --version
docker compose version

# Test Docker installation
docker run hello-world
```

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/username/piwardrive.git
cd piwardrive
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Basic .env Configuration:**
```bash
# Application Settings
PIWARDRIVE_API_PORT=8080
PIWARDRIVE_LOG_LEVEL=INFO
PIWARDRIVE_SECRET_KEY=your-very-secure-secret-key-here

# Database Configuration
PIWARDRIVE_DATABASE_URL=sqlite:///data/piwardrive.db

# Wi-Fi Interface
PIWARDRIVE_WIFI_INTERFACE=wlan0

# Authentication
PIWARDRIVE_API_USER=admin
PIWARDRIVE_API_PASSWORD=change-this-password

# Optional Services
PIWARDRIVE_REDIS_ENABLED=false
PIWARDRIVE_INFLUXDB_ENABLED=false
```

### 3. Deploy with Docker Compose

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### 4. Access the Application

- **Web Dashboard**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **Enhanced Docs**: http://localhost:8080/api-docs

## Docker Images

### Official Images

PiWardrive provides multi-architecture images supporting AMD64 and ARM64:

```bash
# Latest stable release
docker pull piwardrive/piwardrive:latest

# Specific version
docker pull piwardrive/piwardrive:v1.0.0

# Architecture-specific
docker pull piwardrive/piwardrive:latest-arm64
docker pull piwardrive/piwardrive:latest-amd64

# Development builds
docker pull piwardrive/piwardrive:dev
```

### Image Variants

| Image | Description | Size | Use Case |
|-------|-------------|------|----------|
| `piwardrive:latest` | Full featured image | ~500MB | Production, development |
| `piwardrive:slim` | Minimal dependencies | ~200MB | Resource-constrained environments |
| `piwardrive:alpine` | Alpine Linux base | ~150MB | Minimal footprint |
| `piwardrive:gpu` | GPU acceleration support | ~800MB | ML/AI workloads |
| `piwardrive:pi` | Raspberry Pi optimized | ~300MB | Edge deployment |

### Building Custom Images

```dockerfile
# Dockerfile.custom
FROM piwardrive/piwardrive:latest

# Add custom dependencies
RUN apt-get update && apt-get install -y \
    your-custom-package \
    && rm -rf /var/lib/apt/lists/*

# Copy custom configuration
COPY custom-config.yaml /etc/piwardrive/

# Set custom environment
ENV PIWARDRIVE_CUSTOM_SETTING=value

# Use custom entrypoint
COPY custom-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/custom-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/custom-entrypoint.sh"]
```

```bash
# Build custom image
docker build -f Dockerfile.custom -t piwardrive:custom .

# Run custom image
docker run -d --name piwardrive-custom piwardrive:custom
```

## Single Container Deployment

### All-in-One Docker Compose

```yaml
# docker-compose.simple.yml
version: '3.8'

services:
  piwardrive:
    image: piwardrive/piwardrive:latest
    container_name: piwardrive
    restart: unless-stopped
    
    # Privileged mode for Wi-Fi interface access
    privileged: true
    network_mode: host
    
    # Environment configuration
    environment:
      - PIWARDRIVE_API_PORT=8080
      - PIWARDRIVE_LOG_LEVEL=INFO
      - PIWARDRIVE_WIFI_INTERFACE=wlan0
      - PIWARDRIVE_DATABASE_URL=sqlite:///data/piwardrive.db
      - PIWARDRIVE_SECRET_KEY=${PIWARDRIVE_SECRET_KEY}
    
    # Volume mounts
    volumes:
      - piwardrive_data:/data
      - piwardrive_logs:/var/log/piwardrive
      - ./config:/etc/piwardrive:ro
      - /dev:/dev:ro  # Device access for Wi-Fi adapters
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/v1/system/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '2.0'
        reservations:
          memory: 512M
          cpus: '1.0'

volumes:
  piwardrive_data:
    driver: local
  piwardrive_logs:
    driver: local
```

### Run Single Container

```bash
# Using Docker Compose
docker compose -f docker-compose.simple.yml up -d

# Using Docker run
docker run -d \
  --name piwardrive \
  --restart unless-stopped \
  --privileged \
  --network host \
  -e PIWARDRIVE_API_PORT=8080 \
  -e PIWARDRIVE_WIFI_INTERFACE=wlan0 \
  -e PIWARDRIVE_SECRET_KEY=your-secret-key \
  -v piwardrive_data:/data \
  -v piwardrive_logs:/var/log/piwardrive \
  -v /dev:/dev:ro \
  piwardrive/piwardrive:latest
```

## Multi-Container Deployment

### Container Architecture Overview

```mermaid
graph TB
    LB[Load Balancer] --> API[API Container]
    API --> DB[(PostgreSQL Database)]
    API --> REDIS[(Redis Cache)]
    API --> SCANNER[Scanner Service]
    
    SCANNER --> WLAN[Wi-Fi Interface<br/>Monitor Mode]
    SCANNER --> GPS[GPS Device]
    
    API --> GRAFANA[Grafana Dashboard]
    GRAFANA --> INFLUX[(InfluxDB)]
    
    API --> WEB[Web Interface]
    WEB --> USERS[Users/Browsers]
    
    subgraph "Docker Network: piwardrive-internal"
        API
        DB
        REDIS
        SCANNER
        INFLUX
    end
    
    subgraph "Docker Network: piwardrive-external"
        LB
        GRAFANA
        WEB
    end
    
    subgraph "Host Hardware"
        WLAN
        GPS
    end
    
    style API fill:#e1f5fe
    style DB fill:#e8f5e8
    style REDIS fill:#fff3e0
    style SCANNER fill:#fce4ec
    style GRAFANA fill:#f3e5f5
    style INFLUX fill:#ffebee
```

### Service Dependencies

```mermaid
graph LR
    A[piwardrive-api] --> B[piwardrive-db]
    A --> C[piwardrive-redis]
    A --> D[piwardrive-scanner]
    E[piwardrive-grafana] --> F[piwardrive-influxdb]
    E --> A
    G[piwardrive-nginx] --> A
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#ffebee
    style G fill:#e0f2f1
```

### Complete Multi-Service Stack

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Main API and Web Interface
  piwardrive-api:
    image: piwardrive/api:latest
    container_name: piwardrive-api
    restart: unless-stopped
    depends_on:
      - piwardrive-db
      - piwardrive-redis
    
    environment:
      - PIWARDRIVE_API_HOST=0.0.0.0
      - PIWARDRIVE_API_PORT=8080
      - PIWARDRIVE_DATABASE_URL=postgresql://piwardrive:${DB_PASSWORD}@piwardrive-db:5432/piwardrive
      - PIWARDRIVE_REDIS_URL=redis://piwardrive-redis:6379/0  # Enables Redis caching
      - PIWARDRIVE_SECRET_KEY=${PIWARDRIVE_SECRET_KEY}
      - PIWARDRIVE_LOG_LEVEL=INFO
    
    ports:
      - "8080:8080"
    
    volumes:
      - piwardrive_data:/data
      - piwardrive_logs:/var/log/piwardrive
      - ./config/api.yaml:/etc/piwardrive/config.yaml:ro
    
    networks:
      - piwardrive-internal
      - piwardrive-external
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/v1/system/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Wi-Fi Scanner Service
  piwardrive-scanner:
    image: piwardrive/scanner:latest
    container_name: piwardrive-scanner
    restart: unless-stopped
    privileged: true  # Required for Wi-Fi monitor mode
    
    environment:
      - PIWARDRIVE_WIFI_INTERFACE=wlan0
      - PIWARDRIVE_REDIS_URL=redis://piwardrive-redis:6379/0  # Enables Redis caching
      - PIWARDRIVE_LOG_LEVEL=INFO
    
    volumes:
      - /dev:/dev:ro
      - piwardrive_scanner_data:/data
      - ./config/scanner.yaml:/etc/piwardrive/scanner.yaml:ro
    
    networks:
      - piwardrive-internal
    
    depends_on:
      - piwardrive-redis

  # System Monitor Service
  piwardrive-monitor:
    image: piwardrive/monitor:latest
    container_name: piwardrive-monitor
    restart: unless-stopped
    
    environment:
      - PIWARDRIVE_REDIS_URL=redis://piwardrive-redis:6379/0
      - PIWARDRIVE_MONITOR_INTERVAL=30
      - PIWARDRIVE_LOG_LEVEL=INFO
    
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
      - piwardrive_monitor_data:/data
    
    networks:
      - piwardrive-internal
    
    depends_on:
      - piwardrive-redis

  # PostgreSQL Database
  piwardrive-db:
    image: postgres:15-alpine
    container_name: piwardrive-db
    restart: unless-stopped
    
    environment:
      - POSTGRES_DB=piwardrive
      - POSTGRES_USER=piwardrive
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    
    volumes:
      - piwardrive_db_data:/var/lib/postgresql/data
      - ./config/postgres.conf:/etc/postgresql/postgresql.conf:ro
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    
    networks:
      - piwardrive-internal
    
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U piwardrive -d piwardrive"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  piwardrive-redis:
    image: redis:7-alpine
    container_name: piwardrive-redis
    restart: unless-stopped
    
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    
    volumes:
      - piwardrive_redis_data:/data
      - ./config/redis.conf:/etc/redis/redis.conf:ro
    
    networks:
      - piwardrive-internal
    
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # InfluxDB (Optional Time Series Database)
  piwardrive-influxdb:
    image: influxdb:2.7-alpine
    container_name: piwardrive-influxdb
    restart: unless-stopped
    profiles: ["influxdb"]  # Optional service
    
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUXDB_PASSWORD}
      - DOCKER_INFLUXDB_INIT_ORG=piwardrive
      - DOCKER_INFLUXDB_INIT_BUCKET=metrics
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=${INFLUXDB_TOKEN}
    
    ports:
      - "8086:8086"
    
    volumes:
      - piwardrive_influxdb_data:/var/lib/influxdb2
      - piwardrive_influxdb_config:/etc/influxdb2
    
    networks:
      - piwardrive-internal

  # Nginx Reverse Proxy
  piwardrive-nginx:
    image: nginx:alpine
    container_name: piwardrive-nginx
    restart: unless-stopped
    
    ports:
      - "80:80"
      - "443:443"
    
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./config/ssl:/etc/nginx/ssl:ro
      - piwardrive_nginx_logs:/var/log/nginx
    
    networks:
      - piwardrive-external
      - piwardrive-internal
    
    depends_on:
      - piwardrive-api

volumes:
  piwardrive_data:
  piwardrive_logs:
  piwardrive_scanner_data:
  piwardrive_monitor_data:
  piwardrive_db_data:
  piwardrive_redis_data:
  piwardrive_influxdb_data:
  piwardrive_influxdb_config:
  piwardrive_nginx_logs:

networks:
  piwardrive-internal:
    driver: bridge
    internal: true
  piwardrive-external:
    driver: bridge
```

### Environment Variables File

```bash
# .env
# Database Configuration
DB_PASSWORD=secure-database-password-here

# Application Security
PIWARDRIVE_SECRET_KEY=your-very-secure-secret-key-minimum-32-characters

# InfluxDB Configuration (if enabled)
INFLUXDB_PASSWORD=secure-influxdb-password
INFLUXDB_TOKEN=your-influxdb-admin-token

# Optional Settings
COMPOSE_PROFILES=influxdb  # Enable optional services
```

### Deploy Multi-Container Stack

```bash
# Start core services
docker compose up -d

# Start with optional services (InfluxDB)
COMPOSE_PROFILES=influxdb docker compose up -d

# Scale specific services
docker compose up -d --scale piwardrive-scanner=2

# Check status
docker compose ps
docker compose logs -f piwardrive-api
```

## Raspberry Pi Deployment

### Raspberry Pi Specific Configuration

```yaml
# docker-compose.pi.yml
version: '3.8'

services:
  piwardrive-pi:
    image: piwardrive/piwardrive:pi
    container_name: piwardrive-pi
    restart: unless-stopped
    privileged: true
    network_mode: host
    
    environment:
      - PIWARDRIVE_API_PORT=8080
      - PIWARDRIVE_WIFI_INTERFACE=wlan0
      - PIWARDRIVE_LOG_LEVEL=INFO
      - PIWARDRIVE_DATABASE_URL=sqlite:///data/piwardrive.db
      - PIWARDRIVE_MONITOR_TEMPERATURE=true
      - PIWARDRIVE_GPIO_ENABLED=true
      - PIWARDRIVE_PERFORMANCE_MODE=low_power
    
    volumes:
      - piwardrive_data:/data
      - piwardrive_logs:/var/log/piwardrive
      - /dev:/dev:ro
      - /sys:/sys:ro
      - /proc:/proc:ro
      - ./config/pi.yaml:/etc/piwardrive/config.yaml:ro
    
    # Resource constraints for Pi
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '2.0'
        reservations:
          memory: 256M
          cpus: '1.0'
    
    # Pi-specific health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/v1/system/health"]
      interval: 60s
      timeout: 15s
      retries: 3
      start_period: 120s

volumes:
  piwardrive_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /opt/piwardrive/data  # Use faster storage if available

  piwardrive_logs:
    driver: local
```

### Pi-Specific Configuration File

```yaml
# config/pi.yaml
app:
  host: "0.0.0.0"
  port: 8080
  log_level: "INFO"
  performance_mode: "low_power"

wifi:
  interface: "wlan0"
  scan_interval: 120  # Longer intervals for battery life
  monitor_mode: true
  auto_channel_hop: true

monitoring:
  interval: 60  # Less frequent monitoring
  enabled_metrics:
    cpu: true
    memory: true
    disk: true
    temperature: true
    gpio: true
  
  # Pi-specific thresholds
  thresholds:
    temperature_warning: 65.0
    temperature_critical: 75.0
    cpu_warning: 85.0
    cpu_critical: 95.0

performance:
  workers: 1  # Single worker for Pi
  memory:
    max_memory_per_worker: "256MB"
  
  caching:
    enabled: true
    backend: "memory"
    max_entries: 1000

# GPIO Configuration (Pi-specific)
gpio:
  enabled: true
  pins:
    status_led: 18
    buzzer: 12
    button: 16
  
  # LED status indicators
  status_indicators:
    scanning: "blink_green"
    error: "solid_red"
    normal: "solid_green"

# Battery Management (for portable setups)
battery:
  monitoring: true
  low_battery_threshold: 20.0
  critical_battery_threshold: 10.0
  power_saving_mode: true
```

### Raspberry Pi Setup Script

```bash
#!/bin/bash
# setup-pi.sh - Raspberry Pi deployment script

set -e

echo "Setting up PiWardrive on Raspberry Pi..."

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
    git \
    curl \
    htop \
    vim \
    wireless-tools \
    aircrack-ng

# Install Docker (if not already installed)
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Install Docker Compose
sudo apt-get install -y docker-compose-plugin

# Create directories
sudo mkdir -p /opt/piwardrive/{data,logs,config}
sudo chown -R $USER:$USER /opt/piwardrive

# Clone repository
cd /opt/piwardrive
git clone https://github.com/username/piwardrive.git .

# Copy Pi-specific configuration
cp config/examples/pi.yaml config/pi.yaml
cp docker-compose.pi.yml docker-compose.yml

# Set up environment
cp .env.example .env
echo "Please edit /opt/piwardrive/.env with your configuration"

# Enable Wi-Fi monitor mode support
echo "Checking Wi-Fi adapter capabilities..."
sudo airmon-ng check

# Set up systemd service
sudo tee /etc/systemd/system/piwardrive.service > /dev/null <<EOF
[Unit]
Description=PiWardrive Wi-Fi Analysis System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/piwardrive
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable piwardrive.service

echo "Setup complete! Please:"
echo "1. Edit /opt/piwardrive/.env"
echo "2. Configure your Wi-Fi interface in config/pi.yaml"
echo "3. Start with: sudo systemctl start piwardrive"
echo "4. Access dashboard at: http://$(hostname -I | awk '{print $1}'):8080"
```

## Production Deployment

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  piwardrive-api:
    image: piwardrive/api:${PIWARDRIVE_VERSION:-latest}
    restart: always
    depends_on:
      - piwardrive-db
      - piwardrive-redis
    
    environment:
      - PIWARDRIVE_ENV=production
      - PIWARDRIVE_DEBUG=false
      - PIWARDRIVE_LOG_LEVEL=WARNING
      - PIWARDRIVE_DATABASE_URL=postgresql://piwardrive:${DB_PASSWORD}@piwardrive-db:5432/piwardrive
      - PIWARDRIVE_REDIS_URL=redis://piwardrive-redis:6379/0  # Enables Redis caching
      - PIWARDRIVE_SECRET_KEY=${PIWARDRIVE_SECRET_KEY}
      - PIWARDRIVE_CORS_ORIGINS=${PIWARDRIVE_CORS_ORIGINS}
    
    volumes:
      - piwardrive_data:/data
      - piwardrive_logs:/var/log/piwardrive
      - /etc/ssl/certs:/etc/ssl/certs:ro
    
    networks:
      - piwardrive-internal
    
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
      restart_policy:
        condition: any
        delay: 5s
        max_attempts: 3
        window: 120s
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/v1/system/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  piwardrive-db:
    image: postgres:15-alpine
    restart: always
    
    environment:
      - POSTGRES_DB=piwardrive
      - POSTGRES_USER=piwardrive
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    
    volumes:
      - piwardrive_db_data:/var/lib/postgresql/data
      - ./config/postgres-prod.conf:/etc/postgresql/postgresql.conf:ro
    
    networks:
      - piwardrive-internal
    
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'

  piwardrive-redis:
    image: redis:7-alpine
    restart: always
    
    command: >
      redis-server
      --appendonly yes
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
      --requirepass ${REDIS_PASSWORD}
    
    volumes:
      - piwardrive_redis_data:/data
    
    networks:
      - piwardrive-internal

  piwardrive-nginx:
    image: nginx:alpine
    restart: always
    
    ports:
      - "80:80"
      - "443:443"
    
    volumes:
      - ./config/nginx-prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - piwardrive_nginx_logs:/var/log/nginx
    
    networks:
      - piwardrive-external
      - piwardrive-internal
    
    depends_on:
      - piwardrive-api

volumes:
  piwardrive_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /opt/piwardrive/data

  piwardrive_db_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /opt/piwardrive/postgres

  piwardrive_redis_data:
    driver: local

  piwardrive_logs:
    driver: local

  piwardrive_nginx_logs:
    driver: local

networks:
  piwardrive-internal:
    driver: overlay
    attachable: true
    internal: true
  
  piwardrive-external:
    driver: overlay
    attachable: true

configs:
  nginx_config:
    file: ./config/nginx-prod.conf
  
secrets:
  db_password:
    external: true
  redis_password:
    external: true
  jwt_secret:
    external: true
```

### Production Environment

```bash
# .env.production
PIWARDRIVE_VERSION=v1.0.0
PIWARDRIVE_ENV=production

# Security
PIWARDRIVE_SECRET_KEY=your-production-secret-key-minimum-32-characters
PIWARDRIVE_CORS_ORIGINS=https://piwardrive.yourdomain.com,https://dashboard.yourdomain.com

# Database
DB_PASSWORD=secure-production-database-password
REDIS_PASSWORD=secure-production-redis-password

# Monitoring
PIWARDRIVE_LOG_LEVEL=WARNING
PIWARDRIVE_METRICS_ENABLED=true
```

### Production Nginx Configuration

```nginx
# config/nginx-prod.conf
events {
    worker_connections 1024;
}

http {
    upstream piwardrive_backend {
        least_conn;
        server piwardrive-api:8080 max_fails=3 fail_timeout=30s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=1r/s;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    server {
        listen 80;
        server_name piwardrive.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name piwardrive.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://piwardrive_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Authentication endpoints
        location ~ ^/(token|auth)/ {
            limit_req zone=auth burst=5 nodelay;
            
            proxy_pass http://piwardrive_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket endpoints
        location /ws/ {
            proxy_pass http://piwardrive_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            proxy_pass http://piwardrive_backend;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Main application
        location / {
            proxy_pass http://piwardrive_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## Kubernetes Deployment

### Kubernetes Manifests

#### Namespace and Configuration

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: piwardrive
  labels:
    name: piwardrive

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: piwardrive-config
  namespace: piwardrive
data:
  config.yaml: |
    app:
      host: "0.0.0.0"
      port: 8080
      log_level: "INFO"
    
    database:
      url: "postgresql://piwardrive:$(DB_PASSWORD)@piwardrive-postgres:5432/piwardrive"
      pool_size: 20
    
    redis:
      url: "redis://piwardrive-redis:6379/0"
    
    wifi:
      interface: "wlan0"
      scan_interval: 60

---
apiVersion: v1
kind: Secret
metadata:
  name: piwardrive-secrets
  namespace: piwardrive
type: Opaque
stringData:
  db-password: "secure-database-password"
  redis-password: "secure-redis-password"
  jwt-secret: "your-jwt-secret-key"
```

#### Database Deployment

```yaml
# k8s/postgres.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: piwardrive-postgres
  namespace: piwardrive
spec:
  serviceName: piwardrive-postgres
  replicas: 1
  selector:
    matchLabels:
      app: piwardrive-postgres
  template:
    metadata:
      labels:
        app: piwardrive-postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_DB
          value: piwardrive
        - name: POSTGRES_USER
          value: piwardrive
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: piwardrive-secrets
              key: db-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi

---
apiVersion: v1
kind: Service
metadata:
  name: piwardrive-postgres
  namespace: piwardrive
spec:
  selector:
    app: piwardrive-postgres
  ports:
  - port: 5432
    targetPort: 5432
  clusterIP: None
```

#### Redis Deployment

```yaml
# k8s/redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: piwardrive-redis
  namespace: piwardrive
spec:
  replicas: 1
  selector:
    matchLabels:
      app: piwardrive-redis
  template:
    metadata:
      labels:
        app: piwardrive-redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        command:
        - redis-server
        - --appendonly
        - "yes"
        - --maxmemory
        - "512mb"
        - --maxmemory-policy
        - "allkeys-lru"
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: piwardrive-redis
  namespace: piwardrive
spec:
  selector:
    app: piwardrive-redis
  ports:
  - port: 6379
    targetPort: 6379

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: piwardrive
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

#### Main Application Deployment

```yaml
# k8s/api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: piwardrive-api
  namespace: piwardrive
spec:
  replicas: 3
  selector:
    matchLabels:
      app: piwardrive-api
  template:
    metadata:
      labels:
        app: piwardrive-api
    spec:
      containers:
      - name: piwardrive-api
        image: piwardrive/api:latest
        ports:
        - containerPort: 8080
        env:
        - name: PIWARDRIVE_DATABASE_URL
          value: "postgresql://piwardrive:$(DB_PASSWORD)@piwardrive-postgres:5432/piwardrive"
        - name: PIWARDRIVE_REDIS_URL
          value: "redis://piwardrive-redis:6379/0"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: piwardrive-secrets
              key: db-password
        - name: PIWARDRIVE_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: piwardrive-secrets
              key: jwt-secret
        volumeMounts:
        - name: config
          mountPath: /etc/piwardrive
        - name: data
          mountPath: /data
        livenessProbe:
          httpGet:
            path: /api/v1/system/health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/system/health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: config
        configMap:
          name: piwardrive-config
      - name: data
        persistentVolumeClaim:
          claimName: piwardrive-data-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: piwardrive-api
  namespace: piwardrive
spec:
  selector:
    app: piwardrive-api
  ports:
  - port: 8080
    targetPort: 8080
  type: ClusterIP

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: piwardrive-data-pvc
  namespace: piwardrive
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

#### Ingress Configuration

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: piwardrive-ingress
  namespace: piwardrive
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - piwardrive.yourdomain.com
    secretName: piwardrive-tls
  rules:
  - host: piwardrive.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: piwardrive-api
            port:
              number: 8080
```

#### Horizontal Pod Autoscaler

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: piwardrive-api-hpa
  namespace: piwardrive
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: piwardrive-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deploy to Kubernetes

```bash
# Create namespace and secrets
kubectl apply -f k8s/namespace.yaml

# Deploy database and cache
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml

# Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=piwardrive-postgres -n piwardrive --timeout=300s

# Deploy main application
kubectl apply -f k8s/api.yaml

# Set up ingress and autoscaling
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# Check deployment status
kubectl get all -n piwardrive
kubectl logs -f deployment/piwardrive-api -n piwardrive
```

## Configuration Management

### Environment-Specific Configurations

#### Docker Override Files

```yaml
# docker-compose.override.yml (for development)
version: '3.8'

services:
  piwardrive-api:
    environment:
      - PIWARDRIVE_DEBUG=true
      - PIWARDRIVE_LOG_LEVEL=DEBUG
    volumes:
      - ./src:/app/src:ro  # Mount source code for development
    ports:
      - "8080:8080"
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

  piwardrive-db:
    ports:
      - "5432:5432"  # Expose database port for development

  piwardrive-redis:
    ports:
      - "6379:6379"  # Expose Redis port for development
```

```yaml
# docker-compose.staging.yml
version: '3.8'

services:
  piwardrive-api:
    image: piwardrive/api:staging
    environment:
      - PIWARDRIVE_ENV=staging
      - PIWARDRIVE_LOG_LEVEL=INFO
    deploy:
      replicas: 2
```

#### Configuration Templates

```bash
# scripts/generate-config.sh
#!/bin/bash

ENVIRONMENT=${1:-development}
CONFIG_DIR="config/$ENVIRONMENT"

mkdir -p "$CONFIG_DIR"

# Generate API configuration
envsubst < config/templates/api.yaml.template > "$CONFIG_DIR/api.yaml"

# Generate database configuration
envsubst < config/templates/postgres.conf.template > "$CONFIG_DIR/postgres.conf"

# Generate Nginx configuration
envsubst < config/templates/nginx.conf.template > "$CONFIG_DIR/nginx.conf"

echo "Configuration generated for $ENVIRONMENT environment"
```

### Secrets Management

#### Docker Secrets

```bash
# Create Docker secrets
echo "secure-db-password" | docker secret create db_password -
echo "secure-jwt-secret" | docker secret create jwt_secret -

# Use in compose file
```

```yaml
# docker-compose.secrets.yml
version: '3.8'

services:
  piwardrive-api:
    secrets:
      - db_password
      - jwt_secret
    environment:
      - PIWARDRIVE_DATABASE_PASSWORD_FILE=/run/secrets/db_password
      - PIWARDRIVE_JWT_SECRET_FILE=/run/secrets/jwt_secret

secrets:
  db_password:
    external: true
  jwt_secret:
    external: true
```

#### Kubernetes Secrets

```bash
# Create Kubernetes secrets
kubectl create secret generic piwardrive-secrets \
  --from-literal=db-password=secure-db-password \
  --from-literal=jwt-secret=secure-jwt-secret \
  -n piwardrive

# Or from files
kubectl create secret generic piwardrive-secrets \
  --from-file=db-password=./secrets/db-password.txt \
  --from-file=jwt-secret=./secrets/jwt-secret.txt \
  -n piwardrive
```

## Data Persistence

### Volume Management

#### Named Volumes

```yaml
# Persistent named volumes
volumes:
  piwardrive_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/piwardrive/data

  piwardrive_db:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/piwardrive/postgres
```

#### Backup Strategies

```bash
#!/bin/bash
# backup.sh - Database backup script

BACKUP_DIR="/opt/piwardrive/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup PostgreSQL
docker exec piwardrive-db pg_dump -U piwardrive piwardrive | gzip > "$BACKUP_DIR/postgres_$TIMESTAMP.sql.gz"

# Backup data directory
tar -czf "$BACKUP_DIR/data_$TIMESTAMP.tar.gz" -C /opt/piwardrive data

# Backup Redis (optional)
docker exec piwardrive-redis redis-cli BGSAVE
docker cp piwardrive-redis:/data/dump.rdb "$BACKUP_DIR/redis_$TIMESTAMP.rdb"

# Cleanup old backups (keep last 7 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.rdb" -mtime +7 -delete

echo "Backup completed: $TIMESTAMP"
```

#### Restore Procedures

```bash
#!/bin/bash
# restore.sh - Database restore script

BACKUP_FILE=$1
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop services
docker compose down

# Restore PostgreSQL
gunzip -c "$BACKUP_FILE" | docker exec -i piwardrive-db psql -U piwardrive -d piwardrive

# Restore data directory
tar -xzf "data_backup.tar.gz" -C /opt/piwardrive

# Start services
docker compose up -d

echo "Restore completed"
```

## Networking

### Network Configuration

#### Custom Bridge Networks

```yaml
# Custom network configuration
networks:
  piwardrive-frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  
  piwardrive-backend:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.21.0.0/16
```

#### Host Network Mode

```yaml
# For Wi-Fi monitor mode access
services:
  piwardrive-scanner:
    network_mode: host
    privileged: true
```

#### Port Mapping

```yaml
# Port configuration
services:
  piwardrive-api:
    ports:
      - "8080:8080"          # HTTP API
      - "8443:8443"          # HTTPS API
    expose:
      - "8080"               # Internal port
```

### Load Balancing

#### Nginx Load Balancer

```nginx
upstream piwardrive_backend {
    least_conn;
    server piwardrive-api-1:8080 weight=1 max_fails=3 fail_timeout=30s;
    server piwardrive-api-2:8080 weight=1 max_fails=3 fail_timeout=30s;
    server piwardrive-api-3:8080 weight=1 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://piwardrive_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### HAProxy Configuration

```
# haproxy.cfg
global
    daemon

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend piwardrive_frontend
    bind *:80
    default_backend piwardrive_servers

backend piwardrive_servers
    balance roundrobin
    server api1 piwardrive-api-1:8080 check
    server api2 piwardrive-api-2:8080 check
    server api3 piwardrive-api-3:8080 check
```

## Security

### Container Security

#### Security Context

```yaml
services:
  piwardrive-api:
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"  # Non-root user
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to privileged ports
```

#### Network Security

```yaml
# Restrict network access
networks:
  piwardrive-internal:
    driver: bridge
    internal: true  # No external access
    driver_opts:
      com.docker.network.bridge.enable_icc: "false"
```

### SSL/TLS Configuration

#### Certificate Management

```bash
# Generate self-signed certificates (development only)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=piwardrive.local"

# Or use Let's Encrypt (production)
certbot certonly --standalone \
    -d piwardrive.yourdomain.com \
    --email your@email.com \
    --agree-tos
```

#### Certificate Renewal

```bash
#!/bin/bash
# renew-certs.sh - Automatic certificate renewal

# Renew certificates
certbot renew --quiet

# Reload Nginx
docker exec piwardrive-nginx nginx -s reload

# Log renewal
echo "$(date): Certificates renewed" >> /var/log/cert-renewal.log
```

```cron
# Crontab entry for automatic renewal
0 2 * * * /opt/piwardrive/scripts/renew-certs.sh
```

## Monitoring & Logging

### Health Monitoring

#### Docker Health Checks

```yaml
services:
  piwardrive-api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/api/v1/system/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

#### External Monitoring

```yaml
# Prometheus monitoring
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Centralized Logging

#### ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    volumes:
      - ./config/logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
```

#### Log Aggregation

```yaml
# Fluentd log driver
services:
  piwardrive-api:
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: piwardrive.api
```

## Troubleshooting

### Common Issues

#### Permission Problems

```bash
# Fix volume permissions
sudo chown -R 1000:1000 /opt/piwardrive/data
sudo chmod -R 755 /opt/piwardrive/data

# Check container user
docker exec piwardrive-api id

# Fix SELinux contexts (if applicable)
sudo setsebool -P container_manage_cgroup true
sudo chcon -Rt svirt_sandbox_file_t /opt/piwardrive/data
```

#### Network Connectivity

```bash
# Test container networking
docker exec piwardrive-api ping piwardrive-db
docker exec piwardrive-api nslookup piwardrive-db

# Check port bindings
docker port piwardrive-api
netstat -tlnp | grep 8080

# Inspect networks
docker network ls
docker network inspect piwardrive_piwardrive-internal
```

#### Resource Issues

```bash
# Check resource usage
docker stats

# Check logs for OOM kills
journalctl -u docker.service | grep -i "killed process"

# Monitor disk usage
docker system df
docker system prune -a  # Clean up unused resources
```

#### Database Connection Issues

```bash
# Test database connectivity
docker exec piwardrive-db psql -U piwardrive -d piwardrive -c "SELECT 1;"

# Check database logs
docker logs piwardrive-db

# Reset database
docker exec piwardrive-db psql -U piwardrive -d piwardrive -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Debugging Tools

#### Container Debugging

```bash
# Execute shell in container
docker exec -it piwardrive-api /bin/bash

# Debug networking
docker exec piwardrive-api netstat -tlnp
docker exec piwardrive-api ss -tlnp

# Check processes
docker exec piwardrive-api ps aux

# Monitor logs in real-time
docker logs -f piwardrive-api
```

#### Performance Analysis

```bash
# Container resource usage
docker stats --no-stream

# Process monitoring
docker exec piwardrive-api top
docker exec piwardrive-api htop

# Disk I/O monitoring
docker exec piwardrive-api iotop

# Network monitoring
docker exec piwardrive-api iftop
```

## Performance Optimization

### Resource Limits

#### Memory Optimization

```yaml
services:
  piwardrive-api:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
    environment:
      - PIWARDRIVE_WORKERS=2  # Limit workers
      - PIWARDRIVE_MAX_CONNECTIONS=100
```

#### CPU Optimization

```yaml
services:
  piwardrive-api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
        reservations:
          cpus: '1.0'
    cpus: 2.0  # Docker run equivalent
```

### Caching Strategies

#### Redis Caching

```yaml
services:
  piwardrive-redis:
    command: >
      redis-server
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
      --save 900 1
      --save 300 10
      --save 60 10000
```

#### Application Caching

```yaml
services:
  piwardrive-api:
    environment:
      - PIWARDRIVE_CACHE_ENABLED=true
      - PIWARDRIVE_CACHE_TTL=300
      - PIWARDRIVE_CACHE_MAX_SIZE=1000
```
The API automatically uses Redis for caching when `PIWARDRIVE_REDIS_URL` is set.

### Database Optimization

#### PostgreSQL Tuning

```postgresql
-- config/postgres-optimized.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

### Network Optimization

#### Connection Pooling

```yaml
services:
  piwardrive-api:
    environment:
      - PIWARDRIVE_DB_POOL_SIZE=20
      - PIWARDRIVE_DB_MAX_OVERFLOW=30
      - PIWARDRIVE_DB_POOL_TIMEOUT=30
```

#### Keep-Alive Settings

```nginx
# Nginx optimization
http {
    keepalive_timeout 65;
    keepalive_requests 100;
    
    upstream piwardrive_backend {
        server piwardrive-api:8080;
        keepalive 32;
    }
}
```

This comprehensive Docker deployment guide provides everything needed to successfully deploy PiWardrive in any environment, from single Raspberry Pi devices to large-scale Kubernetes clusters. The configurations are production-ready and include best practices for security, monitoring, and performance optimization.
