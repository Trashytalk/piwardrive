"""Cellular scanning API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from piwardrive import service
from piwardrive.database_service import db_service
from piwardrive.models import (
    CellTower,
    CellularDetection,
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


@router.get(
    "/detections",
    response_model=list[CellularDetection],
    responses={401: {"model": ErrorResponse}},
)
async def list_cellular_detections(
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
    offset: int = 0,
    _auth: None = Depends(service._check_auth),
) -> list[CellularDetection]:
    """Return cellular detection rows from the database."""
    query = (
        "SELECT id, scan_session_id, detection_timestamp, cell_id, lac, mcc, ",
        "mnc, signal_strength_dbm, latitude, longitude FROM cellular_detections",
    )
    params: list[object] = []
    clauses: list[str] = []
    if start:
        clauses.append("detection_timestamp >= ?")
        params.append(start)
    if end:
        clauses.append("detection_timestamp <= ?")
        params.append(end)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY detection_timestamp DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    rows = await db_service.fetch(query, *params)
    return [CellularDetection(**row) for row in rows]
