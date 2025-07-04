from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Iterable

import asyncpg

from .adapter import DatabaseAdapter


class PostgresAdapter(DatabaseAdapter):
    """PostgreSQL backend using asyncpg connection pooling."""

    def __init__(
        self, dsn: str, read_replicas: list[str] | None = None, pool_size: int = 10
    ) -> None:
        self.dsn = dsn
        self.read_replicas = read_replicas or []
        self.pool_size = pool_size
        self.pool: asyncpg.Pool | None = None
        self._rr_index = 0
        self.replica_pools: list[asyncpg.Pool] = []

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(
            self.dsn, min_size=1, max_size=self.pool_size
        )
        for replica in self.read_replicas:
            pool = await asyncpg.create_pool(
                replica, min_size=1, max_size=self.pool_size
            )
            self.replica_pools.append(pool)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            self.pool = None
        for pool in self.replica_pools:
            await pool.close()
        self.replica_pools.clear()

    async def _get_read_pool(self) -> asyncpg.Pool:
        if not self.replica_pools:
            assert self.pool
            return self.pool
        pool = self.replica_pools[self._rr_index]
        self._rr_index = (self._rr_index + 1) % len(self.replica_pools)
        return pool

    async def execute(self, query: str, *args: Any) -> None:
        assert self.pool
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        assert self.pool
        async with self.pool.acquire() as conn:
            await conn.executemany(query, list(args_iter))

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        pool = await self._get_read_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
        return [dict(row) for row in rows]

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        assert self.pool
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("SELECT pg_advisory_xact_lock(1)")
                try:
                    yield None
                finally:
                    # lock released automatically at transaction end
                    pass
