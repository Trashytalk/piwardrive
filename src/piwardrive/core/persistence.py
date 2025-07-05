"""Simple persistence helpers using SQLite."""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import sqlite3
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
)

import aiosqlite

logger = logging.getLogger(__name__)

try:
    from pysqlcipher3 import dbapi2 as sqlcipher
except Exception:  # pragma: no cover - optional dependency
    sqlcipher = None

from piwardrive import config


class ShardManager:
    """Simple hash-based shard selector."""

    def __init__(self, shards: int = 1) -> None:
        self.shards = max(1, shards)

    def db_path(self, key: str = "") -> str:
        env = os.getenv("PW_DB_PATH")
        if env:
            base = os.path.expanduser(env)
        else:
            base = os.path.join(config.CONFIG_DIR, "app.db")
        if self.shards == 1:
            return base
        idx = int(hashlib.sha1(key.encode()).hexdigest(), 16) % self.shards
        root, ext = os.path.splitext(base)
        return f"{root}_{idx}{ext}"


_shard_mgr = ShardManager(int(os.getenv("PW_DB_SHARDS", "1")))


def _db_path(key: str = "") -> str:
    """Return the SQLite database path for ``key``."""
    return _shard_mgr.db_path(key)


# SQLite connection pool
_POOL_SIZE = int(os.getenv("PW_DB_POOL_SIZE", "10"))
_DB_POOL: asyncio.Queue[aiosqlite.Connection] | None = None
_DB_DIR: str | None = None
_DB_KEY: str | None = None
_SCHEMA_INITIALISED = False
_POOL_LOCK = asyncio.Lock()

# Connection metrics
_METRICS = {
    "acquired": 0,
    "released": 0,
}

# Pending HealthRecord rows for bulk writes
_HEALTH_BUFFER: list[dict[str, Any]] = []
_LAST_FLUSH: float = 0.0
_FLUSH_TASK: asyncio.Task | None = None

# Flush after this many records or seconds
_BUFFER_LIMIT = int(os.getenv("PW_DB_BUFFER_LIMIT", "50"))
_FLUSH_INTERVAL = float(os.getenv("PW_DB_FLUSH_INTERVAL", "30.0"))

# Schema versioning
LATEST_VERSION = 4
Migration = Callable[[aiosqlite.Connection], Awaitable[None]]
_MIGRATIONS: list[Migration] = []


def _filter_invalid(
    records: list[dict[str, Any]], required: Sequence[str]
) -> list[dict[str, Any]]:
    """Return only records containing all ``required`` keys with non-``None`` values."""
    return [r for r in records if all(r.get(k) is not None for k in required)]


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


