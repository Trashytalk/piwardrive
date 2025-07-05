from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator, Iterable

import aiosqlite

from .adapter import DatabaseAdapter


class SQLiteAdapter(DatabaseAdapter):
    """SQLite backend using aiosqlite with connection pooling."""

    def __init__(
        self,
        path: str,
        *,
        pool_size: int = 5,
        read_replicas: list[str] | None = None,
    ) -> None:
        self.path = path
        self.pool_size = pool_size
        self.read_replicas = read_replicas or []
        self.pool: asyncio.Queue[aiosqlite.Connection] | None = None
        self.replica_pools: list[asyncio.Queue[aiosqlite.Connection]] = []
        self._rr_index = 0
        self.metrics = {"acquired": 0, "released": 0}

    async def _create_conn(
        self, path: str, *, readonly: bool = False
    ) -> aiosqlite.Connection:
        if readonly:
            conn = await aiosqlite.connect(f"file:{path}?mode=ro", uri=True)
        else:
            conn = await aiosqlite.connect(path)
        pragmas = {
            "journal_mode": "WAL",
            "synchronous": "NORMAL",
            "temp_store": "MEMORY",
            "cache_size": 10000,
        }
        for k, v in pragmas.items():
            await conn.execute(f"PRAGMA {k}={v}")
        conn.row_factory = aiosqlite.Row
        return conn

    async def connect(self) -> None:
        self.pool = asyncio.Queue(maxsize=self.pool_size)
        for _ in range(self.pool_size):
            conn = await self._create_conn(self.path)
            await self.pool.put(conn)
        for replica in self.read_replicas:
            rp = asyncio.Queue(maxsize=self.pool_size)
            for _ in range(self.pool_size):
                conn = await self._create_conn(replica, readonly=True)
                await rp.put(conn)
            self.replica_pools.append(rp)

    async def _close_pool(self, pool: asyncio.Queue[aiosqlite.Connection]) -> None:
        while not pool.empty():
            conn = await pool.get()
            await conn.close()

    async def close(self) -> None:
        if self.pool:
            await self._close_pool(self.pool)
            self.pool = None
        for rp in self.replica_pools:
            await self._close_pool(rp)
        self.replica_pools.clear()

    async def _acquire(
        self, *, read: bool = False
    ) -> tuple[aiosqlite.Connection, asyncio.Queue[aiosqlite.Connection]]:
        if read and self.replica_pools:
            pool = self.replica_pools[self._rr_index]
            self._rr_index = (self._rr_index + 1) % len(self.replica_pools)
        else:
            assert self.pool
            pool = self.pool
        conn = await pool.get()
        try:
            await conn.execute("SELECT 1")
        except Exception:
            path = self.path if not read else self.read_replicas[self._rr_index - 1]
            conn = await self._create_conn(path, readonly=read)
        self.metrics["acquired"] += 1
        return conn, pool

    async def _release(
        self, pool: asyncio.Queue[aiosqlite.Connection], conn: aiosqlite.Connection
    ) -> None:
        await pool.put(conn)
        self.metrics["released"] += 1

    async def execute(self, query: str, *args: Any) -> None:
        conn, pool = await self._acquire()
        await conn.execute(query, args)
        await conn.commit()
        await self._release(pool, conn)

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        conn, pool = await self._acquire()
        await conn.executemany(query, list(args_iter))
        await conn.commit()
        await self._release(pool, conn)

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        conn, pool = await self._acquire(read=True)
        cur = await conn.execute(query, args)
        rows = await cur.fetchall()
        await self._release(pool, conn)
        return [dict(row) for row in rows]

    async def transaction(self) -> AsyncIterator[None]:
        conn, pool = await self._acquire()
        async with conn.execute("BEGIN"):
            try:
                yield None
            except Exception:
                await conn.rollback()
                raise
            else:
                await conn.commit()
        await self._release(pool, conn)

    def get_metrics(self) -> dict[str, int]:
        return dict(self.metrics)
