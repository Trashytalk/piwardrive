import gc
import logging
import tracemalloc
from collections import deque
from time import time
from typing import Deque, Tuple

import psutil


class MemoryMonitor:
    """Track memory usage and detect leaks using ``tracemalloc``."""

    def __init__(self, history: int = 5, threshold_mb: float = 10.0) -> None:
        self.history = history
        self.threshold_mb = threshold_mb
        self._snapshots: Deque[Tuple[float, tracemalloc.Snapshot, float]] = deque(
            maxlen=history
        )
        tracemalloc.start()

    def sample(self) -> float:
        """Record current RSS memory usage in MB and return it."""
        gc.collect()
        rss = psutil.Process().memory_info().rss / 1024**2
        snap = tracemalloc.take_snapshot()
        self._snapshots.append((time(), snap, rss))
        if len(self._snapshots) >= 2:
            self._check_leak()
        return rss

    def _check_leak(self) -> None:
        old_time, old_snap, _ = self._snapshots[0]
        new_time, new_snap, _ = self._snapshots[-1]
        diff = new_snap.compare_to(old_snap, "lineno")
        delta = sum(st.size_diff for st in diff) / 1024**2
        if delta > self.threshold_mb:
            logging.warning(
                "Possible memory leak: +%.2f MB over %.1f seconds",
                delta,
                new_time - old_time,
            )

    def stop(self) -> None:
        """Stop tracking allocations."""
        tracemalloc.stop()
