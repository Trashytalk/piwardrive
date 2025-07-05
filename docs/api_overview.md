# PiWardrive API Overview

PiWardrive exposes a REST API served by FastAPI. The base URL is `http://localhost:8000/api` unless overridden by `PW_WEBUI_PORT`.

## API Architecture Overview

```mermaid
graph TB
    A[Client Applications] --> B[FastAPI Server]
    B --> C[API Router]
    C --> D[Health Endpoints]
    C --> E[Wi-Fi Scan Endpoints]
    C --> F[Configuration Endpoints]
    C --> G[Export Endpoints]
    C --> H[Analytics Endpoints]
    C --> I[Security Endpoints]
    
    D --> J[System Health]
    E --> K[Scan Control]
    F --> L[Config Management]
    G --> M[Data Export]
    H --> N[Statistics]
    I --> O[Security Analysis]
    
    B --> P[Interactive Docs]
    P --> Q[Swagger UI]
    P --> R[ReDoc]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#ffebee
    style G fill:#e0f2f1
    style H fill:#e1f5fe
    style I fill:#fff3e0
```

## API Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Router
    participant Service
    participant Database
    
    Client->>FastAPI: HTTP Request
    FastAPI->>Router: Route to Endpoint
    Router->>Service: Business Logic
    Service->>Database: Data Query
    Database-->>Service: Results
    Service-->>Router: Processed Data
    Router-->>FastAPI: JSON Response
    FastAPI-->>Client: HTTP Response
    
    Note over FastAPI: Automatic OpenAPI docs
    Note over Service: Async processing
```

Common endpoints include:

| Endpoint               | Method  | Description                      |
| ---------------------- | ------- | -------------------------------- |
| `/status/health`       | GET     | Return system health information |
| `/wifi/scan`           | POST    | Start a Wi-Fi scan               |
| `/wifi/scan/{scan_id}` | GET     | Retrieve results for a scan      |
| `/config`              | GET/PUT | Read or update configuration     |
| `/export/scans`        | GET     | Export scan data                 |
| `/analytics/daily-stats` | GET | Daily detection statistics |
| `/analytics/coverage-grid` | GET | Network coverage grid |
| `/security/suspicious` | GET | List suspicious activities |

See `docs/api.md` for the complete OpenAPI specification and advanced examples.

Interactive API documentation is available when running the server:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

For a simple demonstration of the detection services see
`examples/security_analysis_example.py`.
