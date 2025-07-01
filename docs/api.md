<!-- filepath: c:\Users\Blake Schmitz\Documents\GitHub\piwardrive\docs\api.md -->

# API Reference

PiWardrive provides a comprehensive REST API built with FastAPI. The API serves as the backend for the React web dashboard and provides programmatic access to all system functionality including health monitoring, service control, data export, and real-time streaming.

## Base URL

The API is served at `http://localhost:8080/api/v1` by default. The port can be changed via the `PIWARDRIVE_API_PORT` environment variable.

## Interactive Documentation

- **Swagger UI**: http://localhost:8080/docs
- **Enhanced Documentation**: http://localhost:8080/api-docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI Schema**: http://localhost:8080/openapi.json

## Authentication

PiWardrive supports multiple authentication methods:

### API Key Authentication (Recommended)

```bash
curl -H "X-API-Key: your-api-key-here" "http://localhost:8080/api/v1/system/health"
```

### JWT Bearer Token Authentication

```bash
# Get token
curl -X POST "http://localhost:8080/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=your_password"

# Use token
curl -H "Authorization: Bearer <token>" "http://localhost:8080/api/v1/system/stats"
```

### OAuth2 Password Flow

```bash
curl -X POST "http://localhost:8080/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=your_password"
```

## Core Endpoints

### Authentication

#### `POST /api/v1/auth/token`

