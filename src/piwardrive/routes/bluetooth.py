"""Bluetooth scanning API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from piwardrive import service
from piwardrive.models import (
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
