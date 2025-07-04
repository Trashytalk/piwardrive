from __future__ import annotations

from typing import Sequence

import aiosqlite

from .base import BaseMigration

MIGRATION_TABLE = "migrations"

async def _ensure_table(conn: aiosqlite.Connection) -> None:
    await conn.execute(
        f"CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE} (version INTEGER PRIMARY KEY)"
    )
    await conn.commit()

async def _applied_versions(conn: aiosqlite.Connection) -> set[int]:
    cur = await conn.execute(
        f"SELECT version FROM {MIGRATION_TABLE} ORDER BY version"
    )
    rows = await cur.fetchall()
    return {row[0] for row in rows}

async def run_migrations(
    conn: aiosqlite.Connection, migrations: Sequence[BaseMigration]
) -> None:
    """Apply all pending migrations using ``conn``."""
    await _ensure_table(conn)
    applied = await _applied_versions(conn)
    for mig in sorted(migrations, key=lambda m: m.get_version()):
        if mig.get_version() in applied:
            continue
        await mig.apply(conn)
        await conn.execute(
            f"INSERT INTO {MIGRATION_TABLE} (version) VALUES (?)",
            (mig.get_version(),),
        )
        await conn.commit()
