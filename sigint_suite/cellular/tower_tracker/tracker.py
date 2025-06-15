import sqlite3
import time
from typing import Optional, Dict, List


class TowerTracker:
    """Maintain a database of observed cell towers."""

    def __init__(self, db_path: str = "towers.db") -> None:
        self.conn = sqlite3.connect(db_path)
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

        cur = self.conn.execute(
            "SELECT tower_id, lat, lon, last_seen FROM towers"
        )
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
