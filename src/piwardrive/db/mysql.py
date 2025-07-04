from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Iterable

import aiomysql

from .adapter import DatabaseAdapter


class MySQLAdapter(DatabaseAdapter):
    """MySQL backend using aiomysql connection pooling."""

    def __init__(
        self,
        dsn: str,
        *,
        min_size: int = 1,
        max_size: int = 10,
        connect_timeout: float = 10.0,
    ) -> None:
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.connect_timeout = connect_timeout
        self.pool: aiomysql.Pool | None = None
        self.metrics = {"acquired": 0, "released": 0, "failed": 0}

    async def connect(self) -> None:
        self.pool = await aiomysql.create_pool(
            self.dsn,
            minsize=self.min_size,
            maxsize=self.max_size,
            autocommit=True,
            connect_timeout=self.connect_timeout,
        )

    async def close(self) -> None:
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def _acquire(self) -> aiomysql.Connection:
        assert self.pool
        conn = await self.pool.acquire()
        try:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
        except Exception:
            self.metrics["failed"] += 1
            await conn.ensure_closed()
            conn = await self.pool.acquire()
        self.metrics["acquired"] += 1
        return conn

    async def _release(self, conn: aiomysql.Connection) -> None:
        assert self.pool
        self.pool.release(conn)
        self.metrics["released"] += 1

    async def execute(self, query: str, *args: Any) -> None:
        conn = await self._acquire()
        async with conn.cursor() as cur:
            await cur.execute(query, args)
        await self._release(conn)

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        conn = await self._acquire()
        async with conn.cursor() as cur:
            await cur.executemany(query, list(args_iter))
        await self._release(conn)

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        conn = await self._acquire()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, args)
            rows = list(await cur.fetchall())
        await self._release(conn)
        return rows

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        conn = await self._acquire()
        async with conn.cursor() as cur:
            await cur.execute("START TRANSACTION")
            try:
                yield None
            except Exception:
                await conn.rollback()
                raise
            else:
                await conn.commit()
        await self._release(conn)

    def get_metrics(self) -> dict[str, int]:
        return dict(self.metrics)
