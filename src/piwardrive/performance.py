"""Performance monitoring and metrics collection utilities.

This module provides tools for measuring and tracking execution times
of operations throughout the PiWardrive application. It includes
context managers for recording timing data and functions for
retrieving performance statistics.
"""

from __future__ import annotations

import time
from collections import defaultdict
from contextlib import contextmanager
from typing import Dict, List

_METRICS: Dict[str, List[float]] = defaultdict(list)


@contextmanager
def record(name: str) -> None:
    """Context manager recording execution time under ``name``."""
    start = time.perf_counter()
    try:
        yield
    finally:
        _METRICS[name].append(time.perf_counter() - start)


def get_metrics() -> Dict[str, Dict[str, float]]:
    """Return average duration metrics."""
    result: Dict[str, Dict[str, float]] = {}
    for key, values in _METRICS.items():
        count = len(values)
        avg = sum(values) / count if count else 0.0
        result[key] = {"count": count, "avg": avg}
    return result


def clear() -> None:
    """Clear all recorded performance metrics."""
    _METRICS.clear()


__all__ = ["record", "get_metrics", "clear"]
