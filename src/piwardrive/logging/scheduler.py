import asyncio
import logging
from typing import Callable, List, TYPE_CHECKING

import schedule

from .storage import LogRetentionManager

if TYPE_CHECKING:
    from .rotation import SmartRotatingHandler


class RotationScheduler:
    """Schedules automatic log rotation and maintenance tasks."""

    def __init__(self) -> None:
        self.scheduled_tasks: List[Callable] = []
        self.running = False
        self.task_handle: asyncio.Task | None = None

    def schedule_rotation_check(self, handler: "SmartRotatingHandler") -> None:
        policy = handler.policy
        if policy.max_size:
            schedule.every(5).minutes.do(self._check_handler_rotation, handler)
        if policy.max_age:
            schedule.every().hour.do(self._check_handler_rotation, handler)
        schedule.every().day.at("02:00").do(self._daily_cleanup, handler)

    def schedule_retention_cleanup(self, retention_manager: LogRetentionManager) -> None:
        schedule.every().day.at("03:00").do(self._run_retention_cleanup, retention_manager)

    async def start(self) -> None:
        self.running = True
        self.task_handle = asyncio.create_task(self._run_scheduler())

    async def stop(self) -> None:
        self.running = False
        if self.task_handle:
            self.task_handle.cancel()

    async def _run_scheduler(self) -> None:
        while self.running:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)
            except Exception as exc:
                logging.error("Error in rotation scheduler: %s", exc)
                await asyncio.sleep(60)

    def _check_handler_rotation(self, handler: "SmartRotatingHandler") -> None:
        try:
            if handler.shouldRollover(None):
                handler.doRollover()
        except Exception as exc:
            logging.error("Error during rotation check: %s", exc)

    def _daily_cleanup(self, handler: "SmartRotatingHandler") -> None:
        try:
            handler._cleanup_old_files()
            handler._compress_old_files()
        except Exception as exc:
            logging.error("Error during daily cleanup: %s", exc)

    def _run_retention_cleanup(self, retention_manager: LogRetentionManager) -> None:
        try:
            asyncio.create_task(retention_manager.cleanup_expired_logs("application"))
            asyncio.create_task(retention_manager.cleanup_expired_logs("security"))
            asyncio.create_task(retention_manager.cleanup_expired_logs("performance"))
        except Exception as exc:
            logging.error("Error during retention cleanup: %s", exc)