async def _migration_3(conn: aiosqlite.Connection) -> None:
    """Add users table for authentication tokens."""
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            token_hash TEXT,
            token_created INTEGER
        )
        """
    )


_MIGRATIONS.append(_migration_3)


async def _migration_4(conn: aiosqlite.Connection) -> None:
    """Create scan_sessions table."""
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scan_sessions (
            id TEXT PRIMARY KEY,
            device_id TEXT NOT NULL,
            scan_type TEXT NOT NULL,
            started_at TIMESTAMP NOT NULL,
            completed_at TIMESTAMP,
            duration_seconds INTEGER,
            location_start_lat REAL,
            location_start_lon REAL,
            location_end_lat REAL,
            location_end_lon REAL,
            interface_used TEXT,
            scan_parameters TEXT,
            total_detections INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_scan_sessions_device_time ON "
        "scan_sessions(device_id, started_at)"
    )
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_scan_sessions_type ON "
        "scan_sessions(scan_type)"
    )
    await conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_scan_sessions_location ON "
        "scan_sessions(location_start_lat, location_start_lon)"
    )


_MIGRATIONS.append(_migration_4)


async def _create_connection(path: str, key: str | None) -> aiosqlite.Connection:
    """Create a new SQLite connection with performance pragmas."""
    if key:
        if sqlcipher is None:
            raise RuntimeError("pysqlcipher3 must be installed to use PW_DB_KEY")
        aiosqlite.core.sqlite3 = sqlcipher
    else:
        aiosqlite.core.sqlite3 = sqlite3
    conn = await aiosqlite.connect(path)
    if key:
        await conn.execute("PRAGMA key = ?", (key,))
    pragmas = {
        "journal_mode": "WAL",
        "synchronous": "NORMAL",
        "temp_store": "MEMORY",
        "cache_size": 10000,
    }
    for k, v in pragmas.items():
        await conn.execute(f"PRAGMA {k}={v}")
    conn.row_factory = aiosqlite.Row
    return conn


async def _init_pool() -> None:
    """Initialise the connection pool and database schema."""
    global _DB_POOL, _DB_DIR, _DB_KEY, _SCHEMA_INITIALISED
    async with _POOL_LOCK:
        cur_dir = config.CONFIG_DIR
        key = os.getenv("PW_DB_KEY")
        path = _db_path()
        if _DB_POOL is not None and _DB_DIR == cur_dir and _DB_KEY == key:
            return
        if _DB_POOL is not None:
            while not _DB_POOL.empty():
                conn = await _DB_POOL.get()
                await conn.close()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _DB_POOL = asyncio.Queue(maxsize=_POOL_SIZE)
        for i in range(_POOL_SIZE):
            conn = await _create_connection(path, key)
            if not _SCHEMA_INITIALISED:
                await _init_db(conn)
                _SCHEMA_INITIALISED = True
            await _DB_POOL.put(conn)
        _DB_DIR = cur_dir
        _DB_KEY = key


async def _acquire_conn() -> aiosqlite.Connection:
    await _init_pool()
    assert _DB_POOL is not None
    conn = await _DB_POOL.get()
    try:
        await conn.execute("SELECT 1")
    except Exception:
        path = _db_path()
        conn = await _create_connection(path, _DB_KEY)
    _METRICS["acquired"] += 1
    return conn


async def _release_conn(conn: aiosqlite.Connection) -> None:
    if _DB_POOL is None:
        await conn.close()
        return
    await _DB_POOL.put(conn)
    _METRICS["released"] += 1


class _ConnCtx:
    def __init__(self) -> None:
        self.conn: aiosqlite.Connection | None = None

    async def __aenter__(self) -> aiosqlite.Connection:
        self.conn = await _acquire_conn()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self.conn is not None
        await _release_conn(self.conn)


def _get_conn() -> _ConnCtx:
    """Return an async context manager yielding a pooled connection."""
    return _ConnCtx()


async def shutdown_pool() -> None:
    """Close all pooled connections."""
    global _DB_POOL
    if _DB_POOL is None:
        return
    await flush_health_records()
    while not _DB_POOL.empty():
        conn = await _DB_POOL.get()
        await conn.close()
    _DB_POOL = None


def get_db_metrics() -> dict[str, int]:
    """Return connection pool metrics."""
    return {
        "pool_size": _POOL_SIZE,
        "available": _DB_POOL.qsize() if _DB_POOL else 0,
        **_METRICS,
    }


async def backup_database(dest: str) -> None:
    """Write a backup of the primary database to ``dest``."""
    async with _get_conn() as conn:
        backup_db = await aiosqlite.connect(dest)
        await conn.backup(backup_db)
        await backup_db.close()


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


@dataclass
class User:
    """Application user credentials and token."""

    username: str
    password_hash: str
    token_hash: str | None = None


@dataclass
class ScanSession:
    """Metadata about a scanning session."""

    id: str
    device_id: str
    scan_type: str
    started_at: str
    completed_at: str | None = None
    duration_seconds: int | None = None
    location_start_lat: float | None = None
    location_start_lon: float | None = None
    location_end_lat: float | None = None
    location_end_lon: float | None = None
    interface_used: str | None = None
    scan_parameters: str | None = None
    total_detections: int = 0
    created_at: str | None = None


async def _init_db(conn: aiosqlite.Connection) -> None:
    """Create or migrate the SQLite schema to the latest version."""
    await conn.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER)")
    cur = await conn.execute("SELECT version FROM schema_version")
    row = await cur.fetchone()
    current = row["version"] if row else 0
    exists = row is not None

    while current < LATEST_VERSION:
        migration = _MIGRATIONS[current]
        await migration(conn)
        current += 1
        if exists:
            await conn.execute("UPDATE schema_version SET version = ?", (current,))
        else:
            await conn.execute(
                "INSERT INTO schema_version (version) VALUES (?)", (current,)
            )
            exists = True

    await conn.commit()


async def flush_health_records() -> None:
    """Write any buffered :class:`HealthRecord` rows to the database."""
    global _LAST_FLUSH
    if not _HEALTH_BUFFER:
        return
    async with _get_conn() as conn:
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
    global _FLUSH_TASK
    # Ensure database exists and start flush worker
    async with _get_conn():
        pass
    _HEALTH_BUFFER.append(asdict(rec))
    now = time.time()
    if len(_HEALTH_BUFFER) >= _BUFFER_LIMIT or now - _LAST_FLUSH >= _FLUSH_INTERVAL:
        await flush_health_records()
    elif _FLUSH_TASK is None or _FLUSH_TASK.done():
        _FLUSH_TASK = asyncio.create_task(_flush_worker())


async def _flush_worker() -> None:
    """Background task periodically flushing buffered records."""
    try:
        while _HEALTH_BUFFER:
            await asyncio.sleep(_FLUSH_INTERVAL)
            await flush_health_records()
    finally:
        global _FLUSH_TASK
        _FLUSH_TASK = None


async def load_recent_health(limit: int = 10, offset: int = 0) -> List[HealthRecord]:
    """Return ``limit`` most recent :class:`HealthRecord` entries with ``offset``."""
    await flush_health_records()
    async with _get_conn() as conn:
        cur = await conn.execute(
            """SELECT timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent
        FROM health_records ORDER BY timestamp DESC LIMIT ? OFFSET ?""",
            (limit, offset),
        )
        rows = await cur.fetchall()
    return [HealthRecord(**dict(row)) for row in rows]


async def iter_health_history(
    start: str | None = None,
    end: str | None = None,
    *,
    limit: int | None = None,
    offset: int = 0,
) -> AsyncIterator[HealthRecord]:
    """Yield :class:`HealthRecord` rows between ``start`` and ``end`` with
    pagination."""
    await flush_health_records()
    async with _get_conn() as conn:
        query = (
            "SELECT timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent"
            " FROM health_records"
        )
        params: list[object] = []
        if start and end:
            query += " WHERE timestamp >= ? AND timestamp <= ?"
            params = [start, end]
        elif start:
            query += " WHERE timestamp >= ?"
            params = [start]
        elif end:
            query += " WHERE timestamp <= ?"
            params = [end]
        query += " ORDER BY timestamp"
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        cur = await conn.execute(query, tuple(params))
        async for row in cur:
            yield HealthRecord(**dict(row))


async def load_health_history(
    start: str | None = None,
    end: str | None = None,
    *,
    limit: int | None = None,
    offset: int = 0,
) -> List[HealthRecord]:
    """Return a list of :class:`HealthRecord` rows between ``start`` and ``end``."""
    return [
        rec async for rec in iter_health_history(start, end, limit=limit, offset=offset)
    ]


async def purge_old_health(days: int) -> None:
    """Delete ``health_records`` older than ``days`` days."""
    await flush_health_records()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    async with _get_conn() as conn:
        await conn.execute(
            "DELETE FROM health_records WHERE timestamp < ?",
            (cutoff,),
        )
        await conn.commit()


async def save_app_state(state: AppState) -> None:
    """Persist application ``state``."""
    async with _get_conn() as conn:
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
    async with _get_conn() as conn:
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


async def get_user(username: str) -> User | None:
    """Return ``User`` row for ``username`` if it exists."""
    async with _get_conn() as conn:
        cur = await conn.execute(
            "SELECT username, password_hash, token_hash FROM users WHERE username = ?",
            (username,),
        )
        row = await cur.fetchone()
    return User(**row) if row else None


async def save_user(user: User) -> None:
    """Insert or replace ``user`` in the database."""
    async with _get_conn() as conn:
        await conn.execute(
            "INSERT OR REPLACE INTO users (username, password_hash, token_hash) "
            "VALUES (?, ?, ?)",
            (user.username, user.password_hash, user.token_hash),
        )
        await conn.commit()


async def update_user_token(username: str, token_hash: str) -> None:
    """Set ``token_hash`` for ``username``."""
    async with _get_conn() as conn:
        await conn.execute(
            "UPDATE users SET token_hash = ?, token_created = strftime('%s','now') "
            "WHERE username = ?",
            (token_hash, username),
        )
        await conn.commit()


async def get_user_by_token(token_hash: str) -> User | None:
    """Return ``User`` matching ``token_hash`` if found."""
    async with _get_conn() as conn:
        cur = await conn.execute(
            "SELECT username, password_hash, token_hash FROM users "
            "WHERE token_hash = ?",
            (token_hash,),
        )
        row = await cur.fetchone()
    return User(**row) if row else None


async def save_scan_session(session: ScanSession) -> None:
    """Insert or update a :class:`ScanSession` row."""
    values = asdict(session)
    async with _get_conn() as conn:
        await conn.execute(
            """
            INSERT OR REPLACE INTO scan_sessions (
                id, device_id, scan_type, started_at, completed_at,
                duration_seconds, location_start_lat, location_start_lon,
                location_end_lat, location_end_lon, interface_used,
                scan_parameters, total_detections, created_at
            ) VALUES (
                :id, :device_id, :scan_type, :started_at, :completed_at,
                :duration_seconds, :location_start_lat, :location_start_lon,
                :location_end_lat, :location_end_lon, :interface_used,
                :scan_parameters, :total_detections,
                COALESCE(:created_at, CURRENT_TIMESTAMP)
            )
            """,
            values,
        )
        await conn.commit()


async def get_scan_session(session_id: str) -> ScanSession | None:
    """Return ``ScanSession`` with ``session_id`` if found."""
    async with _get_conn() as conn:
        cur = await conn.execute(
            """
            SELECT id, device_id, scan_type, started_at, completed_at,
                   duration_seconds, location_start_lat, location_start_lon,
                   location_end_lat, location_end_lon, interface_used,
                   scan_parameters, total_detections, created_at
            FROM scan_sessions WHERE id = ?
            """,
            (session_id,),
        )
        row = await cur.fetchone()
    return ScanSession(**row) if row else None


async def iter_scan_sessions(
    *, limit: int | None = None, offset: int = 0
) -> AsyncIterator[ScanSession]:
    """Yield ``ScanSession`` rows ordered by ``started_at`` descending."""
    async with _get_conn() as conn:
        query = (
            "SELECT id, device_id, scan_type, started_at, completed_at, "
            "duration_seconds, location_start_lat, location_start_lon, "
            "location_end_lat, location_end_lon, interface_used, "
            "scan_parameters, total_detections, created_at "
            "FROM scan_sessions ORDER BY started_at DESC"
        )
        params: list[object] = []
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        cur = await conn.execute(query, tuple(params))
        async for row in cur:
            yield ScanSession(**dict(row))


async def save_ap_cache(records: list[dict[str, Any]]) -> None:
    """Replace ``ap_cache`` contents with ``records``."""
    async with _get_conn() as conn:
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


async def iter_ap_cache(
    after: float | None = None,
    *,
    limit: int | None = None,
    offset: int = 0,
) -> AsyncIterator[dict[str, Any]]:
    """Yield rows from ``ap_cache`` optionally newer than ``after`` with pagination."""
    async with _get_conn() as conn:
        params: list[object] = []
        query = "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache"
        if after is not None:
            query += " WHERE last_time > ?"
            params.append(after)
        query += " ORDER BY last_time"
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        cur = await conn.execute(query, tuple(params))
        async for row in cur:
            yield dict(row)


async def load_ap_cache(
    after: float | None = None,
    *,
    limit: int | None = None,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Return rows from ``ap_cache`` optionally newer than ``after`` with pagination."""
    return [row async for row in iter_ap_cache(after, limit=limit, offset=offset)]


