"""Simple persistence helpers using SQLite."""
from __future__ import annotations

import os
import time
import json
import aiosqlite
from dataclasses import dataclass, asdict, field
from typing import Any, List, Optional, Callable, Awaitable
import asyncio
from datetime import datetime, timedelta
import logging

from piwardrive import config


def _db_path() -> str:
    """
    Return the file path to the SQLite database, using the PW_DB_PATH environment variable if set, or defaulting to the config directory.
    """
    env = os.getenv("PW_DB_PATH")
    if env:
        return os.path.expanduser(env)
    return os.path.join(config.CONFIG_DIR, "app.db")


# Reuse a single connection per event loop and config directory
_DB_CONN: aiosqlite.Connection | None = None
_DB_LOOP: asyncio.AbstractEventLoop | None = None
_DB_DIR: str | None = None

# Pending HealthRecord rows for bulk writes
_HEALTH_BUFFER: list[dict[str, Any]] = []
_LAST_FLUSH: float = 0.0

# Flush after this many records or seconds
_BUFFER_LIMIT = 50
_FLUSH_INTERVAL = 30.0

# Schema versioning
LATEST_VERSION = 2
Migration = Callable[[aiosqlite.Connection], Awaitable[None]]
_MIGRATIONS: list[Migration] = []


async def _migration_1(conn: aiosqlite.Connection) -> None:
    """
    Create the initial database schema with tables for health records, application state, and access point cache, including relevant indexes.
    """
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS health_records (
            timestamp TEXT PRIMARY KEY,
            cpu_temp REAL,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL
        )
        """
    )
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS app_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            last_screen TEXT,
            last_start TEXT,
            first_run INTEGER
        )
        """
    )
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ap_cache (
            bssid TEXT PRIMARY KEY,
            ssid TEXT,
            encryption TEXT,
            lat REAL,
            lon REAL,
            last_time INTEGER
        )
        """
    )
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_health_time ON health_records(timestamp)"
    )
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_apcache_time ON ap_cache(last_time)"
    )


_MIGRATIONS.append(_migration_1)


async def _migration_2(conn: aiosqlite.Connection) -> None:
    """
    Creates the `dashboard_settings` table if it does not exist, adding columns for layout and widgets.
    """
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS dashboard_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            layout TEXT,
            widgets TEXT
        )
        """
    )


_MIGRATIONS.append(_migration_2)


async def _get_conn() -> aiosqlite.Connection:
    """
    Obtain a cached asynchronous SQLite connection, initializing the database schema and applying migrations if necessary.
    
    Returns:
        aiosqlite.Connection: An active SQLite connection configured for the current event loop and configuration directory.
    """
    global _DB_CONN, _DB_LOOP, _DB_DIR
    loop = asyncio.get_running_loop()
    cur_dir = config.CONFIG_DIR
    if _DB_CONN is None or _DB_LOOP is not loop or _DB_DIR != cur_dir:
        if _DB_CONN is not None:
            try:
                await _DB_CONN.close()
            except Exception:
                logging.exception("Error closing previous DB connection")
        path = _db_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _DB_CONN = await aiosqlite.connect(path)
        await _DB_CONN.execute("PRAGMA journal_mode=WAL")
        _DB_CONN.row_factory = aiosqlite.Row
        await _init_db(_DB_CONN)
        _DB_LOOP = loop
        _DB_DIR = cur_dir
    return _DB_CONN


@dataclass
class HealthRecord:
    """System metrics collected by :class:`HealthMonitor`."""

    timestamp: str
    cpu_temp: Optional[float]
    cpu_percent: float
    memory_percent: float
    disk_percent: float


@dataclass
class AppState:
    """Persisted application state."""

    last_screen: str = "Map"
    last_start: str = ""
    first_run: bool = True


@dataclass
class DashboardSettings:
    """Persisted dashboard layout and widgets."""

    layout: list[Any] = field(default_factory=list)
    widgets: list[str] = field(default_factory=list)


async def _init_db(conn: aiosqlite.Connection) -> None:
    """
    Apply all necessary schema migrations to bring the SQLite database to the latest version.
    
    Ensures the `schema_version` table exists, determines the current schema version, and sequentially applies pending migrations. Updates the schema version after each migration and commits changes to the database.
    """
    await conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER)"
    )
    cur = await conn.execute("SELECT version FROM schema_version")
    row = await cur.fetchone()
    current = row["version"] if row else 0

    while current < LATEST_VERSION:
        migration = _MIGRATIONS[current]
        await migration(conn)
        current += 1
        if row is None:
            await conn.execute(
                "INSERT INTO schema_version (version) VALUES (?)", (current,)
            )
            row = {"version": current}  # type: ignore[assignment]
        else:
            await conn.execute(
                "UPDATE schema_version SET version = ?", (current,)
            )

    await conn.commit()


async def flush_health_records() -> None:
    """
    Persist all buffered HealthRecord entries to the database.
    
    Flushes the in-memory buffer of HealthRecord objects by inserting them into the `health_records` table and clears the buffer. If the buffer is empty, no action is taken.
    """
    global _LAST_FLUSH
    if not _HEALTH_BUFFER:
        return
    conn = await _get_conn()
    await conn.executemany(
        """
        INSERT OR REPLACE INTO health_records
        (timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent)
        VALUES (:timestamp, :cpu_temp, :cpu_percent, :memory_percent, :disk_percent)
        """,
        list(_HEALTH_BUFFER),
    )
    await conn.commit()
    _HEALTH_BUFFER.clear()
    _LAST_FLUSH = time.time()


