from __future__ import annotations

"""Demographic analytics API routes."""

from typing import Any, Dict

from fastapi import APIRouter

from piwardrive.services import demographic_analytics
from piwardrive import service

router = APIRouter(prefix="/demographics", tags=["demographics"])


@router.get("/social")
async def get_social_insights(_auth: Any = service.AUTH_DEP) -> Dict[str, Any]:
    """Return social analytics derived from demographic data."""
    return {
        "socioeconomic_correlation": demographic_analytics.socioeconomic_correlation(),
        "technology_adoption_patterns": demographic_analytics.technology_adoption_patterns(),
        "digital_divide": demographic_analytics.digital_divide_assessment(),
        "community_networks": demographic_analytics.community_network_detection(),
    }


@router.get("/adoption")
async def get_technology_adoption(_auth: Any = service.AUTH_DEP) -> Dict[str, Any]:
    """Return technology adoption metrics."""
    return demographic_analytics.adoption_summary()


@router.get("/equity")
async def get_digital_equity(_auth: Any = service.AUTH_DEP) -> Dict[str, Any]:
    """Return digital equity analytics."""
    return demographic_analytics.digital_equity_metrics()


__all__ = ["router"]

