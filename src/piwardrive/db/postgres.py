from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Iterable

import asyncpg

from .adapter import DatabaseAdapter


class PostgresAdapter(DatabaseAdapter):
    """PostgreSQL backend using asyncpg connection pooling."""

    def __init__(
        self,
        dsn: str,
        read_replicas: list[str] | None = None,
        *,
        min_size: int = 1,
        max_size: int = 10,
        timeout: float = 60.0,
    ) -> None:
        self.dsn = dsn
        self.read_replicas = read_replicas or []
        self.min_size = min_size
        self.max_size = max_size
        self.timeout = timeout
        self.pool: asyncpg.Pool | None = None
        self._rr_index = 0
        self.replica_pools: list[asyncpg.Pool] = []
        self.metrics = {"acquired": 0, "released": 0, "failed": 0}

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            timeout=self.timeout,
        )
        for replica in self.read_replicas:
            pool = await asyncpg.create_pool(
                replica,
                min_size=self.min_size,
                max_size=self.max_size,
                timeout=self.timeout,
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

    async def _acquire(
        self, *, read: bool = False
    ) -> tuple[asyncpg.Connection, asyncpg.Pool]:
        pool = await self._get_read_pool() if read else self.pool
        assert pool
        conn = await pool.acquire()
        try:
            await conn.execute("SELECT 1")
        except Exception:
            self.metrics["failed"] += 1
            await conn.close()
            conn = await pool.acquire()
        self.metrics["acquired"] += 1
        return conn, pool

    async def _release(self, pool: asyncpg.Pool, conn: asyncpg.Connection) -> None:
        await pool.release(conn)
        self.metrics["released"] += 1

    async def execute(self, query: str, *args: Any) -> None:
        conn, pool = await self._acquire()
        await conn.execute(query, *args)
        await self._release(pool, conn)

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        conn, pool = await self._acquire()
        await conn.executemany(query, list(args_iter))
        await self._release(pool, conn)

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        conn, pool = await self._acquire(read=True)
        rows = await conn.fetch(query, *args)
        await self._release(pool, conn)
        return [dict(row) for row in rows]

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        conn, pool = await self._acquire()
        async with conn.transaction(isolation="repeatable_read"):
            await conn.execute("SELECT pg_advisory_xact_lock(1)")
            try:
                yield None
            except asyncpg.DeadlockDetectedError:
                await conn.execute("ROLLBACK")
                self.metrics["failed"] += 1
                raise
        await self._release(pool, conn)

    def get_metrics(self) -> dict[str, int]:
        return dict(self.metrics)
