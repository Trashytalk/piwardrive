from __future__ import annotations

"""Background job scheduler for analytics tasks."""

import logging
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from piwardrive.scheduler import AsyncScheduler
from piwardrive.services.analytics_processor import (
    cleanup_old_data,
    detect_anomalies,
    process_hourly_analytics,
    update_fingerprints,
)
from piwardrive.task_queue import BackgroundTaskQueue

logger = logging.getLogger(__name__)


class AnalyticsJobManager:
    """Schedule analytics jobs and track their status."""

    def __init__(self, scheduler: AsyncScheduler, queue: BackgroundTaskQueue) -> None:
        self._scheduler = scheduler
        self._queue = queue
        self._status: Dict[str, Dict[str, Any]] = {}

        self._scheduler.schedule(
            "hourly_analytics",
            lambda: self.enqueue("hourly_analytics", process_hourly_analytics),
            3600,
        )
        self._scheduler.schedule(
            "detect_anomalies",
            lambda: self.enqueue("detect_anomalies", detect_anomalies),
            1800,
        )
        self._scheduler.schedule(
            "update_fingerprints",
            lambda: self.enqueue("update_fingerprints", update_fingerprints),
            3600,
        )
        self._scheduler.schedule(
            "cleanup_old_data",
            lambda: self.enqueue("cleanup_old_data", cleanup_old_data),
            86400,
        )

    # ------------------------------------------------------------------
    def enqueue(self, name: str, func: Callable[[], Awaitable[None]]) -> None:
        async def _run() -> None:
            self._status[name] = {
                "status": "running",
                "started": datetime.utcnow().isoformat(),
            }
            try:
                await func()
            except Exception as exc:  # pragma: no cover - background errors
                logger.exception("Job %s failed: %s", name, exc)
                self._status[name] = {
                    "status": "error",
                    "error": str(exc),
                    "finished": datetime.utcnow().isoformat(),
                }
            else:
                self._status[name] = {
                    "status": "completed",
                    "finished": datetime.utcnow().isoformat(),
                }

        self._queue.enqueue(_run)

    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """Return status for all scheduled jobs."""
        return self._status


job_manager: AnalyticsJobManager | None = None


def init_jobs(scheduler: AsyncScheduler, queue: BackgroundTaskQueue) -> None:
    """Initialize background analytics jobs."""
    global job_manager
    job_manager = AnalyticsJobManager(scheduler, queue)
