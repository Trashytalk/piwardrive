"""Module service."""
from __future__ import annotations

"""Simple FastAPI service for health records."""

from dataclasses import asdict
import os
import inspect

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    Body,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import asyncio
import time


from logconfig import DEFAULT_LOG_PATH
from persistence import load_recent_health
from security import sanitize_path, verify_password
from utils import (
    fetch_metrics_async,
    get_avg_rssi,
    get_cpu_temp,
    get_network_throughput,
    get_gps_fix_quality,
    service_status_async,
    async_tail_file,
)
import config
from sync import upload_data

security = HTTPBasic(auto_error=False)
app = FastAPI()


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
    }


@app.get("/widget-metrics")
async def get_widget_metrics(_auth: None = Depends(_check_auth)) -> dict:
    """Return basic metrics used by dashboard widgets."""
    return await _collect_widget_metrics()


@app.get("/logs")
async def get_logs(
    lines: int = 200,
    path: str = DEFAULT_LOG_PATH,
    _auth: None = Depends(_check_auth),
) -> dict:
    """Return last ``lines`` from ``path``."""
    safe = sanitize_path(path)
    data = async_tail_file(safe, lines)
    if inspect.isawaitable(data):
        lines_out = await data
    else:
        lines_out = data
    return {"path": safe, "lines": lines_out}


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