async def save_wifi_detections(records: list[dict[str, Any]]) -> None:
    """Insert ``records`` into the ``wifi_detections`` table."""
    records = _filter_invalid(
        records,
        ["scan_session_id", "detection_timestamp", "bssid"],
    )
    if not records:
        return
    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT INTO wifi_detections (
                scan_session_id, detection_timestamp, bssid, ssid,
                channel, frequency_mhz, signal_strength_dbm, noise_floor_dbm,
                snr_db, encryption_type, cipher_suite, authentication_method,
                wps_enabled, vendor_oui, vendor_name, device_type,
                latitude, longitude, altitude_meters, accuracy_meters,
                heading_degrees, speed_kmh, beacon_interval_ms, dtim_period,
                ht_capabilities, vht_capabilities, he_capabilities,
                country_code, regulatory_domain, tx_power_dbm,
                load_percentage, station_count, data_rates,
                first_seen, last_seen, detection_count
            ) VALUES (
                :scan_session_id, :detection_timestamp, :bssid, :ssid,
                :channel, :frequency_mhz, :signal_strength_dbm, :noise_floor_dbm,
                :snr_db, :encryption_type, :cipher_suite, :authentication_method,
                :wps_enabled, :vendor_oui, :vendor_name, :device_type,
                :latitude, :longitude, :altitude_meters, :accuracy_meters,
                :heading_degrees, :speed_kmh, :beacon_interval_ms, :dtim_period,
                :ht_capabilities, :vht_capabilities, :he_capabilities,
                :country_code, :regulatory_domain, :tx_power_dbm,
                :load_percentage, :station_count, :data_rates,
                :first_seen, :last_seen, :detection_count
            )
            """,
            records,
        )
        await conn.commit()


async def save_bluetooth_detections(records: list[dict[str, Any]]) -> None:
    """Insert ``records`` into the ``bluetooth_detections`` table."""
    records = _filter_invalid(
        records,
        ["scan_session_id", "detection_timestamp", "mac_address"],
    )
    if not records:
        return
    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT INTO bluetooth_detections (
                scan_session_id, detection_timestamp, mac_address, device_name,
                device_class, device_type, manufacturer_id, manufacturer_name,
                rssi_dbm, tx_power_dbm, bluetooth_version, supported_services,
                is_connectable, is_paired, latitude, longitude, altitude_meters,
                accuracy_meters, heading_degrees, speed_kmh, first_seen,
                last_seen, detection_count
            ) VALUES (
                :scan_session_id, :detection_timestamp, :mac_address, :device_name,
                :device_class, :device_type, :manufacturer_id, :manufacturer_name,
                :rssi_dbm, :tx_power_dbm, :bluetooth_version, :supported_services,
                :is_connectable, :is_paired, :latitude, :longitude, :altitude_meters,
                :accuracy_meters, :heading_degrees, :speed_kmh, :first_seen,
                :last_seen, :detection_count
            )
            """,
            records,
        )
        await conn.commit()


