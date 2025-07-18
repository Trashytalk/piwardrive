# API Documentation Enhancement Plan

## Phase 1: FastAPI OpenAPI Integration

### Step 1: Enable and Configure OpenAPI/Swagger Documentation

Update the FastAPI application instance to include comprehensive metadata and configure the OpenAPI schema:

```python
# src/piwardrive/service.py

from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

# ... existing imports

# Update the FastAPI instance with metadata
app = FastAPI(
    title="PiWardrive API",
    description="Enterprise-grade war-driving and network analysis platform API",
    version="2.0.0",
    docs_url=None,  # Disable the default docs
    redoc_url=None,  # Disable the default redoc
    openapi_url="/api/openapi.json"
)

# ... existing middleware configuration

# Create custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="PiWardrive API Documentation",
        version="2.0.0",
        description="Enterprise-grade war-driving and network analysis platform API documentation",
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    # Add additional metadata
    openapi_schema["info"]["contact"] = {
        "name": "PiWardrive Development Team",
        "url": "https://github.com/TRASHYTALK/piwardrive",
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom documentation endpoints
@app.get("/api/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="PiWardrive API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get("/api/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title="PiWardrive API Documentation - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )
```

### Step 2: Enhance API Route Documentation

Improve the documentation of each endpoint with detailed descriptions, response models, and examples:

```python
# Example for wifi routes module (src/piwardrive/routes/wifi.py)

from __future__ import annotations

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from pydantic import BaseModel, Field

# Define response models with Field for documentation
class AccessPoint(BaseModel):
    ssid: str = Field(..., description="Network name")
    bssid: str = Field(..., description="MAC address of the access point")
    signal_strength: int = Field(..., description="Signal strength in dBm")
    channel: int = Field(..., description="WiFi channel")
    encryption: str = Field(..., description="Encryption type (WPA2, WPA3, Open, etc.)")
    first_seen: str = Field(..., description="Timestamp when first detected")
    last_seen: str = Field(..., description="Timestamp when last detected")
    latitude: Optional[float] = Field(None, description="GPS latitude if available")
    longitude: Optional[float] = Field(None, description="GPS longitude if available")
    
    class Config:
        schema_extra = {
            "example": {
                "ssid": "HomeNetwork",
                "bssid": "00:11:22:33:44:55",
                "signal_strength": -67,
                "channel": 6,
                "encryption": "WPA2",
                "first_seen": "2025-07-08T10:00:00Z",
                "last_seen": "2025-07-08T10:05:00Z",
                "latitude": 37.7749,
                "longitude": -122.4194
            }
        }

class AccessPointList(BaseModel):
    access_points: List[AccessPoint] = Field(..., description="List of detected access points")
    count: int = Field(..., description="Total number of access points")
    scan_time: str = Field(..., description="Timestamp of the scan")

# Create router with prefix and tags for better organization
router = APIRouter(
    prefix="/wifi",
    tags=["WiFi"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)

@router.get(
    "/access-points",
    response_model=AccessPointList,
    summary="List WiFi Access Points",
    description="Returns a list of detected WiFi access points from the most recent scan",
    response_description="List of access points with metadata",
)
async def get_access_points(
    limit: int = Query(100, description="Maximum number of access points to return"),
    min_signal: Optional[int] = Query(None, description="Filter by minimum signal strength in dBm"),
    encryption: Optional[str] = Query(None, description="Filter by encryption type"),
):
    """
    Get a list of detected WiFi access points with optional filtering.
    
    - **limit**: Maximum number of results to return
    - **min_signal**: Only return APs with signal strength greater than this value
    - **encryption**: Filter by encryption type (WPA2, WPA3, Open, etc.)
    """
    # Implementation details...
    pass
```

### Step 3: Create Model Documentation for Complex Data Types

Create a dedicated models module with well-documented schemas:

```python
# src/piwardrive/api/models.py

from __future__ import annotations

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class EncryptionType(str, Enum):
    OPEN = "open"
    WEP = "wep"
    WPA = "wpa"
    WPA2 = "wpa2"
    WPA3 = "wpa3"
    
class DeviceType(str, Enum):
    ROUTER = "router"
    MOBILE = "mobile"
    IOT = "iot"
    UNKNOWN = "unknown"

class GeoPoint(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    accuracy: Optional[float] = Field(None, description="Accuracy of the position in meters")
    timestamp: str = Field(..., description="When the position was recorded")

class ScanResult(BaseModel):
    id: str = Field(..., description="Unique identifier for the scan result")
    device_type: DeviceType = Field(..., description="Type of detected device")
    signal_strength: int = Field(..., description="Signal strength in dBm")
    first_seen: str = Field(..., description="When the device was first detected")
    last_seen: str = Field(..., description="When the device was last detected")
    location: Optional[GeoPoint] = Field(None, description="Location where detected")
    
    @validator("signal_strength")
    def check_signal_strength(cls, v):
        if v > 0:
            raise ValueError("Signal strength should be negative (in dBm)")
        return v
```

