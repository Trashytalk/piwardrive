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
application. Any custom integrations should switch to importing routes from the
new packages, though old names remain for backward compatibility.

## Lazy Widget Manager

Widgets are no longer instantiated directly on startup. A new
`LazyWidgetManager` loads widget classes only when requested and
releases them if memory usage grows.  Existing code creating widgets
directly will continue to work but may load modules eagerly.  To take
advantage of lazy loading use::

    from piwardrive import LazyWidgetManager
    from piwardrive.resource_manager import ResourceManager

    manager = LazyWidgetManager(ResourceManager())
    widget = await manager.get_widget("SignalStrengthWidget")

The manager registers widgets with `ResourceManager` so `deactivate()`
methods run when instances are garbage collected or explicitly
released.

