# PiWardrive Architecture Deep Dive

## Table of Contents

- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Service Architecture](#service-architecture)
- [Database Design](#database-design)
- [Network Architecture](#network-architecture)
- [Security Architecture](#security-architecture)
- [Deployment Architectures](#deployment-architectures)
- [Performance Considerations](#performance-considerations)
- [Scalability Design](#scalability-design)
- [Monitoring & Observability](#monitoring--observability)

## System Overview

PiWardrive is a distributed IoT monitoring and Wi-Fi analysis system designed for edge computing environments. The architecture follows microservices principles with modular components that can be deployed independently or as a unified system.

### Design Principles

- **Modularity**: Each component has a single responsibility
- **Scalability**: Horizontal scaling support for distributed deployments
- **Reliability**: Fault-tolerant design with graceful degradation
- **Security**: Defense-in-depth security model
- **Performance**: Optimized for resource-constrained environments
- **Maintainability**: Clean code architecture with comprehensive testing

## Component Architecture

### High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        PiWardrive System                        │
├─────────────────────────────────────────────────────────────────┤
│  Frontend Layer                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Web Dashboard │  │   Mobile App    │  │   CLI Tools     │ │
│  │   (React/TS)    │  │   (Optional)    │  │   (Python)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  API Gateway Layer                                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              FastAPI Gateway (service.py)                  │ │
│  │  • Authentication • Rate Limiting • Request Routing       │ │
│  └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Service Layer                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Wi-Fi Scanner  │  │ System Monitor  │  │  GPS Service    │ │
│  │   Service       │  │    Service      │  │   (Optional)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Data Layer                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   SQLite DB     │  │   Time Series   │  │   File Storage  │ │
│  │  (Metadata)     │  │   (Metrics)     │  │   (Exports)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  Hardware Layer                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Wi-Fi Adapter  │  │  GPIO Sensors   │  │   GPS Module    │ │
│  │ (Monitor Mode)  │  │ (Temp, etc.)    │  │   (Optional)    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### Frontend Components

**Web Dashboard (React/TypeScript)**

- Real-time data visualization
- User authentication and session management
- Configuration interface
- Export functionality
- Responsive design for mobile devices

**CLI Tools (Python)**

- Command-line interface for automation
- Scripted data collection
- Batch operations
- System administration tasks

#### Backend Services

**API Gateway (FastAPI)**

- Request routing and load balancing
- Authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- CORS handling
- API documentation serving

**Wi-Fi Scanner Service**

- Wireless network discovery
- Signal strength monitoring
- Device detection and tracking
- Channel analysis
- Interference detection

**System Monitor Service**

- Resource usage tracking (CPU, RAM, disk)
- Temperature monitoring
- Network interface statistics
- Service health checks
- Performance metrics collection

**GPS Service (Optional)**

- Location data collection
- GPS coordinate tracking
- Location-aware network mapping
- Geofencing capabilities

## Data Flow

### Wi-Fi Scanning Data Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wi-Fi Adapter │────│  Scanner Service │────│   API Gateway   │
│                 │    │                 │    │                 │
│ • Raw packets   │    │ • Packet parse  │    │ • Data validate │
│ • Signal data   │    │ • Device detect │    │ • Format resp   │
│ • Beacon frames │    │ • Signal proc   │    │ • Rate limit    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │   Database      │    │  Web Dashboard  │
                    │                 │    │                 │
                    │ • Store results │    │ • Real-time UI  │
                    │ • Time series   │    │ • Charts/graphs │
                    │ • Metadata      │    │ • Alerts/notif  │
                    └─────────────────┘    └─────────────────┘
```

### System Monitoring Data Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  System Sensors │────│ Monitor Service │────│   Time Series   │
│                 │    │                 │    │    Database     │
│ • CPU usage     │    │ • Data collect  │    │                 │
│ • Memory stats  │    │ • Aggregation   │    │ • Metrics store │
│ • Temperature   │    │ • Threshold chk │    │ • Data retention│
│ • Network I/O   │    │ • Alert trigger │    │ • Compression   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌─────────────────┐
                    │  Alert System   │
                    │                 │
                    │ • Notifications │
                    │ • Email/SMS     │
                    │ • Webhooks      │
                    └─────────────────┘
```

### Real-Time Updates Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │────│   Event Bus     │────│   WebSocket     │
│                 │    │                 │    │   Connections   │
│ • Scanner       │    │ • Event routing │    │                 │
│ • Monitor       │    │ • Filtering     │    │ • Live updates  │
│ • GPS           │    │ • Transformation│    │ • Push notif    │
│ • Alerts        │    │ • Buffering     │    │ • Client sync   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technology Stack

### Backend Technologies

**Core Framework**

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool

**Data Storage**

- **SQLite**: Primary database for metadata and configuration
- **InfluxDB** (Optional): Time-series database for metrics
- **Redis** (Optional): Caching and session storage

**Networking & Monitoring**

- **psutil**: System and process monitoring
- **scapy**: Packet capture and analysis
- **netifaces**: Network interface enumeration
- **gpsd**: GPS daemon interface

**Async & Concurrency**

- **asyncio**: Asynchronous I/O support
- **aiofiles**: Asynchronous file operations
- **asyncpg**: Async PostgreSQL adapter (optional)

### Frontend Technologies

**Core Framework**

- **React 18**: Modern React with concurrent features
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast build tool and development server

**UI Components**

- **Material-UI**: React component library
- **Chart.js**: Data visualization library
- **Leaflet**: Interactive maps for GPS data

**State Management**

- **React Query**: Server state management
- **Zustand**: Client state management
- **React Hook Form**: Form state management

### Infrastructure

**Containerization**

- **Docker**: Container platform
- **Docker Compose**: Multi-container orchestration
- **BuildKit**: Enhanced Docker build features

**Web Server**

- **Nginx**: Reverse proxy and static file serving
- **Uvicorn**: ASGI server for FastAPI
- **Gunicorn**: WSGI server with worker processes

## Service Architecture

### Service Communication Patterns

#### Synchronous Communication

```python
# Direct API calls between services
async def get_scan_results(scan_id: str) -> ScanResults:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/v1/scans/{scan_id}")
        return ScanResults.parse_obj(response.json())
```

#### Asynchronous Communication

```python
# Event-driven communication via message bus
async def publish_scan_event(event: ScanEvent):
    await event_bus.publish("scan.completed", event.dict())

async def handle_scan_completion(event_data: dict):
    # Process scan completion event
    scan_event = ScanEvent.parse_obj(event_data)
    await notify_subscribers(scan_event)
```

#### Real-Time Communication

```python
# WebSocket connections for live updates
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for message in scan_event_stream():
        await websocket.send_json(message.dict())
```

### Service Discovery

**Static Configuration**

```yaml
# services.yaml
services:
  wifi_scanner:
    host: localhost
    port: 8081
    health_endpoint: /health

  system_monitor:
    host: localhost
    port: 8082
    health_endpoint: /health
```

**Dynamic Discovery** (Optional)

```python
# Service registry pattern
class ServiceRegistry:
    def __init__(self):
        self.services = {}

    def register(self, name: str, endpoint: str):
        self.services[name] = endpoint

    def discover(self, name: str) -> str:
        return self.services.get(name)
```

## Database Design

### SQLite Schema Design

**Core Tables**

```sql
-- Scan metadata and configuration
CREATE TABLE scans (
    id VARCHAR(50) PRIMARY KEY,
    scan_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    duration INTEGER,
    channels TEXT, -- JSON array
    interface VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Access point discoveries
CREATE TABLE access_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id VARCHAR(50) NOT NULL,
    ssid VARCHAR(255),
    bssid VARCHAR(17) NOT NULL,
    channel INTEGER NOT NULL,
    frequency INTEGER NOT NULL,
    signal_strength INTEGER NOT NULL,
    encryption VARCHAR(50),
    vendor VARCHAR(100),
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    beacon_count INTEGER DEFAULT 1,
    FOREIGN KEY (scan_id) REFERENCES scans(id)
);

-- System configuration
CREATE TABLE config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    data_type VARCHAR(20) NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User accounts and API keys
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    api_key VARCHAR(255) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

**Indexes for Performance**

```sql
-- Optimize common queries
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_scans_started_at ON scans(started_at);
CREATE INDEX idx_access_points_scan_id ON access_points(scan_id);
CREATE INDEX idx_access_points_bssid ON access_points(bssid);
CREATE INDEX idx_access_points_signal ON access_points(signal_strength);
CREATE INDEX idx_config_key ON config(key);
```

### Time Series Data (Optional InfluxDB)

**Measurement Schema**

```sql
-- System metrics
system_metrics,host=pi4-001,interface=wlan0
  cpu_usage=25.5,
  memory_usage=68.2,
  disk_usage=45.8,
  temperature=42.5,
  bytes_sent=1024000i,
  bytes_recv=2048000i
  1640995200000000000

-- Wi-Fi signal measurements
wifi_signals,scan_id=scan_123,bssid=aa:bb:cc:dd:ee:ff
  signal_strength=-45i,
  channel=6i,
  frequency=2437i
  1640995200000000000
```

## Network Architecture

### Deployment Network Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                    Network Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│  Internet                                                       │
│     │                                                           │
│     ▼                                                           │
│  ┌─────────────────┐                                           │
│  │   Router/NAT    │                                           │
│  │   (Home/Office) │                                           │
│  └─────────────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                  Local Network                              │ │
│  │                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │ │
│  │  │  PiWardrive     │  │   Client        │  │   Other     │ │ │
│  │  │  Device         │  │   Devices       │  │   Devices   │ │ │
│  │  │                 │  │                 │  │             │ │ │
│  │  │ ┌─────────────┐ │  │ • Laptops       │  │ • IoT       │ │ │
│  │  │ │Monitor Mode │ │  │ • Phones        │  │ • Printers  │ │ │
│  │  │ │Wi-Fi Adapter│ │  │ • Tablets       │  │ • Cameras   │ │ │
│  │  │ └─────────────┘ │  │                 │  │             │ │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Port Configuration

**Default Ports**

- **8080**: Main API and web interface
- **8081**: Wi-Fi scanner service (internal)
- **8082**: System monitor service (internal)
- **5432**: PostgreSQL (if used)
- **6379**: Redis (if used)
- **8086**: InfluxDB (if used)

**Firewall Rules**

```bash
# Allow incoming connections
sudo ufw allow 8080/tcp    # Main web interface
sudo ufw allow 22/tcp      # SSH access

# Block internal service ports from external access
sudo ufw deny 8081/tcp     # Scanner service
sudo ufw deny 8082/tcp     # Monitor service
```

## Security Architecture

### Authentication & Authorization

**Multi-Layer Security Model**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Layers                              │
├─────────────────────────────────────────────────────────────────┤
│  1. Network Security                                            │
│     • TLS/SSL encryption                                        │
│     • Firewall rules                                           │
│     • VPN access (optional)                                    │
├─────────────────────────────────────────────────────────────────┤
│  2. Application Security                                        │
│     • API authentication (JWT/API keys)                        │
│     • Rate limiting                                            │
│     • Input validation                                         │
│     • SQL injection prevention                                 │
├─────────────────────────────────────────────────────────────────┤
│  3. Data Security                                              │
│     • Password hashing (bcrypt)                                │
│     • Database encryption                                      │
│     • Sensitive data masking                                   │
│     • Audit logging                                            │
├─────────────────────────────────────────────────────────────────┤
│  4. System Security                                            │
│     • Privilege separation                                     │
│     • Container isolation                                      │
│     • File system permissions                                  │
│     • Regular security updates                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Authentication Flow**

```python
# JWT-based authentication
async def authenticate_user(credentials: UserCredentials):
    user = await verify_user_credentials(credentials)
    if user:
        token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(hours=24)
        )
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(401, "Invalid credentials")

# API key authentication
async def verify_api_key(api_key: str = Header(...)):
    if not await is_valid_api_key(api_key):
        raise HTTPException(401, "Invalid API key")
    return api_key
```

### Data Privacy & Compliance

**Data Minimization**

- Store only necessary data for functionality
- Automatic data purging based on retention policies
- Anonymize sensitive information where possible

**Access Controls**

- Role-based access control (RBAC)
- Principle of least privilege
- Audit trails for all data access

**Legal Compliance**

- GDPR compliance for EU deployments
- Clear data usage policies
- User consent mechanisms
- Data export/deletion capabilities

## Deployment Architectures

### Single Device Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                 Raspberry Pi 4 Device                          │
├─────────────────────────────────────────────────────────────────┤
│  Container: piwardrive-all-in-one                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  • FastAPI Gateway                                         │ │
│  │  • Wi-Fi Scanner Service                                   │ │
│  │  │  • System Monitor Service                               │ │
│  │  • SQLite Database                                         │ │
│  │  • React Frontend                                          │ │
│  │  • Nginx Web Server                                        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Wi-Fi Adapter: wlan0 (monitor mode)                          │
│  Storage: 32GB SD Card                                         │
│  Network: eth0 (management), wlan1 (optional)                 │
└─────────────────────────────────────────────────────────────────┘
```

### Distributed Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                  Distributed Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│  Central Server (x86/ARM)                                      │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  • API Gateway                                             │ │
│  │  • Web Dashboard                                           │ │
│  │  • PostgreSQL Database                                     │ │
│  │  • InfluxDB (metrics)                                      │ │
│  │  • Redis (caching)                                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Sensor Node 1  │  │  Sensor Node 2  │  │  Sensor Node N  │ │
│  │                 │  │                 │  │                 │ │
│  │ • Scanner Svc   │  │ • Scanner Svc   │  │ • Scanner Svc   │ │
│  │ • Monitor Svc   │  │ • Monitor Svc   │  │ • Monitor Svc   │ │
│  │ • Local Cache   │  │ • Local Cache   │  │ • Local Cache   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Kubernetes Deployment

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: piwardrive-api
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
        - name: api
          image: piwardrive/api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
            - name: REDIS_URL
              value: "redis://redis-service:6379"
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
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
```

## Performance Considerations

### Resource Optimization

**Memory Management**

```python
# Efficient data structures for large datasets
from collections import deque
from typing import Dict, List
import asyncio

class CircularBuffer:
    """Memory-efficient circular buffer for time-series data"""
    def __init__(self, maxsize: int):
        self.buffer = deque(maxlen=maxsize)
        self.maxsize = maxsize

    def append(self, item):
        self.buffer.append(item)

    def get_latest(self, count: int = None):
        if count:
            return list(self.buffer)[-count:]
        return list(self.buffer)

# Connection pooling for database efficiency
class DatabasePool:
    def __init__(self, database_url: str, pool_size: int = 10):
        self.pool = None
        self.database_url = database_url
        self.pool_size = pool_size

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=1,
            max_size=self.pool_size
        )
```

**CPU Optimization**

```python
# Async processing for I/O bound operations
async def process_scan_results(scan_data: List[dict]):
    tasks = []
    for data in scan_data:
        task = asyncio.create_task(process_access_point(data))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results

# Background task processing
async def background_processor():
    while True:
        try:
            # Process pending tasks
            await process_pending_scans()
            await cleanup_old_data()
            await update_metrics()

            # Sleep between iterations
            await asyncio.sleep(30)
        except Exception as e:
            logger.error(f"Background processing error: {e}")
            await asyncio.sleep(60)
```

### Background Task Queue

Long-running scans can tie up the event loop. The `BackgroundTaskQueue`
provides worker coroutines that execute these jobs in the background. Each
iteration of :func:`run_continuous_scan` may be enqueued instead of awaited::

    from piwardrive.task_queue import BackgroundTaskQueue

    queue = BackgroundTaskQueue(workers=2)
    await queue.start()
    await run_continuous_scan(interval=10, iterations=5, queue=queue)
    await queue.stop()

### Caching Strategy

**Multi-Level Caching**

```python
# Application-level caching
from functools import lru_cache
import aioredis
import json

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = None
        self.redis_url = redis_url

    async def init_redis(self):
        self.redis = await aioredis.from_url(self.redis_url)

    @lru_cache(maxsize=1000)
    def get_system_info(self):
        """Memory cache for static system information"""
        return psutil.virtual_memory()._asdict()

    async def cache_scan_results(self, scan_id: str, results: dict, ttl: int = 3600):
        """Redis cache for scan results"""
        await self.redis.setex(
            f"scan:{scan_id}",
            ttl,
            json.dumps(results)
        )

    async def get_cached_scan(self, scan_id: str) -> dict:
        """Retrieve cached scan results"""
        cached = await self.redis.get(f"scan:{scan_id}")
        if cached:
            return json.loads(cached)
        return None
```

### Database Performance

**Query Optimization**

```sql
-- Efficient queries with proper indexing
EXPLAIN QUERY PLAN
SELECT ap.ssid, ap.bssid, ap.signal_strength, s.started_at
FROM access_points ap
JOIN scans s ON ap.scan_id = s.id
WHERE s.started_at >= datetime('now', '-24 hours')
  AND ap.signal_strength > -60
ORDER BY ap.signal_strength DESC
LIMIT 100;

-- Partitioning for large datasets
CREATE TABLE access_points_202506 AS
SELECT * FROM access_points
WHERE started_at >= '2025-06-01' AND started_at < '2025-07-01';

-- Aggregation for analytics
CREATE VIEW signal_strength_summary AS
SELECT
    ap.channel,
    AVG(ap.signal_strength) as avg_signal,
    MIN(ap.signal_strength) as min_signal,
    MAX(ap.signal_strength) as max_signal,
    COUNT(*) as sample_count
FROM access_points ap
JOIN scans s ON ap.scan_id = s.id
WHERE s.started_at >= datetime('now', '-7 days')
GROUP BY ap.channel;
```

## Scalability Design

### Horizontal Scaling Patterns

**Load Balancing**

```nginx
# nginx.conf
upstream piwardrive_backend {
    least_conn;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    server_name piwardrive.local;

    location /api/ {
        proxy_pass http://piwardrive_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        root /var/www/piwardrive;
        try_files $uri $uri/ /index.html;
    }
}
```

**Database Sharding**

```python
# Shard data by geographic region or time
class ShardedDatabase:
    def __init__(self, shard_configs: List[dict]):
        self.shards = {}
        for config in shard_configs:
            self.shards[config['name']] = DatabaseConnection(config['url'])

    def get_shard_for_scan(self, scan_id: str) -> str:
        """Determine which shard to use based on scan_id"""
        # Simple hash-based sharding
        shard_index = hash(scan_id) % len(self.shards)
        return list(self.shards.keys())[shard_index]

    async def store_scan_data(self, scan_id: str, data: dict):
        shard_name = self.get_shard_for_scan(scan_id)
        shard = self.shards[shard_name]
        await shard.insert_scan_data(data)
```

### Auto-Scaling Configuration

**Docker Swarm Scaling**

```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  piwardrive-api:
    image: piwardrive/api:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
    ports:
      - "8080"
    networks:
      - piwardrive-network
```

## Monitoring & Observability

### Metrics Collection

**Application Metrics**

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
scan_counter = Counter('piwardrive_scans_total', 'Total number of scans', ['scan_type', 'status'])
scan_duration = Histogram('piwardrive_scan_duration_seconds', 'Scan duration')
active_connections = Gauge('piwardrive_active_connections', 'Active WebSocket connections')
system_cpu_usage = Gauge('piwardrive_cpu_usage_percent', 'CPU usage percentage')

# Instrument code
async def perform_scan(scan_request: WiFiScanRequest):
    with scan_duration.time():
        scan_counter.labels(scan_type=scan_request.scan_type, status='started').inc()
        try:
            result = await execute_scan(scan_request)
            scan_counter.labels(scan_type=scan_request.scan_type, status='completed').inc()
            return result
        except Exception as e:
            scan_counter.labels(scan_type=scan_request.scan_type, status='failed').inc()
            raise
```

**Health Checks**

```python
# Comprehensive health monitoring
class HealthChecker:
    def __init__(self):
        self.checks = {
            'database': self.check_database,
            'wifi_adapter': self.check_wifi_adapter,
            'disk_space': self.check_disk_space,
            'memory': self.check_memory,
            'external_deps': self.check_external_dependencies
        }

    async def check_database(self) -> bool:
        try:
            async with database.transaction():
                await database.execute("SELECT 1")
            return True
        except Exception:
            return False

    async def check_wifi_adapter(self) -> bool:
        try:
            interfaces = psutil.net_if_addrs()
            return any('wlan' in iface for iface in interfaces)
        except Exception:
            return False

    async def get_health_status(self) -> dict:
        results = {}
        overall_healthy = True

        for check_name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[check_name] = {'status': 'healthy' if result else 'unhealthy'}
                if not result:
                    overall_healthy = False
            except Exception as e:
                results[check_name] = {'status': 'error', 'error': str(e)}
                overall_healthy = False

        return {
            'status': 'healthy' if overall_healthy else 'unhealthy',
            'checks': results,
            'timestamp': datetime.utcnow().isoformat()
        }
```

### Logging Architecture

**Structured Logging**

```python
import structlog
import logging.config

# Configure structured logging
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/piwardrive/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
        },
        "piwardrive": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
})

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Usage in application
logger = structlog.get_logger("piwardrive.scanner")

async def scan_wifi_networks(scan_request: WiFiScanRequest):
    logger.info(
        "Starting Wi-Fi scan",
        scan_id=scan_request.scan_id,
        scan_type=scan_request.scan_type,
        duration=scan_request.duration,
        channels=scan_request.channels
    )

    try:
        results = await perform_scan(scan_request)
        logger.info(
            "Wi-Fi scan completed",
            scan_id=scan_request.scan_id,
            access_points_found=len(results.access_points),
            duration=results.actual_duration
        )
        return results
    except Exception as e:
        logger.error(
            "Wi-Fi scan failed",
            scan_id=scan_request.scan_id,
            error=str(e),
            exc_info=True
        )
        raise
```

---

## Conclusion

This architecture provides a robust, scalable foundation for the PiWardrive system while maintaining flexibility for various deployment scenarios. The modular design allows for incremental adoption of advanced features like distributed deployment, time-series databases, and container orchestration as requirements evolve.

Key architectural benefits:

- **Modularity**: Independent service deployment and scaling
- **Performance**: Optimized for resource-constrained environments
- **Security**: Multi-layer security model with comprehensive protection
- **Observability**: Comprehensive monitoring, logging, and health checking
- **Scalability**: Horizontal scaling patterns for growth
- **Maintainability**: Clean code architecture with comprehensive testing

For deployment guidance, see the [Production Deployment Guide](production-deployment.md) and [Docker Deployment Guide](docker-deployment.md).
