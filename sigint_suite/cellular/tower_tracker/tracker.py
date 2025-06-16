import sqlite3
import time
from typing import Dict, List, Optional


class TowerTracker:
    """Maintain a database of observed cell towers."""

    def __init__(self, db_path: str = "towers.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS towers (
                tower_id TEXT PRIMARY KEY,
                lat REAL,
                lon REAL,
                last_seen INTEGER
            )
            """
        )
        self.conn.execute(
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
        self.conn.execute(
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
        self.conn.commit()

    def update_tower(
        self, tower_id: str, lat: float, lon: float, last_seen: Optional[int] = None
    ) -> None:
        """Insert or update ``tower_id`` with location and timestamp."""

        if last_seen is None:
            last_seen = int(time.time())
        self.conn.execute(
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
        self.conn.commit()

    def get_tower(self, tower_id: str) -> Optional[Dict[str, float]]:
        """Return tower details or ``None`` if not found."""

        cur = self.conn.execute(
            "SELECT tower_id, lat, lon, last_seen FROM towers WHERE tower_id=?",
            (tower_id,),
        )
        row = cur.fetchone()
        if row:
            return {
                "tower_id": row[0],
                "lat": row[1],
                "lon": row[2],
                "last_seen": row[3],
            }
        return None

    def all_towers(self) -> List[Dict[str, float]]:
        """Return all tracked towers."""

        cur = self.conn.execute("SELECT tower_id, lat, lon, last_seen FROM towers")
        return [
            {
                "tower_id": row[0],
                "lat": row[1],
                "lon": row[2],
                "last_seen": row[3],
            }
            for row in cur.fetchall()
        ]

    def close(self) -> None:
        """Close the database connection."""

        self.conn.close()

    # ------------------------------------------------------------------
    # Wi-Fi helpers
    # ------------------------------------------------------------------

    def log_wifi(
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
        self.conn.execute(
            """
            INSERT INTO wifi_observations (bssid, ssid, lat, lon, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (bssid, ssid, lat, lon, timestamp),
        )
        self.conn.commit()

    def wifi_history(self, bssid: str) -> List[Dict[str, float]]:
        """Return all Wi-Fi records for ``bssid`` sorted by newest first."""

        cur = self.conn.execute(
            """
            SELECT bssid, ssid, lat, lon, timestamp
            FROM wifi_observations
            WHERE bssid=? ORDER BY timestamp DESC
            """,
            (bssid,),
        )
        return [dict(row) for row in cur.fetchall()]

    # ------------------------------------------------------------------
    # Bluetooth helpers
    # ------------------------------------------------------------------

    def log_bluetooth(
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
        self.conn.execute(
            """
            INSERT INTO bluetooth_observations (address, name, lat, lon, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (address, name, lat, lon, timestamp),
        )
        self.conn.commit()

    def bluetooth_history(self, address: str) -> List[Dict[str, float]]:
        """Return all Bluetooth records for ``address`` sorted by newest first."""

        cur = self.conn.execute(
            """
            SELECT address, name, lat, lon, timestamp
            FROM bluetooth_observations
            WHERE address=? ORDER BY timestamp DESC
            """,
            (address,),
        )
        return [dict(row) for row in cur.fetchall()]
