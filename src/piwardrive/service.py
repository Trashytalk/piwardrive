"""Simple FastAPI service for health records."""

from __future__ import annotations

import inspect
import logging
import os
import typing
from dataclasses import asdict

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional FastAPI dependency
    from fastapi import (Body, Depends, FastAPI, HTTPException, Request,
                         WebSocket, WebSocketDisconnect)
    from fastapi.responses import Response, StreamingResponse
    from fastapi.security import HTTPBasic, HTTPBasicCredentials
except Exception:
    FastAPI = type(
        "FastAPI",
        (),
        {
            "get": lambda *a, **k: (lambda f: f),
            "post": lambda *a, **k: (lambda f: f),
            "delete": lambda *a, **k: (lambda f: f),
            "websocket": lambda *a, **k: (lambda f: f),
        },
    )

    def _noop(*_a, **_k) -> None:
        return None

    Depends = _noop
    HTTPException = type("HTTPException", (Exception,), {})
    WebSocket = object
    WebSocketDisconnect = Exception
    Body = _noop
    Request = object
    StreamingResponse = Response = object
    HTTPBasic = type("HTTPBasic", (), {"__init__": lambda self, **k: None})
    HTTPBasicCredentials = type("HTTPBasicCredentials", (), {})
import asyncio
import importlib
import json
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Tuple

from piwardrive.logconfig import DEFAULT_LOG_PATH

try:  # allow tests to stub out ``persistence``
    from persistence import load_ap_cache  # type: ignore
    from persistence import (DashboardSettings, _db_path, get_table_counts,
                             load_dashboard_settings, load_recent_health,
                             save_dashboard_settings)
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive.persistence import (
        load_recent_health,
        load_ap_cache,
        load_dashboard_settings,
        save_dashboard_settings,
        get_table_counts,
        _db_path,
        DashboardSettings,
    )

from piwardrive.security import sanitize_path, verify_password

try:  # allow tests to provide a simplified utils module
    import utils as _utils
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive import utils as _utils

from typing import Awaitable, Callable

import config
import psutil
import vehicle_sensors
from sync import upload_data

from piwardrive import export, orientation_sensors
from piwardrive.config import CONFIG_DIR
from piwardrive.gpsd_client import client as gps_client

try:  # allow tests to stub out lora_scanner
    import lora_scanner as _lora_scanner  # type: ignore
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive import lora_scanner as _lora_scanner


async def _default_fetch_metrics_async(
    *_a: Any, **_k: Any
) -> tuple[list[Any], list[Any], int]:
    return [], [], 0


fetch_metrics_async: Callable[..., Awaitable[tuple[list[Any], list[Any], int]]] = (
    getattr(_utils, "fetch_metrics_async", _default_fetch_metrics_async)
)
get_avg_rssi = getattr(_utils, "get_avg_rssi", lambda *_a, **_k: None)
get_cpu_temp = getattr(_utils, "get_cpu_temp", lambda *_a, **_k: None)
get_mem_usage = getattr(_utils, "get_mem_usage", lambda *_a, **_k: None)
get_disk_usage = getattr(_utils, "get_disk_usage", lambda *_a, **_k: None)
get_network_throughput = getattr(
    _utils,
    "get_network_throughput",
    lambda *_a, **_k: (0, 0),
)
get_gps_fix_quality = getattr(_utils, "get_gps_fix_quality", lambda *_a, **_k: None)
get_gps_accuracy = getattr(_utils, "get_gps_accuracy", lambda *_a, **_k: None)

async_scan_lora: Callable[[str], Awaitable[list[str]]] = getattr(
    _lora_scanner, "async_scan_lora", lambda *_a, **_k: []
)


async def _default_service_status_async(*_a: Any, **_k: Any) -> bool:
    return False


service_status_async: Callable[[str], Awaitable[bool]] = getattr(
    _utils, "service_status_async", _default_service_status_async
)

run_service_cmd: Callable[[str, str], Tuple[bool, str, str] | None] = getattr(
    _utils, "run_service_cmd", lambda *_a, **_k: None
)


async def _default_async_tail_file(*_a: Any, **_k: Any) -> list[str]:
    return []


