"""Validate migrated data between SQLite and PostgreSQL."""

from __future__ import annotations

import asyncio
from typing import Iterable

import aiosqlite
import asyncpg


async def count_rows_sqlite(conn: aiosqlite.Connection, table: str) -> int:
    cur = await conn.execute(f"SELECT COUNT(*) FROM {table}")
    row = await cur.fetchone()
    return int(row[0]) if row else 0


async def count_rows_pg(conn: asyncpg.Connection, table: str) -> int:
    row = await conn.fetchrow(f"SELECT COUNT(*) FROM {table}")
    return int(row[0]) if row else 0


async def validate(sqlite_path: str, pg_dsn: str, tables: Iterable[str]) -> None:
    async with aiosqlite.connect(sqlite_path) as src, asyncpg.connect(pg_dsn) as dst:
        for table in tables:
            s_count = await count_rows_sqlite(src, table)
            p_count = await count_rows_pg(dst, table)
            if s_count != p_count:
                raise RuntimeError(
                    f"Mismatch for {table}: sqlite={s_count} pg={p_count}"
                )
    print("Validation passed")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate SQLite to PostgreSQL migration"
    )
    parser.add_argument("src", help="SQLite DB path")
    parser.add_argument("dsn", help="PostgreSQL DSN")
    args = parser.parse_args()

    tables = ["health_records", "ap_cache", "users", "dashboard_settings", "app_state"]
    asyncio.run(validate(args.src, args.dsn, tables))
