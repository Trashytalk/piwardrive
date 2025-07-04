from __future__ import annotations

"""WebSocket and SSE endpoints for live detections."""

import json
from typing import Any

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from piwardrive import service
from piwardrive.services.stream_processor import stream_processor

router = APIRouter(prefix="/stream", tags=["stream"])


@router.websocket("/ws/detections")
async def ws_detections(websocket: WebSocket) -> None:
    await websocket.accept()
    queue = stream_processor.register_listener()
    try:
        while True:
            data = await queue.get()
            try:
                await service.asyncio.wait_for(websocket.send_json(data), timeout=5)
            except Exception:
                break
    except WebSocketDisconnect:
        pass
    finally:
        stream_processor.unregister_listener(queue)
        await websocket.close()


@router.get("/sse/detections")
async def sse_detections(request: Request) -> StreamingResponse:
    async def _gen() -> Any:
        queue = stream_processor.register_listener()
        try:
            while True:
                if await request.is_disconnected():
                    break
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        finally:
            stream_processor.unregister_listener(queue)

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(_gen(), media_type="text/event-stream", headers=headers)
