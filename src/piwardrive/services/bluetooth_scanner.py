"""Bluetooth device scanning service."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, List

from piwardrive import persistence, utils
from piwardrive.services.stream_processor import stream_processor
from piwardrive.sigint_suite.bluetooth.scanner import async_scan_bluetooth
from piwardrive.sigint_suite.models import BluetoothDevice


async def scan_bluetooth_devices(timeout: int | None = None) -> List[BluetoothDevice]:
    """Return nearby Bluetooth devices using the Sigint Suite scanner."""
    return await async_scan_bluetooth(timeout=timeout)


async def record_bluetooth_detections(devices: Iterable[BluetoothDevice]) -> None:
    """Persist ``devices`` to the ``bluetooth_detections`` table."""
    timestamp = datetime.utcnow().isoformat()
    pos = utils.gps_client.get_position()
    acc = utils.get_gps_accuracy()
    fix = utils.get_gps_fix_quality()
    lat = lon = None
    if pos:
        lat, lon = pos
        await persistence.save_gps_tracks(
            [
                {
                    "scan_session_id": "adhoc",
                    "timestamp": timestamp,
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "altitude_meters": None,
                    "accuracy_meters": acc,
                    "heading_degrees": None,
                    "speed_kmh": None,
                    "satellite_count": None,
                    "hdop": None,
                    "vdop": None,
                    "pdop": None,
                    "fix_type": fix,
                }
            ]
        )
    records = [
        {
            "scan_session_id": "adhoc",
            "detection_timestamp": timestamp,
            "mac_address": dev.address,
            "device_name": dev.name,
            "device_class": None,
            "device_type": None,
            "manufacturer_id": None,
            "manufacturer_name": None,
            "rssi_dbm": None,
            "tx_power_dbm": None,
            "bluetooth_version": None,
            "supported_services": None,
            "is_connectable": False,
            "is_paired": False,
            "latitude": getattr(dev, "lat", lat),
            "longitude": getattr(dev, "lon", lon),
            "altitude_meters": None,
            "accuracy_meters": None,
            "heading_degrees": None,
            "speed_kmh": None,
            "first_seen": timestamp,
            "last_seen": timestamp,
            "detection_count": 1,
        }
        for dev in devices
    ]
    await persistence.save_bluetooth_detections(records)
    stream_processor.publish_bluetooth(records)


async def scan_and_save(timeout: int | None = None) -> List[BluetoothDevice]:
    """Scan for Bluetooth devices and store detection records."""
    devices = await scan_bluetooth_devices(timeout=timeout)
    await record_bluetooth_detections(devices)
    return devices
