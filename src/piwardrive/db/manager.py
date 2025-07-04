from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict

from .adapter import DatabaseAdapter


class DatabaseManager:
    """Manage adapters with optional distributed locking."""

    def __init__(self, adapter: DatabaseAdapter) -> None:
        self.adapter = adapter
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        await self.adapter.connect()

    async def close(self) -> None:
        await self.adapter.close()

    @asynccontextmanager
    async def distributed_lock(self) -> AsyncIterator[None]:
        """Simple async lock for critical sections."""
        async with self._lock:
            async with self.adapter.transaction():
                yield None

    async def execute(self, query: str, *args) -> None:
        await self.adapter.execute(query, *args)

    async def executemany(self, query: str, args_iter) -> None:
        await self.adapter.executemany(query, args_iter)

    async def fetchall(self, query: str, *args) -> list[Dict]:
        return await self.adapter.fetchall(query, *args)