async def save_cellular_detections(records: list[dict[str, Any]]) -> None:
    """Insert ``records`` into the ``cellular_detections`` table."""
    records = _filter_invalid(
        records,
        ["scan_session_id", "detection_timestamp"],
    )
    if not records:
        return
    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT INTO cellular_detections (
                scan_session_id, detection_timestamp, cell_id, lac, mcc, mnc,
                network_name, technology, frequency_mhz, band, channel,
                signal_strength_dbm, signal_quality, timing_advance, latitude,
                longitude, altitude_meters, accuracy_meters, heading_degrees,
                speed_kmh, first_seen, last_seen, detection_count
            ) VALUES (
                :scan_session_id, :detection_timestamp, :cell_id, :lac, :mcc,
                :mnc, :network_name, :technology, :frequency_mhz, :band,
                :channel, :signal_strength_dbm, :signal_quality,
                :timing_advance, :latitude, :longitude, :altitude_meters,
                :accuracy_meters, :heading_degrees, :speed_kmh, :first_seen,
                :last_seen, :detection_count
            )
            """,
            records,
        )
        await conn.commit()


async def save_gps_tracks(records: list[dict[str, Any]]) -> None:
    """Insert ``records`` into the ``gps_tracks`` table."""
    records = _filter_invalid(
        records,
        ["scan_session_id", "timestamp", "latitude", "longitude"],
    )
    if not records:
        return
    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT INTO gps_tracks (
                scan_session_id, timestamp, latitude, longitude,
                altitude_meters, accuracy_meters, heading_degrees, speed_kmh,
                satellite_count, hdop, vdop, pdop, fix_type
            ) VALUES (
                :scan_session_id, :timestamp, :latitude, :longitude,
                :altitude_meters, :accuracy_meters, :heading_degrees, :speed_kmh,
                :satellite_count, :hdop, :vdop, :pdop, :fix_type
            )
            """,
            records,
        )
        await conn.commit()


async def save_network_fingerprints(records: list[dict[str, Any]]) -> None:
    """Insert or update records in the ``network_fingerprints`` table."""
    records = _filter_invalid(records, ["bssid", "fingerprint_hash"])
    if not records:
        return
    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT INTO network_fingerprints (
                bssid, ssid, fingerprint_hash, confidence_score,
                device_model, firmware_version, characteristics,
                classification, risk_level, tags,
                created_at, updated_at
            ) VALUES (
                :bssid, :ssid, :fingerprint_hash, :confidence_score,
                :device_model, :firmware_version, :characteristics,
                :classification, :risk_level, :tags,
                COALESCE(:created_at, CURRENT_TIMESTAMP),
                COALESCE(:updated_at, CURRENT_TIMESTAMP)
            )
            ON CONFLICT(bssid) DO UPDATE SET
                ssid=excluded.ssid,
                fingerprint_hash=excluded.fingerprint_hash,
                confidence_score=excluded.confidence_score,
                device_model=excluded.device_model,
                firmware_version=excluded.firmware_version,
                characteristics=excluded.characteristics,
                classification=excluded.classification,
                risk_level=excluded.risk_level,
                tags=excluded.tags,
                updated_at=CURRENT_TIMESTAMP
            """,
            records,
        )
        await conn.commit()


async def save_suspicious_activities(records: list[dict[str, Any]]) -> None:
    """Insert ``records`` into the ``suspicious_activities`` table."""
    records = _filter_invalid(
        records, ["scan_session_id", "activity_type", "severity", "detected_at"]
    )
    if not records:
        return
    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT INTO suspicious_activities (
                scan_session_id, activity_type, severity, target_bssid,
                target_ssid, evidence, description, detected_at,
                latitude, longitude, false_positive, analyst_notes
            ) VALUES (
                :scan_session_id, :activity_type, :severity, :target_bssid,
                :target_ssid, :evidence, :description, :detected_at,
                :latitude, :longitude, :false_positive, :analyst_notes
            )
            """,
            records,
        )
        await conn.commit()


async def count_suspicious_activities(since: str | None = None) -> int:
    """Count suspicious activities, optionally since a specific timestamp."""
    async with _get_conn() as conn:
        if since:
            cursor = await conn.execute(
                "SELECT COUNT(*) FROM suspicious_activities WHERE detected_at >= ?",
                (since,),
            )
        else:
            cursor = await conn.execute("SELECT COUNT(*) FROM suspicious_activities")

        result = await cursor.fetchone()
        return result[0] if result else 0


