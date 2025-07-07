from __future__ import annotations

"""WebSocket handlers."""

import inspect
import json
import time
from typing import Any

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from piwardrive import service
from piwardrive.database_service import db_service

router = APIRouter()


@router.websocket("/ws/aps")
async def ws_aps(websocket: WebSocket) -> None:
    await websocket.accept()
    seq = 0
    last_time = 0.0
    error_count = 0
    try:
        while True:
            start = time.perf_counter()
            records = db_service.load_ap_cache(last_time)
            if inspect.isawaitable(records):
                records = await records
            load_time = time.perf_counter() - start
            new = records
            service.logger.debug("ws_aps: fetched %d aps in %.6fs", len(new), load_time)
            if new:
                last_time = max(r["last_time"] for r in new)
            _data = {
                "seq": seq,
                "timestamp": time.time(),
                "aps": new,
                "load_time": load_time,
                "errors": error_count,
            }
            try:
                await service.asyncio.wait_for(
                    websocket.send_json(data), timeout=service.WEBSOCKET_SEND_TIMEOUT
                )
            except (service.asyncio.TimeoutError, Exception):
                error_count += 1
                await websocket.close()
                break
            seq += 1
            await service.asyncio.sleep(service.STREAM_SLEEP)
    except WebSocketDisconnect:
        pass


@router.get("/sse/aps")
async def sse_aps(request: Request) -> StreamingResponse:
    async def _event_gen():
        seq = 0
        last_time = 0.0
        error_count = 0
        while True:
            if await request.is_disconnected():
                break
            start = time.perf_counter()
            records = db_service.load_ap_cache(last_time)
            if inspect.isawaitable(records):
                records = await records
            load_time = time.perf_counter() - start
            new = records
            service.logger.debug(
                "sse_aps: fetched %d aps in %.6fs", len(new), load_time
            )
            if new:
                last_time = max(r["last_time"] for r in new)
            _data = {
                "seq": seq,
                "timestamp": time.time(),
                "aps": new,
                "load_time": load_time,
                "errors": error_count,
            }
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await service.asyncio.sleep(service.STREAM_SLEEP)

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )


@router.websocket("/ws/status")
async def ws_status(websocket: WebSocket) -> None:
    await websocket.accept()
    seq = 0
    error_count = 0
    try:
        while True:
            _data = {
                "seq": seq,
                "timestamp": time.time(),
                "status": await service.get_status(),
                "metrics": await service._collect_widget_metrics(),
                "errors": error_count,
            }
            try:
                await service.asyncio.wait_for(
                    websocket.send_json(data), timeout=service.WEBSOCKET_SEND_TIMEOUT
                )
            except (service.asyncio.TimeoutError, Exception):
                error_count += 1
                await websocket.close()
                break
            seq += 1
            await service.asyncio.sleep(service.STREAM_SLEEP)
    except WebSocketDisconnect:
        pass


@router.get("/sse/status")
async def sse_status(request: Request) -> StreamingResponse:
    async def _event_gen():
        seq = 0
        error_count = 0
        while True:
            if await request.is_disconnected():
                break
            _data = {
                "seq": seq,
                "timestamp": time.time(),
                "status": await service.get_status(),
                "metrics": await service._collect_widget_metrics(),
                "errors": error_count,
            }
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await service.asyncio.sleep(service.STREAM_SLEEP)

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )
