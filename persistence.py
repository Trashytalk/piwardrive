from __future__ import annotations

"""Simple persistence helpers using SQLite."""

import os
import aiosqlite
from dataclasses import dataclass, asdict
from typing import Any, List, Optional
import asyncio
import logging

import config


def _db_path() -> str:
    env = os.getenv("PW_DB_PATH")
    if env:
        return os.path.expanduser(env)
    return os.path.join(config.CONFIG_DIR, "app.db")


# Reuse a single connection per event loop and config directory
_DB_CONN: aiosqlite.Connection | None = None
_DB_LOOP: asyncio.AbstractEventLoop | None = None
_DB_DIR: str | None = None


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


async def _init_db(conn: aiosqlite.Connection) -> None:
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
    await conn.commit()


async def save_health_record(rec: HealthRecord) -> None:
    """Insert ``rec`` into the ``health_records`` table."""
    conn = await _get_conn()
    await conn.execute(
        """
        INSERT OR REPLACE INTO health_records
        (timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent)
        VALUES (:timestamp, :cpu_temp, :cpu_percent, :memory_percent, :disk_percent)
        """,
        asdict(rec),
    )
    await conn.commit()


async def load_recent_health(limit: int = 10) -> List[HealthRecord]:
    """Return up to ``limit`` most recent :class:`HealthRecord` entries."""
    conn = await _get_conn()
    cur = await conn.execute(
        """SELECT timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent
        FROM health_records ORDER BY timestamp DESC LIMIT ?""",
        (limit,),
    )
    rows = await cur.fetchall()
    return [HealthRecord(**dict(row)) for row in rows]


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


async def load_ap_cache() -> list[dict[str, Any]]:
    """Return all rows from ``ap_cache`` as dictionaries."""
    conn = await _get_conn()
    cur = await conn.execute(
        "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache"
    )
    rows = await cur.fetchall()
    return [dict(row) for row in rows]