async def save_health_record(rec: HealthRecord) -> None:
    """
    Buffers a health record for later insertion into the database, flushing the buffer if limits are exceeded.
    
    The record is added to an in-memory buffer and will be written to the database when the buffer reaches a size or time threshold.
    """
    await _get_conn()  # ensure DB file exists
    _HEALTH_BUFFER.append(asdict(rec))
    now = time.time()
    if len(_HEALTH_BUFFER) >= _BUFFER_LIMIT or now - _LAST_FLUSH >= _FLUSH_INTERVAL:
        await flush_health_records()


async def load_recent_health(limit: int = 10) -> List[HealthRecord]:
    """
    Retrieve the most recent health records up to the specified limit.
    
    Parameters:
        limit (int): Maximum number of recent HealthRecord entries to return. Defaults to 10.
    
    Returns:
        List[HealthRecord]: A list of HealthRecord objects ordered from most to least recent.
    """
    await flush_health_records()
    conn = await _get_conn()
    cur = await conn.execute(
        """SELECT timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent
        FROM health_records ORDER BY timestamp DESC LIMIT ?""",
        (limit,),
    )
    rows = await cur.fetchall()
    return [HealthRecord(**dict(row)) for row in rows]


async def purge_old_health(days: int) -> None:
    """
    Delete health records older than the specified number of days from the database.
    
    Parameters:
        days (int): The age threshold in days; records older than this will be removed.
    """
    await flush_health_records()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    conn = await _get_conn()
    await conn.execute(
        "DELETE FROM health_records WHERE timestamp < ?",
        (cutoff,),
    )
    await conn.commit()


async def save_app_state(state: AppState) -> None:
    """
    Persist the provided application state to the database, replacing any existing state.
    
    Parameters:
        state (AppState): The application state to be saved.
    """
    conn = await _get_conn()
    await conn.execute("DELETE FROM app_state WHERE id = 1")
    await conn.execute(
        (
            "INSERT INTO app_state (id, last_screen, last_start, first_run) "
            "VALUES (1, ?, ?, ?)"
        ),
        (state.last_screen, state.last_start, int(state.first_run)),
    )
    await conn.commit()


async def load_app_state() -> AppState:
    """
    Load the persisted application state from the database, or return default values if none exist.
    
    Returns:
        AppState: The loaded application state, or a default AppState if no record is found.
    """
    conn = await _get_conn()
    cur = await conn.execute(
        "SELECT last_screen, last_start, first_run FROM app_state WHERE id = 1"
    )
    row = await cur.fetchone()
    if row is None:
        return AppState()
    return AppState(
        last_screen=row["last_screen"],
        last_start=row["last_start"],
        first_run=bool(row["first_run"]),
    )


async def save_dashboard_settings(settings: DashboardSettings) -> None:
    """
    Persist the provided dashboard layout and widget configuration to the database, replacing any existing settings.
    """
    conn = await _get_conn()
    await conn.execute("DELETE FROM dashboard_settings WHERE id = 1")
    await conn.execute(
        (
            "INSERT INTO dashboard_settings (id, layout, widgets) "
            "VALUES (1, ?, ?)"
        ),
        (json.dumps(settings.layout), json.dumps(settings.widgets)),
    )
    await conn.commit()


async def load_dashboard_settings() -> DashboardSettings:
    """
    Load the persisted dashboard settings from the database, or return default settings if none are found.
    
    Returns:
        DashboardSettings: The loaded dashboard settings, or defaults if not previously saved.
    """
    conn = await _get_conn()
    cur = await conn.execute(
        "SELECT layout, widgets FROM dashboard_settings WHERE id = 1"
    )
    row = await cur.fetchone()
    if row is None:
        return DashboardSettings()
    return DashboardSettings(
        layout=json.loads(row["layout"]) if row["layout"] else [],
        widgets=json.loads(row["widgets"]) if row["widgets"] else [],
    )


async def save_ap_cache(records: list[dict[str, Any]]) -> None:
    """
    Replace all rows in the `ap_cache` table with the provided records.
    
    Parameters:
        records (list[dict[str, Any]]): List of dictionaries representing access point cache entries to be inserted.
    """
    conn = await _get_conn()
    await conn.execute("DELETE FROM ap_cache")
    if records:
        await conn.executemany(
            """
            INSERT INTO ap_cache (bssid, ssid, encryption, lat, lon, last_time)
            VALUES (:bssid, :ssid, :encryption, :lat, :lon, :last_time)
            """,
            records,
        )
    await conn.commit()


async def load_ap_cache() -> list[dict[str, Any]]:
    """
    Retrieve all access point cache entries from the database.
    
    Returns:
        A list of dictionaries, each representing a row from the `ap_cache` table with keys: bssid, ssid, encryption, lat, lon, and last_time.
    """
    conn = await _get_conn()
    cur = await conn.execute(
        "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache"
    )
    rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def get_table_counts() -> dict[str, int]:
    """
    Return a dictionary mapping each user-defined table name to its row count in the database.
    
    Returns:
        dict[str, int]: A mapping of table names to the number of rows in each table, excluding SQLite internal tables.
    """
    conn = await _get_conn()
    cur = await conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
        " AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row["name"] for row in await cur.fetchall()]
    result: dict[str, int] = {}
    for name in tables:
        cur = await conn.execute(f"SELECT COUNT(*) as cnt FROM {name}")
        row = await cur.fetchone()
        result[name] = int(row["cnt"]) if row else 0
    return result


async def vacuum() -> None:
    """
    Flushes any buffered health records and runs the SQLite VACUUM command to optimize the database.
    """
    await flush_health_records()
    conn = await _get_conn()
    await conn.execute("VACUUM")
    await conn.commit()


async def migrate() -> None:
    """
    Ensures the SQLite database schema is migrated to the latest version.
    
    This function initializes the database connection and applies any pending schema migrations as needed.
    """
    await _get_conn()
