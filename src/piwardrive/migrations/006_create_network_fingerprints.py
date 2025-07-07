"""Migration 006: Create network fingerprints table."""

from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create network_fingerprints table."""

    version = 6

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS network_fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT NOT NULL,
                ssid TEXT,
                fingerprint_hash TEXT NOT NULL,
                confidence_score REAL,
                device_model TEXT,
                firmware_version TEXT,
                characteristics TEXT,
                classification TEXT,
                risk_level TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_fingerprints_bssid ON network_fingerprints(bssid)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_fingerprints_hash ON network_fingerprints(fingerprint_hash)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_fingerprints_classification ON network_fingerprints(classification)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_fingerprints_classification")
        await conn.execute("DROP INDEX IF EXISTS idx_fingerprints_hash")
        await conn.execute("DROP INDEX IF EXISTS idx_fingerprints_bssid")
        await conn.execute("DROP TABLE IF EXISTS network_fingerprints")
        await conn.commit()
