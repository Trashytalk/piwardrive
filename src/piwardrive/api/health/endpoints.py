from __future__ import annotations

"""Health monitoring API routes."""

import inspect
import json
from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from piwardrive import service
from piwardrive.analytics.baseline import analyze_health_baseline, load_baseline_health
from piwardrive.database_service import db_service
from piwardrive.exceptions import ServiceError
from piwardrive.sync import upload_data

from .models import BaselineAnalysisResult, HealthRecordDict, SyncResponse

router = APIRouter()


@router.get("/status")
async def get_status(
    limit: int = 5, _auth: Any = service.AUTH_DEP
) -> list[HealthRecordDict]:
    records = db_service.load_recent_health(limit)
    if inspect.isawaitable(records):
        records = await records
    return [asdict(rec) for rec in records]


@router.get("/baseline-analysis")
async def baseline_analysis_endpoint(
    limit: int = 10,
    days: int = 30,
    threshold: float = 5.0,
    _auth: Any = service.AUTH_DEP,
) -> BaselineAnalysisResult:
    recent = db_service.load_recent_health(limit)
    if inspect.isawaitable(recent):
        recent = await recent
    baseline = load_baseline_health(days, limit)
    if inspect.isawaitable(baseline):
        baseline = await baseline
    return analyze_health_baseline(recent, baseline, threshold)


@router.post("/sync")
async def sync_records(limit: int = 100, _auth: Any = service.AUTH_DEP) -> SyncResponse:
    records = db_service.load_recent_health(limit)
    if inspect.isawaitable(records):
        records = await records
    success = await upload_data([asdict(r) for r in records])
    if not success:
        raise ServiceError("Upload failed", status_code=502)
    return {"uploaded": len(records)}


@router.get("/sse/history")
async def sse_history(
    request: Request, limit: int = 100, interval: float = 1.0
) -> StreamingResponse:
    records = await db_service.load_health_history()
    if limit:
        records = records[-limit:]

    async def _event_gen():
        seq = 0
        for rec in records:
            if await request.is_disconnected():
                break
            data = {"seq": seq, "record": asdict(rec)}
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await service.asyncio.sleep(max(interval, service.MIN_EVENT_INTERVAL))

    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )
