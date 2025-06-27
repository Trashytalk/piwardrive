"""Simple persistence helpers using SQLite."""

from __future__ import annotations

import asyncio
import logging
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, List, Optional

import aiosqlite

from piwardrive import config


def _db_path() -> str:
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
    """Create initial database schema."""
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
    """Add dashboard settings table."""
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
    """Return a cached SQLite connection initialized with the proper schema."""
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
    """Create or migrate the SQLite schema to the latest version."""
    await conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER)")
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
            await conn.execute("UPDATE schema_version SET version = ?", (current,))

    await conn.commit()


async def flush_health_records() -> None:
    """Write any buffered :class:`HealthRecord` rows to the database."""
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
        _HEALTH_BUFFER,
    )
    await conn.commit()
    _HEALTH_BUFFER.clear()
    _LAST_FLUSH = time.time()


async def save_health_record(rec: HealthRecord) -> None:
    """Queue ``rec`` for insertion into ``health_records``."""
    await _get_conn()  # ensure DB file exists
    _HEALTH_BUFFER.append(asdict(rec))
    now = time.time()
    if len(_HEALTH_BUFFER) >= _BUFFER_LIMIT or now - _LAST_FLUSH >= _FLUSH_INTERVAL:
        await flush_health_records()


async def load_recent_health(limit: int = 10) -> List[HealthRecord]:
    """Return up to ``limit`` most recent :class:`HealthRecord` entries."""
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
    """Delete ``health_records`` older than ``days`` days."""
    await flush_health_records()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    conn = await _get_conn()
    await conn.execute(
        "DELETE FROM health_records WHERE timestamp < ?",
        (cutoff,),
    )
    await conn.commit()


async def save_app_state(state: AppState) -> None:
    """Persist application ``state``."""
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
    """Load persisted :class:`AppState` or defaults."""
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
    """Persist dashboard layout to ``config.json``."""
    cfg = config.load_config()
    cfg.dashboard_layout = settings.layout
    config.save_config(cfg)


async def load_dashboard_settings() -> DashboardSettings:
    """Load persisted :class:`DashboardSettings` from ``config.json``."""
    cfg = config.load_config()
    layout = cfg.dashboard_layout
    widgets = [
        cls for item in layout if isinstance(item, dict) and (cls := item.get("cls"))
    ]
    return DashboardSettings(layout=layout, widgets=widgets)


async def save_ap_cache(records: list[dict[str, Any]]) -> None:
    """Replace ``ap_cache`` contents with ``records``."""
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


async def load_ap_cache(after: float | None = None) -> list[dict[str, Any]]:
    """Return rows from ``ap_cache`` optionally newer than ``after``."""
    conn = await _get_conn()
    if after is None:
        cur = await conn.execute(
            "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache"
        )
    else:
        cur = await conn.execute(
            "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache "
            "WHERE last_time > ?",
            (after,),
        )
    rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def get_table_counts() -> dict[str, int]:
    """Return row counts for all user tables."""
    path = _db_path()

    def _work() -> dict[str, int]:
        result: dict[str, int] = {}
        if not os.path.exists(path):
            return result
        import sqlite3

        with sqlite3.connect(path) as db:
            cur = db.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = [row[0] for row in cur.fetchall()]
            for name in tables:
                row = db.execute(
                    f"SELECT COUNT(*) FROM {name}"  # nosec B608
                ).fetchone()
                result[name] = int(row[0]) if row else 0
        return result

    return await asyncio.to_thread(_work)


async def vacuum() -> None:
    """Run ``VACUUM`` on the active database connection."""
    await flush_health_records()
    conn = await _get_conn()
    await conn.execute("VACUUM")
    await conn.commit()


async def migrate() -> None:
    """Ensure the database schema is up to date."""
    await _get_conn()
