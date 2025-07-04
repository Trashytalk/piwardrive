"""Bluetooth scanning API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from piwardrive import service
from piwardrive.database_service import db_service
from piwardrive.models import (
    BluetoothDetection,
    BluetoothDevice,
    BluetoothScanRequest,
    BluetoothScanResponse,
    ErrorResponse,
)
from piwardrive.services import bluetooth_scanner

router = APIRouter(prefix="/bluetooth", tags=["bluetooth"])


@router.get(
    "/scan",
    response_model=BluetoothScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_bluetooth_get(
    timeout: int | None = None,
    _auth: None = Depends(service._check_auth),
) -> BluetoothScanResponse:
    """Perform a Bluetooth scan and return discovered devices."""
    devices = await bluetooth_scanner.scan_bluetooth_devices(timeout=timeout)
    result = [BluetoothDevice.model_validate(d.model_dump()) for d in devices]
    await bluetooth_scanner.record_bluetooth_detections(result)
    return BluetoothScanResponse(devices=result)


@router.post(
    "/scan",
    response_model=BluetoothScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_bluetooth_post(
    req: BluetoothScanRequest,
    _auth: None = Depends(service._check_auth),
) -> BluetoothScanResponse:
    """Perform a Bluetooth scan using parameters in the request body."""
    devices = await bluetooth_scanner.scan_bluetooth_devices(timeout=req.timeout)
    result = [BluetoothDevice.model_validate(d.model_dump()) for d in devices]
    await bluetooth_scanner.record_bluetooth_detections(result)
    return BluetoothScanResponse(devices=result)


@router.get(
    "/detections",
    response_model=list[BluetoothDetection],
    responses={401: {"model": ErrorResponse}},
)
async def list_bluetooth_detections(
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
    offset: int = 0,
    _auth: None = Depends(service._check_auth),
) -> list[BluetoothDetection]:
    """Return Bluetooth detection rows from the database."""
    query = (
        "SELECT id, scan_session_id, detection_timestamp, mac_address, "
        "device_name, rssi_dbm, latitude, longitude "
        "FROM bluetooth_detections"
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
    return [BluetoothDetection(**row) for row in rows]
