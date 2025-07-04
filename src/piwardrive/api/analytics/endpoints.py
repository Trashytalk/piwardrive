from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from piwardrive import persistence, service
from piwardrive.analytics import (
    capacity_planning_forecast,
    failure_prediction,
    identify_expansion_opportunities,
    predict_network_lifecycle,
)

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


@router.get("/lifecycle")
async def get_lifecycle_forecast(
    bssid: str | None = None,
    steps: int = 7,
    _auth: Any = service.AUTH_DEP,
) -> dict[str, list[float]]:
    rows = await persistence.load_network_analytics(bssid=bssid, limit=50)
    pred, ci = predict_network_lifecycle(rows, steps)
    return {"forecast": pred, "confidence": ci}


@router.get("/capacity")
async def get_capacity_forecast(
    steps: int = 7,
    _auth: Any = service.AUTH_DEP,
) -> dict[str, list[float]]:
    rows = await persistence.load_daily_detection_stats(limit=50)
    pred, ci = capacity_planning_forecast(rows, steps)
    return {"forecast": pred, "confidence": ci}


@router.get("/predictive")
async def get_predictive_summary(
    _auth: Any = service.AUTH_DEP,
) -> dict[str, Any]:
    lifecycle_rows = await persistence.load_network_analytics(limit=50)
    daily_rows = await persistence.load_daily_detection_stats(limit=50)
    life_pred, life_ci = predict_network_lifecycle(lifecycle_rows, 7)
    cap_pred, cap_ci = capacity_planning_forecast(daily_rows, 7)
    fail_pred, fail_ci = failure_prediction(lifecycle_rows, 7)
    expansion = identify_expansion_opportunities(lifecycle_rows)
    return {
        "lifecycle": {"forecast": life_pred, "confidence": life_ci},
        "capacity": {"forecast": cap_pred, "confidence": cap_ci},
        "failure": {"forecast": fail_pred, "confidence": fail_ci},
        "expansion": expansion,
    }
