from __future__ import annotations

"""API endpoints exposing maintenance job status."""

from typing import Any, Dict

from fastapi import APIRouter

from piwardrive.api.auth import AUTH_DEP
from piwardrive.jobs import maintenance_jobs

router = APIRouter(prefix="/maintenance-jobs", tags=["maintenance-jobs"])


@router.get("/status")
async def get_job_status(_auth: Any = AUTH_DEP) -> Dict[str, Dict[str, Any]]:
    """Return execution status for background maintenance jobs."""
    mgr = maintenance_jobs.job_manager
    if mgr is None:
        return {}
    return mgr.get_status()


__all__ = ["router"]
