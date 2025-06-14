import os
import sqlite3
from typing import Iterable, Mapping, Any

from utils import now_timestamp

DEFAULT_DB_PATH = os.path.join(os.path.expanduser("~"), ".piwardrive", "history.db")


def get_connection(path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection with :class:`sqlite3.Row` rows."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create history tables if missing."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ap_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            bssid TEXT,
            ssid TEXT,
            lat REAL,
            lon REAL,
            rssi INTEGER
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            cpu_temp REAL,
            mem_pct REAL,
            disk_pct REAL,
            handshake_count INTEGER,
            lat REAL,
            lon REAL
        )
        """
    )
    conn.commit()


def ingest_ap_data(conn: sqlite3.Connection, aps: Iterable[Mapping[str, Any]]) -> None:
    """Insert access point records into ``ap_data``."""
    for ap in aps:
        gps = ap.get("gps-info")
        lat = gps[0] if gps and len(gps) >= 2 else None
        lon = gps[1] if gps and len(gps) >= 2 else None
        conn.execute(
            """
            INSERT INTO ap_data (ts, bssid, ssid, lat, lon, rssi)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                now_timestamp(),
                ap.get("bssid"),
                ap.get("ssid"),
                lat,
                lon,
                ap.get("signal"),
            ),
        )
    conn.commit()


def ingest_metrics(conn: sqlite3.Connection, data: Mapping[str, Any]) -> None:
    """Insert a metrics snapshot into ``metrics``."""
    conn.execute(
        """
        INSERT INTO metrics (
            ts, cpu_temp, mem_pct, disk_pct, handshake_count, lat, lon
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            now_timestamp(),
            data.get("cpu_temp"),
            data.get("mem_pct"),
            data.get("disk_pct"),
            data.get("handshake_count"),
            data.get("lat"),
            data.get("lon"),
        ),
    )
    conn.commit()


def query_recent_aps(conn: sqlite3.Connection, limit: int = 100) -> list[sqlite3.Row]:
    """Return recent access point entries ordered by newest first."""
    cur = conn.execute(
        "SELECT * FROM ap_data ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()


def query_recent_metrics(
    conn: sqlite3.Connection, limit: int = 100
) -> list[sqlite3.Row]:
    """Return recent metrics entries ordered by newest first."""
    cur = conn.execute(
        "SELECT * FROM metrics ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()