async def load_recent_suspicious(limit: int = 10) -> List[Dict[str, Any]]:
    """Load recent suspicious activities."""
    async with _get_conn() as conn:
        cursor = await conn.execute(
            """
            SELECT 
                id, scan_session_id, activity_type, severity, target_bssid,
                target_ssid, evidence, description, detected_at,
                latitude, longitude, false_positive, analyst_notes
            FROM suspicious_activities 
            ORDER BY detected_at DESC 
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in await cursor.fetchall()]


async def get_table_counts() -> Dict[str, int]:
    """Get row counts for all main tables."""
    counts = {}

    async with _get_conn() as conn:
        # Get list of tables
        cursor = await conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = [row[0] for row in await cursor.fetchall()]

        # Count rows in each table
        for table in tables:
            try:
                cursor = await conn.execute(f"SELECT COUNT(*) FROM {table}")
                result = await cursor.fetchone()
                counts[table] = result[0] if result else 0
            except Exception as e:
                counts[table] = 0

    return counts


async def load_daily_detection_stats(
    session_id: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int | None = None,
) -> List[Dict[str, Any]]:
    """Load daily detection statistics."""
    async with _get_conn() as conn:
        query = """
        SELECT 
            DATE(detection_timestamp) as date,
            COUNT(*) as total_detections,
            COUNT(DISTINCT bssid) as unique_networks,
            AVG(signal_strength_dbm) as avg_signal_strength,
            MAX(signal_strength_dbm) as max_signal_strength,
            MIN(signal_strength_dbm) as min_signal_strength
        FROM wifi_detections
        WHERE 1=1
        """
        params = []

        if session_id:
            query += " AND scan_session_id = ?"
            params.append(session_id)

        if start:
            query += " AND detection_timestamp >= ?"
            params.append(start)

        if end:
            query += " AND detection_timestamp < ?"
            params.append(end)

        query += " GROUP BY DATE(detection_timestamp) ORDER BY date DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor = await conn.execute(query, params)
        return [dict(row) for row in await cursor.fetchall()]


async def load_hourly_detection_stats(
    session_id: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int | None = None,
) -> List[Dict[str, Any]]:
    """Load hourly detection statistics."""
    async with _get_conn() as conn:
        query = """
        SELECT 
            strftime('%Y-%m-%d %H:00:00', detection_timestamp) as hour,
            COUNT(*) as total_detections,
            COUNT(DISTINCT bssid) as unique_networks,
            AVG(signal_strength_dbm) as avg_signal_strength
        FROM wifi_detections
        WHERE 1=1
        """
        params = []

        if session_id:
            query += " AND scan_session_id = ?"
            params.append(session_id)

        if start:
            query += " AND detection_timestamp >= ?"
            params.append(start)

        if end:
            query += " AND detection_timestamp < ?"
            params.append(end)

        query += " GROUP BY hour ORDER BY hour DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor = await conn.execute(query, params)
        return [dict(row) for row in await cursor.fetchall()]


async def load_network_analytics(
    bssid: str | None = None,
    start: str | None = None,
    end: str | None = None,
    limit: int | None = None,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Load network analytics records."""
    async with _get_conn() as conn:
        query = """
        SELECT 
            bssid, analysis_date, total_detections, unique_locations,
            avg_signal_strength, max_signal_strength, min_signal_strength,
            signal_variance, coverage_radius_meters, mobility_score,
            encryption_changes, ssid_changes, channel_changes,
            suspicious_score, last_analyzed
        FROM network_analytics
        WHERE 1=1
        """
        params = []

        if bssid:
            query += " AND bssid = ?"
            params.append(bssid)

        if start:
            query += " AND analysis_date >= ?"
            params.append(start)

        if end:
            query += " AND analysis_date < ?"
            params.append(end)

        query += " ORDER BY analysis_date DESC, bssid"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        if offset:
            query += " OFFSET ?"
            params.append(offset)

        cursor = await conn.execute(query, params)
        return [dict(row) for row in await cursor.fetchall()]


async def load_network_coverage_grid(
    limit: int | None = None, offset: int = 0
) -> List[Dict[str, Any]]:
    """Load network coverage grid data."""
    async with _get_conn() as conn:
        query = """
        SELECT 
            latitude, longitude, COUNT(*) as detection_count,
            AVG(signal_strength_dbm) as avg_signal_strength,
            COUNT(DISTINCT bssid) as unique_networks
        FROM wifi_detections
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        GROUP BY 
            CAST(latitude * 1000 AS INT),
            CAST(longitude * 1000 AS INT)
        ORDER BY detection_count DESC
        """
        params = []

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        if offset:
            query += " OFFSET ?"
            params.append(offset)

        cursor = await conn.execute(query, params)
        return [dict(row) for row in await cursor.fetchall()]


async def refresh_daily_detection_stats() -> None:
    """Rebuild the ``daily_detection_stats`` materialized view."""
    async with _get_conn() as conn:
        await conn.execute("DROP TABLE IF EXISTS daily_detection_stats")
        await conn.execute(
            """
            CREATE TABLE daily_detection_stats AS
            SELECT
                DATE(detection_timestamp) AS detection_date,
                scan_session_id,
                COUNT(*) AS total_detections,
                COUNT(DISTINCT bssid) AS unique_networks,
                AVG(signal_strength_dbm) AS avg_signal,
                MIN(signal_strength_dbm) AS min_signal,
                MAX(signal_strength_dbm) AS max_signal,
                COUNT(DISTINCT channel) AS channels_used,
                COUNT(CASE WHEN encryption_type = 'OPEN' THEN 1 END) AS open_networks,
                COUNT(CASE WHEN encryption_type LIKE '%WEP%' THEN 1 END) AS wep_networks,
                COUNT(CASE WHEN encryption_type LIKE '%WPA%' THEN 1 END) AS wpa_networks
            FROM wifi_detections
            GROUP BY DATE(detection_timestamp), scan_session_id
            """
        )
        await conn.commit()


async def refresh_network_coverage_grid() -> None:
    """Rebuild the ``network_coverage_grid`` materialized view."""
    async with _get_conn() as conn:
        await conn.execute("DROP TABLE IF EXISTS network_coverage_grid")
        await conn.execute(
            """
            CREATE TABLE network_coverage_grid AS
            SELECT
                ROUND(latitude, 4) AS lat_grid,
                ROUND(longitude, 4) AS lon_grid,
                COUNT(*) AS detection_count,
                COUNT(DISTINCT bssid) AS unique_networks,
                AVG(signal_strength_dbm) AS avg_signal,
                MAX(signal_strength_dbm) AS max_signal
            FROM wifi_detections
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            GROUP BY ROUND(latitude, 4), ROUND(longitude, 4)
            """
        )
        await conn.commit()


async def save_network_analytics(records: List[Dict[str, Any]]) -> None:
    """Insert or update records in the network_analytics table."""
    if not records:
        return

    async with _get_conn() as conn:
        await conn.executemany(
            """
            INSERT OR REPLACE INTO network_analytics (
                bssid, analysis_date, total_detections, unique_locations,
                avg_signal_strength, max_signal_strength, min_signal_strength,
                signal_variance, coverage_radius_meters, mobility_score,
                encryption_changes, ssid_changes, channel_changes,
                suspicious_score, last_analyzed
            ) VALUES (
                :bssid, :analysis_date, :total_detections, :unique_locations,
                :avg_signal_strength, :max_signal_strength, :min_signal_strength,
                :signal_variance, :coverage_radius_meters, :mobility_score,
                :encryption_changes, :ssid_changes, :channel_changes,
                :suspicious_score, :last_analyzed
            )
            """,
            records,
        )
        await conn.commit()


async def get_network_analytics(
    bssid: str | None = None, limit: int = 100
) -> List[Dict[str, Any]]:
    """Get network analytics records."""
    return await load_network_analytics(bssid=bssid, limit=limit)


async def analyze_network_behavior(bssid: str) -> Dict[str, Any]:
    """Analyze network behavior for a specific BSSID."""
    async with _get_conn() as conn:
        # Get detection stats
        cursor = await conn.execute(
            """
            SELECT 
                COUNT(*) as total_detections,
                COUNT(DISTINCT latitude || ',' || longitude) as unique_locations,
                AVG(signal_strength_dbm) as avg_signal,
                COUNT(DISTINCT encryption_type) as encryption_changes,
                COUNT(DISTINCT ssid) as ssid_changes,
                COUNT(DISTINCT channel) as channel_changes
            FROM wifi_detections
            WHERE bssid = ?
            """,
            (bssid,),
        )

        detection_stats = dict(await cursor.fetchone())

        # Calculate mobility score (0-1 based on location diversity)
        mobility_score = min(
            1.0,
            detection_stats["unique_locations"]
            / max(1, detection_stats["total_detections"]),
        )

        # Calculate suspicion score based on various factors
        suspicion_score = 0.0

        # Check for excessive encryption changes
        if detection_stats["encryption_changes"] > 3:
            suspicion_score += 0.3

        # Check for excessive SSID changes
        if detection_stats["ssid_changes"] > 2:
            suspicion_score += 0.4

        # Check for excessive channel changes
        if detection_stats["channel_changes"] > 5:
            suspicion_score += 0.3

        suspicion_score = min(1.0, suspicion_score)

        return {
            "detection_stats": detection_stats,
            "mobility_score": mobility_score,
            "suspicion_score": suspicion_score,
        }


async def detect_suspicious_activities(scan_session_id: str) -> List[Dict[str, Any]]:
    """Detect suspicious activities in a scan session."""
    async with _get_conn() as conn:
        # Get all detections for this session
        cursor = await conn.execute(
            """
            SELECT bssid, ssid, encryption_type, signal_strength_dbm,
                   latitude, longitude, detection_timestamp
            FROM wifi_detections
            WHERE scan_session_id = ?
            ORDER BY detection_timestamp
            """,
            (scan_session_id,),
        )

        detections = [dict(row) for row in await cursor.fetchall()]

        suspicious_activities = []

        # Check for rapid signal strength changes (possible spoofing)
        bssid_signals = {}
        for detection in detections:
            bssid = detection["bssid"]
            signal = detection["signal_strength_dbm"]
            if bssid not in bssid_signals:
                bssid_signals[bssid] = []
            bssid_signals[bssid].append(signal)

        for bssid, signals in bssid_signals.items():
            if len(signals) > 1:
                signal_variance = max(signals) - min(signals)
                if signal_variance > 40:  # Large signal changes
                    suspicious_activities.append(
                        {
                            "activity_type": "signal_anomaly",
                            "severity": "medium",
                            "target_bssid": bssid,
                            "evidence": f"Signal variance: {signal_variance} dBm",
                        }
                    )

        # Check for networks with suspicious SSIDs
        for detection in detections:
            ssid = detection.get("ssid", "")
            if ssid and any(
                word in ssid.lower() for word in ["free", "wifi", "test", "default"]
            ):
                suspicious_activities.append(
                    {
                        "activity_type": "suspicious_ssid",
                        "severity": "low",
                        "target_bssid": detection["bssid"],
                        "target_ssid": ssid,
                        "evidence": f"Suspicious SSID: {ssid}",
                    }
                )

        return suspicious_activities


async def run_suspicious_activity_detection(scan_session_id: str) -> int:
    """Run suspicious activity detection and store results."""
    activities = await detect_suspicious_activities(scan_session_id)

    if activities:
        # Add required fields
        for activity in activities:
            activity.update(
                {
                    "scan_session_id": scan_session_id,
                    "description": f"Detected {activity['activity_type']}",
                    "detected_at": datetime.now().isoformat(),
                    "false_positive": False,
                    "analyst_notes": None,
                }
            )

        await save_suspicious_activities(activities)

    return len(activities)


async def migrate() -> None:
    """Ensure the database schema is up to date."""
    async with _get_conn():
        pass


# Export Functions
async def export_detections_to_csv(
    start_date: str | None = None,
    end_date: str | None = None,
    output_path: str | None = None,
) -> str:
    """Export detections to CSV format."""
    import csv
    import tempfile

    if not output_path:
        output_path = tempfile.mktemp(suffix=".csv")

    async with _get_conn() as conn:
        query = """
        SELECT 
            wd.detection_timestamp,
            wd.bssid,
            wd.ssid,
            wd.channel,
            wd.signal_strength_dbm,
            wd.encryption_type,
            wd.latitude,
            wd.longitude,
            ss.scan_type,
            ss.device_id
        FROM wifi_detections wd
        LEFT JOIN scan_sessions ss ON wd.scan_session_id = ss.id
        WHERE 1=1
        """
        params = []

        if start_date:
            query += " AND wd.detection_timestamp >= ?"
            params.append(start_date)

        if end_date:
            query += " AND wd.detection_timestamp < ?"
            params.append(end_date)

        query += " ORDER BY wd.detection_timestamp"

        cursor = await conn.execute(query, params)
        rows = await cursor.fetchall()

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "timestamp",
                "bssid",
                "ssid",
                "channel",
                "signal_strength",
                "encryption",
                "latitude",
                "longitude",
                "scan_type",
                "device_id",
            ]
        )
        writer.writerows(rows)

    return output_path


