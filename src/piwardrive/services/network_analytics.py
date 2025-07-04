from __future__ import annotations

import math
from datetime import datetime, timedelta, date
from typing import Any, List

import numpy as np

from piwardrive import persistence, network_analytics as heuristics
from piwardrive.scheduler import PollScheduler
from piwardrive.utils import run_async_task


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


async def analyze_day(day: date) -> None:
    """Compute analytics for ``day`` and store results."""
    start = datetime.combine(day, datetime.min.time()).isoformat()
    end = (datetime.combine(day, datetime.min.time()) + timedelta(days=1)).isoformat()
    async with persistence._get_conn() as conn:
        cur = await conn.execute(
            """
            SELECT bssid, ssid, channel, encryption_type, signal_strength_dbm,
                   latitude, longitude
            FROM wifi_detections
            WHERE detection_timestamp >= ? AND detection_timestamp < ?
            """,
            (start, end),
        )
        rows = await cur.fetchall()
    records = [dict(r) for r in rows]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for rec in records:
        bssid = rec.get("bssid")
        if not bssid:
            continue
        grouped.setdefault(bssid, []).append(rec)

    out_rows: List[dict[str, Any]] = []
    for bssid, items in grouped.items():
        total = len(items)
        locs = [
            (float(r["latitude"]), float(r["longitude"]))
            for r in items
            if r.get("latitude") is not None and r.get("longitude") is not None
        ]
        unique_locs = {
            (round(lat, 5), round(lon, 5)) for lat, lon in locs
        }
        signals = [
            float(r["signal_strength_dbm"])
            for r in items
            if isinstance(r.get("signal_strength_dbm"), (int, float))
        ]
        avg_sig = float(np.mean(signals)) if signals else None
        max_sig = max(signals) if signals else None
        min_sig = min(signals) if signals else None
        var_sig = float(np.var(signals)) if signals else None
        radius = None
        if unique_locs:
            lat_c = sum(p[0] for p in unique_locs) / len(unique_locs)
            lon_c = sum(p[1] for p in unique_locs) / len(unique_locs)
            radius = max(_haversine(lat_c, lon_c, lat, lon) for lat, lon in unique_locs)
        mobility = min(1.0, len(unique_locs) / total) if total else None
        encs = {r.get("encryption_type") for r in items if r.get("encryption_type")}
        ssids = {r.get("ssid") for r in items if r.get("ssid")}
        chans = {r.get("channel") for r in items if r.get("channel") is not None}
        susp = heuristics.find_suspicious_aps(items)
        out_rows.append(
            {
                "bssid": bssid,
                "analysis_date": day.isoformat(),
                "total_detections": total,
                "unique_locations": len(unique_locs),
                "avg_signal_strength": avg_sig,
                "max_signal_strength": max_sig,
                "min_signal_strength": min_sig,
                "signal_variance": var_sig,
                "coverage_radius_meters": radius,
                "mobility_score": mobility,
                "encryption_changes": max(0, len(encs) - 1),
                "ssid_changes": max(0, len(ssids) - 1),
                "channel_changes": max(0, len(chans) - 1),
                "suspicious_score": min(1.0, len(susp) / total) if total else 0.0,
                "last_analyzed": datetime.utcnow().isoformat(),
            }
        )

    await persistence.save_network_analytics(out_rows)


class NetworkAnalyticsService:
    """Schedule daily network analytics processing."""

    def __init__(self, scheduler: PollScheduler, hour: int = 2) -> None:
        self._scheduler = scheduler
        self._event = "network_analytics"
        scheduler.schedule(
            self._event, lambda _dt: run_async_task(self.run()), 86400
        )
        # optional immediate run for testing
        run_async_task(self.run())

    async def run(self) -> None:
        day = datetime.utcnow().date() - timedelta(days=1)
        await analyze_day(day)


__all__ = ["NetworkAnalyticsService", "analyze_day"]
