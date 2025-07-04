from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Iterable

import aiomysql

from .adapter import DatabaseAdapter


class MySQLAdapter(DatabaseAdapter):
    """MySQL backend using aiomysql connection pooling."""

    def __init__(self, dsn: str, pool_size: int = 10) -> None:
        self.dsn = dsn
        self.pool_size = pool_size
        self.pool: aiomysql.Pool | None = None

    async def connect(self) -> None:
        self.pool = await aiomysql.create_pool(
            self.dsn, minsize=1, maxsize=self.pool_size, autocommit=True
        )

    async def close(self) -> None:
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def execute(self, query: str, *args: Any) -> None:
        assert self.pool
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, args)

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        assert self.pool
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, list(args_iter))

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        assert self.pool
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return list(await cur.fetchall())

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        assert self.pool
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("START TRANSACTION")
                try:
                    yield None
                except Exception:
                    await conn.rollback()
                    raise
                else:
                    await conn.commit()
