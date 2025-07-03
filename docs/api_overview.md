# PiWardrive API Overview

PiWardrive exposes a REST API served by FastAPI. The base URL is `http://localhost:8000/api` unless overridden by `PW_WEBUI_PORT`.

Common endpoints include:

| Endpoint               | Method  | Description                      |
| ---------------------- | ------- | -------------------------------- |
| `/status/health`       | GET     | Return system health information |
| `/wifi/scan`           | POST    | Start a Wi-Fi scan               |
| `/wifi/scan/{scan_id}` | GET     | Retrieve results for a scan      |
| `/config`              | GET/PUT | Read or update configuration     |
| `/export/scans`        | GET     | Export scan data                 |

See `docs/api.md` for the complete OpenAPI specification and advanced examples.
