"""Migrate data from a SQLite database to PostgreSQL."""

from __future__ import annotations

import asyncio
from typing import Iterable

import aiosqlite
import asyncpg


async def copy_table(
    src: aiosqlite.Connection, dst: asyncpg.Connection, table: str
) -> None:
    cur = await src.execute(f"SELECT * FROM {table}")
    columns = [d[0] for d in cur.description]
    rows = await cur.fetchall()
    if not rows:
        return
    placeholders = ", ".join(f"${i}" for i in range(1, len(columns) + 1))
    cols = ", ".join(columns)
    query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    await dst.executemany(query, [tuple(row) for row in rows])


async def migrate(sqlite_path: str, pg_dsn: str, tables: Iterable[str]) -> None:
    async with (
        aiosqlite.connect(sqlite_path) as src,
        asyncpg.create_pool(pg_dsn) as pool,
    ):
        async with pool.acquire() as dst:
            for table in tables:
                await copy_table(src, dst, table)


async def main(sqlite_path: str, pg_dsn: str) -> None:
    tables = ["health_records", "ap_cache", "users", "dashboard_settings", "app_state"]
    await migrate(sqlite_path, pg_dsn, tables)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate SQLite DB to PostgreSQL")
    parser.add_argument("src", help="Path to SQLite database")
    parser.add_argument("dsn", help="PostgreSQL DSN")
    args = parser.parse_args()

    asyncio.run(main(args.src, args.dsn))
