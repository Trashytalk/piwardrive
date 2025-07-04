from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from piwardrive import service
from piwardrive.jobs import analytics_jobs

router = APIRouter(prefix="/analytics-jobs", tags=["analytics-jobs"])


@router.get("/status")
async def get_job_status(_auth: Any = service.AUTH_DEP) -> Dict[str, Dict[str, Any]]:
    """Return execution status for background analytics jobs."""
    mgr = analytics_jobs.job_manager
    if mgr is None:
        return {}
    return mgr.get_status()


__all__ = ["router"]
