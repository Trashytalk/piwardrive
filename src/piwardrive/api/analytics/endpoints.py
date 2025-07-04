from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from piwardrive import persistence, service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/networks")
async def get_network_analytics(
    bssid: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int | None = None,
    _auth: Any = service.AUTH_DEP,
) -> list[dict[str, Any]]:
    return await persistence.load_network_analytics(
        bssid=bssid, start=start, end=end, limit=limit
    )


@router.get("/daily-stats")
async def get_daily_stats(
    session_id: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int | None = None,
    _auth: Any = service.AUTH_DEP,
) -> list[dict[str, Any]]:
    return await persistence.load_daily_detection_stats(
        session_id=session_id, start=start, end=end, limit=limit
    )


@router.get("/coverage-grid")
async def get_coverage_grid(
    limit: int | None = None,
    offset: int = 0,
    _auth: Any = service.AUTH_DEP,
) -> list[dict[str, Any]]:
    return await persistence.load_network_coverage_grid(limit=limit, offset=offset)
