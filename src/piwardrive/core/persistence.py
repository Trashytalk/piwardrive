"""Simple persistence helpers using SQLite."""

from __future__ import annotations

import asyncio
import hashlib
import os
import sqlite3
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any, AsyncIterator, Awaitable, Callable, List, Optional

import aiosqlite

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
    async with _get_conn() as conn:
        await conn.execute("VACUUM")
        await conn.commit()


async def migrate() -> None:
    """Ensure the database schema is up to date."""
    async with _get_conn():
        pass