async_tail_file: Callable[[str, int], Awaitable[list[str]]] = getattr(
    _utils, "async_tail_file", _default_async_tail_file
)


security = HTTPBasic(auto_error=False)
app = FastAPI()

# Allowed log file paths for the /logs endpoint
ALLOWED_LOG_PATHS = [
    sanitize_path(p) for p in config.DEFAULT_CONFIG.log_paths + [DEFAULT_LOG_PATH]
]

# Path storing polygon geofences
GEOFENCE_FILE = os.path.join(CONFIG_DIR, "geofences.json")


def _load_geofences() -> list:
    """Return list of saved geofence dictionaries."""
    try:
        with open(GEOFENCE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    except FileNotFoundError:
        return []
    except Exception:
        return []
    return []


def _save_geofences(polys: list) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(GEOFENCE_FILE, "w", encoding="utf-8") as fh:
            json.dump(polys, fh, indent=2)
    except OSError as exc:
        logging.exception("Failed to save geofences: %s", exc)


def _check_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """Validate optional HTTP basic authentication."""
    pw_hash = os.getenv("PW_API_PASSWORD_HASH")
    if not pw_hash:
        return
    if not credentials or not verify_password(credentials.password, pw_hash):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/status")
async def get_status(limit: int = 5) -> list[dict]:
    """Return ``limit`` most recent :class:`HealthRecord` entries."""
    records = load_recent_health(limit)
    if inspect.isawaitable(records):
        records = await records

    return [asdict(rec) for rec in records]


async def _collect_widget_metrics() -> dict:
    """Return basic metrics used by dashboard widgets."""
    aps, _clients, handshakes = await fetch_metrics_async()
    rx, tx = get_network_throughput()
    batt_percent = batt_plugged = None
    try:
        batt = psutil.sensors_battery()
        if batt is not None:
            batt_percent = batt.percent
            batt_plugged = batt.power_plugged
    except Exception:  # pragma: no cover - optional dependency
        pass

    return {
        "cpu_temp": get_cpu_temp(),
        "bssid_count": len(aps),
        "handshake_count": handshakes,
        "avg_rssi": get_avg_rssi(aps),
        "kismet_running": await service_status_async("kismet"),
        "bettercap_running": await service_status_async("bettercap"),
        "gps_fix": get_gps_fix_quality(),
        "rx_kbps": rx,
        "tx_kbps": tx,
        "battery_percent": batt_percent,
        "battery_plugged": batt_plugged,
        "vehicle_speed": vehicle_sensors.read_speed_obd(),
        "vehicle_rpm": vehicle_sensors.read_rpm_obd(),
        "engine_load": vehicle_sensors.read_engine_load_obd(),
    }


@app.get("/api/widgets")
async def list_widgets(_auth: None = Depends(_check_auth)) -> dict:
    """Return available dashboard widget class names."""
    widgets_mod = importlib.import_module("piwardrive.widgets")
    return {"widgets": list(getattr(widgets_mod, "__all__", []))}


# Alias without the "/api" prefix for mounting under ``/api``


@app.get("/widgets")
async def list_widgets_alias(_auth: None = Depends(_check_auth)) -> dict:
    return await list_widgets(_auth)


@app.get("/widget-metrics")
async def get_widget_metrics(_auth: None = Depends(_check_auth)) -> dict:
    """Return basic metrics used by dashboard widgets."""
    return await _collect_widget_metrics()


@app.get("/plugins")
async def get_plugins(_auth: None = Depends(_check_auth)) -> list[str]:
    """Return discovered plugin widget class names."""
    from piwardrive import widgets

    return widgets.list_plugins()


@app.get("/cpu")
async def get_cpu(_auth: None = Depends(_check_auth)) -> dict:
    """Return CPU temperature and usage percentage."""
    return {
        "temp": get_cpu_temp(),
        "percent": psutil.cpu_percent(interval=None),
    }


@app.get("/ram")
async def get_ram(_auth: None = Depends(_check_auth)) -> dict:
    """Return system memory usage percentage."""
    return {"percent": get_mem_usage()}


@app.get("/storage")
async def get_storage(
    path: str = "/mnt/ssd",
    _auth: None = Depends(_check_auth),
) -> dict:
    """Return disk usage percentage for ``path``."""
    return {"percent": get_disk_usage(path)}


@app.get("/orientation")
async def get_orientation_endpoint(
    _auth: None = Depends(_check_auth),
) -> dict:
    """Return device orientation and raw sensor data."""
    orient = await asyncio.to_thread(orientation_sensors.get_orientation_dbus)
    angle = None
    accel = gyro = None
    if orient:
        angle = orientation_sensors.orientation_to_angle(orient)
    else:
        data = await asyncio.to_thread(orientation_sensors.read_mpu6050)
        if data:
            accel = data.get("accelerometer")
            gyro = data.get("gyroscope")
    return {
        "orientation": orient,
        "angle": angle,
        "accelerometer": accel,
        "gyroscope": gyro,
    }


@app.get("/vehicle")
async def get_vehicle_endpoint(_auth: None = Depends(_check_auth)) -> dict:
    """Return vehicle metrics from OBD-II sensors."""
    return {
        "speed": vehicle_sensors.read_speed_obd(),
        "rpm": vehicle_sensors.read_rpm_obd(),
        "engine_load": vehicle_sensors.read_engine_load_obd(),
    }


@app.get("/gps")
async def get_gps_endpoint(_auth: None = Depends(_check_auth)) -> dict:
    """Return current GPS position."""
    pos = await asyncio.to_thread(gps_client.get_position)
    lat = lon = None
    if pos:
        lat, lon = pos
    return {
        "lat": lat,
        "lon": lon,
        "accuracy": get_gps_accuracy(),
        "fix": get_gps_fix_quality(),
    }


@app.get("/logs")
async def get_logs(
    lines: int = 200,
    path: str = DEFAULT_LOG_PATH,
    _auth: None = Depends(_check_auth),
) -> dict:
    """Return last ``lines`` from ``path``."""
    safe = sanitize_path(path)
    if safe not in ALLOWED_LOG_PATHS:
        raise HTTPException(status_code=400, detail="Invalid log path")
    data = async_tail_file(safe, lines)
    if inspect.isawaitable(data):
        lines_out = await data
    else:
        lines_out = data
    return {"path": safe, "lines": lines_out}


@app.get("/db-stats")
async def get_db_stats_endpoint(_auth: None = Depends(_check_auth)) -> dict:
    """Return SQLite table counts and database size."""
    counts = await get_table_counts()
    try:
        size_kb = os.path.getsize(_db_path()) / 1024
    except OSError:
        size_kb = None
    return {"size_kb": size_kb, "tables": counts}


@app.get("/lora-scan")
async def lora_scan_endpoint(
    iface: str = "lora0", _auth: None = Depends(_check_auth)
) -> dict:
    """Run ``lora-scan`` on ``iface`` and return output lines."""
    lines = await async_scan_lora(iface)
    return {"count": len(lines), "lines": lines}


@app.post("/command")
async def run_command(
    data: dict = Body(...), _auth: None = Depends(_check_auth)
) -> dict:
    """Execute a shell command and return its output."""
    cmd = str(data.get("cmd", "")).strip()
    if not cmd:
        raise HTTPException(status_code=400, detail="cmd required")
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    try:
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
    except asyncio.TimeoutError:
        proc.kill()
        return {"output": "", "error": "timeout"}
    return {"output": out.decode()}


@app.post("/service/{name}/{action}")
async def control_service_endpoint(
    name: str,
    action: str,
    _auth: None = Depends(_check_auth),
) -> dict:
    """Start or stop a systemd service."""
    if action not in {"start", "stop", "restart"}:
        raise HTTPException(status_code=400, detail="Invalid action")
    result = run_service_cmd(name, action) or (False, "", "")
    success, _out, err = result
    if not success:
        msg = err.strip() if isinstance(err, str) else str(err)
        raise HTTPException(status_code=500, detail=msg or "command failed")
    return {"service": name, "action": action, "success": True}


@app.get("/service/{name}")
async def get_service_status_endpoint(
    name: str, _auth: None = Depends(_check_auth)
) -> dict:
    """Return whether a ``systemd`` service is active."""
    active = await service_status_async(name)
    return {"service": name, "active": active}


@app.get("/config")
async def get_config_endpoint(_auth: None = Depends(_check_auth)) -> dict:
    """Return the current configuration from ``config.json``."""
    return asdict(config.load_config())


@app.post("/config")
async def update_config_endpoint(
    updates: dict = Body(...),
    _auth: None = Depends(_check_auth),
) -> dict:
    """Update configuration values and persist them."""
    cfg = config.load_config()
    data = asdict(cfg)
    for key, value in updates.items():
        if key not in data:
            raise HTTPException(status_code=400, detail=f"Unknown field: {key}")
        data[key] = value
    if data.get("remote_sync_url", "") == "":
        data["remote_sync_url"] = None
    try:
        config.validate_config_data(data)
    except Exception as exc:  # pragma: no cover - validation tested separately
        raise HTTPException(status_code=400, detail=str(exc))
    config.save_config(config.Config(**data))
    return data


@app.get("/dashboard-settings")
async def get_dashboard_settings_endpoint(
    _auth: None = Depends(_check_auth),
) -> dict:
    """Return persisted dashboard layout and widget list."""
    settings = await load_dashboard_settings()
    return {"layout": settings.layout, "widgets": settings.widgets}


@app.post("/dashboard-settings")
async def update_dashboard_settings_endpoint(
    data: dict = Body(...),
    _auth: None = Depends(_check_auth),
) -> dict:
    """Persist dashboard layout and widget list."""
    layout = data.get("layout", [])
    widgets = data.get("widgets", [])
    await save_dashboard_settings(DashboardSettings(layout=layout, widgets=widgets))
    return {"layout": layout, "widgets": widgets}


@app.get("/geofences")
async def list_geofences_endpoint(_auth: None = Depends(_check_auth)) -> list:
    """Return saved geofence polygons."""
    return _load_geofences()


@app.post("/geofences")
async def add_geofence_endpoint(
    data: dict = Body(...), _auth: None = Depends(_check_auth)
) -> list:
    """Add a new polygon to ``geofences.json``."""
    polys = _load_geofences()
    polys.append(
        {
            "name": data.get("name", "geofence"),
            "points": data.get("points", []),
            "enter_message": data.get("enter_message"),
            "exit_message": data.get("exit_message"),
        }
    )
    _save_geofences(polys)
    return polys


@app.put("/geofences/{name}")
async def update_geofence_endpoint(
    name: str,
    updates: dict = Body(...),
    _auth: None = Depends(_check_auth),
) -> dict:
    """Modify a saved polygon."""
    polys = _load_geofences()
    for poly in polys:
        if poly.get("name") == name:
            if "name" in updates:
                poly["name"] = updates["name"]
            if "points" in updates:
                poly["points"] = updates["points"]
            if "enter_message" in updates:
                poly["enter_message"] = updates["enter_message"]
            if "exit_message" in updates:
                poly["exit_message"] = updates["exit_message"]
            _save_geofences(polys)
            return poly
    raise HTTPException(status_code=404, detail="Not found")


@app.delete("/geofences/{name}")
async def remove_geofence_endpoint(
    name: str, _auth: None = Depends(_check_auth)
) -> dict:
    """Delete ``name`` from ``geofences.json``."""
    polys = _load_geofences()
    for idx, poly in enumerate(polys):
        if poly.get("name") == name:
            polys.pop(idx)
            _save_geofences(polys)
            return {"removed": True}
    raise HTTPException(status_code=404, detail="Not found")


@app.post("/sync")
async def sync_records(limit: int = 100, _auth: None = Depends(_check_auth)) -> dict:
    """Upload recent health records to the configured sync endpoint."""
    records = load_recent_health(limit)
    if inspect.isawaitable(records):
        records = await records
    success = await upload_data([asdict(r) for r in records])
    if not success:
        raise HTTPException(status_code=502, detail="Upload failed")
    return {"uploaded": len(records)}


EXPORT_CONTENT_TYPES = {
    "csv": "text/csv",
    "json": "application/json",
    "gpx": "application/gpx+xml",
    "kml": "application/vnd.google-earth.kml+xml",
    "geojson": "application/geo+json",
    "shp": "application/octet-stream",
}


def _make_export_response(data: bytes, fmt: str, name: str) -> Response:
    """Return ``Response`` serving ``data`` as ``name.fmt``."""
    return Response(
        content=data,
        media_type=EXPORT_CONTENT_TYPES.get(fmt, "application/octet-stream"),
        headers={"Content-Disposition": f"attachment; filename={name}.{fmt}"},
    )


async def _export_layer(
    records: Sequence[Mapping[str, Any]], fmt: str, name: str
) -> Response:
    """Convert ``records`` to ``fmt`` and return as HTTP response."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        export.export_records(records, tmp.name, fmt)
        tmp.flush()
        path = tmp.name
    data = Path(path).read_bytes()
    os.remove(path)
    return _make_export_response(data, fmt, name)


@app.get("/export/aps")
async def export_access_points(
    fmt: str = "geojson", _auth: None = Depends(_check_auth)
) -> Response:
    """Return saved Wi-Fi access points in the specified format."""
    records = load_ap_cache()
    if inspect.isawaitable(records):
        records = await records
    try:
        from sigint_integration import load_sigint_data

        records.extend(load_sigint_data("wifi"))
    except Exception:
        pass
    return await _export_layer(records, fmt.lower(), "aps")


@app.get("/export/bt")
async def export_bluetooth(
    fmt: str = "geojson", _auth: None = Depends(_check_auth)
) -> Response:
    """Return saved Bluetooth device data in the specified format."""
    try:
        from sigint_integration import load_sigint_data

        records = load_sigint_data("bluetooth")
    except Exception:
        records = []
    return await _export_layer(records, fmt.lower(), "bt")


@app.websocket("/ws/aps")
async def ws_aps(websocket: WebSocket) -> None:
    """Stream new access points over WebSocket."""
    await websocket.accept()
    seq = 0
    last_time = 0.0
    error_count = 0
    try:
        while True:
            start = time.perf_counter()
            records = load_ap_cache(last_time)
            if inspect.isawaitable(records):
                records = await records
            load_time = time.perf_counter() - start
            new = records
            logger.debug("ws_aps: fetched %d aps in %.6fs", len(new), load_time)
            if new:
                last_time = max(r["last_time"] for r in new)
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "aps": new,
                "load_time": load_time,
                "errors": error_count,
            }
            try:
                await asyncio.wait_for(websocket.send_json(data), timeout=1)
            except (asyncio.TimeoutError, Exception):
                error_count += 1
                await websocket.close()
                break
            seq += 1
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass


@app.get("/sse/aps")
async def sse_aps(request: Request) -> StreamingResponse:
    """Stream new access points via Server-Sent Events."""

    async def _event_gen() -> typing.AsyncGenerator[str, None]:
        seq = 0
        last_time = 0.0
        error_count = 0
        while True:
            if await request.is_disconnected():
                break
            start = time.perf_counter()
            records = load_ap_cache(last_time)
            if inspect.isawaitable(records):
                records = await records
            load_time = time.perf_counter() - start
            new = records
            logger.debug("sse_aps: fetched %d aps in %.6fs", len(new), load_time)
            if new:
                last_time = max(r["last_time"] for r in new)
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "aps": new,
                "load_time": load_time,
                "errors": error_count,
            }
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await asyncio.sleep(2)

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )


@app.websocket("/ws/status")
async def ws_status(websocket: WebSocket) -> None:
    """Stream status and widget metrics periodically over WebSocket."""
    await websocket.accept()
    seq = 0
    error_count = 0
    try:
        while True:
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "status": await get_status(),
                "metrics": await _collect_widget_metrics(),
                "errors": error_count,
            }
            try:
                await asyncio.wait_for(websocket.send_json(data), timeout=1)
            except (asyncio.TimeoutError, Exception):
                error_count += 1
                await websocket.close()
                break
            seq += 1
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass


@app.get("/sse/status")
async def sse_status(request: Request) -> StreamingResponse:
    """Stream status and widget metrics via Server-Sent Events."""

    async def _event_gen() -> typing.AsyncGenerator[str, None]:
        seq = 0
        error_count = 0
        while True:
            if await request.is_disconnected():
                break
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "status": await get_status(),
                "metrics": await _collect_widget_metrics(),
                "errors": error_count,
            }
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await asyncio.sleep(2)

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )


async def main() -> None:

    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        from utils import shutdown_async_loop

        shutdown_async_loop()
