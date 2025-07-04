# Service API Refactor Migration Guide

The original `piwardrive.service` module provided all API endpoints in a single file.
This refactor splits the routes into domain specific packages under `piwardrive/api`.
Existing public functions are re-exported from `piwardrive.service` so existing
imports continue to work.

## New Packages
- `piwardrive/api/auth` – authentication and token management
- `piwardrive/api/health` – health records and sync endpoints
- `piwardrive/api/widgets` – widget metadata and settings
- `piwardrive/api/system` – system information and configuration
- `piwardrive/api/websockets` – WebSocket and SSE handlers

The main `service.py` now imports these routers and includes them on the FastAPI
application.  Authentication helpers and common utility functions moved to
`api/auth/dependencies.py` and `api/common.py`.  Any custom integrations should
switch to importing routes from the new packages, though old names remain for
backward compatibility.
