from __future__ import annotations

"""Simple FastAPI service for health records."""

from dataclasses import asdict
import os
import inspect

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import asyncio


from logconfig import DEFAULT_LOG_PATH
from persistence import load_recent_health
from security import sanitize_path, verify_password
from utils import (
    fetch_metrics_async,
    get_avg_rssi,
    get_cpu_temp,
    get_gps_fix_quality,
    service_status_async,
    tail_file,
)

security = HTTPBasic(auto_error=False)
app = FastAPI()


def _check_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """Validate optional HTTP basic authentication."""
    pw_hash = os.getenv("PW_API_PASSWORD_HASH")
    if not pw_hash:
        return
    if not verify_password(credentials.password, pw_hash):
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
    return {
        "cpu_temp": get_cpu_temp(),
        "bssid_count": len(aps),
        "handshake_count": handshakes,
        "avg_rssi": get_avg_rssi(aps),
        "kismet_running": await service_status_async("kismet"),
        "bettercap_running": await service_status_async("bettercap"),
        "gps_fix": get_gps_fix_quality(),
    }


@app.get("/widget-metrics")
async def get_widget_metrics(_auth: None = Depends(_check_auth)) -> dict:
    """Return basic metrics used by dashboard widgets."""
    return await _collect_widget_metrics()


@app.get("/logs")
def get_logs(
    lines: int = 200,
    path: str = DEFAULT_LOG_PATH,
    _auth: None = Depends(_check_auth),
) -> dict:
    """Return last ``lines`` from ``path``."""
    safe = sanitize_path(path)
    return {"path": safe, "lines": tail_file(safe, lines)}


@app.websocket("/ws/status")
async def ws_status(websocket: WebSocket) -> None:
    """Stream status and widget metrics periodically over WebSocket."""
    await websocket.accept()
    try:
        while True:
            data = {
                "status": await get_status(),
                "metrics": await _collect_widget_metrics(),
            }
            await websocket.send_json(data)
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
