"""Runtime performance monitoring utilities."""

from __future__ import annotations

import logging
import os
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Mapping

import psutil

from piwardrive.api.common import (
    fetch_metrics_async,
    get_network_throughput,
)
from piwardrive.database_service import db_service
from piwardrive.services import db_monitor

logger = logging.getLogger(__name__)

# store raw metric samples
_METRICS: dict[str, List[float]] = defaultdict(list)


def record_metric(name: str, value: float) -> None:
    """Record a single metric sample."""
    _METRICS[name].append(value)
    logger.debug("metric %s=%.2", name, value)


def aggregate_metrics() -> Dict[str, Dict[str, float]]:
    """Return aggregated metrics for all recorded values."""
    summary: Dict[str, Dict[str, float]] = {}
    for key, values in _METRICS.items():
        count = len(values)
        if not count:
            continue
        summary[key] = {
            "count": count,
            "avg": sum(values) / count,
            "max": max(values),
            "min": min(values),
        }
    return summary


async def monitor_database_performance() -> Dict[str, Any]:
    """Collect database performance metrics."""
    metrics = {
        "pool": db_service.manager.get_metrics(),
        "queries": db_monitor.get_query_metrics(),
    }
    index_usage = await db_monitor.analyze_index_usage()
    metrics["index_usage"] = index_usage
    try:
        size_bytes = os.path.getsize(db_service.db_path())
    except OSError:
        size_bytes = None
    metrics["size_bytes"] = size_bytes
    if size_bytes is not None:
        record_metric("db_size_bytes", float(size_bytes))
    total_queries = sum(m["count"] for m in metrics["queries"].values())
    record_metric("db_query_total", float(total_queries))
    return metrics


def monitor_memory_usage() -> Dict[str, float | int]:
    """Collect memory usage metrics."""
    mem = psutil.virtual_memory()
    record_metric("mem_percent", float(mem.percent))
    return {
        "total": mem.total,
        "available": mem.available,
        "percent": mem.percent,
        "used": mem.used,
        "free": mem.free,
    }


def monitor_disk_usage(path: str = "/") -> Dict[str, float | int | None]:
    """Collect disk usage metrics for ``path`` and the database file."""
    usage = psutil.disk_usage(path)
    record_metric("disk_percent", float(usage.percent))
    try:
        db_size = os.path.getsize(db_service.db_path())
    except OSError:
        db_size = None
    if db_size is not None:
        record_metric("db_size_bytes", float(db_size))
    return {
        "path": path,
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent": usage.percent,
        "db_size_bytes": db_size,
    }


async def monitor_network_performance(iface: str | None = None) -> Dict[str, Any]:
    """Collect basic network performance metrics."""
    metrics_result = await fetch_metrics_async()
    rx_kbps, tx_kbps = get_network_throughput(iface)
    record_metric("rx_kbps", rx_kbps)
    record_metric("tx_kbps", tx_kbps)
    return {
        "ap_count": len(metrics_result.aps),
        "client_count": len(metrics_result.clients),
        "handshake_count": metrics_result.handshake_count,
        "rx_kbps": rx_kbps,
        "tx_kbps": tx_kbps,
    }


async def collect_performance_metrics() -> Dict[str, Any]:
    """Collect metrics from all monitors."""
    db = await monitor_database_performance()
    mem = monitor_memory_usage()
    disk = monitor_disk_usage()
    net = await monitor_network_performance()
    return {
        "database": db,
        "memory": mem,
        "disk": disk,
        "network": net,
        "aggregates": aggregate_metrics(),
    }


__all__ = [
    "record_metric",
    "aggregate_metrics",
    "monitor_database_performance",
    "monitor_memory_usage",
    "monitor_disk_usage",
    "monitor_network_performance",
    "collect_performance_metrics",
]
