"""Wi-Fi scanning API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from piwardrive import service
from piwardrive.models import (
    AccessPoint,
    ErrorResponse,
    WiFiScanRequest,
    WiFiScanResponse,
)
from piwardrive.sigint_suite.wifi.scanner import async_scan_wifi

router = APIRouter(prefix="/wifi", tags=["wifi"])


@router.get(
    "/scan",
    response_model=WiFiScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_wifi_get(
    interface: str = "wlan0",
    timeout: int | None = None,
    _auth: None = Depends(service._check_auth),
) -> WiFiScanResponse:
    """Perform a Wi-Fi scan and return discovered access points."""
    nets = await async_scan_wifi(interface=interface, timeout=timeout)
    aps = [AccessPoint.model_validate(n.model_dump()) for n in nets]
    return WiFiScanResponse(access_points=aps)


@router.post(
    "/scan",
    response_model=WiFiScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_wifi_post(
    req: WiFiScanRequest,
    _auth: None = Depends(service._check_auth),
) -> WiFiScanResponse:
    """Perform a Wi-Fi scan using parameters in the request body."""
    nets = await async_scan_wifi(interface=req.interface, timeout=req.timeout)
    aps = [AccessPoint.model_validate(n.model_dump()) for n in nets]
    return WiFiScanResponse(access_points=aps)
