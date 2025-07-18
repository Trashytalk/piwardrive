"""Compute trends by comparing recent metrics to historical baselines."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List

from ..analysis import compute_health_stats
from ..cpu_pool import run_cpu_bound
from ..persistence import HealthRecord, _get_conn, flush_health_records


async def load_baseline_health(days: int, limit: int) -> List[HealthRecord]:
    """Return ``limit`` records older than ``days`` days."""
    await flush_health_records()
    conn = await _get_conn()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    cur = await conn.execute(
        """
        SELECT timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent
        FROM health_records WHERE timestamp < ? ORDER BY timestamp DESC LIMIT ?
        """,
        (cutoff, limit),
    )
    rows = await cur.fetchall()
    return [HealthRecord(**dict(row)) for row in rows]


def analyze_health_baseline(
    recent: Iterable[HealthRecord],
    baseline: Iterable[HealthRecord],
    threshold: float = 5.0,
) -> Dict[str, Any]:
    """Return averages and deltas between ``recent`` records and ``baseline``."""
    recent_stats = compute_health_stats(list(recent))
    base_stats = compute_health_stats(list(baseline))
    delta = {
        k: recent_stats.get(k, float("nan")) - base_stats.get(k, float("nan"))
        for k in recent_stats
    }
    anomalies = [k for k, d in delta.items() if abs(d) >= threshold]
    return {
        "recent": recent_stats,
        "baseline": base_stats,
        "delta": delta,
        "anomalies": anomalies,
    }


async def analyze_health_baseline_async(
    recent: Iterable[HealthRecord],
    baseline: Iterable[HealthRecord],
    threshold: float = 5.0,
) -> Dict[str, Any]:
    """Async wrapper for :func:`analyze_health_baseline`."""
    return await run_cpu_bound(
        analyze_health_baseline, list(recent), list(baseline), threshold
    )


__all__ = [
    "load_baseline_health",
    "analyze_health_baseline",
    "analyze_health_baseline_async",
]
