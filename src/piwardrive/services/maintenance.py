"""Database maintenance and optimization utilities.

This module provides automated database maintenance functionality including
cleanup operations, optimization routines, archival processes, and performance
monitoring for the PiWardrive database systems.
"""
from __future__ import annotations

import asyncio
import csv
import json
import logging
import os
import shutil
from dataclasses import asdict
from datetime import datetime, timedelta

from piwardrive import config, r_integration
from piwardrive.database_service import db_service
from piwardrive.notifications import NotificationManager
from piwardrive.persistence import _db_path, _get_conn, backup_database, shutdown_pool
from piwardrive.services import db_monitor

logger = logging.getLogger(__name__)


async def optimize_database_indexes() -> None:
    """Run ANALYZE and REINDEX on the active database."""
    async with _get_conn() as conn:
        await conn.execute("ANALYZE")
        await conn.execute("REINDEX")
        await conn.commit()


async def vacuum_database() -> None:
    """Run VACUUM on the active database."""
    await db_service.vacuum()


async def archive_old_data(days: int = 30) -> None:
    """Move records older than ``days`` into archive tables."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    tables: dict[str, str] = {
        "wifi_detections": "detection_timestamp",
        "bluetooth_detections": "detection_timestamp",
        "cellular_detections": "detection_timestamp",
        "gps_tracks": "timestamp",
    }
    async with _get_conn() as conn:
        for table, ts_col in tables.items():
            archive = f"{table}_archive"
            await conn.execute(
                f"CREATE TABLE IF NOT EXISTS {archive} AS SELECT * FROM {table} WHERE 0"
            )
            await conn.execute(
                f"INSERT INTO {archive} SELECT * FROM {table} WHERE {ts_col} < ?",
                (cutoff,),
            )
            await conn.execute(
                f"DELETE FROM {table} WHERE {ts_col} < ?",
                (cutoff,),
            )
        await conn.commit()


async def generate_health_reports() -> None:
    """Write daily health summary reports to the configured reports directory."""
    records = await db_service.load_recent_health(10000)
    if not records:
        return
    cfg = config.AppConfig.load()
    os.makedirs(cfg.reports_dir, exist_ok=True)
    date = datetime.utcnow().strftime("%Y%m%d")
    csv_path = os.path.join(cfg.reports_dir, f"health_{date}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "timestamp",
                "cpu_temp",
                "cpu_percent",
                "memory_percent",
                "disk_percent",
            ],
        )
        writer.writeheader()
        writer.writerows(asdict(r) for r in records)

    plot_path = os.path.join(cfg.reports_dir, f"health_{date}.png")
    _result = await asyncio.to_thread(r_integration.health_summary, csv_path, plot_path)
    json_path = os.path.join(cfg.reports_dir, f"health_{date}.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh)


async def check_database_health(nm: NotificationManager | None = None) -> bool:
    """Verify database connectivity and optionally send alerts."""
    healthy = await db_monitor.health_check()
    if not healthy:
        logger.warning("Database health check failed")
        if nm is not None:
            await nm._post({"event": "database_unhealthy"})
    return healthy


async def automatic_backup(dest: str | None = None) -> str:
    """Create a backup of the database to ``dest`` and return the path."""
    if dest is None:
        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        dest = os.path.join(config.CONFIG_DIR, f"backup_{ts}.db")
    await backup_database(dest)
    return dest


async def restore_backup(src: str) -> None:
    """Restore the database from ``src``."""
    await shutdown_pool()
    shutil.copy2(src, _db_path())


__all__ = [
    "optimize_database_indexes",
    "vacuum_database",
    "archive_old_data",
    "generate_health_reports",
    "check_database_health",
    "automatic_backup",
    "restore_backup",
]
