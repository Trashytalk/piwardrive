from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Callable

from ..resource_manager import ResourceManager

from .adapter import DatabaseAdapter


class DatabaseManager:
    """Manage one or more adapters with optional distributed locking."""

    def __init__(
        self,
        adapter: DatabaseAdapter | dict[str, DatabaseAdapter],
        *,
        shard_func: Callable[[str], str] | None = None,
        resource_manager: ResourceManager | None = None,
    ) -> None:
        if isinstance(adapter, dict):
            self.adapters = adapter
        else:
            self.adapters = {"default": adapter}
        self._shard_func = shard_func or (lambda key: "default")
        self._lock = asyncio.Lock()
        self._rm = resource_manager
        if self._rm is not None:
            self._rm.register(self, lambda: asyncio.run(self.close()))

    async def connect(self) -> None:
        for adapter in self.adapters.values():
            await adapter.connect()

    async def close(self) -> None:
        for adapter in self.adapters.values():
            await adapter.close()

    @asynccontextmanager
    async def distributed_lock(self, key: str | None = None) -> AsyncIterator[None]:
        """Simple async lock for critical sections."""
        async with self._lock:
            async with self._get_adapter(key).transaction():
                yield None

    def _get_adapter(self, key: str | None = None) -> DatabaseAdapter:
        if len(self.adapters) == 1:
            return next(iter(self.adapters.values()))
        if key is None:
            raise ValueError("key required for sharded manager")
        shard = self._shard_func(key)
        return self.adapters[shard]

    async def execute(self, query: str, *args, key: str | None = None) -> None:
        await self._get_adapter(key).execute(query, *args)

    async def executemany(self, query: str, args_iter, key: str | None = None) -> None:
        await self._get_adapter(key).executemany(query, args_iter)

    async def fetchall(self, query: str, *args, key: str | None = None) -> list[Dict]:
        return await self._get_adapter(key).fetchall(query, *args)

    def get_metrics(self) -> dict[str, Dict[str, int]]:
        return {name: adapter.get_metrics() for name, adapter in self.adapters.items()}
