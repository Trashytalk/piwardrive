"""Async wrapper around :class:`GPSDClient` using background threads."""
import asyncio
from gpsd_client import GPSDClient


class AsyncGPSDClient(GPSDClient):
    """Provide awaitable GPS queries using threads."""

    async def get_position_async(self):
        return await asyncio.to_thread(self.get_position)

    async def get_accuracy_async(self):
        return await asyncio.to_thread(self.get_accuracy)

    async def get_fix_quality_async(self):
        return await asyncio.to_thread(self.get_fix_quality)


async_client = AsyncGPSDClient()
