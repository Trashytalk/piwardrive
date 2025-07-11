from __future__ import annotations

"""Monitoring and alerting API endpoints."""

from typing import Any

from fastapi import APIRouter

from piwardrive.api.auth import AUTH_DEP
from piwardrive.services import monitoring

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/performance")
async def get_performance(_auth: Any = AUTH_DEP) -> dict[str, Any]:
    """Return aggregated performance metrics."""
    return await monitoring.collect_performance_metrics()


__all__ = ["router"]