**Description:** Obtain a JWT bearer token for API access.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "refresh_token": "string"
}
```

#### `POST /api/v1/auth/refresh`

**Description:** Refresh an expired JWT token.

**Request Body:**

```json
{
  "refresh_token": "string"
}
```

**Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### `POST /api/v1/auth/logout`

**Description:** Invalidate the current authentication token.

**Headers:** `Authorization: Bearer <token>`

**Response:**

```json
{
  "message": "Successfully logged out"
}
```

### Wi-Fi Scanning

#### `POST /api/v1/wifi/scan`

**Description:** Start a new Wi-Fi scan with specified parameters.

**Request Body:**

```json
{
  "scan_type": "passive",
  "duration": 60,
  "channels": [1, 6, 11],
  "interface": "wlan0",
  "description": "Quick scan of common channels"
}
```

**Response:**

```json
{
  "scan_id": "scan_20250630_120000",
  "status": "started",
  "started_at": "2025-06-30T12:00:00Z",
  "estimated_completion": "2025-06-30T12:01:00Z",
  "scan_params": {
    "scan_type": "passive",
    "duration": 60,
    "channels": [1, 6, 11],
    "interface": "wlan0"
  }
}
```

#### `GET /api/v1/wifi/scan/{scan_id}`

**Description:** Get results from a specific Wi-Fi scan.

**Path Parameters:**

- `scan_id`: Unique scan identifier

**Response:**

```json
{
  "scan_id": "scan_20250630_120000",
  "status": "completed",
  "started_at": "2025-06-30T12:00:00Z",
  "completed_at": "2025-06-30T12:01:00Z",
  "access_points": [
    {
      "ssid": "HomeNetwork",
      "bssid": "AA:BB:CC:DD:EE:FF",
      "channel": 6,
      "frequency": 2437,
      "signal_strength": -45,
      "encryption": "WPA2-PSK",
      "vendor": "Cisco Systems",
      "first_seen": "2025-06-30T12:00:15Z",
      "last_seen": "2025-06-30T12:00:55Z",
      "beacon_count": 40
    }
  ],
  "total_count": 15,
  "scan_params": {
    "scan_type": "passive",
    "duration": 60,
    "channels": [1, 6, 11],
    "interface": "wlan0"
  }
}
```

#### `GET /api/v1/wifi/scans`

**Description:** List all Wi-Fi scans with optional filtering.

**Query Parameters:**

- `status` (optional): Filter by scan status (started, completed, failed)
- `limit` (optional): Number of scans to return (default: 20)
- `offset` (optional): Number of scans to skip (default: 0)
- `order_by` (optional): Sort field (started_at, duration, status)

**Response:**

```json
{
  "scans": [
    {
      "scan_id": "scan_20250630_120000",
      "status": "completed",
      "started_at": "2025-06-30T12:00:00Z",
      "completed_at": "2025-06-30T12:01:00Z",
      "access_points_count": 15,
      "scan_type": "passive",
      "duration": 60
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

#### `DELETE /api/v1/wifi/scan/{scan_id}`

**Description:** Cancel a running scan or delete scan results.

**Path Parameters:**

- `scan_id`: Unique scan identifier

**Response:**

```json
{
  "scan_id": "scan_20250630_120000",
  "status": "cancelled",
  "message": "Scan cancelled successfully"
}
```

#### `GET /api/v1/wifi/scan/{scan_id}/stream`

**Description:** Stream real-time updates from an active scan.

**Path Parameters:**

- `scan_id`: Unique scan identifier

**Response:** Server-Sent Events stream

```
data: {"event": "access_point_found", "data": {"ssid": "TestAP", "bssid": "...", "signal_strength": -60}}

data: {"event": "scan_progress", "data": {"progress": 50, "access_points_found": 8}}

data: {"event": "scan_completed", "data": {"total_access_points": 15, "duration": 60}}
```

#### `GET /api/v1/wifi/interfaces`

**Description:** List available Wi-Fi interfaces and their capabilities.

**Response:**

```json
{
  "interfaces": [
    {
      "name": "wlan0",
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "driver": "ath9k_htc",
      "monitor_mode_capable": true,
      "current_mode": "managed",
      "supported_channels": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
      "current_channel": 6,
      "power_management": false
    }
  ]
}
```

#### `POST /api/v1/wifi/interfaces/{interface}/mode`

**Description:** Change Wi-Fi interface mode (monitor/managed).

**Path Parameters:**

- `interface`: Interface name (e.g., "wlan0")

**Request Body:**

```json
{
  "mode": "monitor",
  "channel": 6
}
```

**Response:**

```json
{
  "interface": "wlan0",
  "previous_mode": "managed",
  "new_mode": "monitor",
  "channel": 6,
  "success": true
}
```

### System Status & Monitoring

#### `GET /api/v1/system/health`

**Description:** Get system health check status.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-06-30T12:00:00Z",
  "version": "1.0.0",
  "uptime": 86400,
  "checks": {
    "database": { "status": "healthy" },
    "wifi_adapter": { "status": "healthy" },
    "disk_space": { "status": "healthy" },
    "memory": { "status": "healthy" }
  }
}
```

#### `GET /api/v1/system/stats`

**Description:** Get comprehensive system statistics.

**Response:**

```json
{
  "cpu_usage": 25.5,
  "memory_usage": 68.2,
  "disk_usage": 45.8,
  "temperature": 42.5,
  "uptime": 86400,
  "load_average": [0.5, 0.3, 0.2],
  "network_interfaces": {
    "wlan0": {
      "bytes_sent": 1024000,
      "bytes_recv": 2048000,
      "packets_sent": 1000,
      "packets_recv": 1500,
      "errors_in": 0,
      "errors_out": 0
    }
  }
}
```

#### `GET /api/v1/system/info`

**Description:** Get system information and capabilities.

**Response:**

```json
{
  "hostname": "piwardrive-001",
  "platform": "Linux",
  "architecture": "armv7l",
  "kernel_version": "5.10.17-v7l+",
  "python_version": "3.9.2",
  "piwardrive_version": "1.0.0",
  "hardware": {
    "model": "Raspberry Pi 4 Model B Rev 1.4",
    "serial": "10000000a1b2c3d4",
    "memory_total": 4294967296,
    "cpu_count": 4,
    "cpu_model": "ARMv7 Processor rev 3 (v7l)"
  },
  "capabilities": {
    "wifi_monitor_mode": true,
    "gps": false,
    "bluetooth": true,
    "gpio": true
  }
}
```

### Configuration Management

#### `GET /api/v1/config`

**Description:** Get current system configuration.

**Response:**

```json
{
  "app": {
    "debug": false,
    "log_level": "INFO"
  },
  "wifi": {
    "default_interface": "wlan0",
    "scan_interval": 60,
    "monitor_mode": true
  },
  "monitoring": {
    "interval": 30,
    "enabled_metrics": ["cpu", "memory", "disk", "temperature"]
  },
  "api": {
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 100
    }
  }
}
```

#### `PUT /api/v1/config`

**Description:** Update system configuration.

**Request Body:**

```json
{
  "wifi": {
    "scan_interval": 120
  },
  "monitoring": {
    "interval": 15
  }
}
```

**Response:**

```json
{
  "message": "Configuration updated successfully",
  "updated_fields": ["wifi.scan_interval", "monitoring.interval"],
  "restart_required": false
}
```

#### `POST /api/v1/config/reset`

**Description:** Reset configuration to defaults.

**Response:**

```json
{
  "message": "Configuration reset to defaults",
  "restart_required": true
}
```

### Data Export

#### `GET /api/v1/export/scans`

**Description:** Export scan data in various formats.

**Query Parameters:**

- `format`: Export format (json, csv, xml, geojson)
- `scan_ids` (optional): Comma-separated scan IDs
- `start_date` (optional): Start date filter (ISO 8601)
- `end_date` (optional): End date filter (ISO 8601)
- `include_raw_data` (optional): Include raw packet data (default: false)

**Response:** File download in requested format

#### `GET /api/v1/export/access-points`

**Description:** Export access point data.

**Query Parameters:**

- `format`: Export format (json, csv, xml, geojson, kml)
- `min_signal_strength` (optional): Minimum signal strength filter
- `encryption_types` (optional): Comma-separated encryption types
- `include_location` (optional): Include GPS coordinates (default: true)

**Response:** File download in requested format

#### `GET /api/v1/export/system-metrics`

**Description:** Export system monitoring data.

**Query Parameters:**

- `format`: Export format (json, csv, xml)
- `start_date` (optional): Start date filter
- `end_date` (optional): End date filter
- `metrics` (optional): Comma-separated metric names

**Response:** File download in requested format

### Advanced Features

#### `POST /api/v1/analysis/fingerprint`

**Description:** Create a Wi-Fi fingerprint for location identification.

**Request Body:**

```json
{
  "name": "office_location_1",
  "description": "Fingerprint for office area",
  "scan_duration": 300,
  "location": {
    "lat": 40.7128,
    "lon": -74.006,
    "accuracy": 5.0
  }
}
```

**Response:**

```json
{
  "fingerprint_id": "fp_20250630_120000",
  "name": "office_location_1",
  "created_at": "2025-06-30T12:00:00Z",
  "scan_id": "scan_20250630_120000",
  "access_points_count": 25,
  "unique_networks": 18,
  "location": {
    "lat": 40.7128,
    "lon": -74.006,
    "accuracy": 5.0
  }
}
```

#### `POST /api/v1/analysis/locate`

**Description:** Estimate location based on current Wi-Fi environment.

**Request Body:**

```json
{
  "scan_duration": 30,
  "fingerprint_database": "all",
  "min_confidence": 0.7
}
```

**Response:**

```json
{
  "estimated_location": {
    "lat": 40.7128,
    "lon": -74.006,
    "accuracy": 10.0,
    "confidence": 0.85
  },
  "matched_fingerprints": [
    {
      "fingerprint_id": "fp_20250630_120000",
      "name": "office_location_1",
      "similarity": 0.92,
      "distance": 5.2
    }
  ],
  "scan_used": "scan_20250630_123000"
}
```

#### `GET /api/v1/analysis/interference`

**Description:** Analyze Wi-Fi channel interference and congestion.

**Query Parameters:**

- `scan_id` (optional): Use specific scan data
- `channels` (optional): Comma-separated channel list to analyze

**Response:**

```json
{
  "analysis_timestamp": "2025-06-30T12:00:00Z",
  "channel_analysis": [
    {
      "channel": 6,
      "frequency": 2437,
      "access_points_count": 8,
      "interference_level": "high",
      "congestion_score": 0.85,
      "recommended": false,
      "overlapping_channels": [1, 11]
    }
  ],
  "recommendations": {
    "best_channels": [1, 11],
    "avoid_channels": [6, 7],
    "optimal_channel": 1
  }
}
```

## Real-time Streaming

### WebSocket Endpoints

#### `WebSocket /ws/v1/scans/{scan_id}`

**Description:** Stream real-time updates from an active Wi-Fi scan.

**Connection URL:** `ws://localhost:8080/ws/v1/scans/{scan_id}`

**Authentication:** Include `Authorization` header or `token` query parameter.

**Message Types:**

```json
// Scan started
{
  "type": "scan_started",
  "timestamp": "2025-06-30T12:00:00Z",
  "scan_id": "scan_20250630_120000",
  "data": {
    "scan_params": {...}
  }
}

// Access point discovered
{
  "type": "access_point_found",
  "timestamp": "2025-06-30T12:00:15Z",
  "scan_id": "scan_20250630_120000",
  "data": {
    "ssid": "TestNetwork",
    "bssid": "AA:BB:CC:DD:EE:FF",
    "signal_strength": -60,
    "channel": 6
  }
}

// Scan progress update
{
  "type": "scan_progress",
  "timestamp": "2025-06-30T12:00:30Z",
  "scan_id": "scan_20250630_120000",
  "data": {
    "progress_percent": 50,
    "access_points_found": 8,
    "current_channel": 6,
    "estimated_completion": "2025-06-30T12:01:00Z"
  }
}

// Scan completed
{
  "type": "scan_completed",
  "timestamp": "2025-06-30T12:01:00Z",
  "scan_id": "scan_20250630_120000",
  "data": {
    "total_access_points": 15,
    "unique_networks": 12,
    "actual_duration": 60,
    "scan_results_url": "/api/v1/wifi/scan/scan_20250630_120000"
  }
}
```

#### `WebSocket /ws/v1/system/metrics`

**Description:** Stream real-time system metrics and status updates.

**Connection URL:** `ws://localhost:8080/ws/v1/system/metrics`

**Message Format:**

```json
{
  "type": "system_metrics",
  "timestamp": "2025-06-30T12:00:00Z",
  "data": {
    "cpu_usage": 25.5,
    "memory_usage": 68.2,
    "disk_usage": 45.8,
    "temperature": 42.5,
    "network_io": {
      "bytes_sent": 1024,
      "bytes_recv": 2048
    }
  }
}
```

### Server-Sent Events (SSE)

#### `GET /api/v1/events/scans`

**Description:** Subscribe to scan events via Server-Sent Events.

**Query Parameters:**

- `scan_types` (optional): Filter by scan types
- `include_progress` (optional): Include progress updates (default: true)

**Content-Type:** `text/event-stream`

**Example Events:**

```
event: scan_started
data: {"scan_id": "scan_20250630_120000", "scan_type": "passive"}

event: access_point_found
data: {"scan_id": "scan_20250630_120000", "ssid": "TestAP", "signal_strength": -60}

event: scan_completed
data: {"scan_id": "scan_20250630_120000", "access_points_found": 15}
```

#### `GET /api/v1/events/system`

**Description:** Subscribe to system events and alerts.

**Content-Type:** `text/event-stream`

**Example Events:**

```
event: system_alert
data: {"level": "warning", "message": "High CPU usage detected", "metric": "cpu_usage", "value": 85.2}

event: interface_status
data: {"interface": "wlan0", "status": "monitor_mode_enabled", "channel": 6}

event: service_status
data: {"service": "kismet", "status": "started", "pid": 1234}
```

## SDK and Client Libraries

### Python SDK

```python
from piwardrive_client import PiWardriveClient

# Initialize client
client = PiWardriveClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

# Start a Wi-Fi scan
scan = await client.wifi.start_scan(
    scan_type="passive",
    duration=60,
    channels=[1, 6, 11]
)

# Get scan results
results = await client.wifi.get_scan_results(scan.scan_id)

# Get system stats
stats = await client.system.get_stats()

# Stream real-time updates
async for update in client.wifi.stream_scan_updates(scan.scan_id):
    print(f"Found AP: {update.data.ssid}")
```

### JavaScript/TypeScript SDK

```typescript
import { PiWardriveClient } from "@piwardrive/client";

const client = new PiWardriveClient({
  baseURL: "http://localhost:8080",
  apiKey: "your-api-key",
});

// Start scan
const scan = await client.wifi.startScan({
  scanType: "passive",
  duration: 60,
  channels: [1, 6, 11],
});

// Get results
const results = await client.wifi.getScanResults(scan.scanId);

// Real-time updates
client.wifi.onScanUpdate(scan.scanId, (update) => {
  console.log("Scan update:", update);
});
```

## Error Handling

### Standard Error Response Format

All API endpoints return errors in a consistent format following RFC 7807 Problem Details:

```json
{
  "error": "ValidationError",
  "message": "Scan duration must be between 5 and 3600 seconds",
  "details": {
    "field": "duration",
    "constraint": "must be between 5 and 3600",
    "received_value": 3700
  },
  "timestamp": "2025-06-30T12:00:00Z",
  "request_id": "req_123456789"
}
```

### Common Error Codes

| HTTP Status | Error Code                | Description                                    |
| ----------- | ------------------------- | ---------------------------------------------- |
| 400         | `ValidationError`         | Request validation failed                      |
| 401         | `AuthenticationError`     | Invalid or missing authentication              |
| 403         | `AuthorizationError`      | Insufficient permissions                       |
| 404         | `NotFoundError`           | Resource not found                             |
| 409         | `ConflictError`           | Resource conflict (e.g., scan already running) |
| 422         | `ProcessingError`         | Request valid but processing failed            |
| 429         | `RateLimitError`          | Rate limit exceeded                            |
| 500         | `InternalServerError`     | Server error                                   |
| 503         | `ServiceUnavailableError` | Service temporarily unavailable                |

### Error Handling Examples

```python
import httpx
from piwardrive_client.exceptions import PiWardriveAPIError

try:
    response = await client.wifi.start_scan(duration=5000)  # Invalid duration
except PiWardriveAPIError as e:
    if e.error_code == "ValidationError":
        print(f"Validation failed: {e.message}")
        print(f"Field: {e.details.get('field')}")
    elif e.error_code == "RateLimitError":
        print("Rate limit exceeded, waiting...")
        await asyncio.sleep(60)
    else:
        print(f"API error: {e}")
```

## Rate Limiting

### Default Limits

- **Unauthenticated requests**: 100 requests per minute
- **Authenticated requests**: 1000 requests per minute
- **Scan operations**: 10 requests per minute
- **Export operations**: 5 requests per minute

### Rate Limit Headers

All responses include rate limiting information:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1719748800
X-RateLimit-Window: 60
```

### Handling Rate Limits

```python
async def make_request_with_retry(client, endpoint, **kwargs):
    for attempt in range(3):
        try:
            return await client.get(endpoint, **kwargs)
        except RateLimitError as e:
            if attempt == 2:  # Last attempt
                raise
            wait_time = int(e.retry_after or 60)
            await asyncio.sleep(wait_time)
```

## Performance Optimization

### Pagination

Large datasets use cursor-based pagination:

```bash
# First page
GET /api/v1/wifi/scans?limit=50

# Next page using cursor
GET /api/v1/wifi/scans?limit=50&cursor=eyJ0aW1lc3RhbXAiOiIyMDI1LTA2LTMwVDEy...
```

### Caching

API responses include caching headers:

```
Cache-Control: public, max-age=300
ETag: "abc123def456"
Last-Modified: Wed, 30 Jun 2025 12:00:00 GMT
```

Use conditional requests to avoid unnecessary data transfer:

```bash
curl -H "If-None-Match: abc123def456" "http://localhost:8080/api/v1/system/stats"
```

### Compression

The API supports gzip compression:

```bash
curl -H "Accept-Encoding: gzip" "http://localhost:8080/api/v1/wifi/scans"
```

## Security Considerations

### API Key Management

- Store API keys securely (environment variables, key vaults)
- Rotate keys regularly
- Use different keys for different environments
- Monitor key usage for anomalies

### HTTPS in Production

Always use HTTPS in production environments:

```yaml
# nginx configuration
server {
listen 443 ssl http2;
ssl_certificate /path/to/cert.pem;
ssl_certificate_key /path/to/key.pem;

location /api/ {
proxy_pass http://localhost:8080;
proxy_set_header X-Forwarded-Proto https;
}
}
```

### Input Validation

All inputs are validated server-side. Client-side validation is for UX only:

```python
# Server validates all inputs
@app.post("/api/v1/wifi/scan")
async def start_scan(request: WiFiScanRequest):
    # Request automatically validated by Pydantic
    pass
```

## Legacy Compatibility

### Legacy Endpoints (Deprecated)

For backward compatibility, some legacy endpoints are still supported:

- `GET /status` → `GET /api/v1/system/health`
- `POST /token` → `POST /api/v1/auth/token`
- `GET /cpu` → `GET /api/v1/system/stats` (cpu_usage field)

### Migration Guide

When migrating from legacy endpoints:

1. Update base URLs from `/` to `/api/v1/`
2. Check response format changes
3. Update authentication headers
4. Test error handling with new format

## Configuration

API behavior can be customized via environment variables:

- `PIWARDRIVE_API_HOST`: Server bind address (default: "0.0.0.0")
- `PIWARDRIVE_API_PORT`: Server port (default: 8080)
- `PIWARDRIVE_CORS_ORIGINS`: CORS allowed origins
- `PIWARDRIVE_RATE_LIMIT_REQUESTS`: Rate limit per minute
- `PIWARDRIVE_SECRET_KEY`: JWT signing key
- `PIWARDRIVE_LOG_LEVEL`: API logging level

Refer to `docs/configuration.md` for complete configuration options.

## GraphQL Support (Optional)

When enabled via configuration (`PW_ENABLE_GRAPHQL=true`), PiWardrive provides a GraphQL endpoint at `/graphql` for more flexible querying:

```graphql
query GetScanResults($scanId: String!) {
  scan(id: $scanId) {
    id
    status
    startedAt
    accessPoints {
      ssid
      bssid
      signalStrength
      encryption
    }
  }

  systemStats {
    cpuUsage
    memoryUsage
    temperature
  }
}
```

## Testing the API

### Health Check

```bash
curl http://localhost:8080/api/v1/system/health
```

### API Documentation

Visit the interactive documentation:

- Swagger UI: http://localhost:8080/docs
- Enhanced docs: http://localhost:8080/api-docs

### Example Test Script

```bash
#!/bin/bash
# test-api.sh - Basic API functionality test

API_BASE="http://localhost:8080/api/v1"
API_KEY="your-api-key-here"

echo "Testing PiWardrive API..."

# Health check
echo "1. Health check..."
curl -s "$API_BASE/system/health" | jq .status

# Get system stats
echo "2. System stats..."
curl -s -H "X-API-Key: $API_KEY" "$API_BASE/system/stats" | jq .cpu_usage

# Start a scan
echo "3. Starting Wi-Fi scan..."
SCAN_RESPONSE=$(curl -s -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"scan_type":"passive","duration":30,"channels":[1,6,11]}' \
  "$API_BASE/wifi/scan")

SCAN_ID=$(echo $SCAN_RESPONSE | jq -r .scan_id)
echo "Scan ID: $SCAN_ID"

# Wait and get results
echo "4. Waiting for scan completion..."
sleep 35

echo "5. Getting scan results..."
curl -s -H "X-API-Key: $API_KEY" "$API_BASE/wifi/scan/$SCAN_ID" | jq .total_count

echo "API test completed!"
```

This comprehensive API documentation provides all the information needed to integrate with PiWardrive's REST API, including authentication, endpoints, real-time streaming, error handling, and best practices for production use.
