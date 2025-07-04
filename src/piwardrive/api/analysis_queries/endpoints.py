from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from piwardrive import service
from piwardrive.services import analysis_queries

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/evil-twins")
async def get_evil_twins(_auth: Any = service.AUTH_DEP) -> list[dict[str, Any]]:
    return await analysis_queries.evil_twin_detection()


@router.get("/signal-strength")
async def get_signal_strength(_auth: Any = service.AUTH_DEP) -> list[dict[str, Any]]:
    return await analysis_queries.signal_strength_analysis()


@router.get("/network-security")
async def get_network_security(_auth: Any = service.AUTH_DEP) -> list[dict[str, Any]]:
    return await analysis_queries.network_security_analysis()


@router.get("/temporal-patterns")
async def get_temporal_patterns(_auth: Any = service.AUTH_DEP) -> list[dict[str, Any]]:
    return await analysis_queries.temporal_pattern_analysis()


@router.get("/mobile-devices")
async def get_mobile_devices(_auth: Any = service.AUTH_DEP) -> list[dict[str, Any]]:
    return await analysis_queries.mobile_device_detection()
