from __future__ import annotations

"""Background scheduler for maintenance tasks."""

import inspect
import logging
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from piwardrive.scheduler import AsyncScheduler
from piwardrive.services import maintenance
from piwardrive.task_queue import BackgroundTaskQueue

logger = logging.getLogger(__name__)


class MaintenanceJobManager:
    """Schedule database maintenance tasks and track their status."""

    def __init__(self, scheduler: AsyncScheduler, queue: BackgroundTaskQueue) -> None:
        self._scheduler = scheduler
        self._queue = queue
        self._status: Dict[str, Dict[str, Any]] = {}

        self._scheduler.schedule(
            "vacuum_database",
            lambda: self.enqueue("vacuum_database", maintenance.vacuum_database),
            86400,
        )
        self._scheduler.schedule(
            "optimize_indexes",
            lambda: self.enqueue(
                "optimize_indexes", maintenance.optimize_database_indexes
            ),
            604800,
        )
        self._scheduler.schedule(
            "archive_old_data",
            lambda: self.enqueue("archive_old_data", maintenance.archive_old_data),
            604800,
        )
        self._scheduler.schedule(
            "health_reports",
            lambda: self.enqueue("health_reports", maintenance.generate_health_reports),
            86400,
        )
        self._scheduler.schedule(
            "backup_database",
            lambda: self.enqueue("backup_database", maintenance.automatic_backup),
            86400,
        )
        self._scheduler.schedule(
            "db_health_check",
            lambda: self.enqueue("db_health_check", maintenance.check_database_health),
            300,
        )

    # ------------------------------------------------------------------
    def enqueue(self, name: str, func: Callable[[], Awaitable[Any]]) -> None:
        async def _run() -> None:
            self._status[name] = {
                "status": "running",
                "started": datetime.utcnow().isoformat(),
            }
            try:
                _result = func()
                if inspect.isawaitable(result):
                    await result
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


job_manager: MaintenanceJobManager | None = None


def init_jobs(scheduler: AsyncScheduler, queue: BackgroundTaskQueue) -> None:
    """Initialize background maintenance jobs."""
    global job_manager
    job_manager = MaintenanceJobManager(scheduler, queue)
