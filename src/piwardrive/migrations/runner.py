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
    cur = await conn.execute(f"SELECT version FROM {MIGRATION_TABLE} ORDER BY version")
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


async def get_applied_migrations(conn: aiosqlite.Connection) -> set[int]:
    """Get set of applied migration versions."""
    await _ensure_table(conn)
    return await _applied_versions(conn)


async def get_available_migrations() -> list[BaseMigration]:
    """Get list of available migrations."""
    from . import MIGRATIONS

    return MIGRATIONS


async def check_migration_status(conn: aiosqlite.Connection) -> dict[str, any]:
    """Check migration status."""
    applied = await get_applied_migrations(conn)
    available = get_available_migrations()
    available_versions = {m.get_version() for m in available}

    return {
        "applied": sorted(applied),
        "available": sorted(available_versions),
        "pending": sorted(available_versions - applied),
        "unknown": sorted(applied - available_versions),
    }


async def run_pending_migrations(conn: aiosqlite.Connection) -> int:
    """Run all pending migrations and return count of applied migrations."""
    from . import MIGRATIONS

    status = await check_migration_status(conn)
    pending_count = len(status["pending"])

    if pending_count > 0:
        await run_migrations(conn, MIGRATIONS)

    return pending_count
