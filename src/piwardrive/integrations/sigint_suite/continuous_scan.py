"""Continuous scanning orchestration for SIGINT suite integration."""

from __future__ import annotations

import asyncio
from typing import Any, Callable, Dict, List

from piwardrive.task_queue import BackgroundTaskQueue

from .bluetooth import scan_bluetooth
from .bluetooth.scanner import async_scan_bluetooth
from .wifi import scan_wifi
from .wifi.scanner import async_scan_wifi

Result = Dict[str, List[Any]]


def scan_once() -> Result:
    """Return Wi-Fi and Bluetooth scan results."""
    wifi = scan_wifi()
    bt = scan_bluetooth()
    return {"wifi": wifi, "bluetooth": bt}


async def run_continuous_scan(
    interval: float = 60.0,
    iterations: int = 0,
    on_result: Callable[[Result], None] | None = None,
    *,
    queue: "BackgroundTaskQueue | None" = None,
) -> None:
    """Run Wi-Fi and Bluetooth scans repeatedly.

    When ``queue`` is provided each scan iteration is enqueued for background
    processing so the loop itself is non-blocking.
    """
    count = 0

    async def _scan_once() -> None:
        wifi, bt = await asyncio.gather(
            async_scan_wifi(),
            async_scan_bluetooth(),
        )
        _result = {"wifi": wifi, "bluetooth": bt}
        if on_result:
            on_result(_result)

    while True:
        if queue is not None:
            queue.enqueue(_scan_once)
        else:
            await _scan_once()
        count += 1
        if iterations and count >= iterations:
            break
        await asyncio.sleep(interval)
