"""Cellular scanning API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from piwardrive import service
from piwardrive.models import (
    CellTower,
    CellularScanRequest,
    CellularScanResponse,
    ErrorResponse,
)
from piwardrive.services import cellular_scanner

router = APIRouter(prefix="/cellular", tags=["cellular"])


@router.get(
    "/scan",
    response_model=CellularScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_cellular_get(
    timeout: int | None = None,
    _auth: None = Depends(service._check_auth),
) -> CellularScanResponse:
    """Perform a cellular scan and return discovered towers."""
    towers = await cellular_scanner.scan_cell_towers(timeout=timeout)
    result = [CellTower.model_validate(t.__dict__) for t in towers]
    await cellular_scanner.record_cellular_detections(result)
    return CellularScanResponse(towers=result)


@router.post(
    "/scan",
    response_model=CellularScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_cellular_post(
    req: CellularScanRequest,
    _auth: None = Depends(service._check_auth),
) -> CellularScanResponse:
    """Perform a cellular scan using parameters in the request body."""
    towers = await cellular_scanner.scan_cell_towers(timeout=req.timeout)
    result = [CellTower.model_validate(t.__dict__) for t in towers]
    await cellular_scanner.record_cellular_detections(result)
    return CellularScanResponse(towers=result)
