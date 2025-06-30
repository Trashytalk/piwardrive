"""Webhook notification helpers."""

from __future__ import annotations

import logging
from typing import Iterable, List

import httpx

from .core import config
from .scheduler import PollScheduler
from .utils import get_cpu_temp, get_disk_usage, run_async_task

logger = logging.getLogger(__name__)

WEBHOOK_TIMEOUT = 5


class NotificationManager:
    """Send webhook notifications when thresholds are exceeded."""

    def __init__(
        self,
        scheduler: PollScheduler,
        *,
        interval: int = 60,
        webhooks: Iterable[str] | None = None,
        cpu_temp_threshold: float | None = None,
        disk_percent_threshold: float | None = None,
    ) -> None:
        self._scheduler = scheduler
        self.webhooks: List[str] = list(webhooks or [])
        cfg = config.AppConfig.load()
        self.cpu_temp_threshold = (
            cpu_temp_threshold
            if cpu_temp_threshold is not None
            else cfg.notify_cpu_temp
        )
        self.disk_percent_threshold = (
            disk_percent_threshold
            if disk_percent_threshold is not None
            else cfg.notify_disk_percent
        )
        self._event = "notification_check"
        self._cpu_alert = False
        self._disk_alert = False
        scheduler.schedule(
            self._event, lambda _dt: run_async_task(self._check()), interval
        )

    async def _post(self, payload: dict) -> None:
        if not self.webhooks:
            return
        async with httpx.AsyncClient() as client:
            for url in self.webhooks:
                try:
                    await client.post(url, json=payload, timeout=WEBHOOK_TIMEOUT)
                except Exception as exc:  # pragma: no cover - network errors
                    logger.warning("notification to %s failed: %s", url, exc)

    async def _check(self) -> None:
        cpu = get_cpu_temp()
        disk = get_disk_usage("/")
        if cpu is not None and self.cpu_temp_threshold > 0:
            if cpu >= self.cpu_temp_threshold and not self._cpu_alert:
                await self._post({"event": "cpu_temp", "value": cpu})
                self._cpu_alert = True
            elif cpu < self.cpu_temp_threshold - 5:
                self._cpu_alert = False
        if disk is not None and self.disk_percent_threshold > 0:
            if disk >= self.disk_percent_threshold and not self._disk_alert:
                await self._post({"event": "disk_percent", "value": disk})
                self._disk_alert = True
            elif disk < self.disk_percent_threshold - 5:
                self._disk_alert = False

    def update_webhooks(self, urls: Iterable[str]) -> None:
        """Replace the configured webhook URL list."""
        self.webhooks = list(urls)
