"""Advanced export helpers for various formats."""

from __future__ import annotations

import csv
import json
from typing import Any

from piwardrive import export, persistence


async def _fetch(query: str) -> list[dict[str, Any]]:
    async with persistence._get_conn() as conn:
        cur = await conn.execute(query)
        rows = await cur.fetchall()
    return [dict(r) for r in rows]


async def export_to_csv(table: str, path: str) -> None:
    """Export all rows from ``table`` to ``path`` in CSV format."""
    rows = await _fetch(f"SELECT * FROM {table}")
    export.export_csv(rows, path, list(rows[0].keys()) if rows else None)


async def export_to_json(
    table: str, path: str, *, group_by: str = "scan_session_id"
) -> None:
    """Export rows from ``table`` grouped by ``group_by`` to JSON."""
    rows = await _fetch(f"SELECT * FROM {table}")
    grouped: dict[str, list[dict[str, Any]]] = {}
    for rec in rows:
        key = str(rec.get(group_by, "default"))
        grouped.setdefault(key, []).append(rec)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(grouped, fh)


async def export_to_kml(path: str) -> None:
    """Export GPS tracks and detection points to ``path`` as KML."""
    track_rows = await _fetch(
        "SELECT latitude AS lat, longitude AS lon " "FROM gps_tracks ORDER BY timestamp"
    )
    aps = await _fetch(
        "SELECT latitude AS lat, longitude AS lon, ssid, bssid, ",
        "signal_strength_dbm as rssi FROM wifi_detections"
    )
    bts = await _fetch(
        "SELECT latitude AS lat, longitude AS lon, device_name as name, ",
        "mac_address as address, rssi_dbm as rssi FROM bluetooth_detections"
    )
    track = [
        (r["lat"], r["lon"])
        for r in track_rows
        if r.get("lat") is not None and r.get("lon") is not None
    ]
    export.export_map_kml(track, aps, bts, path)


async def export_to_wigle(path: str) -> None:
    """Export Wi-Fi detections to a WiGLE compatible CSV file."""
    rows = await _fetch(
        "SELECT bssid, ssid, frequency_mhz, channel, first_seen, last_seen, ",
        "latitude, longitude FROM wifi_detections"
    )
    fieldnames = [
        "netid",
        "ssid",
        "frequency_mhz",
        "channel",
        "last_seen",
        "first_seen",
        "lat",
        "lon",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(
                {
                    "netid": r.get("bssid"),
                    "ssid": r.get("ssid"),
                    "frequency_mhz": r.get("frequency_mhz"),
                    "channel": r.get("channel"),
                    "last_seen": r.get("last_seen"),
                    "first_seen": r.get("first_seen"),
                    "lat": r.get("latitude"),
                    "lon": r.get("longitude"),
                }
            )


__all__ = [
    "export_to_csv",
    "export_to_json",
    "export_to_kml",
    "export_to_wigle",
]
