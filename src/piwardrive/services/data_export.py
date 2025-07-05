from __future__ import annotations

"""Helpers for exporting database tables to various formats."""

from importlib import resources
from typing import Sequence

from piwardrive import export, persistence


async def _fetch_all(query: str) -> list[dict[str, object]]:
    async with persistence._get_conn() as conn:
        cur = await conn.execute(query)
        rows = await cur.fetchall()
    return [dict(r) for r in rows]


async def export_wifi_detections(path: str, fmt: str = "csv") -> None:
    rows = await _fetch_all("SELECT * FROM wifi_detections")
    export.export_records(rows, path, fmt)


async def export_bluetooth_detections(path: str, fmt: str = "csv") -> None:
    rows = await _fetch_all("SELECT * FROM bluetooth_detections")
    export.export_records(rows, path, fmt)


async def export_cellular_detections(path: str, fmt: str = "csv") -> None:
    rows = await _fetch_all("SELECT * FROM cellular_detections")
    export.export_records(rows, path, fmt)


async def export_gps_tracks(path: str, fmt: str = "kml") -> None:
    rows = await _fetch_all(
        "SELECT latitude AS lat, longitude AS lon, timestamp FROM gps_tracks"
    )
    export.export_records(rows, path, fmt)


__all__ = [
    "export_wifi_detections",
    "export_bluetooth_detections",
    "export_cellular_detections",
    "export_gps_tracks",
]
