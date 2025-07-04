from __future__ import annotations

from typing import Any, AsyncIterator, Iterable

import aiosqlite

from .adapter import DatabaseAdapter


class SQLiteAdapter(DatabaseAdapter):
    """SQLite backend using aiosqlite."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()
            self.conn = None

    async def execute(self, query: str, *args: Any) -> None:
        assert self.conn
        await self.conn.execute(query, args)
        await self.conn.commit()

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        assert self.conn
        await self.conn.executemany(query, args_iter)
        await self.conn.commit()

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        assert self.conn
        cur = await self.conn.execute(query, args)
        rows = await cur.fetchall()
        return [dict(row) for row in rows]

    async def transaction(self) -> AsyncIterator[None]:
        assert self.conn
        async with self.conn.execute("BEGIN"):
            try:
                yield None
            except Exception:
                await self.conn.rollback()
                raise
            else:
                await self.conn.commit()
