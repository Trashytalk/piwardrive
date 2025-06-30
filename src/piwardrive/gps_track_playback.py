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
    if interval <= 0:
        raise ValueError(f"interval must be > 0, got {interval}")

    for lat, lon in points:
        await callback(lat, lon)
        await asyncio.sleep(interval)
