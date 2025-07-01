WORKING FILE !!!   NOT YET COMPLETE !!!!

# PiWardrive Production Deployment Guide

## Table of Contents
- [Overview](#overview)
- [Architecture Planning](#architecture-planning)
- [Infrastructure Requirements](#infrastructure-requirements)
- [Security Hardening](#security-hardening)
- [High Availability Setup](#high-availability-setup)
- [Load Balancing](#load-balancing)
- [Database Configuration](#database-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Backup and Recovery](#backup-and-recovery)
- [Performance Optimization](#performance-optimization)
- [Scaling Strategies](#scaling-strategies)
- [Maintenance Procedures](#maintenance-procedures)
- [Troubleshooting](#troubleshooting)
- [Compliance and Auditing](#compliance-and-auditing)

## Overview

This guide covers deploying PiWardrive in production environments, from single-site installations to large-scale distributed networks. It addresses enterprise requirements including security, scalability, monitoring, and compliance.

### Production Deployment Types

- **Single Site Enterprise** - Centralized deployment for large organizations
- **Multi-Site Distributed** - Geographic distribution with central management
- **Cloud-Native** - Kubernetes orchestration with auto-scaling
- **Hybrid Edge** - Edge devices with cloud coordination
- **Compliance-Ready** - Regulated industry deployments

### Key Production Requirements

- **High Availability** (99.9%+ uptime)
- **Scalability** (1000+ concurrent users)
- **Security** (Enterprise-grade protection)
- **Monitoring** (Real-time observability)
- **Compliance** (Audit trails and data protection)

## Architecture Planning

### Reference Architectures

#### 1. Single Site Enterprise

```
┌─────────────────────────────────────────────────────────────┐
│                    Enterprise Network                        │
├─────────────────────────────────────────────────────────────┤
│  Load Balancer (HAProxy/NGINX)                              │
│  ├── API Node 1 (Active)                                    │
│  ├── API Node 2 (Standby)                                   │
│  └── API Node 3 (Standby)                                   │
├─────────────────────────────────────────────────────────────┤
│  Database Cluster                                           │
│  ├── PostgreSQL Primary                                     │
│  ├── PostgreSQL Replica 1                                   │
│  └── PostgreSQL Replica 2                                   │
├─────────────────────────────────────────────────────────────┤
│  Cache Layer                                                │
│  ├── Redis Cluster Node 1                                   │
│  ├── Redis Cluster Node 2                                   │
│  └── Redis Cluster Node 3                                   │
├─────────────────────────────────────────────────────────────┤
│  Monitoring Stack                                           │
│  ├── Prometheus + Grafana                                   │
│  ├── ELK Stack (Logs)                                       │
│  └── Alert Manager                                          │
└─────────────────────────────────────────────────────────────┘
```

#### 2. Multi-Site Distributed

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Site A (HQ)   │    │   Site B        │    │   Site C        │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │Central Mgmt │ │    │ │Local Scanner│ │    │ │Local Scanner│ │
│ │+ Database   │ │◄───┤ │+ Local Cache│ │    │ │+ Local Cache│ │
│ │+ Analytics  │ │    │ │             │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────── VPN/MPLS ────┴───────────────────────┘
```

#### 3. Cloud-Native Kubernetes

```yaml
# High-level Kubernetes architecture
apiVersion: v1
kind: Namespace
metadata:
  name: piwardrive-prod

---
# API Deployment with HPA
apiVersion: apps/v1
kind: Deployment
metadata:
  name: piwardrive-api
  namespace: piwardrive-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: piwardrive-api
  template:
    spec:
      containers:
      - name: api
        image: piwardrive/api:v1.0.0
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
# Database StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-cluster
  namespace: piwardrive-prod
spec:
  serviceName: postgres
  replicas: 3
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### Capacity Planning

#### Hardware Requirements

| Component | Small (100 devices) | Medium (500 devices) | Large (2000+ devices) |
|-----------|---------------------|----------------------|-----------------------|
| **API Servers** | 2x 4vCPU, 8GB RAM | 3x 8vCPU, 16GB RAM | 5x 16vCPU, 32GB RAM |
| **Database** | 1x 8vCPU, 16GB RAM | 2x 16vCPU, 32GB RAM | 3x 32vCPU, 64GB RAM |
| **Cache (Redis)** | 1x 2vCPU, 4GB RAM | 2x 4vCPU, 8GB RAM | 3x 8vCPU, 16GB RAM |
| **Storage** | 500GB SSD | 2TB SSD | 10TB+ NVMe |
| **Network** | 1Gbps | 10Gbps | 40Gbps+ |

#### Traffic Estimation

```bash
# Calculate expected load
DEVICES=1000
SCAN_INTERVAL=60  # seconds
PACKETS_PER_SCAN=10000
API_CALLS_PER_DEVICE_PER_HOUR=60

# Peak calculations
PEAK_SCANS_PER_SECOND=$((DEVICES / SCAN_INTERVAL))
PEAK_PACKETS_PER_SECOND=$((PEAK_SCANS_PER_SECOND * PACKETS_PER_SCAN))
PEAK_API_CALLS_PER_SECOND=$((DEVICES * API_CALLS_PER_DEVICE_PER_HOUR / 3600))

echo "Peak scans/second: $PEAK_SCANS_PER_SECOND"
echo "Peak packets/second: $PEAK_PACKETS_PER_SECOND"
echo "Peak API calls/second: $PEAK_API_CALLS_PER_SECOND"
```

## Infrastructure Requirements

### Network Architecture

#### 1. Network Segmentation

```bash
# Production network design
MANAGEMENT_VLAN=10    # Management interfaces
API_VLAN=20          # API and web traffic
DATABASE_VLAN=30     # Database cluster
SCANNER_VLAN=40      # Wi-Fi scanning devices
MONITORING_VLAN=50   # Monitoring and logging

# Firewall rules example
# Allow API traffic
iptables -A FORWARD -s 10.0.20.0/24 -d 10.0.30.0/24 -p tcp --dport 5432 -j ACCEPT

# Allow monitoring
iptables -A FORWARD -s 10.0.50.0/24 -d 10.0.20.0/24 -p tcp --dport 8000 -j ACCEPT

# Deny all other inter-VLAN traffic
iptables -A FORWARD -j DROP
```

#### 2. Load Balancer Configuration

```nginx
# /etc/nginx/sites-available/piwardrive-prod
upstream piwardrive_api {
    least_conn;
    server 10.0.20.10:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.11:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.12:8000 max_fails=3 fail_timeout=30s weight=1;
    keepalive 32;
}

upstream piwardrive_websocket {
    ip_hash;  # Sticky sessions for WebSocket
    server 10.0.20.10:8000;
    server 10.0.20.11:8000;
    server 10.0.20.12:8000;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=10r/s;

server {
    listen 443 ssl http2;
    server_name piwardrive.company.com;
    
    # SSL configuration
    ssl_certificate /etc/ssl/certs/piwardrive.crt;
    ssl_certificate_key /etc/ssl/private/piwardrive.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;
    
    # API endpoints
    location /api/ {
        limit_req zone=api_limit burst=200 nodelay;
        
        proxy_pass http://piwardrive_api;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Authentication endpoints
    location ~ ^/(auth|token)/ {
        limit_req zone=auth_limit burst=20 nodelay;
        
        proxy_pass http://piwardrive_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket endpoints
    location /ws/ {
        proxy_pass http://piwardrive_websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
    
    # Static files with caching
    location /static/ {
        proxy_pass http://piwardrive_api;
        expires 1y;
        add_header Cache-Control "public, immutable";
        gzip on;
        gzip_types text/css application/javascript image/svg+xml;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://piwardrive_api;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name piwardrive.company.com;
    return 301 https://$server_name$request_uri;
}
```

### Certificate Management

#### 1. TLS Certificate Setup

```bash
# Generate Certificate Signing Request (CSR)
openssl req -new -newkey rsa:4096 -nodes \
    -keyout piwardrive.key \
    -out piwardrive.csr \
    -subj "/C=US/ST=State/L=City/O=Company/CN=piwardrive.company.com"

# Alternative: Let's Encrypt with certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d piwardrive.company.com

# Set up automatic renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 2. Certificate Rotation Script

```bash
#!/bin/bash
# /opt/piwardrive/scripts/cert-rotation.sh

CERT_PATH="/etc/ssl/certs/piwardrive.crt"
KEY_PATH="/etc/ssl/private/piwardrive.key"
NGINX_SERVICE="nginx"
BACKUP_DIR="/etc/ssl/backup"

# Create backup
mkdir -p "$BACKUP_DIR"
cp "$CERT_PATH" "$BACKUP_DIR/piwardrive.crt.$(date +%Y%m%d)"
cp "$KEY_PATH" "$BACKUP_DIR/piwardrive.key.$(date +%Y%m%d)"

# Deploy new certificate
cp /tmp/new-piwardrive.crt "$CERT_PATH"
cp /tmp/new-piwardrive.key "$KEY_PATH"

# Set permissions
chmod 644 "$CERT_PATH"
chmod 600 "$KEY_PATH"
chown root:root "$CERT_PATH" "$KEY_PATH"

# Test configuration
if nginx -t; then
    systemctl reload "$NGINX_SERVICE"
    echo "Certificate rotation successful"
else
    # Rollback on failure
    cp "$BACKUP_DIR/piwardrive.crt.$(date +%Y%m%d)" "$CERT_PATH"
    cp "$BACKUP_DIR/piwardrive.key.$(date +%Y%m%d)" "$KEY_PATH"
    echo "Certificate rotation failed, rolled back"
    exit 1
fi
```

## Security Hardening

### Application Security

#### 1. Environment Configuration

```bash
# /etc/piwardrive/production.env
# Security settings
PIWARDRIVE_ENV=production
PIWARDRIVE_DEBUG=false
PIWARDRIVE_SECRET_KEY=$(openssl rand -hex 32)
PIWARDRIVE_ALLOWED_HOSTS=piwardrive.company.com,10.0.20.0/24

# Database security
PIWARDRIVE_DATABASE_URL=postgresql://piwardrive:$(cat /etc/piwardrive/secrets/db_password)@postgres-cluster:5432/piwardrive
PIWARDRIVE_DATABASE_SSL_MODE=require

# Session security
PIWARDRIVE_SESSION_TIMEOUT=3600
PIWARDRIVE_SESSION_SECURE=true
PIWARDRIVE_SESSION_HTTPONLY=true
PIWARDRIVE_SESSION_SAMESITE=strict

# CORS settings
PIWARDRIVE_CORS_ALLOWED_ORIGINS=https://piwardrive.company.com
PIWARDRIVE_CORS_ALLOW_CREDENTIALS=true

# Rate limiting
PIWARDRIVE_RATE_LIMIT_ENABLED=true
PIWARDRIVE_RATE_LIMIT_PER_MINUTE=100

# Logging
PIWARDRIVE_LOG_LEVEL=WARNING
PIWARDRIVE_AUDIT_LOG_ENABLED=true
PIWARDRIVE_AUDIT_LOG_PATH=/var/log/piwardrive/audit.log
```

#### 2. API Security Configuration

```yaml
# config/security.yaml
security:
  authentication:
    method: "jwt"
    jwt:
      algorithm: "RS256"
      public_key_path: "/etc/piwardrive/keys/jwt-public.pem"
      private_key_path: "/etc/piwardrive/keys/jwt-private.pem"
      expiration: 3600
    
    password_policy:
      min_length: 12
      require_uppercase: true
      require_lowercase: true
      require_numbers: true
      require_symbols: true
      max_age_days: 90
  
  authorization:
    rbac:
      enabled: true
      roles:
        - name: "admin"
          permissions: ["*"]
        - name: "operator"
          permissions: ["read:*", "write:scans", "write:reports"]
        - name: "viewer"
          permissions: ["read:dashboard", "read:reports"]
  
  encryption:
    data_at_rest:
      enabled: true
      algorithm: "AES-256-GCM"
      key_rotation_days: 30
    
    data_in_transit:
      tls_min_version: "1.2"
      cipher_suites:
        - "ECDHE-RSA-AES256-GCM-SHA384"
        - "ECDHE-RSA-AES128-GCM-SHA256"
  
  audit:
    enabled: true
    events:
      - "authentication"
      - "authorization_failure"
      - "data_access"
      - "configuration_change"
    retention_days: 365
    storage: "database"
```

#### 3. Network Security

```bash
# Firewall configuration
#!/bin/bash
# /opt/piwardrive/scripts/configure-firewall.sh

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# SSH access (restricted)
iptables -A INPUT -p tcp --dport 22 -s 10.0.10.0/24 -j ACCEPT

# HTTPS access
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# HTTP redirect
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Database access (internal only)
iptables -A INPUT -p tcp --dport 5432 -s 10.0.20.0/24 -j ACCEPT

# Redis access (internal only)
iptables -A INPUT -p tcp --dport 6379 -s 10.0.20.0/24 -j ACCEPT

# Monitoring
iptables -A INPUT -p tcp --dport 9090 -s 10.0.50.0/24 -j ACCEPT  # Prometheus
iptables -A INPUT -p tcp --dport 3000 -s 10.0.50.0/24 -j ACCEPT  # Grafana

# Rate limiting for HTTP/HTTPS
iptables -A INPUT -p tcp --dport 443 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "IPT-INPUT-DROP: "
iptables -A FORWARD -j LOG --log-prefix "IPT-FORWARD-DROP: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### Container Security

#### 1. Docker Security

```yaml
# docker-compose.prod.yml security hardening
version: '3.8'

services:
  piwardrive-api:
    image: piwardrive/api:v1.0.0
    user: "1000:1000"  # Non-root user
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    security_opt:
      - no-new-privileges:true
      - seccomp:unconfined
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port < 1024
    
    environment:
      - PIWARDRIVE_ENV=production
    
    secrets:
      - source: db_password
        target: /run/secrets/db_password
        mode: 0400
      - source: jwt_private_key
        target: /run/secrets/jwt_private_key
        mode: 0400
    
    networks:
      - api_network
    
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

secrets:
  db_password:
    external: true
  jwt_private_key:
    external: true

networks:
  api_network:
    driver: bridge
    internal: true
```

#### 2. Kubernetes Security

```yaml
# k8s/security-policy.yaml
apiVersion: v1
kind: SecurityContext
metadata:
  name: piwardrive-security-context
spec:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: piwardrive-network-policy
  namespace: piwardrive-prod
spec:
  podSelector:
    matchLabels:
      app: piwardrive-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

## High Availability Setup

### Database High Availability

#### 1. PostgreSQL Cluster with Patroni

```yaml
# docker-compose.postgres-ha.yml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.0
    environment:
      ETCD_NAME: etcd1
      ETCD_INITIAL_CLUSTER: etcd1=http://etcd:2380
      ETCD_INITIAL_CLUSTER_STATE: new
      ETCD_INITIAL_CLUSTER_TOKEN: etcd-cluster
      ETCD_INITIAL_ADVERTISE_PEER_URLS: http://etcd:2380
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd:2379
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_LISTEN_PEER_URLS: http://0.0.0.0:2380
    ports:
      - "2379:2379"
      - "2380:2380"
    networks:
      - postgres_network

  postgres-master:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: piwardrive
      PATRONI_SCOPE: postgres-cluster
      PATRONI_NAME: postgres-master
      PATRONI_ETCD_URL: http://etcd:2379
    volumes:
      - postgres_master_data:/var/lib/postgresql/data
      - ./config/patroni.yml:/etc/patroni.yml
    command: patroni /etc/patroni.yml
    networks:
      - postgres_network
    depends_on:
      - etcd

  postgres-replica1:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: piwardrive
      PATRONI_SCOPE: postgres-cluster
      PATRONI_NAME: postgres-replica1
      PATRONI_ETCD_URL: http://etcd:2379
    volumes:
      - postgres_replica1_data:/var/lib/postgresql/data
      - ./config/patroni.yml:/etc/patroni.yml
    command: patroni /etc/patroni.yml
    networks:
      - postgres_network
    depends_on:
      - etcd

  haproxy:
    image: haproxy:2.8-alpine
    ports:
      - "5432:5432"
      - "5433:5433"
    volumes:
      - ./config/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    networks:
      - postgres_network
    depends_on:
      - postgres-master
      - postgres-replica1

volumes:
  postgres_master_data:
  postgres_replica1_data:

networks:
  postgres_network:
    driver: bridge
```

#### 2. Patroni Configuration

```yaml
# config/patroni.yml
scope: postgres-cluster
namespace: /db/
name: ${PATRONI_NAME}

restapi:
  listen: 0.0.0.0:8008
  connect_address: ${PATRONI_NAME}:8008

etcd:
  url: ${PATRONI_ETCD_URL}

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 30
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        max_connections: 200
        shared_buffers: 256MB
        effective_cache_size: 1GB
        maintenance_work_mem: 64MB
        checkpoint_completion_target: 0.9
        wal_buffers: 16MB
        default_statistics_target: 100
        random_page_cost: 1.1
        effective_io_concurrency: 200
        work_mem: 4MB
        min_wal_size: 1GB
        max_wal_size: 4GB
        max_worker_processes: 8
        max_parallel_workers_per_gather: 2
        max_parallel_workers: 8
        max_parallel_maintenance_workers: 2
        wal_level: replica
        hot_standby: "on"
        wal_keep_segments: 8
        max_wal_senders: 10
        max_replication_slots: 10
        hot_standby_feedback: "on"
        logging_collector: "on"
        log_checkpoints: "on"
        log_connections: "on"
        log_disconnections: "on"
        log_lock_waits: "on"
        log_temp_files: 0

  initdb:
  - encoding: UTF8
  - data-checksums

  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host replication replicator 10.0.0.0/8 md5
  - host all all 0.0.0.0/0 md5

  users:
    admin:
      password: ${POSTGRES_PASSWORD}
      options:
        - createrole
        - createdb

postgresql:
  listen: 0.0.0.0:5432
  connect_address: ${PATRONI_NAME}:5432
  data_dir: /var/lib/postgresql/data
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: ${POSTGRES_PASSWORD}
    superuser:
      username: postgres
      password: ${POSTGRES_PASSWORD}
  parameters:
    unix_socket_directories: '.'

tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false
```

#### 3. HAProxy Configuration for PostgreSQL

```
# config/haproxy.cfg
global
    maxconn 100

defaults
    log global
    mode tcp
    retries 2
    timeout client 30m
    timeout connect 4s
    timeout server 30m
    timeout check 5s

# PostgreSQL Master (Read/Write)
listen postgres_master
    bind *:5432
    option httpchk
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server postgres-master postgres-master:5432 maxconn 100 check port 8008
    server postgres-replica1 postgres-replica1:5432 maxconn 100 check port 8008 backup

# PostgreSQL Replica (Read Only)
listen postgres_replica
    bind *:5433
    option httpchk
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server postgres-replica1 postgres-replica1:5432 maxconn 100 check port 8008
    server postgres-master postgres-master:5432 maxconn 100 check port 8008 backup

# Stats interface
listen stats
    bind *:7000
    stats enable
    stats uri /
```

### Redis High Availability

#### 1. Redis Sentinel Setup

```yaml
# docker-compose.redis-ha.yml
version: '3.8'

services:
  redis-master:
    image: redis:7-alpine
    command: redis-server --port 6379 --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_master_data:/data
    networks:
      - redis_network

  redis-replica1:
    image: redis:7-alpine
    command: redis-server --port 6379 --requirepass ${REDIS_PASSWORD} --replicaof redis-master 6379 --masterauth ${REDIS_PASSWORD}
    ports:
      - "6380:6379"
    volumes:
      - redis_replica1_data:/data
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-replica2:
    image: redis:7-alpine
    command: redis-server --port 6379 --requirepass ${REDIS_PASSWORD} --replicaof redis-master 6379 --masterauth ${REDIS_PASSWORD}
    ports:
      - "6381:6379"
    volumes:
      - redis_replica2_data:/data
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-sentinel1:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26379:26379"
    volumes:
      - ./config/sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-sentinel2:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26380:26379"
    volumes:
      - ./config/sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-sentinel3:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26381:26379"
    volumes:
      - ./config/sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis_network
    depends_on:
      - redis-master

volumes:
  redis_master_data:
  redis_replica1_data:
  redis_replica2_data:

networks:
  redis_network:
    driver: bridge
```

#### 2. Redis Sentinel Configuration

```
# config/sentinel.conf
port 26379
sentinel monitor piwardrive-redis redis-master 6379 2
sentinel auth-pass piwardrive-redis ${REDIS_PASSWORD}
sentinel down-after-milliseconds piwardrive-redis 30000
sentinel parallel-syncs piwardrive-redis 1
sentinel failover-timeout piwardrive-redis 180000
sentinel deny-scripts-reconfig yes
```

### Application High Availability

#### 1. Health Checks and Circuit Breakers

```python
# piwardrive/core/health.py
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    response_time: float
    timestamp: float

class HealthMonitor:
    def __init__(self):
        self.checks: Dict[str, HealthCheck] = {}
        self.logger = logging.getLogger(__name__)
    
    async def check_database(self) -> HealthCheck:
        """Check database connectivity"""
        start_time = time.time()
        try:
            async with get_db_connection() as conn:
                await conn.execute("SELECT 1")
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                message="Database connection successful",
                response_time=response_time,
                timestamp=time.time()
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {str(e)}",
                response_time=response_time,
                timestamp=time.time()
            )
    
    async def check_redis(self) -> HealthCheck:
        """Check Redis connectivity"""
        start_time = time.time()
        try:
            redis_client = get_redis_client()
            await redis_client.ping()
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="redis",
                status=HealthStatus.HEALTHY,
                message="Redis connection successful",
                response_time=response_time,
                timestamp=time.time()
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                message=f"Redis connection failed: {str(e)}",
                response_time=response_time,
                timestamp=time.time()
            )
    
    async def check_disk_space(self) -> HealthCheck:
        """Check available disk space"""
        start_time = time.time()
        try:
            import shutil
            total, used, free = shutil.disk_usage("/var/lib/piwardrive")
            free_percent = (free / total) * 100
            
            if free_percent < 10:
                status = HealthStatus.UNHEALTHY
                message = f"Low disk space: {free_percent:.1f}% free"
            elif free_percent < 20:
                status = HealthStatus.DEGRADED
                message = f"Disk space warning: {free_percent:.1f}% free"
            else:
                status = HealthStatus.HEALTHY
                message = f"Disk space OK: {free_percent:.1f}% free"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time()
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=HealthStatus.UNHEALTHY,
                message=f"Disk space check failed: {str(e)}",
                response_time=response_time,
                timestamp=time.time()
            )
    
    async def run_all_checks(self) -> Dict[str, HealthCheck]:
        """Run all health checks concurrently"""
        checks = await asyncio.gather(
            self.check_database(),
            self.check_redis(),
            self.check_disk_space(),
            return_exceptions=True
        )
        
        result = {}
        for check in checks:
            if isinstance(check, HealthCheck):
                result[check.name] = check
                self.checks[check.name] = check
        
        return result
    
    def get_overall_status(self) -> HealthStatus:
        """Get overall system health status"""
        if not self.checks:
            return HealthStatus.UNHEALTHY
        
        statuses = [check.status for check in self.checks.values()]
        
        if any(status == HealthStatus.UNHEALTHY for status in statuses):
            return HealthStatus.UNHEALTHY
        elif any(status == HealthStatus.DEGRADED for status in statuses):
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
```

#### 2. Graceful Shutdown

```python
# piwardrive/core/shutdown.py
import asyncio
import signal
import logging
from typing import List, Callable

class GracefulShutdown:
    def __init__(self):
        self.shutdown_handlers: List[Callable] = []
        self.is_shutting_down = False
        self.logger = logging.getLogger(__name__)
    
    def add_shutdown_handler(self, handler: Callable):
        """Add a shutdown handler function"""
        self.shutdown_handlers.append(handler)
    
    async def shutdown(self, sig: int = None):
        """Perform graceful shutdown"""
        if self.is_shutting_down:
            return
        
        self.is_shutting_down = True
        signal_name = signal.Signals(sig).name if sig else "UNKNOWN"
        self.logger.info(f"Received shutdown signal: {signal_name}")
        
        # Run shutdown handlers in reverse order
        for handler in reversed(self.shutdown_handlers):
            try:
                self.logger.info(f"Running shutdown handler: {handler.__name__}")
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                self.logger.error(f"Error in shutdown handler {handler.__name__}: {e}")
        
        self.logger.info("Graceful shutdown completed")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        for sig in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(sig, lambda s, f: asyncio.create_task(self.shutdown(s)))
```

## Load Balancing

### Application Load Balancing

#### 1. NGINX Configuration

```nginx
# /etc/nginx/sites-available/piwardrive-lb
upstream piwardrive_api_pool {
    least_conn;
    
    # API servers with health checks
    server 10.0.20.10:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.11:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.12:8000 max_fails=3 fail_timeout=30s weight=1;
    
    # Keep alive connections
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

# Separate pool for WebSocket connections (sticky sessions)
upstream piwardrive_ws_pool {
    ip_hash;  # Ensure WebSocket connections stick to same server
    server 10.0.20.10:8000;
    server 10.0.20.11:8000;
    server 10.0.20.12:8000;
}

# Rate limiting zones
limit_req_zone $binary_remote_addr zone=general:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api:10m rate=500r/s;

# Connection limiting
limit_conn_zone $binary_remote_addr zone=perip:10m;

server {
    listen 443 ssl http2;
    server_name piwardrive.company.com;
    
    # Connection limits
    limit_conn perip 20;
    
    # SSL configuration (omitted for brevity)
    
    # Health check endpoint (no rate limiting)
    location = /health {
        access_log off;
        proxy_pass http://piwardrive_api_pool;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }
    
    # Authentication endpoints
    location ~ ^/(auth|token)/ {
        limit_req zone=auth burst=20 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Security headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Authentication-specific timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=1000 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Load balancing headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
        
        # API-specific timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 300s;  # Longer for complex queries
        
        # Retry logic
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
    
    # WebSocket endpoints (sticky sessions)
    location /ws/ {
        proxy_pass http://piwardrive_ws_pool;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # WebSocket headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
        
        # Disable buffering for real-time data
        proxy_buffering off;
    }
    
    # Static files with caching
    location /static/ {
        limit_req zone=general burst=200 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        
        # Aggressive caching for static content
        expires 1y;
        add_header Cache-Control "public, immutable";
        
        # Compression
        gzip on;
        gzip_types
            text/css
            application/javascript
            application/json
            image/svg+xml
            application/font-woff
            application/font-woff2;
    }
    
    # Main application
    location / {
        limit_req zone=general burst=200 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

# Status page for monitoring
server {
    listen 8080;
    server_name localhost;
    
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        allow 10.0.50.0/24;  # Monitoring subnet
        deny all;
    }
    
    location /upstream_status {
        # Custom upstream status (requires additional module)
        upstream_status;
        access_log off;
        allow 127.0.0.1;
        allow 10.0.50.0/24;
        deny all;
    }
}
```

#### 2. HAProxy Alternative Configuration

```
# /etc/haproxy/haproxy.cfg
global
    log 127.0.0.1:514 local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    
    # SSL configuration
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private
    ssl-default-bind-ciphers ECDHE+AESGCM:ECDHE+CHACHA20:RSA+AESGCM:RSA+SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    mode http
    log global
    option httplog
    option dontlognull
    option log-health-checks
    option forwardfor except 127.0.0.0/8
    option redispatch
    retries 3
    timeout connect 5s
    timeout client 50s
    timeout server 50s
    timeout http-request 10s
    timeout http-keep-alive 2s
    timeout check 10s
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

# Frontend
frontend piwardrive_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/private/piwardrive.pem
    
    # Redirect HTTP to HTTPS
    redirect scheme https if !{ ssl_fc }
    
    # Rate limiting
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request reject if { sc_http_req_rate(0) gt 100 }
    
    # ACL definitions
    acl is_websocket hdr(Upgrade) -i websocket
    acl is_api path_beg /api/
    acl is_auth path_beg /auth/ /token/
    acl is_static path_beg /static/
    
    # Route to appropriate backend
    use_backend piwardrive_websocket if is_websocket
    use_backend piwardrive_api if is_api
    use_backend piwardrive_auth if is_auth
    use_backend piwardrive_static if is_static
    default_backend piwardrive_web

# API Backend
backend piwardrive_api
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    
    server api1 10.0.20.10:8000 check maxconn 100 weight 1
    server api2 10.0.20.11:8000 check maxconn 100 weight 1
    server api3 10.0.20.12:8000 check maxconn 100 weight 1

# WebSocket Backend (sticky sessions)
backend piwardrive_websocket
    balance source
    option httpchk GET /health
    http-check expect status 200
    timeout server 7d
    
    server api1 10.0.20.10:8000 check
    server api2 10.0.20.11:8000 check
    server api3 10.0.20.12:8000 check

# Authentication Backend (higher security)
backend piwardrive_auth
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    timeout server 30s
    
    server api1 10.0.20.10:8000 check maxconn 50
    server api2 10.0.20.11:8000 check maxconn 50
    server api3 10.0.20.12:8000 check maxconn 50

# Static Files Backend
backend piwardrive_static
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    
    server api1 10.0.20.10:8000 check
    server api2 10.0.20.11:8000 check
    server api3 10.0.20.12:8000 check

# Web Interface Backend
backend piwardrive_web
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    
    server api1 10.0.20.10:8000 check
    server api2 10.0.20.11:8000 check
    server api3 10.0.20.12:8000 check

# Stats interface
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE
    acl is_monitoring src 10.0.50.0/24
    stats http-request auth unless is_monitoring
```

## Database Configuration

### PostgreSQL Production Setup

#### 1. Production Configuration

```postgresql
-- postgresql.conf optimized for production

# Connection settings
listen_addresses = '*'
port = 5432
max_connections = 200
shared_buffers = 1GB                    # 25% of RAM
effective_cache_size = 3GB              # 75% of RAM
work_mem = 32MB
maintenance_work_mem = 256MB

# WAL settings
wal_level = replica
wal_buffers = 64MB
checkpoint_completion_target = 0.9
checkpoint_timeout = 30min
max_wal_size = 4GB
min_wal_size = 1GB

# Replication
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
hot_standby_feedback = on

# Query tuning
random_page_cost = 1.1                  # For SSD storage
effective_io_concurrency = 200
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_parallel_maintenance_workers = 4

# Monitoring
logging_collector = on
log_destination = 'stderr'
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_statement = 'ddl'
log_min_duration_statement = 1000      # Log slow queries

# Autovacuum
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = 10s
autovacuum_vacuum_threshold = 50
autovacuum_analyze_threshold = 50
autovacuum_vacuum_scale_factor = 0.05
autovacuum_analyze_scale_factor = 0.02
autovacuum_vacuum_cost_delay = 10ms
autovacuum_vacuum_cost_limit = 1000

# Memory
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

#### 2. Database Optimization Scripts

```sql
-- Database performance tuning
-- /opt/piwardrive/sql/performance-tuning.sql

-- Create performance monitoring views
CREATE OR REPLACE VIEW slow_queries AS
SELECT
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- Index usage statistics
CREATE OR REPLACE VIEW index_usage AS
SELECT
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table statistics
CREATE OR REPLACE VIEW table_stats AS
SELECT
    schemaname,
    tablename,
    n_tup_ins AS inserts,
    n_tup_upd AS updates,
    n_tup_del AS deletes,
    n_live_tup AS live_tuples,
    n_dead_tup AS dead_tuples,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Create optimized indexes for PiWardrive
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_scans_timestamp 
ON wifi_scans (timestamp DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_scans_device_id 
ON wifi_scans (device_id, timestamp DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_packets_scan_id 
ON wifi_packets (scan_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_packets_mac_address 
ON wifi_packets (source_mac, destination_mac);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_devices_last_seen 
ON devices (last_seen DESC) WHERE active = true;

-- Partitioning for large tables
CREATE TABLE wifi_scans_y2024m01 PARTITION OF wifi_scans
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE wifi_scans_y2024m02 PARTITION OF wifi_scans
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Add more partitions as needed...
```

#### 3. Backup and Maintenance Scripts

```bash
#!/bin/bash
# /opt/piwardrive/scripts/db-maintenance.sh

DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="piwardrive"
DB_USER="piwardrive"
BACKUP_DIR="/var/backups/piwardrive"
LOG_FILE="/var/log/piwardrive/maintenance.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Daily backup
daily_backup() {
    local backup_file="$BACKUP_DIR/piwardrive_$(date +%Y%m%d_%H%M%S).sql.gz"
    
    log "Starting daily backup to $backup_file"
    
    pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        --verbose --no-password --format=custom | gzip > "$backup_file"
    
    if [ $? -eq 0 ]; then
        log "Backup completed successfully"
        
        # Remove backups older than 30 days
        find "$BACKUP_DIR" -name "piwardrive_*.sql.gz" -mtime +30 -delete
        log "Cleaned up old backups"
    else
        log "Backup failed!"
        exit 1
    fi
}

# Vacuum and analyze
maintenance() {
    log "Starting database maintenance"
    
    # Vacuum analyze
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "VACUUM ANALYZE;" 2>&1 | tee -a "$LOG_FILE"
    
    # Reindex if needed
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "REINDEX DATABASE $DB_NAME;" 2>&1 | tee -a "$LOG_FILE"
    
    log "Database maintenance completed"
}

# Check database size and growth
check_size() {
    log "Checking database size"
    
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "SELECT 
                pg_size_pretty(pg_database_size('$DB_NAME')) as database_size,
                pg_size_pretty(pg_total_relation_size('wifi_scans')) as wifi_scans_size,
                pg_size_pretty(pg_total_relation_size('wifi_packets')) as wifi_packets_size;" \
        2>&1 | tee -a "$LOG_FILE"
}

# Run based on argument
case "$1" in
    backup)
        daily_backup
        ;;
    maintenance)
        maintenance
        ;;
    size)
        check_size
        ;;
    all)
        daily_backup
        maintenance
        check_size
        ;;
    *)
        echo "Usage: $0 {backup|maintenance|size|all}"
        exit 1
        ;;
esac
```

## Monitoring and Logging

### Prometheus and Grafana Setup

#### 1. Monitoring Stack Configuration

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./config/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_SECURITY_ADMIN_USER=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/provisioning:/etc/grafana/provisioning
      - ./config/grafana/dashboards:/var/lib/grafana/dashboards
    networks:
      - monitoring
    depends_on:
      - prometheus

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    ports:
      - "9093:9093"
    volumes:
      - ./config/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
      - '--web.external-url=http://localhost:9093'
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    comman// filepath: docs/production-deployment.md
# PiWardrive Production Deployment Guide

## Table of Contents
- [Overview](#overview)
- [Architecture Planning](#architecture-planning)
- [Infrastructure Requirements](#infrastructure-requirements)
- [Security Hardening](#security-hardening)
- [High Availability Setup](#high-availability-setup)
- [Load Balancing](#load-balancing)
- [Database Configuration](#database-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Backup and Recovery](#backup-and-recovery)
- [Performance Optimization](#performance-optimization)
- [Scaling Strategies](#scaling-strategies)
- [Maintenance Procedures](#maintenance-procedures)
- [Troubleshooting](#troubleshooting)
- [Compliance and Auditing](#compliance-and-auditing)

## Overview

This guide covers deploying PiWardrive in production environments, from single-site installations to large-scale distributed networks. It addresses enterprise requirements including security, scalability, monitoring, and compliance.

### Production Deployment Types

- **Single Site Enterprise** - Centralized deployment for large organizations
- **Multi-Site Distributed** - Geographic distribution with central management
- **Cloud-Native** - Kubernetes orchestration with auto-scaling
- **Hybrid Edge** - Edge devices with cloud coordination
- **Compliance-Ready** - Regulated industry deployments

### Key Production Requirements

- **High Availability** (99.9%+ uptime)
- **Scalability** (1000+ concurrent users)
- **Security** (Enterprise-grade protection)
- **Monitoring** (Real-time observability)
- **Compliance** (Audit trails and data protection)

## Architecture Planning

### Reference Architectures

#### 1. Single Site Enterprise

```
┌─────────────────────────────────────────────────────────────┐
│                    Enterprise Network                        │
├─────────────────────────────────────────────────────────────┤
│  Load Balancer (HAProxy/NGINX)                              │
│  ├── API Node 1 (Active)                                    │
│  ├── API Node 2 (Standby)                                   │
│  └── API Node 3 (Standby)                                   │
├─────────────────────────────────────────────────────────────┤
│  Database Cluster                                           │
│  ├── PostgreSQL Primary                                     │
│  ├── PostgreSQL Replica 1                                   │
│  └── PostgreSQL Replica 2                                   │
├─────────────────────────────────────────────────────────────┤
│  Cache Layer                                                │
│  ├── Redis Cluster Node 1                                   │
│  ├── Redis Cluster Node 2                                   │
│  └── Redis Cluster Node 3                                   │
├─────────────────────────────────────────────────────────────┤
│  Monitoring Stack                                           │
│  ├── Prometheus + Grafana                                   │
│  ├── ELK Stack (Logs)                                       │
│  └── Alert Manager                                          │
└─────────────────────────────────────────────────────────────┘
```

#### 2. Multi-Site Distributed

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Site A (HQ)   │    │   Site B        │    │   Site C        │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │Central Mgmt │ │    │ │Local Scanner│ │    │ │Local Scanner│ │
│ │+ Database   │ │◄───┤ │+ Local Cache│ │    │ │+ Local Cache│ │
│ │+ Analytics  │ │    │ │             │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────── VPN/MPLS ────┴───────────────────────┘
```

#### 3. Cloud-Native Kubernetes

```yaml
# High-level Kubernetes architecture
apiVersion: v1
kind: Namespace
metadata:
  name: piwardrive-prod

---
# API Deployment with HPA
apiVersion: apps/v1
kind: Deployment
metadata:
  name: piwardrive-api
  namespace: piwardrive-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: piwardrive-api
  template:
    spec:
      containers:
      - name: api
        image: piwardrive/api:v1.0.0
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"

---
# Database StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-cluster
  namespace: piwardrive-prod
spec:
  serviceName: postgres
  replicas: 3
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### Capacity Planning

#### Hardware Requirements

| Component | Small (100 devices) | Medium (500 devices) | Large (2000+ devices) |
|-----------|---------------------|----------------------|-----------------------|
| **API Servers** | 2x 4vCPU, 8GB RAM | 3x 8vCPU, 16GB RAM | 5x 16vCPU, 32GB RAM |
| **Database** | 1x 8vCPU, 16GB RAM | 2x 16vCPU, 32GB RAM | 3x 32vCPU, 64GB RAM |
| **Cache (Redis)** | 1x 2vCPU, 4GB RAM | 2x 4vCPU, 8GB RAM | 3x 8vCPU, 16GB RAM |
| **Storage** | 500GB SSD | 2TB SSD | 10TB+ NVMe |
| **Network** | 1Gbps | 10Gbps | 40Gbps+ |

#### Traffic Estimation

```bash
# Calculate expected load
DEVICES=1000
SCAN_INTERVAL=60  # seconds
PACKETS_PER_SCAN=10000
API_CALLS_PER_DEVICE_PER_HOUR=60

# Peak calculations
PEAK_SCANS_PER_SECOND=$((DEVICES / SCAN_INTERVAL))
PEAK_PACKETS_PER_SECOND=$((PEAK_SCANS_PER_SECOND * PACKETS_PER_SCAN))
PEAK_API_CALLS_PER_SECOND=$((DEVICES * API_CALLS_PER_DEVICE_PER_HOUR / 3600))

echo "Peak scans/second: $PEAK_SCANS_PER_SECOND"
echo "Peak packets/second: $PEAK_PACKETS_PER_SECOND"
echo "Peak API calls/second: $PEAK_API_CALLS_PER_SECOND"
```

## Infrastructure Requirements

### Network Architecture

#### 1. Network Segmentation

```bash
# Production network design
MANAGEMENT_VLAN=10    # Management interfaces
API_VLAN=20          # API and web traffic
DATABASE_VLAN=30     # Database cluster
SCANNER_VLAN=40      # Wi-Fi scanning devices
MONITORING_VLAN=50   # Monitoring and logging

# Firewall rules example
# Allow API traffic
iptables -A FORWARD -s 10.0.20.0/24 -d 10.0.30.0/24 -p tcp --dport 5432 -j ACCEPT

# Allow monitoring
iptables -A FORWARD -s 10.0.50.0/24 -d 10.0.20.0/24 -p tcp --dport 8000 -j ACCEPT

# Deny all other inter-VLAN traffic
iptables -A FORWARD -j DROP
```

#### 2. Load Balancer Configuration

```nginx
# /etc/nginx/sites-available/piwardrive-prod
upstream piwardrive_api {
    least_conn;
    server 10.0.20.10:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.11:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.12:8000 max_fails=3 fail_timeout=30s weight=1;
    keepalive 32;
}

upstream piwardrive_websocket {
    ip_hash;  # Sticky sessions for WebSocket
    server 10.0.20.10:8000;
    server 10.0.20.11:8000;
    server 10.0.20.12:8000;
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=10r/s;

server {
    listen 443 ssl http2;
    server_name piwardrive.company.com;
    
    # SSL configuration
    ssl_certificate /etc/ssl/certs/piwardrive.crt;
    ssl_certificate_key /etc/ssl/private/piwardrive.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;
    
    # API endpoints
    location /api/ {
        limit_req zone=api_limit burst=200 nodelay;
        
        proxy_pass http://piwardrive_api;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Authentication endpoints
    location ~ ^/(auth|token)/ {
        limit_req zone=auth_limit burst=20 nodelay;
        
        proxy_pass http://piwardrive_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket endpoints
    location /ws/ {
        proxy_pass http://piwardrive_websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
    
    # Static files with caching
    location /static/ {
        proxy_pass http://piwardrive_api;
        expires 1y;
        add_header Cache-Control "public, immutable";
        gzip on;
        gzip_types text/css application/javascript image/svg+xml;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://piwardrive_api;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name piwardrive.company.com;
    return 301 https://$server_name$request_uri;
}
```

### Certificate Management

#### 1. TLS Certificate Setup

```bash
# Generate Certificate Signing Request (CSR)
openssl req -new -newkey rsa:4096 -nodes \
    -keyout piwardrive.key \
    -out piwardrive.csr \
    -subj "/C=US/ST=State/L=City/O=Company/CN=piwardrive.company.com"

# Alternative: Let's Encrypt with certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d piwardrive.company.com

# Set up automatic renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 2. Certificate Rotation Script

```bash
#!/bin/bash
# /opt/piwardrive/scripts/cert-rotation.sh

CERT_PATH="/etc/ssl/certs/piwardrive.crt"
KEY_PATH="/etc/ssl/private/piwardrive.key"
NGINX_SERVICE="nginx"
BACKUP_DIR="/etc/ssl/backup"

# Create backup
mkdir -p "$BACKUP_DIR"
cp "$CERT_PATH" "$BACKUP_DIR/piwardrive.crt.$(date +%Y%m%d)"
cp "$KEY_PATH" "$BACKUP_DIR/piwardrive.key.$(date +%Y%m%d)"

# Deploy new certificate
cp /tmp/new-piwardrive.crt "$CERT_PATH"
cp /tmp/new-piwardrive.key "$KEY_PATH"

# Set permissions
chmod 644 "$CERT_PATH"
chmod 600 "$KEY_PATH"
chown root:root "$CERT_PATH" "$KEY_PATH"

# Test configuration
if nginx -t; then
    systemctl reload "$NGINX_SERVICE"
    echo "Certificate rotation successful"
else
    # Rollback on failure
    cp "$BACKUP_DIR/piwardrive.crt.$(date +%Y%m%d)" "$CERT_PATH"
    cp "$BACKUP_DIR/piwardrive.key.$(date +%Y%m%d)" "$KEY_PATH"
    echo "Certificate rotation failed, rolled back"
    exit 1
fi
```

## Security Hardening

### Application Security

#### 1. Environment Configuration

```bash
# /etc/piwardrive/production.env
# Security settings
PIWARDRIVE_ENV=production
PIWARDRIVE_DEBUG=false
PIWARDRIVE_SECRET_KEY=$(openssl rand -hex 32)
PIWARDRIVE_ALLOWED_HOSTS=piwardrive.company.com,10.0.20.0/24

# Database security
PIWARDRIVE_DATABASE_URL=postgresql://piwardrive:$(cat /etc/piwardrive/secrets/db_password)@postgres-cluster:5432/piwardrive
PIWARDRIVE_DATABASE_SSL_MODE=require

# Session security
PIWARDRIVE_SESSION_TIMEOUT=3600
PIWARDRIVE_SESSION_SECURE=true
PIWARDRIVE_SESSION_HTTPONLY=true
PIWARDRIVE_SESSION_SAMESITE=strict

# CORS settings
PIWARDRIVE_CORS_ALLOWED_ORIGINS=https://piwardrive.company.com
PIWARDRIVE_CORS_ALLOW_CREDENTIALS=true

# Rate limiting
PIWARDRIVE_RATE_LIMIT_ENABLED=true
PIWARDRIVE_RATE_LIMIT_PER_MINUTE=100

# Logging
PIWARDRIVE_LOG_LEVEL=WARNING
PIWARDRIVE_AUDIT_LOG_ENABLED=true
PIWARDRIVE_AUDIT_LOG_PATH=/var/log/piwardrive/audit.log
```

#### 2. API Security Configuration

```yaml
# config/security.yaml
security:
  authentication:
    method: "jwt"
    jwt:
      algorithm: "RS256"
      public_key_path: "/etc/piwardrive/keys/jwt-public.pem"
      private_key_path: "/etc/piwardrive/keys/jwt-private.pem"
      expiration: 3600
    
    password_policy:
      min_length: 12
      require_uppercase: true
      require_lowercase: true
      require_numbers: true
      require_symbols: true
      max_age_days: 90
  
  authorization:
    rbac:
      enabled: true
      roles:
        - name: "admin"
          permissions: ["*"]
        - name: "operator"
          permissions: ["read:*", "write:scans", "write:reports"]
        - name: "viewer"
          permissions: ["read:dashboard", "read:reports"]
  
  encryption:
    data_at_rest:
      enabled: true
      algorithm: "AES-256-GCM"
      key_rotation_days: 30
    
    data_in_transit:
      tls_min_version: "1.2"
      cipher_suites:
        - "ECDHE-RSA-AES256-GCM-SHA384"
        - "ECDHE-RSA-AES128-GCM-SHA256"
  
  audit:
    enabled: true
    events:
      - "authentication"
      - "authorization_failure"
      - "data_access"
      - "configuration_change"
    retention_days: 365
    storage: "database"
```

#### 3. Network Security

```bash
# Firewall configuration
#!/bin/bash
# /opt/piwardrive/scripts/configure-firewall.sh

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# SSH access (restricted)
iptables -A INPUT -p tcp --dport 22 -s 10.0.10.0/24 -j ACCEPT

# HTTPS access
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# HTTP redirect
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Database access (internal only)
iptables -A INPUT -p tcp --dport 5432 -s 10.0.20.0/24 -j ACCEPT

# Redis access (internal only)
iptables -A INPUT -p tcp --dport 6379 -s 10.0.20.0/24 -j ACCEPT

# Monitoring
iptables -A INPUT -p tcp --dport 9090 -s 10.0.50.0/24 -j ACCEPT  # Prometheus
iptables -A INPUT -p tcp --dport 3000 -s 10.0.50.0/24 -j ACCEPT  # Grafana

# Rate limiting for HTTP/HTTPS
iptables -A INPUT -p tcp --dport 443 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "IPT-INPUT-DROP: "
iptables -A FORWARD -j LOG --log-prefix "IPT-FORWARD-DROP: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### Container Security

#### 1. Docker Security

```yaml
# docker-compose.prod.yml security hardening
version: '3.8'

services:
  piwardrive-api:
    image: piwardrive/api:v1.0.0
    user: "1000:1000"  # Non-root user
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    security_opt:
      - no-new-privileges:true
      - seccomp:unconfined
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to port < 1024
    
    environment:
      - PIWARDRIVE_ENV=production
    
    secrets:
      - source: db_password
        target: /run/secrets/db_password
        mode: 0400
      - source: jwt_private_key
        target: /run/secrets/jwt_private_key
        mode: 0400
    
    networks:
      - api_network
    
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
        reservations:
          memory: 512M
          cpus: '0.5'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

secrets:
  db_password:
    external: true
  jwt_private_key:
    external: true

networks:
  api_network:
    driver: bridge
    internal: true
```

#### 2. Kubernetes Security

```yaml
# k8s/security-policy.yaml
apiVersion: v1
kind: SecurityContext
metadata:
  name: piwardrive-security-context
spec:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: piwardrive-network-policy
  namespace: piwardrive-prod
spec:
  podSelector:
    matchLabels:
      app: piwardrive-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

## High Availability Setup

### Database High Availability

#### 1. PostgreSQL Cluster with Patroni

```yaml
# docker-compose.postgres-ha.yml
version: '3.8'

services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.0
    environment:
      ETCD_NAME: etcd1
      ETCD_INITIAL_CLUSTER: etcd1=http://etcd:2380
      ETCD_INITIAL_CLUSTER_STATE: new
      ETCD_INITIAL_CLUSTER_TOKEN: etcd-cluster
      ETCD_INITIAL_ADVERTISE_PEER_URLS: http://etcd:2380
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd:2379
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_LISTEN_PEER_URLS: http://0.0.0.0:2380
    ports:
      - "2379:2379"
      - "2380:2380"
    networks:
      - postgres_network

  postgres-master:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: piwardrive
      PATRONI_SCOPE: postgres-cluster
      PATRONI_NAME: postgres-master
      PATRONI_ETCD_URL: http://etcd:2379
    volumes:
      - postgres_master_data:/var/lib/postgresql/data
      - ./config/patroni.yml:/etc/patroni.yml
    command: patroni /etc/patroni.yml
    networks:
      - postgres_network
    depends_on:
      - etcd

  postgres-replica1:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: piwardrive
      PATRONI_SCOPE: postgres-cluster
      PATRONI_NAME: postgres-replica1
      PATRONI_ETCD_URL: http://etcd:2379
    volumes:
      - postgres_replica1_data:/var/lib/postgresql/data
      - ./config/patroni.yml:/etc/patroni.yml
    command: patroni /etc/patroni.yml
    networks:
      - postgres_network
    depends_on:
      - etcd

  haproxy:
    image: haproxy:2.8-alpine
    ports:
      - "5432:5432"
      - "5433:5433"
    volumes:
      - ./config/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    networks:
      - postgres_network
    depends_on:
      - postgres-master
      - postgres-replica1

volumes:
  postgres_master_data:
  postgres_replica1_data:

networks:
  postgres_network:
    driver: bridge
```

#### 2. Patroni Configuration

```yaml
# config/patroni.yml
scope: postgres-cluster
namespace: /db/
name: ${PATRONI_NAME}

restapi:
  listen: 0.0.0.0:8008
  connect_address: ${PATRONI_NAME}:8008

etcd:
  url: ${PATRONI_ETCD_URL}

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 30
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        max_connections: 200
        shared_buffers: 256MB
        effective_cache_size: 1GB
        maintenance_work_mem: 64MB
        checkpoint_completion_target: 0.9
        wal_buffers: 16MB
        default_statistics_target: 100
        random_page_cost: 1.1
        effective_io_concurrency: 200
        work_mem: 4MB
        min_wal_size: 1GB
        max_wal_size: 4GB
        max_worker_processes: 8
        max_parallel_workers_per_gather: 2
        max_parallel_workers: 8
        max_parallel_maintenance_workers: 2
        wal_level: replica
        hot_standby: "on"
        wal_keep_segments: 8
        max_wal_senders: 10
        max_replication_slots: 10
        hot_standby_feedback: "on"
        logging_collector: "on"
        log_checkpoints: "on"
        log_connections: "on"
        log_disconnections: "on"
        log_lock_waits: "on"
        log_temp_files: 0

  initdb:
  - encoding: UTF8
  - data-checksums

  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host replication replicator 10.0.0.0/8 md5
  - host all all 0.0.0.0/0 md5

  users:
    admin:
      password: ${POSTGRES_PASSWORD}
      options:
        - createrole
        - createdb

postgresql:
  listen: 0.0.0.0:5432
  connect_address: ${PATRONI_NAME}:5432
  data_dir: /var/lib/postgresql/data
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: ${POSTGRES_PASSWORD}
    superuser:
      username: postgres
      password: ${POSTGRES_PASSWORD}
  parameters:
    unix_socket_directories: '.'

tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false
```

#### 3. HAProxy Configuration for PostgreSQL

```
# config/haproxy.cfg
global
    maxconn 100

defaults
    log global
    mode tcp
    retries 2
    timeout client 30m
    timeout connect 4s
    timeout server 30m
    timeout check 5s

# PostgreSQL Master (Read/Write)
listen postgres_master
    bind *:5432
    option httpchk
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server postgres-master postgres-master:5432 maxconn 100 check port 8008
    server postgres-replica1 postgres-replica1:5432 maxconn 100 check port 8008 backup

# PostgreSQL Replica (Read Only)
listen postgres_replica
    bind *:5433
    option httpchk
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server postgres-replica1 postgres-replica1:5432 maxconn 100 check port 8008
    server postgres-master postgres-master:5432 maxconn 100 check port 8008 backup

# Stats interface
listen stats
    bind *:7000
    stats enable
    stats uri /
```

### Redis High Availability

#### 1. Redis Sentinel Setup

```yaml
# docker-compose.redis-ha.yml
version: '3.8'

services:
  redis-master:
    image: redis:7-alpine
    command: redis-server --port 6379 --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_master_data:/data
    networks:
      - redis_network

  redis-replica1:
    image: redis:7-alpine
    command: redis-server --port 6379 --requirepass ${REDIS_PASSWORD} --replicaof redis-master 6379 --masterauth ${REDIS_PASSWORD}
    ports:
      - "6380:6379"
    volumes:
      - redis_replica1_data:/data
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-replica2:
    image: redis:7-alpine
    command: redis-server --port 6379 --requirepass ${REDIS_PASSWORD} --replicaof redis-master 6379 --masterauth ${REDIS_PASSWORD}
    ports:
      - "6381:6379"
    volumes:
      - redis_replica2_data:/data
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-sentinel1:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26379:26379"
    volumes:
      - ./config/sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-sentinel2:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26380:26379"
    volumes:
      - ./config/sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis_network
    depends_on:
      - redis-master

  redis-sentinel3:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26381:26379"
    volumes:
      - ./config/sentinel.conf:/etc/redis/sentinel.conf
    networks:
      - redis_network
    depends_on:
      - redis-master

volumes:
  redis_master_data:
  redis_replica1_data:
  redis_replica2_data:

networks:
  redis_network:
    driver: bridge
```

#### 2. Redis Sentinel Configuration

```
# config/sentinel.conf
port 26379
sentinel monitor piwardrive-redis redis-master 6379 2
sentinel auth-pass piwardrive-redis ${REDIS_PASSWORD}
sentinel down-after-milliseconds piwardrive-redis 30000
sentinel parallel-syncs piwardrive-redis 1
sentinel failover-timeout piwardrive-redis 180000
sentinel deny-scripts-reconfig yes
```

### Application High Availability

#### 1. Health Checks and Circuit Breakers

```python
# piwardrive/core/health.py
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    response_time: float
    timestamp: float

class HealthMonitor:
    def __init__(self):
        self.checks: Dict[str, HealthCheck] = {}
        self.logger = logging.getLogger(__name__)
    
    async def check_database(self) -> HealthCheck:
        """Check database connectivity"""
        start_time = time.time()
        try:
            async with get_db_connection() as conn:
                await conn.execute("SELECT 1")
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                message="Database connection successful",
                response_time=response_time,
                timestamp=time.time()
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {str(e)}",
                response_time=response_time,
                timestamp=time.time()
            )
    
    async def check_redis(self) -> HealthCheck:
        """Check Redis connectivity"""
        start_time = time.time()
        try:
            redis_client = get_redis_client()
            await redis_client.ping()
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="redis",
                status=HealthStatus.HEALTHY,
                message="Redis connection successful",
                response_time=response_time,
                timestamp=time.time()
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                message=f"Redis connection failed: {str(e)}",
                response_time=response_time,
                timestamp=time.time()
            )
    
    async def check_disk_space(self) -> HealthCheck:
        """Check available disk space"""
        start_time = time.time()
        try:
            import shutil
            total, used, free = shutil.disk_usage("/var/lib/piwardrive")
            free_percent = (free / total) * 100
            
            if free_percent < 10:
                status = HealthStatus.UNHEALTHY
                message = f"Low disk space: {free_percent:.1f}% free"
            elif free_percent < 20:
                status = HealthStatus.DEGRADED
                message = f"Disk space warning: {free_percent:.1f}% free"
            else:
                status = HealthStatus.HEALTHY
                message = f"Disk space OK: {free_percent:.1f}% free"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=status,
                message=message,
                response_time=response_time,
                timestamp=time.time()
            )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=HealthStatus.UNHEALTHY,
                message=f"Disk space check failed: {str(e)}",
                response_time=response_time,
                timestamp=time.time()
            )
    
    async def run_all_checks(self) -> Dict[str, HealthCheck]:
        """Run all health checks concurrently"""
        checks = await asyncio.gather(
            self.check_database(),
            self.check_redis(),
            self.check_disk_space(),
            return_exceptions=True
        )
        
        result = {}
        for check in checks:
            if isinstance(check, HealthCheck):
                result[check.name] = check
                self.checks[check.name] = check
        
        return result
    
    def get_overall_status(self) -> HealthStatus:
        """Get overall system health status"""
        if not self.checks:
            return HealthStatus.UNHEALTHY
        
        statuses = [check.status for check in self.checks.values()]
        
        if any(status == HealthStatus.UNHEALTHY for status in statuses):
            return HealthStatus.UNHEALTHY
        elif any(status == HealthStatus.DEGRADED for status in statuses):
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.HEALTHY
```

#### 2. Graceful Shutdown

```python
# piwardrive/core/shutdown.py
import asyncio
import signal
import logging
from typing import List, Callable

class GracefulShutdown:
    def __init__(self):
        self.shutdown_handlers: List[Callable] = []
        self.is_shutting_down = False
        self.logger = logging.getLogger(__name__)
    
    def add_shutdown_handler(self, handler: Callable):
        """Add a shutdown handler function"""
        self.shutdown_handlers.append(handler)
    
    async def shutdown(self, sig: int = None):
        """Perform graceful shutdown"""
        if self.is_shutting_down:
            return
        
        self.is_shutting_down = True
        signal_name = signal.Signals(sig).name if sig else "UNKNOWN"
        self.logger.info(f"Received shutdown signal: {signal_name}")
        
        # Run shutdown handlers in reverse order
        for handler in reversed(self.shutdown_handlers):
            try:
                self.logger.info(f"Running shutdown handler: {handler.__name__}")
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
            except Exception as e:
                self.logger.error(f"Error in shutdown handler {handler.__name__}: {e}")
        
        self.logger.info("Graceful shutdown completed")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        for sig in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(sig, lambda s, f: asyncio.create_task(self.shutdown(s)))
```

## Load Balancing

### Application Load Balancing

#### 1. NGINX Configuration

```nginx
# /etc/nginx/sites-available/piwardrive-lb
upstream piwardrive_api_pool {
    least_conn;
    
    # API servers with health checks
    server 10.0.20.10:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.11:8000 max_fails=3 fail_timeout=30s weight=1;
    server 10.0.20.12:8000 max_fails=3 fail_timeout=30s weight=1;
    
    # Keep alive connections
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

# Separate pool for WebSocket connections (sticky sessions)
upstream piwardrive_ws_pool {
    ip_hash;  # Ensure WebSocket connections stick to same server
    server 10.0.20.10:8000;
    server 10.0.20.11:8000;
    server 10.0.20.12:8000;
}

# Rate limiting zones
limit_req_zone $binary_remote_addr zone=general:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api:10m rate=500r/s;

# Connection limiting
limit_conn_zone $binary_remote_addr zone=perip:10m;

server {
    listen 443 ssl http2;
    server_name piwardrive.company.com;
    
    # Connection limits
    limit_conn perip 20;
    
    # SSL configuration (omitted for brevity)
    
    # Health check endpoint (no rate limiting)
    location = /health {
        access_log off;
        proxy_pass http://piwardrive_api_pool;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }
    
    # Authentication endpoints
    location ~ ^/(auth|token)/ {
        limit_req zone=auth burst=20 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Security headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Authentication-specific timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=1000 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Load balancing headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
        
        # API-specific timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 300s;  # Longer for complex queries
        
        # Retry logic
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
    
    # WebSocket endpoints (sticky sessions)
    location /ws/ {
        proxy_pass http://piwardrive_ws_pool;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # WebSocket headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
        
        # Disable buffering for real-time data
        proxy_buffering off;
    }
    
    # Static files with caching
    location /static/ {
        limit_req zone=general burst=200 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        
        # Aggressive caching for static content
        expires 1y;
        add_header Cache-Control "public, immutable";
        
        # Compression
        gzip on;
        gzip_types
            text/css
            application/javascript
            application/json
            image/svg+xml
            application/font-woff
            application/font-woff2;
    }
    
    # Main application
    location / {
        limit_req zone=general burst=200 nodelay;
        
        proxy_pass http://piwardrive_api_pool;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

# Status page for monitoring
server {
    listen 8080;
    server_name localhost;
    
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        allow 10.0.50.0/24;  # Monitoring subnet
        deny all;
    }
    
    location /upstream_status {
        # Custom upstream status (requires additional module)
        upstream_status;
        access_log off;
        allow 127.0.0.1;
        allow 10.0.50.0/24;
        deny all;
    }
}
```

#### 2. HAProxy Alternative Configuration

```
# /etc/haproxy/haproxy.cfg
global
    log 127.0.0.1:514 local0
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    
    # SSL configuration
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private
    ssl-default-bind-ciphers ECDHE+AESGCM:ECDHE+CHACHA20:RSA+AESGCM:RSA+SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    mode http
    log global
    option httplog
    option dontlognull
    option log-health-checks
    option forwardfor except 127.0.0.0/8
    option redispatch
    retries 3
    timeout connect 5s
    timeout client 50s
    timeout server 50s
    timeout http-request 10s
    timeout http-keep-alive 2s
    timeout check 10s
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

# Frontend
frontend piwardrive_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/private/piwardrive.pem
    
    # Redirect HTTP to HTTPS
    redirect scheme https if !{ ssl_fc }
    
    # Rate limiting
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request reject if { sc_http_req_rate(0) gt 100 }
    
    # ACL definitions
    acl is_websocket hdr(Upgrade) -i websocket
    acl is_api path_beg /api/
    acl is_auth path_beg /auth/ /token/
    acl is_static path_beg /static/
    
    # Route to appropriate backend
    use_backend piwardrive_websocket if is_websocket
    use_backend piwardrive_api if is_api
    use_backend piwardrive_auth if is_auth
    use_backend piwardrive_static if is_static
    default_backend piwardrive_web

# API Backend
backend piwardrive_api
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    
    server api1 10.0.20.10:8000 check maxconn 100 weight 1
    server api2 10.0.20.11:8000 check maxconn 100 weight 1
    server api3 10.0.20.12:8000 check maxconn 100 weight 1

# WebSocket Backend (sticky sessions)
backend piwardrive_websocket
    balance source
    option httpchk GET /health
    http-check expect status 200
    timeout server 7d
    
    server api1 10.0.20.10:8000 check
    server api2 10.0.20.11:8000 check
    server api3 10.0.20.12:8000 check

# Authentication Backend (higher security)
backend piwardrive_auth
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    timeout server 30s
    
    server api1 10.0.20.10:8000 check maxconn 50
    server api2 10.0.20.11:8000 check maxconn 50
    server api3 10.0.20.12:8000 check maxconn 50

# Static Files Backend
backend piwardrive_static
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    
    server api1 10.0.20.10:8000 check
    server api2 10.0.20.11:8000 check
    server api3 10.0.20.12:8000 check

# Web Interface Backend
backend piwardrive_web
    balance leastconn
    option httpchk GET /health
    http-check expect status 200
    
    server api1 10.0.20.10:8000 check
    server api2 10.0.20.11:8000 check
    server api3 10.0.20.12:8000 check

# Stats interface
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats admin if TRUE
    acl is_monitoring src 10.0.50.0/24
    stats http-request auth unless is_monitoring
```

## Database Configuration

### PostgreSQL Production Setup

#### 1. Production Configuration

```postgresql
-- postgresql.conf optimized for production

# Connection settings
listen_addresses = '*'
port = 5432
max_connections = 200
shared_buffers = 1GB                    # 25% of RAM
effective_cache_size = 3GB              # 75% of RAM
work_mem = 32MB
maintenance_work_mem = 256MB

# WAL settings
wal_level = replica
wal_buffers = 64MB
checkpoint_completion_target = 0.9
checkpoint_timeout = 30min
max_wal_size = 4GB
min_wal_size = 1GB

# Replication
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
hot_standby_feedback = on

# Query tuning
random_page_cost = 1.1                  # For SSD storage
effective_io_concurrency = 200
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
max_parallel_maintenance_workers = 4

# Monitoring
logging_collector = on
log_destination = 'stderr'
log_directory = '/var/log/postgresql'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_statement = 'ddl'
log_min_duration_statement = 1000      # Log slow queries

# Autovacuum
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = 10s
autovacuum_vacuum_threshold = 50
autovacuum_analyze_threshold = 50
autovacuum_vacuum_scale_factor = 0.05
autovacuum_analyze_scale_factor = 0.02
autovacuum_vacuum_cost_delay = 10ms
autovacuum_vacuum_cost_limit = 1000

# Memory
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.track = all
```

#### 2. Database Optimization Scripts

```sql
-- Database performance tuning
-- /opt/piwardrive/sql/performance-tuning.sql

-- Create performance monitoring views
CREATE OR REPLACE VIEW slow_queries AS
SELECT
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- Index usage statistics
CREATE OR REPLACE VIEW index_usage AS
SELECT
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table statistics
CREATE OR REPLACE VIEW table_stats AS
SELECT
    schemaname,
    tablename,
    n_tup_ins AS inserts,
    n_tup_upd AS updates,
    n_tup_del AS deletes,
    n_live_tup AS live_tuples,
    n_dead_tup AS dead_tuples,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Create optimized indexes for PiWardrive
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_scans_timestamp 
ON wifi_scans (timestamp DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_scans_device_id 
ON wifi_scans (device_id, timestamp DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_packets_scan_id 
ON wifi_packets (scan_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wifi_packets_mac_address 
ON wifi_packets (source_mac, destination_mac);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_devices_last_seen 
ON devices (last_seen DESC) WHERE active = true;

-- Partitioning for large tables
CREATE TABLE wifi_scans_y2024m01 PARTITION OF wifi_scans
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE wifi_scans_y2024m02 PARTITION OF wifi_scans
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Add more partitions as needed...
```

#### 3. Backup and Maintenance Scripts

```bash
#!/bin/bash
# /opt/piwardrive/scripts/db-maintenance.sh

DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="piwardrive"
DB_USER="piwardrive"
BACKUP_DIR="/var/backups/piwardrive"
LOG_FILE="/var/log/piwardrive/maintenance.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Daily backup
daily_backup() {
    local backup_file="$BACKUP_DIR/piwardrive_$(date +%Y%m%d_%H%M%S).sql.gz"
    
    log "Starting daily backup to $backup_file"
    
    pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        --verbose --no-password --format=custom | gzip > "$backup_file"
    
    if [ $? -eq 0 ]; then
        log "Backup completed successfully"
        
        # Remove backups older than 30 days
        find "$BACKUP_DIR" -name "piwardrive_*.sql.gz" -mtime +30 -delete
        log "Cleaned up old backups"
    else
        log "Backup failed!"
        exit 1
    fi
}

# Vacuum and analyze
maintenance() {
    log "Starting database maintenance"
    
    # Vacuum analyze
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "VACUUM ANALYZE;" 2>&1 | tee -a "$LOG_FILE"
    
    # Reindex if needed
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "REINDEX DATABASE $DB_NAME;" 2>&1 | tee -a "$LOG_FILE"
    
    log "Database maintenance completed"
}

# Check database size and growth
check_size() {
    log "Checking database size"
    
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
        -c "SELECT 
                pg_size_pretty(pg_database_size('$DB_NAME')) as database_size,
                pg_size_pretty(pg_total_relation_size('wifi_scans')) as wifi_scans_size,
                pg_size_pretty(pg_total_relation_size('wifi_packets')) as wifi_packets_size;" \
        2>&1 | tee -a "$LOG_FILE"
}

# Run based on argument
case "$1" in
    backup)
        daily_backup
        ;;
    maintenance)
        maintenance
        ;;
    size)
        check_size
        ;;
    all)
        daily_backup
        maintenance
        check_size
        ;;
    *)
        echo "Usage: $0 {backup|maintenance|size|all}"
        exit 1
        ;;
esac
```

## Monitoring and Logging

### Prometheus and Grafana Setup

#### 1. Monitoring Stack Configuration

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./config/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_SECURITY_ADMIN_USER=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/provisioning:/etc/grafana/provisioning
      - ./config/grafana/dashboards:/var/lib/grafana/dashboards
    networks:
      - monitoring
    depends_on:
      - prometheus

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    ports:
      - "9093:9093"
    volumes:
      - ./config/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
      - '--web.external-url=http://localhost:9093'
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