## Phase 2: API Client Generation

### Step 1: Generate TypeScript Client for the Frontend

Create a script to generate a TypeScript client from the OpenAPI schema:

```bash
#!/bin/bash

# Install OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Generate TypeScript client
openapi-generator-cli generate \
  -i http://localhost:8080/api/openapi.json \
  -g typescript-fetch \
  -o ./webui/src/api-client \
  --additional-properties=npmName=piwardrive-api-client,supportsES6=true,withInterfaces=true

# Clean up temporary files
rm -rf ./webui/src/api-client/.openapi-generator

echo "TypeScript API client generated successfully"
```

Save this as `scripts/generate_api_client.sh` and make it executable.

### Step 2: Create API Documentation Portal

Create a dedicated documentation portal that combines the OpenAPI documentation with additional information:

```python
# src/piwardrive/web/api_docs_server.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import markdown
import re

app = FastAPI()

# Mount the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root documentation page
@app.get("/", response_class=HTMLResponse)
async def get_docs_root():
    with open("documentation/api_comprehensive_documentation.md", "r") as f:
        content = f.read()
    
    html_content = markdown.markdown(
        content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    return create_html_page("PiWardrive API Documentation", html_content)

# Helper function to create HTML pages
def create_html_page(title, content):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
        <style>
            body {{ padding: 20px; }}
            pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; }}
            .nav-tabs {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class="nav-link active" href="/">Overview</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/api/docs">Swagger UI</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/api/redoc">ReDoc</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/examples">Examples</a>
                </li>
            </ul>
            <div class="content">
                {content}
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
    </body>
    </html>
    """

# Example API usage pages
@app.get("/examples", response_class=HTMLResponse)
async def get_examples():
    examples = {
        "Authentication": """
```python
import requests

# Get authentication token
response = requests.post(
    "http://localhost:8080/api/auth/token",
    json={"username": "admin", "password": "password123"}
)
token = response.json()["access_token"]

# Use token in subsequent requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8080/api/wifi/access-points",
    headers=headers
)
```
        """,
        "WebSocket Connection": """
```javascript
const ws = new WebSocket('ws://localhost:8080/api/ws/status');

ws.onopen = () => {
  console.log('Connected to status stream');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received data:', data);
};

// Keep connection alive
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 15000);
```
        """
    }
    
    content = "<h2>API Usage Examples</h2>"
    
    for title, example in examples.items():
        content += f"<h3>{title}</h3>"
        content += markdown.markdown(example, extensions=['fenced_code', 'codehilite'])
    
    return create_html_page("PiWardrive API Examples", content)
```

## Phase 3: Create Comprehensive API Documentation

Create a comprehensive API documentation file:

```markdown
# PiWardrive API Documentation

## Overview

The PiWardrive API provides programmatic access to all features of the PiWardrive platform. This includes WiFi scanning, device detection, geospatial data, and system monitoring.

## Authentication

Most API endpoints require authentication. The API uses JWT (JSON Web Tokens) for authentication.

To authenticate:

1. Make a POST request to `/api/auth/token` with your credentials
2. Include the returned token in the `Authorization` header of subsequent requests

Example:

```python
import requests

# Get token
response = requests.post(
    "http://localhost:8080/api/auth/token",
    json={"username": "admin", "password": "password123"}
)
token = response.json()["access_token"]

# Use token
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8080/api/wifi/access-points",
    headers=headers
)
```

## API Endpoints

The API is organized into the following sections:

- WiFi - Access point scanning and analysis
- Bluetooth - Bluetooth device detection
- Cellular - Cellular network information
- Analytics - Network analysis and statistics
- Monitoring - System status and metrics
- Widgets - Dashboard widget configuration

### Common Response Formats

Most API endpoints return data in the following format:

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "metadata": {
    "timestamp": "2025-07-08T12:34:56Z",
    "version": "2.0.0"
  }
}
```

Error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "The requested resource was not found",
    "details": {
      // Additional error details
    }
  }
}
```

## WebSocket APIs

In addition to REST endpoints, PiWardrive provides real-time data through WebSockets.

Available WebSocket endpoints:

- `/api/ws/status` - System status updates
- `/api/ws/metrics` - Real-time performance metrics
- `/api/ws/scan` - Live network scanning results

WebSocket messages are JSON-formatted and follow the same structure as REST API responses.

## Rate Limiting

API requests are rate-limited to protect the system. The limits are:

- 60 requests per minute for authenticated users
- 10 requests per minute for unauthenticated users

When rate limited, the API will respond with a 429 status code.

## Versioning

The API is versioned through the URI path. The current version is v2.

- v2 (current): `/api/v2/...`
- v1 (deprecated): `/api/v1/...`

## Client Libraries

Official client libraries:

- Python: `pip install piwardrive-client`
- JavaScript: `npm install piwardrive-api-client`

## Further Documentation

- [Swagger UI](/api/docs)
- [ReDoc](/api/redoc)
- [Usage Examples](/examples)
```
