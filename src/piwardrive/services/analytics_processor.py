from __future__ import annotations

"""Background analytics processing tasks."""

import logging
from datetime import datetime, timedelta
from typing import Any

import numpy as np

from piwardrive import network_analytics as heuristics
from piwardrive import persistence
from piwardrive.services import network_fingerprinting

logger = logging.getLogger(__name__)


async def process_hourly_analytics() -> None:
    """Calculate network statistics for the previous hour."""
    end = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(hours=1)
    async with persistence._get_conn() as conn:
        cur = await conn.execute(
            """
            SELECT bssid, ssid, channel, encryption_type,
                   signal_strength_dbm, latitude, longitude
            FROM wifi_detections
            WHERE detection_timestamp >= ? AND detection_timestamp < ?
            """,
            (start.isoformat(), end.isoformat()),
        )
        rows = await cur.fetchall()
    records = [dict(r) for r in rows]

    grouped: dict[str, list[dict[str, Any]]] = {}
    for rec in records:
        bssid = rec.get("bssid")
        if not bssid:
            continue
        grouped.setdefault(bssid, []).append(rec)

    out_rows: list[dict[str, Any]] = []
    for bssid, items in grouped.items():
        total = len(items)
        signals = [
            float(r["signal_strength_dbm"])
            for r in items
            if isinstance(r.get("signal_strength_dbm"), (int, float))
        ]
        avg_sig = float(np.mean(signals)) if signals else None
        max_sig = max(signals) if signals else None
        min_sig = min(signals) if signals else None
        var_sig = float(np.var(signals)) if signals else None
        encs = {r.get("encryption_type") for r in items if r.get("encryption_type")}
        ssids = {r.get("ssid") for r in items if r.get("ssid")}
        chans = {r.get("channel") for r in items if r.get("channel") is not None}
        susp = heuristics.find_suspicious_aps(items)
        out_rows.append(
            {
                "bssid": bssid,
                "analysis_date": start.isoformat(),
                "total_detections": total,
                "unique_locations": None,
                "avg_signal_strength": avg_sig,
                "max_signal_strength": max_sig,
                "min_signal_strength": min_sig,
                "signal_variance": var_sig,
                "coverage_radius_meters": None,
                "mobility_score": None,
                "encryption_changes": max(0, len(encs) - 1),
                "ssid_changes": max(0, len(ssids) - 1),
                "channel_changes": max(0, len(chans) - 1),
                "suspicious_score": min(1.0, len(susp) / total) if total else 0.0,
                "last_analyzed": datetime.utcnow().isoformat(),
            }
        )

    if out_rows:
        await persistence.save_network_analytics(out_rows)


async def detect_anomalies() -> None:
    """Identify unusual network patterns."""
    end = datetime.utcnow()
    start = end - timedelta(hours=1)
    async with persistence._get_conn() as conn:
        cur = await conn.execute(
            """
            SELECT scan_session_id, bssid, ssid, channel, encryption_type,
                   signal_strength_dbm AS signal_dbm, latitude, longitude
            FROM wifi_detections
            WHERE detection_timestamp >= ? AND detection_timestamp < ?
            """,
            (start.isoformat(), end.isoformat()),
        )
        rows = await cur.fetchall()
    records = [dict(r) for r in rows]
    anomalies = heuristics.detect_rogue_devices(records)
    if anomalies:
        await persistence.save_suspicious_activities(
            [
                {
                    "scan_session_id": a.get("scan_session_id", "adhoc"),
                    "activity_type": "rogue_ap",
                    "severity": "medium",
                    "target_bssid": a.get("bssid"),
                    "target_ssid": a.get("ssid"),
                    "evidence": "{}",
                    "description": "Possible rogue access point",
                    "detected_at": datetime.utcnow().isoformat(),
                    "latitude": a.get("latitude"),
                    "longitude": a.get("longitude"),
                    "false_positive": False,
                    "analyst_notes": None,
                }
                for a in anomalies
            ]
        )


async def update_fingerprints() -> None:
    """Update the device fingerprint database."""
    end = datetime.utcnow()
    start = end - timedelta(hours=1)
    async with persistence._get_conn() as conn:
        cur = await conn.execute(
            """
            SELECT * FROM wifi_detections
            WHERE detection_timestamp >= ? AND detection_timestamp < ?
            """,
            (start.isoformat(), end.isoformat()),
        )
        rows = await cur.fetchall()
    records = [dict(r) for r in rows]
    await network_fingerprinting.fingerprint_wifi_records(records)


async def cleanup_old_data(days: int = 30) -> None:
    """Remove old records based on the retention policy."""
    await persistence.purge_old_health(days)
    await persistence.vacuum()


__all__ = [
    "process_hourly_analytics",
    "detect_anomalies",
    "update_fingerprints",
    "cleanup_old_data",
]
