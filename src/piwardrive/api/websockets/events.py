from __future__ import annotations

import json
from typing import AsyncGenerator

from fastapi import Request
from fastapi.responses import StreamingResponse

from piwardrive import service
from piwardrive.database_service import db_service


async def broadcast_events(request: Request) -> StreamingResponse:
    """Stream access point updates using Server-Sent Events."""

    async def _gen() -> AsyncGenerator[str, None]:
        seq = 0
        last_time = 0.0
        while True:
            if await request.is_disconnected():
                break
            records = db_service.load_ap_cache(last_time)
            if service.inspect.isawaitable(records):
                records = await records
            if records:
                last_time = max(r["last_time"] for r in records)
            _data = {"seq": seq, "aps": records}
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await service.asyncio.sleep(service.STREAM_SLEEP)

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(_gen(), media_type="text/event-stream", headers=headers)
