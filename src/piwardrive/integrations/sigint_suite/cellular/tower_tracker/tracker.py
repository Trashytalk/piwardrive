"""Module tracker."""
import time
from typing import Dict, List, Optional
from types import TracebackType

import aiosqlite


class TowerTracker:
    """Maintain a database of observed cell towers."""

    def __init__(self, db_path: str = "towers.db") -> None:
        self.db_path = db_path
        self.conn: aiosqlite.Connection | None = None

    async def __aenter__(self) -> "TowerTracker":
        """Allow usage as an async context manager."""
        await self._get_conn()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Close the underlying database connection."""
        await self.close()

    async def _get_conn(self) -> aiosqlite.Connection:
        if self.conn is None:
            self.conn = await aiosqlite.connect(self.db_path)
            self.conn.row_factory = aiosqlite.Row
            await self._init_db()
        return self.conn

    async def _init_db(self) -> None:
        assert self.conn is not None
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS towers (
                tower_id TEXT PRIMARY KEY,
                lat REAL,
                lon REAL,
                last_seen INTEGER
            )
            """
        )
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS wifi_observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT,
                ssid TEXT,
                lat REAL,
                lon REAL,
                timestamp INTEGER
            )
            """
        )
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bluetooth_observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT,
                name TEXT,
                lat REAL,
                lon REAL,
                timestamp INTEGER
            )
            """
        )
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tower_observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tower_id TEXT,
                rssi TEXT,
                lat REAL,
                lon REAL,
                timestamp INTEGER
            )
            """
        )
        await self.conn.commit()

    async def update_tower(
        self, tower_id: str, lat: float, lon: float, last_seen: Optional[int] = None
    ) -> None:
        """Insert or update ``tower_id`` with location and timestamp."""
        if last_seen is None:
            last_seen = int(time.time())
        conn = await self._get_conn()
        await conn.execute(
            """
            INSERT INTO towers (tower_id, lat, lon, last_seen)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(tower_id) DO UPDATE SET
                lat=excluded.lat,
                lon=excluded.lon,
                last_seen=excluded.last_seen
            """,
            (tower_id, lat, lon, last_seen),
        )
        await conn.commit()

    async def get_tower(self, tower_id: str) -> Optional[Dict[str, float]]:
        """Return tower details or ``None`` if not found."""
        conn = await self._get_conn()
        cur = await conn.execute(
            "SELECT tower_id, lat, lon, last_seen FROM towers WHERE tower_id=?",
            (tower_id,),
        )
        row = await cur.fetchone()
        if row:
            return {
                "tower_id": row[0],
                "lat": row[1],
                "lon": row[2],
                "last_seen": row[3],
            }
        return None

    async def all_towers(self) -> List[Dict[str, float]]:
        """Return all tracked towers."""
        conn = await self._get_conn()
        cur = await conn.execute(
            "SELECT tower_id, lat, lon, last_seen FROM towers"
        )
        rows = await cur.fetchall()
        return [dict(row) for row in rows]

    async def close(self) -> None:
        """Close the database connection."""
        if self.conn is not None:
            await self.conn.close()

    # ------------------------------------------------------------------
    # Cellular tower helpers
    # ------------------------------------------------------------------

    async def log_tower(
        self,
        tower_id: str,
        rssi: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        timestamp: Optional[int] = None,
    ) -> None:
        """Persist a cell tower observation."""
        if timestamp is None:
            timestamp = int(time.time())
        conn = await self._get_conn()
        await conn.execute(
            """
            INSERT INTO tower_observations (tower_id, rssi, lat, lon, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (tower_id, rssi, lat, lon, timestamp),
        )
        await conn.commit()

    async def tower_history(self, tower_id: str) -> List[Dict[str, float]]:
        """Return all records for ``tower_id`` sorted by newest first."""
        conn = await self._get_conn()
        cur = await conn.execute(
            """
            SELECT tower_id, rssi, lat, lon, timestamp
            FROM tower_observations
            WHERE tower_id=? ORDER BY timestamp DESC
            """,
            (tower_id,),
        )
        rows = await cur.fetchall()
        return [dict(row) for row in rows]

    # ------------------------------------------------------------------
    # Wi-Fi helpers
    # ------------------------------------------------------------------

    async def log_wifi(
        self,
        bssid: str,
        ssid: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        timestamp: Optional[int] = None,
    ) -> None:
        """Persist a Wi-Fi observation."""
        if timestamp is None:
            timestamp = int(time.time())
        conn = await self._get_conn()
        await conn.execute(
            """
            INSERT INTO wifi_observations (bssid, ssid, lat, lon, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (bssid, ssid, lat, lon, timestamp),
        )
        await conn.commit()

    async def wifi_history(self, bssid: str) -> List[Dict[str, float]]:
        """Return all Wi-Fi records for ``bssid`` sorted by newest first."""
        conn = await self._get_conn()
        cur = await conn.execute(
            """
            SELECT bssid, ssid, lat, lon, timestamp
            FROM wifi_observations
            WHERE bssid=? ORDER BY timestamp DESC
            """,
            (bssid,),
        )
        rows = await cur.fetchall()
        return [dict(row) for row in rows]

    # ------------------------------------------------------------------
    # Bluetooth helpers
    # ------------------------------------------------------------------

    async def log_bluetooth(
        self,
        address: str,
        name: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        timestamp: Optional[int] = None,
    ) -> None:
        """Persist a Bluetooth observation."""
        if timestamp is None:
            timestamp = int(time.time())
        conn = await self._get_conn()
        await conn.execute(
            """
            INSERT INTO bluetooth_observations (address, name, lat, lon, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (address, name, lat, lon, timestamp),
        )
        await conn.commit()

    async def bluetooth_history(self, address: str) -> List[Dict[str, float]]:
        """Return all Bluetooth records for ``address`` sorted by newest first."""
        conn = await self._get_conn()
        cur = await conn.execute(
            """
            SELECT address, name, lat, lon, timestamp
            FROM bluetooth_observations
            WHERE address=? ORDER BY timestamp DESC
            """,
            (address,),
        )
        rows = await cur.fetchall()
        return [dict(row) for row in rows]
