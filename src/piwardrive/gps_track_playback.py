"""GPS track playback utilities."""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, Iterable, Tuple


async def playback_track(
    points: Iterable[Tuple[float, float]],
    callback: Callable[[float, float], Awaitable[None]],
    interval: float = 1.0,
) -> None:
    """Replay ``points`` by invoking ``callback`` for each coordinate."""
    for lat, lon in points:
        await callback(lat, lon)
        await asyncio.sleep(interval)
