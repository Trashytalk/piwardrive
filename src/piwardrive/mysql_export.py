from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence

import aiomysql

from .persistence import HealthRecord


@dataclass
class MySQLConfig:
    """Connection information for a MySQL or MariaDB server."""

    host: str = "localhost"
    port: int = 3306
    user: str = "piwardrive"
    password: str = ""
    database: str = "piwardrive"


async def connect(config: MySQLConfig) -> aiomysql.Connection:
    """Return an ``aiomysql`` connection using ``config``."""

    return await aiomysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        db=config.database,
        autocommit=False,
    )


async def init_schema(conn: aiomysql.Connection) -> None:
    """Create database tables if they do not exist."""

    async with conn.cursor() as cur:
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS health_records (
                timestamp VARCHAR(32) PRIMARY KEY,
                cpu_temp DOUBLE,
                cpu_percent DOUBLE,
                memory_percent DOUBLE,
                disk_percent DOUBLE
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_health_time ON health_records(timestamp)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS wifi_observations (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                bssid VARCHAR(32),
                ssid VARCHAR(255),
                lat DOUBLE,
                lon DOUBLE,
                timestamp BIGINT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_bssid ON wifi_observations(bssid)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_time ON wifi_observations(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_loc ON wifi_observations(lat, lon)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bluetooth_observations (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(64),
                name VARCHAR(255),
                lat DOUBLE,
                lon DOUBLE,
                timestamp BIGINT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_addr ON bluetooth_observations(address)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_time ON bluetooth_observations(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_loc ON bluetooth_observations(lat, lon)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tower_observations (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                tower_id VARCHAR(32),
                rssi VARCHAR(32),
                lat DOUBLE,
                lon DOUBLE,
                timestamp BIGINT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tower_id ON tower_observations(tower_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tower_time ON tower_observations(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tower_loc ON tower_observations(lat, lon)"
        )
    await conn.commit()


async def insert_health_records(
    conn: aiomysql.Connection, records: Iterable[HealthRecord]
) -> None:
    """Insert ``records`` into ``health_records``."""

    rows = [
        (
            r.timestamp,
            r.cpu_temp,
            r.cpu_percent,
            r.memory_percent,
            r.disk_percent,
        )
        for r in records
    ]
    if not rows:
        return
    async with conn.cursor() as cur:
        await cur.executemany(
            """
            INSERT INTO health_records
            (timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )
    await conn.commit()


async def insert_wifi_observations(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    """Insert Wi-Fi observation ``records``."""

    rows: List[Sequence[Any]] = [
        (
            r.get("bssid"),
            r.get("ssid"),
            r.get("lat"),
            r.get("lon"),
            r.get("timestamp") or r.get("last_time"),
        )
        for r in records
    ]
    if not rows:
        return
    async with conn.cursor() as cur:
        await cur.executemany(
            """
            INSERT INTO wifi_observations (bssid, ssid, lat, lon, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )
    await conn.commit()


async def export_data(
    config: MySQLConfig,
    health: Iterable[HealthRecord],
    wifi: Iterable[dict[str, Any]],
) -> None:
    """Create schema and export ``health`` and ``wifi`` records."""

    conn = await connect(config)
    try:
        await init_schema(conn)
        await insert_health_records(conn, health)
        await insert_wifi_observations(conn, wifi)
    finally:
        conn.close()
        await conn.wait_closed()