async def export_analytics_to_json(
    start_date: str | None = None,
    end_date: str | None = None,
    output_path: str | None = None,
) -> str:
    """Export analytics data to JSON format."""
    import json
    import tempfile

    if not output_path:
        output_path = tempfile.mktemp(suffix=".json")

    # Get analytics data
    analytics = await load_network_analytics(start=start_date, end=end_date)

    # Get detection stats
    detection_stats = await load_daily_detection_stats(start=start_date, end=end_date)

    # Get suspicious activities
    suspicious = await load_recent_suspicious(limit=1000)

    export_data = {
        "export_timestamp": datetime.now().isoformat(),
        "network_analytics": analytics,
        "detection_stats": detection_stats,
        "suspicious_activities": suspicious,
        "metadata": {
            "start_date": start_date,
            "end_date": end_date,
            "total_analytics_records": len(analytics),
            "total_detection_records": len(detection_stats),
        },
    }

    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(export_data, jsonfile, indent=2, default=str)

    return output_path


# Data Validation Functions
async def validate_detection_data() -> Dict[str, Any]:
    """Validate wifi detection data integrity."""
    validation_results = {"status": "valid", "errors": [], "warnings": [], "stats": {}}

    async with _get_conn() as conn:
        # Check for NULL BSSIDs
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM wifi_detections WHERE bssid IS NULL OR bssid = ''"
        )
        null_bssids = (await cursor.fetchone())[0]
        if null_bssids > 0:
            validation_results["errors"].append(
                f"Found {null_bssids} detections with NULL/empty BSSID"
            )

        # Check for invalid signal strengths
        cursor = await conn.execute(
            "SELECT COUNT(*) FROM wifi_detections WHERE signal_strength_dbm > 0 OR signal_strength_dbm < -120"
        )
        invalid_signals = (await cursor.fetchone())[0]
        if invalid_signals > 0:
            validation_results["warnings"].append(
                f"Found {invalid_signals} detections with unusual signal strength"
            )

        # Check for invalid coordinates
        cursor = await conn.execute(
            """
            SELECT COUNT(*) FROM wifi_detections 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            AND (latitude < -90 OR latitude > 90 OR longitude < -180 OR longitude > 180)
            """
        )
        invalid_coords = (await cursor.fetchone())[0]
        if invalid_coords > 0:
            validation_results["errors"].append(
                f"Found {invalid_coords} detections with invalid coordinates"
            )

        # Check for duplicate detections
        cursor = await conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT bssid, detection_timestamp, COUNT(*) as cnt
                FROM wifi_detections
                GROUP BY bssid, detection_timestamp
                HAVING cnt > 1
            )
            """
        )
        duplicates = (await cursor.fetchone())[0]
        if duplicates > 0:
            validation_results["warnings"].append(
                f"Found {duplicates} potential duplicate detections"
            )

        # Get general stats
        cursor = await conn.execute("SELECT COUNT(*) FROM wifi_detections")
        total_detections = (await cursor.fetchone())[0]

        cursor = await conn.execute("SELECT COUNT(DISTINCT bssid) FROM wifi_detections")
        unique_bssids = (await cursor.fetchone())[0]

        validation_results["stats"] = {
            "total_detections": total_detections,
            "unique_bssids": unique_bssids,
            "null_bssids": null_bssids,
            "invalid_signals": invalid_signals,
            "invalid_coordinates": invalid_coords,
            "duplicate_detections": duplicates,
        }

    if validation_results["errors"]:
        validation_results["status"] = "invalid"
    elif validation_results["warnings"]:
        validation_results["status"] = "warning"

    return validation_results


async def cleanup_duplicate_detections() -> int:
    """Remove duplicate detections, keeping the first occurrence."""
    async with _get_conn() as conn:
        # Find and remove duplicates
        cursor = await conn.execute(
            """
            DELETE FROM wifi_detections 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM wifi_detections 
                GROUP BY bssid, detection_timestamp, scan_session_id
            )
            """
        )

        deleted_count = cursor.rowcount
        await conn.commit()

        return deleted_count


async def repair_data_integrity() -> Dict[str, int]:
    """Repair data integrity issues."""
    repairs = {
        "null_bssids_removed": 0,
        "invalid_signals_fixed": 0,
        "invalid_coordinates_removed": 0,
        "duplicates_removed": 0,
    }

    async with _get_conn() as conn:
        # Remove detections with NULL/empty BSSID
        cursor = await conn.execute(
            "DELETE FROM wifi_detections WHERE bssid IS NULL OR bssid = ''"
        )
        repairs["null_bssids_removed"] = cursor.rowcount

        # Fix invalid signal strengths (clamp to reasonable range)
        cursor = await conn.execute(
            """
            UPDATE wifi_detections 
            SET signal_strength_dbm = CASE 
                WHEN signal_strength_dbm > 0 THEN -30
                WHEN signal_strength_dbm < -120 THEN -120
                ELSE signal_strength_dbm
            END
            WHERE signal_strength_dbm > 0 OR signal_strength_dbm < -120
            """
        )
        repairs["invalid_signals_fixed"] = cursor.rowcount

        # Remove detections with invalid coordinates
        cursor = await conn.execute(
            """
            UPDATE wifi_detections 
            SET latitude = NULL, longitude = NULL
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            AND (latitude < -90 OR latitude > 90 OR longitude < -180 OR longitude > 180)
            """
        )
        repairs["invalid_coordinates_removed"] = cursor.rowcount

        # Remove duplicates
        repairs["duplicates_removed"] = await cleanup_duplicate_detections()

        await conn.commit()

    return repairs


# Backup and Maintenance Functions
async def backup_database(backup_path: str) -> Dict[str, Any]:
    """Create a full database backup."""
    import shutil
    import os

    try:
        db_path = _db_path()
        if not os.path.exists(db_path):
            return {"status": "error", "message": "Database file not found"}

        # Create backup
        shutil.copy2(db_path, backup_path)

        # Verify backup
        backup_size = os.path.getsize(backup_path)
        original_size = os.path.getsize(db_path)

        return {
            "status": "success",
            "backup_path": backup_path,
            "original_size": original_size,
            "backup_size": backup_size,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat(),
        }


async def vacuum_database() -> Dict[str, Any]:
    """Vacuum the database to reclaim space and optimize performance."""
    async with _get_conn() as conn:
        # Get database size before vacuum
        cursor = await conn.execute("PRAGMA page_count")
        pages_before = (await cursor.fetchone())[0]

        cursor = await conn.execute("PRAGMA page_size")
        page_size = (await cursor.fetchone())[0]

        size_before = pages_before * page_size

        # Vacuum the database
        await conn.execute("VACUUM")

        # Get database size after vacuum
        cursor = await conn.execute("PRAGMA page_count")
        pages_after = (await cursor.fetchone())[0]

        size_after = pages_after * page_size

        return {
            "status": "success",
            "size_before": size_before,
            "size_after": size_after,
            "space_reclaimed": size_before - size_after,
            "timestamp": datetime.now().isoformat(),
        }


async def analyze_database_performance() -> Dict[str, Any]:
    """Analyze database performance and provide recommendations."""
    async with _get_conn() as conn:
        # Get table sizes
        cursor = await conn.execute(
            """
            SELECT name, 
                   (SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=m.name) as table_count
            FROM sqlite_master m WHERE type='table'
            """
        )
        tables = await cursor.fetchall()

        table_stats = {}
        for table_name, _ in tables:
            if table_name.startswith("sqlite_"):
                continue

            cursor = await conn.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = (await cursor.fetchone())[0]
            table_stats[table_name] = count

        # Get index usage
        cursor = await conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
        )
        indexes = [row[0] for row in await cursor.fetchall()]

        # Get database size
        cursor = await conn.execute("PRAGMA page_count")
        pages = (await cursor.fetchone())[0]

        cursor = await conn.execute("PRAGMA page_size")
        page_size = (await cursor.fetchone())[0]

        total_size = pages * page_size

        # Generate recommendations
        recommendations = []

        if table_stats.get("wifi_detections", 0) > 100000:
            recommendations.append(
                "Consider partitioning wifi_detections table by date"
            )

        if len(indexes) < 10:
            recommendations.append(
                "Consider adding more indexes for frequently queried columns"
            )

        if total_size > 1000000000:  # 1GB
            recommendations.append("Database is large, consider archiving old data")

        return {
            "table_stats": table_stats,
            "index_count": len(indexes),
            "total_size": total_size,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat(),
        }


async def cleanup_old_data(days_to_keep: int = 30) -> Dict[str, int]:
    """Remove old data based on retention policy."""
    cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()

    cleanup_stats = {
        "wifi_detections_removed": 0,
        "network_analytics_removed": 0,
        "suspicious_activities_removed": 0,
        "scan_sessions_removed": 0,
    }

    async with _get_conn() as conn:
        # Remove old wifi detections
        cursor = await conn.execute(
            "DELETE FROM wifi_detections WHERE detection_timestamp < ?", (cutoff_date,)
        )
        cleanup_stats["wifi_detections_removed"] = cursor.rowcount

        # Remove old network analytics
        cursor = await conn.execute(
            "DELETE FROM network_analytics WHERE analysis_date < ?",
            (cutoff_date[:10],),  # Just the date part
        )
        cleanup_stats["network_analytics_removed"] = cursor.rowcount

        # Remove old suspicious activities
        cursor = await conn.execute(
            "DELETE FROM suspicious_activities WHERE detected_at < ?", (cutoff_date,)
        )
        cleanup_stats["suspicious_activities_removed"] = cursor.rowcount

        # Remove old scan sessions
        cursor = await conn.execute(
            "DELETE FROM scan_sessions WHERE started_at < ?", (cutoff_date,)
        )
        cleanup_stats["scan_sessions_removed"] = cursor.rowcount

        await conn.commit()

    return cleanup_stats


async def schedule_maintenance_tasks() -> Dict[str, Any]:
    """Schedule regular maintenance tasks."""
    maintenance_results = {
        "vacuum_result": await vacuum_database(),
        "validation_result": await validate_detection_data(),
        "performance_analysis": await analyze_database_performance(),
        "cleanup_result": await cleanup_old_data(days_to_keep=90),
        "timestamp": datetime.now().isoformat(),
    }

    return maintenance_results
