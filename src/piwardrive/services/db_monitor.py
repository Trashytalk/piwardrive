"""Database monitoring utilities.

This module provides database performance monitoring, query analysis, and
health check functionality for PiWardrive database operations.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Dict, List

from piwardrive import persistence

logger = logging.getLogger(__name__)

# store query durations grouped by SQL verb
_QUERY_METRICS: dict[str, List[float]] = defaultdict(list)


def record_query(sql: str, duration: float) -> None:
    """Record execution time for ``sql``."""
    key = (sql.split() or ["?"])[0].upper()
    _QUERY_METRICS[key].append(duration)
    logger.debug("query %s took %.4f sec", key, duration)


def get_query_metrics() -> Dict[str, Dict[str, float]]:
    """Return aggregated query metrics."""
    result: Dict[str, Dict[str, float]] = {}
    for key, values in _QUERY_METRICS.items():
        count = len(values)
        avg = sum(values) / count if count else 0.0
        result[key] = {"count": count, "avg": avg}
    return result

async def health_check() -> bool:
    """Return ``True`` if the database is reachable."""
    try:
        async with persistence._get_conn() as conn:
            await conn.execute("SELECT 1")
    except Exception:
        logger.exception("database health check failed")
        return False
    return True

async def analyze_index_usage() -> List[Dict[str, Any]]:
    """Return basic index size information using the ``dbstat`` virtual table."""
    async with persistence._get_conn() as conn:
        try:
            cur = await conn.execute(
                "SELECT name, SUM(pgsize) AS size FROM dbstat WHERE name IN (SELECT name FROM sqlite_master WHERE type='index') GROUP BY name ORDER BY size DESC"
            )
            rows = await cur.fetchall()
        except Exception as exc:  # pragma: no cover - dbstat may not exist
            logger.debug("index usage query failed: %s", exc)
            return []
    return [dict(row) for row in rows]

__all__ = ["record_query", "get_query_metrics", "health_check", "analyze_index_usage"]
