from __future__ import annotations

import time
from typing import Callable, Dict, List

from .bluetooth import scan_bluetooth
from .wifi import scan_wifi

Result = Dict[str, List]


def scan_once() -> Result:
    """Return Wi-Fi and Bluetooth scan results."""
    wifi = scan_wifi()
    bt = scan_bluetooth()
    return {"wifi": wifi, "bluetooth": bt}


def run_continuous_scan(
    interval: float = 60.0,
    iterations: int = 0,
    on_result: Callable[[Result], None] | None = None,
) -> None:
    """Run :func:`scan_once` repeatedly."""
    count = 0
    while True:
        result = scan_once()
        if on_result:
            on_result(result)
        count += 1
        if iterations and count >= iterations:
            break
        time.sleep(interval)
