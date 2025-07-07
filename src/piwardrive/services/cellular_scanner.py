"""Cellular tower scanning service."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, List

from piwardrive import persistence, utils
from piwardrive.services.stream_processor import stream_processor
from piwardrive.sigint_suite.cellular.tower_scanner import async_scan_towers


async def scan_cell_towers(timeout: int | None = None) -> List[object]:
    """Return nearby cell towers using the Sigint Suite scanner."""
    return await async_scan_towers(timeout=timeout)


async def record_cellular_detections(towers: Iterable[object]) -> None:
    """Persist ``towers`` to the ``cellular_detections`` table."""
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
            "cell_id": getattr(t, "tower_id", None),
            "lac": None,
            "mcc": None,
            "mnc": None,
            "network_name": None,
            "technology": None,
            "frequency_mhz": None,
            "band": None,
            "channel": None,
            "signal_strength_dbm": getattr(t, "rssi", None),
            "signal_quality": None,
            "timing_advance": None,
            "latitude": getattr(t, "lat", lat),
            "longitude": getattr(t, "lon", lon),
            "altitude_meters": None,
            "accuracy_meters": None,
            "heading_degrees": None,
            "speed_kmh": None,
            "first_seen": timestamp,
            "last_seen": timestamp,
            "detection_count": 1,
        }
        for t in towers
    ]
    await persistence.save_cellular_detections(records)
    stream_processor.publish_cellular(records)


async def scan_and_save(timeout: int | None = None) -> List[object]:
    """Scan for cell towers and store detection records."""
    towers = await scan_cell_towers(timeout=timeout)
    await record_cellular_detections(towers)
    return towers
