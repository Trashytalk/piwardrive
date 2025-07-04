from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from piwardrive import service, persistence

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
