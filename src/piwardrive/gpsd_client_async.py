"""Async wrapper around :class:`GPSDClient` using background threads."""
import asyncio
from gpsd_client import GPSDClient


class AsyncGPSDClient(GPSDClient):
    """Provide awaitable GPS queries using threads."""

    async def get_position_async(self) -> tuple[float, float] | None:
        """Return the device position or ``None`` if unavailable."""
        return await asyncio.to_thread(self.get_position)

    async def get_accuracy_async(self) -> float | None:
        """Return the current fix accuracy in meters."""
        return await asyncio.to_thread(self.get_accuracy)

    async def get_fix_quality_async(self) -> str:
        """Return the fix quality string from :class:`GPSDClient`."""
        return await asyncio.to_thread(self.get_fix_quality)


async_client = AsyncGPSDClient()
