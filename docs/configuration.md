# PiWardrive Configuration Reference

## Table of Contents
- [Overview](#overview)
- [Configuration Methods](#configuration-methods)
- [Environment Variables](#environment-variables)
- [Configuration File](#configuration-file)
- [Database Configuration](#database-configuration)
- [Wi-Fi Scanner Configuration](#wi-fi-scanner-configuration)
- [System Monitor Configuration](#system-monitor-configuration)
- [API & Security Configuration](#api--security-configuration)
- [Web Interface Configuration](#web-interface-configuration)
- [Logging Configuration](#logging-configuration)
- [Performance Tuning](#performance-tuning)
- [Deployment-Specific Configuration](#deployment-specific-configuration)
- [Configuration Validation](#configuration-validation)
- [Troubleshooting](#troubleshooting)

## Overview

PiWardrive supports multiple configuration methods to accommodate different deployment scenarios. Configuration is loaded in the following priority order:

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration files**
4. **Default values** (lowest priority)

All configuration parameters are validated at startup, and invalid configurations will prevent the service from starting with clear error messages.

```mermaid
graph TD
    A[Application Startup] --> B[Load Configuration]
    B --> C{Command Line Args?}
    C -->|Yes| D[Apply CLI Args]
    C -->|No| E{Environment Variables?}
    D --> E
    E -->|Yes| F[Apply Environment Variables]
    E -->|No| G{Configuration File?}
    F --> G
    G -->|Yes| H[Load Config File]
    G -->|No| I[Apply Default Values]
    H --> J[Validate Configuration]
    I --> J
    J --> K{Valid?}
    K -->|Yes| L[Start Services]
    K -->|No| M[Exit with Error]
    
    style A fill:#e1f5fe
    style L fill:#e8f5e8
    style M fill:#ffebee
```

### Configuration Hierarchy

```mermaid
graph LR
    A[CLI Args<br/>Priority: 1] --> B[Env Variables<br/>Priority: 2]
    B --> C[Config File<br/>Priority: 3]
    C --> D[Default Values<br/>Priority: 4]
    
    A -.-> E[Final Config]
    B -.-> E
    C -.-> E
    D -.-> E
    
    style A fill:#ffcdd2
    style B fill:#fff3e0
    style C fill:#e3f2fd
    style D fill:#f3e5f5
    style E fill:#e8f5e8
```

## Configuration Methods

### 1. Environment Variables
```bash
# Set environment variables
export PIWARDRIVE_API_PORT=8080
export PIWARDRIVE_LOG_LEVEL=INFO
export PIWARDRIVE_DATABASE_URL="sqlite:///data/piwardrive.db"

# Run the service
python service.py
```

### 2. Configuration File
```bash
# Use YAML configuration file
python service.py --config /etc/piwardrive/config.yaml

# Use JSON configuration file
python service.py --config /etc/piwardrive/config.json
```

### 3. Command Line Arguments
```bash
# Override specific settings
python service.py \
    --port 8080 \
    --log-level DEBUG \
    --wifi-interface wlan0 \
    --scan-interval 30
```

### 4. Docker Environment
```yaml
# docker-compose.yml
version: '3.8'
services:
  piwardrive:
    image: piwardrive/api:latest
    environment:
      - PIWARDRIVE_API_PORT=8080
      - PIWARDRIVE_DATABASE_URL=sqlite:///data/piwardrive.db
      - PIWARDRIVE_LOG_LEVEL=INFO
    volumes:
      - ./config:/etc/piwardrive
      - ./data:/data
```

## Environment Variables

### Core Application Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PIWARDRIVE_API_HOST` | string | `"0.0.0.0"` | API server bind address |
| `PIWARDRIVE_API_PORT` | integer | `8080` | API server port |
| `PIWARDRIVE_DEBUG` | boolean | `false` | Enable debug mode |
| `PIWARDRIVE_LOG_LEVEL` | string | `"INFO"` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `PIWARDRIVE_CONFIG_FILE` | string | `""` | Path to configuration file |
| `PIWARDRIVE_DATA_DIR` | string | `"./data"` | Data storage directory |
| `PIWARDRIVE_STATIC_DIR` | string | `"./static"` | Static files directory |
| `PIWARDRIVE_TEMPLATES_DIR` | string | `"./templates"` | Templates directory |

### Database Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PIWARDRIVE_DATABASE_URL` | string | `"sqlite:///data/piwardrive.db"` | Database connection URL |
| `PIWARDRIVE_DATABASE_POOL_SIZE` | integer | `10` | Database connection pool size |
| `PIWARDRIVE_DATABASE_MAX_OVERFLOW` | integer | `20` | Max database connections overflow |
| `PIWARDRIVE_DATABASE_TIMEOUT` | integer | `30` | Database connection timeout (seconds) |
| `PIWARDRIVE_DATABASE_ECHO` | boolean | `false` | Echo SQL queries to logs |

### Wi-Fi Scanner Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PIWARDRIVE_WIFI_INTERFACE` | string | `"wlan0"` | Default Wi-Fi interface |
| `PIWARDRIVE_WIFI_SCAN_INTERVAL` | integer | `60` | Default scan interval (seconds) |
| `PIWARDRIVE_WIFI_SCAN_TIMEOUT` | integer | `300` | Maximum scan duration (seconds) |
| `PIWARDRIVE_WIFI_MONITOR_MODE` | boolean | `true` | Enable monitor mode scanning |
| `PIWARDRIVE_WIFI_CHANNEL_HOP` | boolean | `true` | Enable automatic channel hopping |
| `PIWARDRIVE_WIFI_MAX_CONCURRENT_SCANS` | integer | `3` | Maximum concurrent scans |

### System Monitoring Settings

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PIWARDRIVE_MONITOR_INTERVAL` | integer | `30` | System monitoring interval (seconds) |
| `PIWARDRIVE_MONITOR_CPU` | boolean | `true` | Enable CPU monitoring |
| `PIWARDRIVE_MONITOR_MEMORY` | boolean | `true` | Enable memory monitoring |
| `PIWARDRIVE_MONITOR_DISK` | boolean | `true` | Enable disk monitoring |
| `PIWARDRIVE_MONITOR_NETWORK` | boolean | `true` | Enable network monitoring |
| `PIWARDRIVE_MONITOR_TEMPERATURE` | boolean | `true` | Enable temperature monitoring |

### Security & Authentication

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PIWARDRIVE_SECRET_KEY` | string | `""` | JWT secret key (required for production) |
| `PIWARDRIVE_API_KEY_LENGTH` | integer | `32` | Generated API key length |
| `PIWARDRIVE_JWT_EXPIRY` | integer | `86400` | JWT token expiry (seconds) |
| `PIWARDRIVE_RATE_LIMIT_REQUESTS` | integer | `100` | Rate limit per minute |
| `PIWARDRIVE_RATE_LIMIT_WINDOW` | integer | `60` | Rate limit window (seconds) |
| `PIWARDRIVE_CORS_ORIGINS` | string | `"*"` | CORS allowed origins (comma-separated) |

### Optional Services

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PIWARDRIVE_REDIS_URL` | string | `""` | Redis connection URL used for caching (optional) |
| `PIWARDRIVE_INFLUXDB_URL` | string | `""` | InfluxDB connection URL (optional) |
| `PIWARDRIVE_GPS_ENABLED` | boolean | `false` | Enable GPS functionality |
| `PIWARDRIVE_GPS_DEVICE` | string | `"/dev/ttyUSB0"` | GPS device path |

### Configuration Structure Overview

```mermaid
graph TB
    A[PiWardrive Configuration] --> B[Application Settings]
    A --> C[Database Configuration]
    A --> D[Wi-Fi Scanner Settings]
    A --> E[System Monitoring]
    A --> F[Security & Auth]
    A --> G[Optional Services]
    
    B --> B1[Host/Port]
    B --> B2[Debug Mode]
    B --> B3[Logging]
    B --> B4[Data Directories]
    
    C --> C1[Database URL]
    C --> C2[Connection Pool]
    C --> C3[Timeouts]
    C --> C4[SQLite/PostgreSQL]
    
    D --> D1[Interface Selection]
    D --> D2[Scan Parameters]
    D --> D3[Monitor Mode]
    D --> D4[Channel Configuration]
    
    E --> E1[System Metrics]
    E --> E2[Performance Monitoring]
    E --> E3[Health Checks]
    E --> E4[Alerting]
    
    F --> F1[JWT Tokens]
    F --> F2[API Keys]
    F --> F3[Rate Limiting]
    F --> F4[CORS Settings]
    
    G --> G1[Redis Cache]
    G --> G2[InfluxDB]
    G --> G3[GPS Integration]
    G --> G4[External APIs]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
    style F fill:#ffebee
    style G fill:#e0f2f1
```

## Configuration File

### YAML Configuration Example

```yaml
# filepath: config/piwardrive.yaml
# PiWardrive Configuration File

# Application Settings
app:
  host: "0.0.0.0"
  port: 8080
  debug: false
  log_level: "INFO"
  secret_key: "your-secret-key-here"
  data_dir: "./data"

# Database Configuration
database:
  url: "sqlite:///data/piwardrive.db"
  pool_size: 10
  max_overflow: 20
  timeout: 30
  echo: false
  # For PostgreSQL:
  # url: "postgresql://user:password@localhost:5432/piwardrive"

# Wi-Fi Scanner Configuration
wifi:
  interface: "wlan0"
  scan_interval: 60
  scan_timeout: 300
  monitor_mode: true
  channel_hop: true
  max_concurrent_scans: 3
  
  # Channel configuration
  channels:
    # 2.4GHz channels
    "2.4ghz": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # 5GHz channels
    "5ghz": [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]
  
  # Scan presets
  presets:
    quick:
      duration: 30
      channels: [1, 6, 11]
      scan_type: "passive"
    
    comprehensive:
      duration: 300
      channels: "all"
      scan_type: "passive"
    
    targeted:
      duration: 60
      channels: [36, 40, 44, 48]
      scan_type: "active"

# System Monitoring Configuration
monitoring:
  interval: 30
  enabled_metrics:
    cpu: true
    memory: true
    disk: true
    network: true
    temperature: true
    processes: false
  
  # Alert thresholds
  thresholds:
    cpu_warning: 80.0
    cpu_critical: 95.0
    memory_warning: 85.0
    memory_critical: 95.0
    disk_warning: 90.0
    disk_critical: 98.0
    temperature_warning: 70.0
    temperature_critical: 80.0

# API Configuration
api:
  rate_limiting:
    enabled: true
    requests_per_minute: 100
    burst_limit: 20
  
  cors:
    enabled: true
    origins: ["*"]
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    headers: ["*"]
  
  authentication:
    jwt_expiry: 86400  # 24 hours
    api_key_length: 32
    require_auth: true

# Web Interface Configuration
web:
  title: "PiWardrive Dashboard"
  theme: "dark"  # light, dark, auto
  auto_refresh: true
  refresh_interval: 5000  # milliseconds
  
  # Dashboard widgets
  widgets:
    enabled:
      - "system_stats"
      - "wifi_overview"
      - "recent_scans"
      - "signal_strength_chart"
      - "network_map"
    
    layouts:
      default: [
        {"id": "system_stats", "x": 0, "y": 0, "w": 6, "h": 4},
        {"id": "wifi_overview", "x": 6, "y": 0, "w": 6, "h": 4},
        {"id": "recent_scans", "x": 0, "y": 4, "w": 12, "h": 6},
        {"id": "signal_strength_chart", "x": 0, "y": 10, "w": 8, "h": 6},
        {"id": "network_map", "x": 8, "y": 10, "w": 4, "h": 6}
      ]

# Logging Configuration
logging:
  level: "INFO"
  format: "json"  # json, text
  
  handlers:
    console:
      enabled: true
      level: "INFO"
    
    file:
      enabled: true
      level: "DEBUG"
      path: "/var/log/piwardrive/app.log"
      max_size: "10MB"
      backup_count: 5
      rotation: "time"  # time, size
    
    syslog:
      enabled: false
      facility: "local0"
      address: "/dev/log"

# Data Management
data:
  retention:
    # Automatic cleanup of old data
    enabled: true
    scan_results: "30d"     # Keep scan results for 30 days
    system_metrics: "7d"    # Keep system metrics for 7 days
    audit_logs: "90d"       # Keep audit logs for 90 days
  
  export:
    # Data export settings
    formats: ["json", "csv", "xml"]
    compression: true
    max_export_size: "100MB"

# Optional Services
services:
  redis:
    enabled: false
    url: "redis://localhost:6379/0"
    password: ""
    timeout: 5
  
  influxdb:
    enabled: false
    url: "http://localhost:8086"
    database: "piwardrive"
    username: ""
    password: ""
    retention_policy: "30d"
  
  gps:
    enabled: false
    device: "/dev/ttyUSB0"
    baud_rate: 9600
    timeout: 10
    
  email:
    enabled: false
    smtp_host: "smtp.gmail.com"
    smtp_port: 587
    username: ""
    password: ""
    from_address: "piwardrive@example.com"
    use_tls: true

# Security Settings
security:
  encryption:
    # Database encryption (requires cryptography package)
    database_encryption: false
    encryption_key: ""
  
  network:
    # Network security settings
    bind_localhost_only: false
    require_https: false
    https_redirect: false
    ssl_cert_path: ""
    ssl_key_path: ""
  
  api_keys:
    # API key management
    auto_generate: true
    require_for_all_endpoints: false
    allow_multiple_per_user: true
    expiry_days: 365

# Development Settings (only used in debug mode)
development:
  hot_reload: true
  mock_hardware: false
  test_data_generation: false
  profiling: false
  sql_echo: false
```

### JSON Configuration Example

```json
// filepath: config/piwardrive.json
{
  "app": {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": false,
    "log_level": "INFO",
    "secret_key": "your-secret-key-here",
    "data_dir": "./data"
  },
  "database": {
    "url": "sqlite:///data/piwardrive.db",
    "pool_size": 10,
    "max_overflow": 20,
    "timeout": 30,
    "echo": false
  },
  "wifi": {
    "interface": "wlan0",
    "scan_interval": 60,
    "scan_timeout": 300,
    "monitor_mode": true,
    "channel_hop": true,
    "max_concurrent_scans": 3,
    "channels": {
      "2.4ghz": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
      "5ghz": [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]
    },
    "presets": {
      "quick": {
        "duration": 30,
        "channels": [1, 6, 11],
        "scan_type": "passive"
      },
      "comprehensive": {
        "duration": 300,
        "channels": "all",
        "scan_type": "passive"
      }
    }
  },
  "monitoring": {
    "interval": 30,
    "enabled_metrics": {
      "cpu": true,
      "memory": true,
      "disk": true,
      "network": true,
      "temperature": true
    },
    "thresholds": {
      "cpu_warning": 80.0,
      "cpu_critical": 95.0,
      "memory_warning": 85.0,
      "memory_critical": 95.0
    }
  }
}
```

## Database Configuration

### SQLite Configuration (Default)

```yaml
database:
  url: "sqlite:///data/piwardrive.db"
  # SQLite-specific settings
  sqlite:
    journal_mode: "WAL"
    cache_size: 2000
    temp_store: "memory"
    mmap_size: 268435456  # 256MB
```

### PostgreSQL Configuration

```yaml
database:
  url: "postgresql://piwardrive:password@localhost:5432/piwardrive"
  pool_size: 20
  max_overflow: 30
  timeout: 60
  
  # PostgreSQL-specific settings
  postgresql:
    sslmode: "prefer"
    connect_timeout: 10
    command_timeout: 30
    server_settings:
      application_name: "piwardrive"
      timezone: "UTC"
```

### Database Connection Examples

```bash
# SQLite (default)
export PIWARDRIVE_DATABASE_URL="sqlite:///data/piwardrive.db"

# PostgreSQL
export PIWARDRIVE_DATABASE_URL="postgresql://user:pass@localhost/piwardrive"

# PostgreSQL with SSL
export PIWARDRIVE_DATABASE_URL="postgresql://user:pass@localhost/piwardrive?sslmode=require"

# MySQL/MariaDB
export PIWARDRIVE_DATABASE_URL="mysql://user:pass@localhost/piwardrive"
```

## Wi-Fi Scanner Configuration

### Interface Configuration

```yaml
wifi:
  # Primary interface for scanning
  interface: "wlan0"
  
  # Multiple interface support
  interfaces:
    - name: "wlan0"
      role: "monitor"
      channels: [1, 6, 11]
    - name: "wlan1"
      role: "management"
      channels: [36, 40, 44, 48]
  
  # Interface detection
  auto_detect_interfaces: true
  preferred_vendors: ["Ralink", "Atheros", "Realtek"]
```

### Scanning Parameters

```yaml
wifi:
  scanning:
    # Default scan parameters
    default_duration: 60
    min_duration: 5
    max_duration: 3600
    
    # Channel configuration
    channel_dwell_time: 100  # milliseconds
    channel_hop_interval: 500  # milliseconds
    
    # Signal processing
    min_signal_strength: -100  # dBm
    signal_smoothing: true
    noise_filtering: true
    
    # Performance tuning
    packet_buffer_size: 65536
    capture_timeout: 1000  # milliseconds
    max_packets_per_scan: 10000
```

### Advanced Wi-Fi Settings

```yaml
wifi:
  advanced:
    # Monitor mode settings
    monitor_mode:
      auto_enable: true
      restore_on_exit: true
      set_channel: true
    
    # Packet capture filters
    capture_filters:
      beacon_frames: true
      probe_requests: true
      probe_responses: true
      data_frames: false
      management_frames: true
    
    # Vendor OUI database
    oui_database:
      enabled: true
      update_interval: "7d"
      local_file: "data/oui.txt"
      remote_url: "https://standards-oui.ieee.org/oui/oui.txt"
```

## System Monitor Configuration

### Monitoring Intervals

```yaml
monitoring:
  # Base monitoring interval
  interval: 30
  
  # Per-metric intervals
  intervals:
    cpu: 15
    memory: 30
    disk: 60
    network: 10
    temperature: 30
    processes: 300
```

### Metric Collection

```yaml
monitoring:
  metrics:
    cpu:
      enabled: true
      per_core: true
      load_average: true
      
    memory:
      enabled: true
      include_swap: true
      include_buffers: true
      
    disk:
      enabled: true
      mount_points: ["/", "/boot", "/tmp"]
      include_io_stats: true
      
    network:
      enabled: true
      interfaces: ["eth0", "wlan0", "wlan1"]
      include_errors: true
      
    temperature:
      enabled: true
      sensors: ["cpu_thermal", "gpu_thermal"]
      fahrenheit: false
```

### Alerting Configuration

```yaml
monitoring:
  alerts:
    enabled: true
    
    rules:
      - name: "high_cpu_usage"
        metric: "cpu_usage"
        operator: ">"
        threshold: 85.0
        duration: "5m"
        severity: "warning"
        
      - name: "critical_cpu_usage"
        metric: "cpu_usage"
        operator: ">"
        threshold: 95.0
        duration: "2m"
        severity: "critical"
        
      - name: "low_disk_space"
        metric: "disk_usage"
        operator: ">"
        threshold: 90.0
        duration: "1m"
        severity: "warning"
        
      - name: "high_temperature"
        metric: "temperature"
        operator: ">"
        threshold: 75.0
        duration: "3m"
        severity: "warning"
    
    # Notification channels
    notifications:
      console: true
      file: true
      email: false
      webhook: false
```

## API & Security Configuration

### Authentication Settings

```yaml
api:
  authentication:
    # JWT configuration
    jwt:
      secret_key: "your-jwt-secret-key"
      algorithm: "HS256"
      expiry: 86400  # 24 hours
      refresh_enabled: true
      refresh_expiry: 604800  # 7 days
    
    # API key configuration
    api_keys:
      enabled: true
      length: 32
      prefix: "pk_"
      auto_generate: true
      expiry_days: 365
    
    # Session configuration
    sessions:
      enabled: true
      timeout: 3600  # 1 hour
      max_sessions_per_user: 5
```

### Rate Limiting

```yaml
api:
  rate_limiting:
    enabled: true
    
    # Global limits
    global:
      requests_per_minute: 1000
      burst_limit: 100
    
    # Per-user limits
    authenticated:
      requests_per_minute: 500
      burst_limit: 50
    
    # Per-IP limits
    anonymous:
      requests_per_minute: 100
      burst_limit: 20
    
    # Endpoint-specific limits
    endpoints:
      "/api/v1/wifi/scan":
        requests_per_minute: 10
        burst_limit: 3
      "/api/v1/system/stats":
        requests_per_minute: 60
        burst_limit: 10
```

### CORS Configuration

```yaml
api:
  cors:
    enabled: true
    
    # Allowed origins
    origins:
      - "http://localhost:3000"
      - "https://piwardrive.local"
      - "https://*.piwardrive.com"
    
    # Allowed methods
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    
    # Allowed headers
    headers:
      - "Content-Type"
      - "Authorization"
      - "X-API-Key"
      - "X-Requested-With"
    
    # Expose headers
    expose_headers:
      - "X-Request-ID"
      - "X-Process-Time"
    
    # Credentials and caching
    allow_credentials: true
    max_age: 86400
```

## Web Interface Configuration

### Theme and Appearance

```yaml
web:
  appearance:
    title: "PiWardrive Dashboard"
    subtitle: "Wi-Fi Analysis & IoT Monitoring"
    logo_url: "/static/images/logo.png"
    favicon_url: "/static/images/favicon.ico"
    
    theme:
      default: "dark"  # light, dark, auto
      allow_user_override: true
      custom_css: "/static/css/custom.css"
    
    language:
      default: "en"
      supported: ["en", "es", "fr", "de", "zh"]
      auto_detect: true
```

### Dashboard Configuration

```yaml
web:
  dashboard:
    auto_refresh: true
    refresh_interval: 5000  # milliseconds
    
    # Widget configuration
    widgets:
      system_stats:
        enabled: true
        refresh_interval: 10000
        show_charts: true
        
      wifi_overview:
        enabled: true
        refresh_interval: 15000
        max_networks: 20
        
      recent_scans:
        enabled: true
        max_items: 10
        show_details: true
        
      signal_map:
        enabled: true
        map_provider: "openstreetmap"
        default_zoom: 15
    
    # Layout presets
    layouts:
      compact: "single_column"
      standard: "two_column"
      wide: "three_column"
      custom: "user_defined"
```

## Logging Configuration

### Log Levels and Formats

```yaml
logging:
  # Global log level
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  
  # Log format
  format: "json"  # json, text, structured
  
  # Include additional context
  include_context:
    request_id: true
    user_id: true
    session_id: true
    timestamp: true
    module: true
    function: true
    line_number: false
```

### Log Handlers

```yaml
logging:
  handlers:
    console:
      enabled: true
      level: "INFO"
      format: "text"
      colorized: true
      
    file:
      enabled: true
      level: "DEBUG"
      format: "json"
      path: "/var/log/piwardrive/app.log"
      
      # Rotation settings
      rotation:
        type: "time"  # time, size
        when: "midnight"  # for time rotation
        interval: 1
        backup_count: 7
        max_size: "10MB"  # for size rotation
      
    syslog:
      enabled: false
      level: "WARNING"
      facility: "local0"
      address: "/dev/log"
      format: "structured"
      
    remote:
      enabled: false
      level: "ERROR"
      url: "https://logs.example.com/api/logs"
      api_key: "your-api-key"
      batch_size: 100
      flush_interval: 30
```

### Component-Specific Logging

```yaml
logging:
  loggers:
    # Root logger
    root:
      level: "INFO"
      handlers: ["console", "file"]
      
    # Application components
    "piwardrive.scanner":
      level: "DEBUG"
      handlers: ["file"]
      propagate: false
      
    "piwardrive.monitor":
      level: "INFO"
      handlers: ["console", "file"]
      
    "piwardrive.api":
      level: "WARNING"
      handlers: ["file", "syslog"]
      
    # Third-party libraries
    "uvicorn":
      level: "WARNING"
      handlers: ["console"]
      
    "sqlalchemy":
      level: "WARNING"
      handlers: ["file"]
```

## Performance Tuning

### Application Performance

```yaml
performance:
  # Worker processes
  workers:
    count: 4  # auto-detected based on CPU cores
    worker_class: "uvicorn.workers.UvicornWorker"
    max_requests: 1000
    max_requests_jitter: 100
    timeout: 30
    keepalive: 5
  
  # Memory management
  memory:
    max_memory_per_worker: "512MB"
    garbage_collection: true
    gc_threshold: [700, 10, 10]
  
  # Connection pooling
  connections:
    database_pool_size: 20
    redis_pool_size: 10
    http_client_pool_size: 100
    connection_timeout: 30
    read_timeout: 60
```

### Caching Configuration

```yaml
performance:
  caching:
    # Application-level caching
    application:
      enabled: true
      backend: "memory"  # memory, redis, memcached
      default_timeout: 300
      max_entries: 10000
    
    # API response caching
    api_responses:
      enabled: true
      timeout: 60
      vary_on_headers: ["Authorization", "Accept-Language"]
      
    # Static file caching
    static_files:
      enabled: true
      max_age: 86400
      etag: true
      gzip: true
```

### Database Optimization

```yaml
performance:
  database:
    # Connection pooling
    pool_size: 20
    max_overflow: 30
    pool_timeout: 30
    pool_recycle: 3600
    
    # Query optimization
    query_cache: true
    prepared_statements: true
    batch_size: 1000
    
    # Specific optimizations
    sqlite:
      journal_mode: "WAL"
      cache_size: 10000
      mmap_size: 268435456
      temp_store: "memory"
    
    postgresql:
      shared_preload_libraries: ["pg_stat_statements"]
      effective_cache_size: "256MB"
      work_mem: "4MB"
```

## Deployment-Specific Configuration

### Development Environment

```yaml
# config/development.yaml
app:
  debug: true
  log_level: "DEBUG"
  hot_reload: true

database:
  url: "sqlite:///data/dev_piwardrive.db"
  echo: true

wifi:
  mock_hardware: true
  test_data_generation: true

monitoring:
  interval: 10  # More frequent monitoring

api:
  rate_limiting:
    enabled: false
  cors:
    origins: ["*"]

logging:
  level: "DEBUG"
  handlers:
    console:
      enabled: true
      colorized: true
```

### Production Environment

```yaml
# config/production.yaml
app:
  debug: false
  log_level: "INFO"
  secret_key: "${PIWARDRIVE_SECRET_KEY}"

database:
  url: "${PIWARDRIVE_DATABASE_URL}"
  pool_size: 20
  echo: false

wifi:
  interface: "wlan0"
  monitor_mode: true

api:
  rate_limiting:
    enabled: true
    requests_per_minute: 100
  
  authentication:
    require_auth: true
    jwt_expiry: 3600

security:
  require_https: true
  api_keys:
    require_for_all_endpoints: true

logging:
  level: "WARNING"
  handlers:
    file:
      enabled: true
      path: "/var/log/piwardrive/app.log"
    syslog:
      enabled: true
```

### Docker Configuration

```yaml
# config/docker.yaml
app:
  host: "0.0.0.0"
  port: 8080
  data_dir: "/data"

database:
  url: "sqlite:///data/piwardrive.db"

wifi:
  interface: "wlan0"
  auto_detect_interfaces: true

logging:
  handlers:
    console:
      enabled: true
      format: "json"
    file:
      enabled: false

# Health check configuration
health:
  enabled: true
  endpoint: "/health"
  checks:
    - "database"
    - "wifi_adapter"
    - "disk_space"
```

### Raspberry Pi Configuration

```yaml
# config/raspberry-pi.yaml
app:
  log_level: "INFO"

wifi:
  interface: "wlan0"
  monitor_mode: true
  channel_hop: true

monitoring:
  interval: 30
  enabled_metrics:
    cpu: true
    memory: true
    disk: true
    temperature: true  # Important for Pi
  
  thresholds:
    temperature_warning: 65.0
    temperature_critical: 75.0

performance:
  workers:
    count: 2  # Limited CPU cores
  
  memory:
    max_memory_per_worker: "256MB"

# Pi-specific GPIO configuration
gpio:
  enabled: false
  status_led_pin: 18
  buzzer_pin: 12
```

## Configuration Validation

### Validation Schema

```python
# Configuration validation using Pydantic
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any

class WiFiConfig(BaseModel):
    interface: str = Field(default="wlan0", regex=r"^wlan\d+$")
    scan_interval: int = Field(default=60, ge=5, le=3600)
    scan_timeout: int = Field(default=300, ge=10, le=7200)
    monitor_mode: bool = True
    channels: Optional[List[int]] = None
    
    @validator('channels')
    def validate_channels(cls, v):
        if v is not None:
            valid_channels = list(range(1, 15)) + [36, 40, 44, 48, 52, 56, 60, 64]
            for channel in v:
                if channel not in valid_channels:
                    raise ValueError(f'Invalid channel: {channel}')
        return v

class DatabaseConfig(BaseModel):
    url: str = Field(..., regex=r"^(sqlite|postgresql|mysql)://")
    pool_size: int = Field(default=10, ge=1, le=100)
    timeout: int = Field(default=30, ge=5, le=300)
    
class AppConfig(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080, ge=1024, le=65535)
    debug: bool = False
    log_level: str = Field(default="INFO", regex=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
class Config(BaseModel):
    app: AppConfig = AppConfig()
    database: DatabaseConfig = DatabaseConfig()
    wifi: WiFiConfig = WiFiConfig()
```

### Environment Variable Validation

```bash
#!/bin/bash
# validate_config.sh - Configuration validation script

# Required environment variables
REQUIRED_VARS=(
    "PIWARDRIVE_SECRET_KEY"
    "PIWARDRIVE_DATABASE_URL"
)

# Optional environment variables with defaults
OPTIONAL_VARS=(
    "PIWARDRIVE_API_PORT:8080"
    "PIWARDRIVE_LOG_LEVEL:INFO"
    "PIWARDRIVE_WIFI_INTERFACE:wlan0"
)

# Validation functions
validate_port() {
    local port=$1
    if [[ ! $port =~ ^[0-9]+$ ]] || [ $port -lt 1024 ] || [ $port -gt 65535 ]; then
        echo "Error: Invalid port number: $port"
        return 1
    fi
}

validate_log_level() {
    local level=$1
    case $level in
        DEBUG|INFO|WARNING|ERROR|CRITICAL) ;;
        *) echo "Error: Invalid log level: $level"; return 1 ;;
    esac
}

validate_interface() {
    local interface=$1
    if ! ip link show $interface &>/dev/null; then
        echo "Warning: Interface $interface not found"
        return 1
    fi
}

# Main validation
echo "Validating PiWardrive configuration..."

# Check required variables
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

# Validate port
if [ ! -z "$PIWARDRIVE_API_PORT" ]; then
    validate_port "$PIWARDRIVE_API_PORT"
fi

# Validate log level
if [ ! -z "$PIWARDRIVE_LOG_LEVEL" ]; then
    validate_log_level "$PIWARDRIVE_LOG_LEVEL"
fi

# Validate Wi-Fi interface
if [ ! -z "$PIWARDRIVE_WIFI_INTERFACE" ]; then
    validate_interface "$PIWARDRIVE_WIFI_INTERFACE"
fi

echo "Configuration validation completed successfully!"
```

## Troubleshooting

### Common Configuration Issues

#### Database Connection Problems

```bash
# Test database connectivity
python -c "
from sqlalchemy import create_engine
engine = create_engine('$PIWARDRIVE_DATABASE_URL')
try:
    engine.connect()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
"
```

#### Wi-Fi Interface Issues

```bash
# Check available interfaces
ip link show | grep wlan

# Check interface capabilities
iw dev wlan0 info

# Test monitor mode
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

#### Permission Problems

```bash
# Check file permissions
ls -la data/
ls -la /var/log/piwardrive/

# Set correct permissions
sudo chown -R piwardrive:piwardrive /var/log/piwardrive/
sudo chmod 755 /var/log/piwardrive/
sudo chmod 644 /var/log/piwardrive/*.log
```

### Configuration Debugging

#### Enable Debug Mode

```yaml
app:
  debug: true
  log_level: "DEBUG"

logging:
  level: "DEBUG"
  handlers:
    console:
      enabled: true
      level: "DEBUG"
```

#### Configuration Dump

```python
# Dump current configuration
python -c "
import yaml
from config import load_config

config = load_config()
print(yaml.dump(config.dict(), default_flow_style=False))
"
```

#### Health Check

```bash
# Check service health
curl -s http://localhost:8080/api/v1/system/health | jq .

# Check configuration endpoint
curl -s http://localhost:8080/api/v1/system/config | jq .
```

### Performance Troubleshooting

#### Memory Usage

```bash
# Monitor memory usage
watch -n 5 'ps aux | grep piwardrive'

# Check for memory leaks
python -m memory_profiler service.py
```

#### CPU Usage

```bash
# Monitor CPU usage
top -p $(pgrep -f piwardrive)

# Profile CPU usage
python -m cProfile -o profile.stats service.py
```

#### Database Performance

```sql
-- SQLite performance analysis
.timer on
.headers on
EXPLAIN QUERY PLAN SELECT * FROM access_points LIMIT 10;

-- Check database size
SELECT 
    name,
    SUM("pgsize") as size
FROM "dbstat" 
GROUP BY name 
ORDER BY size DESC;
```

---

This configuration reference provides comprehensive documentation for all aspects of PiWardrive configuration, from basic setup to advanced performance tuning and troubleshooting. Use this guide to customize PiWardrive for your specific deployment needs.
