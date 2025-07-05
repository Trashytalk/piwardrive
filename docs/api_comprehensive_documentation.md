# PiWardrive API Comprehensive Documentation

This document provides comprehensive documentation for all PiWardrive API endpoints, including detailed examples, error handling, and best practices.

## Table of Contents

- [Authentication](#authentication)
- [Core Endpoints](#core-endpoints)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Real-time Streaming](#real-time-streaming)
- [Performance Optimization](#performance-optimization)
- [Security Best Practices](#security-best-practices)
- [SDK and Client Libraries](#sdk-and-client-libraries)
- [Testing Guide](#testing-guide)

## Authentication

### OAuth2 Password Flow

The primary authentication method for PiWardrive API uses OAuth2 password flow with JWT tokens.

#### Obtaining a Token

```bash
curl -X POST "http://localhost:8080/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=your_password"
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_token_here"
}
```

#### Using the Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8080/api/v1/system/health"
```

#### Token Refresh

```bash
curl -X POST "http://localhost:8080/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your_refresh_token"}'
```

### API Key Authentication

For server-to-server communication, use API keys:

```bash
curl -H "X-API-Key: your-api-key" \
  "http://localhost:8080/api/v1/system/stats"
```

## Core Endpoints

### System Monitoring

#### GET /api/v1/system/health

**Description:** Comprehensive system health check including all subsystems.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-04T15:30:00Z",
  "version": "1.0.0",
  "uptime": 86400,
  "checks": {
    "database": {
      "status": "healthy",
      "response_time": 12,
      "details": {
        "connection_pool": "8/20 active",
        "query_avg_time": "45ms"
      }
    },
    "wifi_adapter": {
      "status": "healthy",
      "interface": "wlan0",
      "mode": "monitor",
      "channel": 6
    },
    "disk_space": {
      "status": "healthy",
      "usage": 45.2,
      "free_space": "120GB"
    },
    "memory": {
      "status": "healthy",
      "usage": 68.5,
      "available": "2.1GB"
    },
    "services": {
      "kismet": "running",
      "gpsd": "running",
      "bettercap": "stopped"
    }
  }
}
```

**Error Responses:**
- `500` - System health check failed
- `503` - One or more critical services are down

#### GET /api/v1/system/stats

**Description:** Real-time system performance metrics.

**Query Parameters:**
- `interval` (optional): Aggregation interval in seconds (default: 60)
- `history` (optional): Number of historical points to include (default: 1)

**Response:**
```json
{
  "timestamp": "2025-01-04T15:30:00Z",
  "system": {
    "cpu_usage": 25.5,
    "memory_usage": 68.2,
    "disk_usage": 45.8,
    "temperature": 42.5,
    "uptime": 86400,
    "load_average": [0.5, 0.3, 0.2]
  },
  "network": {
    "interfaces": {
      "wlan0": {
        "bytes_sent": 1024000,
        "bytes_recv": 2048000,
        "packets_sent": 1000,
        "packets_recv": 1500,
        "errors_in": 0,
        "errors_out": 0,
        "speed": "1000Mbps",
        "duplex": "full"
      }
    },
    "throughput": {
      "tx_kbps": 125.5,
      "rx_kbps": 256.7
    }
  },
  "storage": {
    "total": 120000000000,
    "used": 55000000000,
    "free": 65000000000,
    "filesystem": "ext4"
  }
}
```

### Wi-Fi Scanning

#### POST /api/v1/wifi/scan

**Description:** Start a new Wi-Fi scan with advanced configuration options.

**Request Body:**
```json
{
  "scan_type": "passive",
  "duration": 60,
  "channels": [1, 6, 11],
  "interface": "wlan0",
  "description": "Office scan",
  "advanced_options": {
    "packet_capture": true,
    "beacon_analysis": true,
    "probe_requests": true,
    "handshake_capture": true
  },
  "filters": {
    "min_signal_strength": -80,
    "ssid_patterns": ["office*", "guest*"],
    "exclude_hidden": false
  },
  "location": {
    "lat": 40.7128,
    "lon": -74.0060,
    "accuracy": 5.0
  }
}
```

**Response:**
```json
{
  "scan_id": "scan_20250104_153000",
  "status": "started",
  "started_at": "2025-01-04T15:30:00Z",
  "estimated_completion": "2025-01-04T15:31:00Z",
  "scan_params": {
    "scan_type": "passive",
    "duration": 60,
    "channels": [1, 6, 11],
    "interface": "wlan0"
  },
  "websocket_url": "/ws/v1/scans/scan_20250104_153000",
  "stream_url": "/api/v1/wifi/scan/scan_20250104_153000/stream"
}
```

#### GET /api/v1/wifi/scan/{scan_id}

**Description:** Get detailed scan results including access point analysis.

**Path Parameters:**
- `scan_id`: Unique scan identifier

**Query Parameters:**
- `include_packets` (optional): Include raw packet data (default: false)
- `format` (optional): Response format (json, csv, xml)
- `analysis` (optional): Include security analysis (default: true)

**Response:**
```json
{
  "scan_id": "scan_20250104_153000",
  "status": "completed",
  "started_at": "2025-01-04T15:30:00Z",
  "completed_at": "2025-01-04T15:31:00Z",
  "duration": 60,
  "access_points": [
    {
      "bssid": "AA:BB:CC:DD:EE:FF",
      "ssid": "Office-WiFi",
      "channel": 6,
      "frequency": 2437,
      "signal_strength": -45,
      "encryption": {
        "type": "WPA2-PSK",
        "cipher": "CCMP",
        "authentication": "PSK"
      },
      "vendor": {
        "oui": "AA:BB:CC",
        "manufacturer": "Cisco Systems"
      },
      "capabilities": {
        "wps": false,
        "ht": true,
        "vht": true,
        "he": false
      },
      "location": {
        "lat": 40.7128,
        "lon": -74.0060,
        "accuracy": 5.0
      },
      "security_analysis": {
        "risk_level": "low",
        "vulnerabilities": [],
        "recommendations": ["Consider WPA3 upgrade"]
      },
      "first_seen": "2025-01-04T15:30:15Z",
      "last_seen": "2025-01-04T15:30:55Z",
      "beacon_count": 40
    }
  ],
  "statistics": {
    "total_access_points": 15,
    "unique_networks": 12,
    "hidden_networks": 2,
    "open_networks": 1,
    "encrypted_networks": 14,
    "channels_scanned": [1, 6, 11],
    "packets_captured": 1500
  },
  "scan_params": {
    "scan_type": "passive",
    "duration": 60,
    "channels": [1, 6, 11],
    "interface": "wlan0"
  }
}
```

### Analysis Endpoints

#### GET /api/v1/analysis/evil-twins

**Description:** Detect potential evil twin access points.

**Query Parameters:**
- `threshold` (optional): Similarity threshold (0.0-1.0, default: 0.8)
- `time_window` (optional): Analysis time window in hours (default: 24)

**Response:**
```json
{
  "evil_twins": [
    {
      "original": {
        "bssid": "AA:BB:CC:DD:EE:FF",
        "ssid": "Office-WiFi",
        "first_seen": "2025-01-04T10:00:00Z"
      },
      "suspicious": {
        "bssid": "11:22:33:44:55:66",
        "ssid": "Office-WiFi",
        "first_seen": "2025-01-04T14:30:00Z"
      },
      "similarity_score": 0.95,
      "risk_indicators": [
        "identical_ssid",
        "similar_signal_strength",
        "different_vendor"
      ],
      "confidence": "high"
    }
  ],
  "analysis_timestamp": "2025-01-04T15:30:00Z",
  "total_suspicious": 1
}
```

#### GET /api/v1/analysis/signal-strength

**Description:** Analyze signal strength patterns and coverage.

**Response:**
```json
{
  "coverage_analysis": {
    "total_measurements": 1500,
    "average_signal": -55.2,
    "signal_distribution": {
      "excellent": 25,
      "good": 45,
      "fair": 20,
      "poor": 10
    },
    "dead_zones": [
      {
        "location": {"lat": 40.7128, "lon": -74.0060},
        "radius": 10,
        "description": "Low signal area"
      }
    ]
  },
  "recommendations": [
    "Consider additional access point placement",
    "Investigate interference on channel 6"
  ]
}
```

## Error Handling

### Standard Error Response Format

All API endpoints return errors in a consistent RFC 7807 Problem Details format:

```json
{
  "type": "https://api.piwardrive.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "Scan duration must be between 5 and 3600 seconds",
  "instance": "/api/v1/wifi/scan",
  "timestamp": "2025-01-04T15:30:00Z",
  "request_id": "req_123456789",
  "errors": [
    {
      "field": "duration",
      "code": "range_error",
      "message": "Value must be between 5 and 3600",
      "received_value": 3700
    }
  ]
}
```

### Common HTTP Status Codes

| Status | Error Type | Description |
|--------|------------|-------------|
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (scan already running) |
| 422 | Unprocessable Entity | Valid syntax but processing failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Error Recovery Examples

#### Handling Rate Limits

```python
import time
import requests

def api_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            continue
            
        return response
    
    raise Exception("Max retries exceeded")
```

#### Handling Scan Conflicts

```python
def start_scan_with_conflict_handling(scan_params):
    response = requests.post('/api/v1/wifi/scan', json=scan_params)
    
    if response.status_code == 409:
        # Another scan is running, wait for it to complete
        active_scans = requests.get('/api/v1/wifi/scans?status=running')
        if active_scans.json()['scans']:
            scan_id = active_scans.json()['scans'][0]['scan_id']
            print(f"Waiting for scan {scan_id} to complete...")
            # Poll scan status until complete
            return wait_for_scan_completion(scan_id)
    
    return response.json()
```

## Rate Limiting

### Rate Limit Headers

All responses include rate limiting information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1641312000
X-RateLimit-Window: 60
```

### Rate Limits by Endpoint Type

| Endpoint Category | Limit | Window |
|------------------|--------|---------|
| Authentication | 10 requests | 1 minute |
| System Status | 100 requests | 1 minute |
| Wi-Fi Scanning | 10 scans | 1 hour |
| Data Export | 5 requests | 1 minute |
| Real-time Streams | 5 concurrent | - |

### Implementing Rate Limit Handling

```javascript
class PiWardriveClient {
  constructor(baseURL, apiKey) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
    this.rateLimitDelay = 0;
  }

  async request(endpoint, options = {}) {
    // Wait if we're rate limited
    if (this.rateLimitDelay > 0) {
      await new Promise(resolve => setTimeout(resolve, this.rateLimitDelay * 1000));
      this.rateLimitDelay = 0;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'X-API-Key': this.apiKey,
        ...options.headers
      }
    });

    // Handle rate limiting
    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After');
      this.rateLimitDelay = parseInt(retryAfter) || 60;
      throw new Error(`Rate limited. Retry after ${this.rateLimitDelay} seconds`);
    }

    return response;
  }
}
```

## Real-time Streaming

### WebSocket Connections

#### Scan Progress Stream

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/v1/scans/scan_123?token=your_token');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch (data.type) {
    case 'scan_started':
      console.log('Scan started:', data.scan_id);
      break;
      
    case 'access_point_found':
      console.log('New AP:', data.data.ssid, data.data.signal_strength);
      updateAPList(data.data);
      break;
      
    case 'scan_progress':
      console.log('Progress:', data.data.progress_percent + '%');
      updateProgressBar(data.data.progress_percent);
      break;
      
    case 'scan_completed':
      console.log('Scan completed. Total APs:', data.data.total_access_points);
      break;
  }
};
```

#### System Metrics Stream

```javascript
const metricsWs = new WebSocket('ws://localhost:8080/ws/v1/system/metrics');

metricsWs.onmessage = (event) => {
  const metrics = JSON.parse(event.data);
  
  updateDashboard({
    cpu: metrics.data.cpu_usage,
    memory: metrics.data.memory_usage,
    temperature: metrics.data.temperature,
    network: metrics.data.network_io
  });
};
```

### Server-Sent Events (SSE)

For simpler one-way streaming:

```javascript
const eventSource = new EventSource('/api/v1/events/system');

eventSource.addEventListener('system_alert', (event) => {
  const alert = JSON.parse(event.data);
  showNotification(alert.message, alert.severity);
});

eventSource.addEventListener('scan_update', (event) => {
  const update = JSON.parse(event.data);
  updateScanStatus(update);
});
```

## Performance Optimization

### Pagination

Use cursor-based pagination for large datasets:

```bash
# First page
GET /api/v1/wifi/scans?limit=50

# Next page
GET /api/v1/wifi/scans?limit=50&cursor=eyJ0aW1lc3RhbXAiOiIyMDI1LTAxLTA0VDE1OjMwOjAwWiJ9
```

### Caching

Leverage HTTP caching headers:

```bash
# Conditional requests
curl -H "If-None-Match: \"abc123\"" \
  "http://localhost:8080/api/v1/system/stats"

# Cache control
curl -H "Cache-Control: max-age=300" \
  "http://localhost:8080/api/v1/wifi/interfaces"
```

### Compression

Enable gzip compression:

```bash
curl -H "Accept-Encoding: gzip" \
  "http://localhost:8080/api/v1/wifi/scans"
```

### Field Selection

Request only needed fields:

```bash
GET /api/v1/wifi/scan/123?fields=scan_id,status,access_points.ssid,access_points.signal_strength
```

## Security Best Practices

### API Key Management

1. **Environment Variables**: Store API keys in environment variables
2. **Key Rotation**: Rotate keys regularly
3. **Scope Limitation**: Use different keys for different access levels
4. **Monitoring**: Monitor key usage for anomalies

```bash
# Example: Using environment variables
export PIWARDRIVE_API_KEY="your-secure-api-key"
curl -H "X-API-Key: $PIWARDRIVE_API_KEY" \
  "http://localhost:8080/api/v1/system/health"
```

### HTTPS in Production

Always use HTTPS in production:

```nginx
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

The API validates all inputs server-side:

```python
# Example: Scan duration validation
{
  "duration": 3700,  # Invalid: exceeds maximum
  "channels": [0, 15]  # Invalid: channels out of range
}

# Response:
{
  "type": "validation-error",
  "errors": [
    {
      "field": "duration",
      "message": "Must be between 5 and 3600 seconds"
    },
    {
      "field": "channels",
      "message": "Channel 0 is invalid"
    }
  ]
}
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

# Start a scan
scan = await client.wifi.start_scan(
    scan_type="passive",
    duration=60,
    channels=[1, 6, 11]
)

# Stream real-time updates
async for update in client.wifi.stream_scan_updates(scan.scan_id):
    if update.type == "access_point_found":
        print(f"Found AP: {update.data.ssid}")

# Get final results
results = await client.wifi.get_scan_results(scan.scan_id)
```

### JavaScript/TypeScript SDK

```typescript
import { PiWardriveClient } from "@piwardrive/client";

const client = new PiWardriveClient({
    baseURL: "http://localhost:8080",
    apiKey: "your-api-key",
});

// Start scan with promise
const scan = await client.wifi.startScan({
    scanType: "passive",
    duration: 60,
    channels: [1, 6, 11],
});

// Real-time updates with callback
client.wifi.onScanUpdate(scan.scanId, (update) => {
    console.log("Scan update:", update);
});

// Get results
const results = await client.wifi.getScanResults(scan.scanId);
```

## Testing Guide

### Health Check Test

```bash
#!/bin/bash
# Basic API health test

API_BASE="http://localhost:8080/api/v1"
API_KEY="your-api-key"

echo "Testing PiWardrive API..."

# Health check
echo "1. Health check..."
HEALTH=$(curl -s "$API_BASE/system/health" | jq -r .status)
if [ "$HEALTH" != "healthy" ]; then
    echo "❌ Health check failed"
    exit 1
fi
echo "✅ Health check passed"

# Authentication test
echo "2. Authentication test..."
AUTH_RESPONSE=$(curl -s -H "X-API-Key: $API_KEY" "$API_BASE/system/stats")
if echo "$AUTH_RESPONSE" | jq -e .system > /dev/null; then
    echo "✅ Authentication successful"
else
    echo "❌ Authentication failed"
    exit 1
fi

echo "All tests passed! 🎉"
```

### Integration Test Script

```python
import asyncio
import json
import requests
from piwardrive_client import PiWardriveClient

async def test_full_workflow():
    """Test complete scan workflow"""
    client = PiWardriveClient(
        base_url="http://localhost:8080",
        api_key="test-api-key"
    )
    
    # 1. Check system health
    health = await client.system.get_health()
    assert health.status == "healthy"
    
    # 2. Start a scan
    scan = await client.wifi.start_scan(
        scan_type="passive",
        duration=30,
        channels=[1, 6, 11]
    )
    
    # 3. Monitor progress
    access_points = []
    async for update in client.wifi.stream_scan_updates(scan.scan_id):
        if update.type == "access_point_found":
            access_points.append(update.data)
        elif update.type == "scan_completed":
            break
    
    # 4. Get final results
    results = await client.wifi.get_scan_results(scan.scan_id)
    
    # 5. Verify results
    assert len(results.access_points) > 0
    assert results.status == "completed"
    
    print(f"✅ Scan completed successfully. Found {len(access_points)} APs")

if __name__ == "__main__":
    asyncio.run(test_full_workflow())
```

### Load Testing

```python
import asyncio
import aiohttp
import time

async def load_test_api(concurrent_requests=10, duration=60):
    """Load test the API with concurrent requests"""
    
    async def make_request(session, url):
        try:
            async with session.get(url) as response:
                return response.status
        except Exception as e:
            return str(e)
    
    start_time = time.time()
    results = {"success": 0, "error": 0}
    
    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < duration:
            tasks = []
            for _ in range(concurrent_requests):
                task = make_request(session, "http://localhost:8080/api/v1/system/health")
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for response in responses:
                if response == 200:
                    results["success"] += 1
                else:
                    results["error"] += 1
            
            await asyncio.sleep(1)  # 1 second between batches
    
    total_requests = results["success"] + results["error"]
    success_rate = (results["success"] / total_requests) * 100
    
    print(f"Load test completed:")
    print(f"Total requests: {total_requests}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Requests per second: {total_requests / duration:.2f}")

if __name__ == "__main__":
    asyncio.run(load_test_api())
```

This comprehensive API documentation provides detailed information about all endpoints, authentication methods, error handling, real-time streaming, performance optimization, security best practices, and testing approaches. It serves as a complete reference for developers integrating with the PiWardrive API.
