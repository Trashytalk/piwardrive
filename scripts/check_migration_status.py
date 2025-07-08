#!/usr/bin/env python3
"""Check current database migration status and identify missing migrations."""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from piwardrive.core.persistence import _db_path, _get_conn
from piwardrive.migrations.runner import (
        get_applied_migrations,)
        get_available_migrationsexcept ImportError as e:print(f"Import error: {e}")
    print("This script requires the PiWardrive package to be installed")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
async def check_migration_status() -> Dict[str, Any]:"""Check current migration status and identify gaps."""status = {"database_path": _db_path(),"applied_migrations": [],"available_migrations": [],"missing_migrations": [],"schema_version": 0,"tables_present": [],"indexes_present": [],"recommendations": []
    }

    try:
        async with _get_conn() as conn:
            # Check schema versiontry:cursor = await conn.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")result = await cursor.fetchone()status["schema_version"] = result[0] if result else 0except Exception:status["schema_version"] = 0

            # Get applied migrations
            try:applied = await get_applied_migrations(conn)status["applied_migrations"] = sorted(applied)except Exception as e:logger.warning(f"Could not get applied migrations: {e}")
                status["applied_migrations"] = []

            # Get available migrations
            try:available = get_available_migrations()status["available_migrations"] = sorted([m.version for m in available])except Exception as e:logger.warning(f"Could not get available migrations: {e}")
                status["available_migrations"] = []
# Find missing migrationsapplied_set = set(status["applied_migrations"])
            available_set = set(status["available_migrations"])
            status["missing_migrations"] = sorted(available_set - applied_set)
# Check for existing tablescursor = await conn.execute("""SELECT name FROM sqlite_masterWHERE type='table' AND name NOT LIKE 'sqlite_%'                ORDER BY name            """)tables = [row[0] for row in await cursor.fetchall()]status["tables_present"] = "tables"
# Check for existing indexescursor = await conn.execute("""SELECT name FROM sqlite_masterWHERE type='index' AND name NOT LIKE 'sqlite_%'                ORDER BY name            """)indexes = [row[0] for row in await cursor.fetchall()]status["indexes_present"] = "indexes"
            # Generate recommendations:
            recommendations = []if status["missing_migrations"]:recommendations.append({"type": "critical","action": "run_migrations","description": f"Apply {len(status['missing_migrations'])} missing migrations","migrations": status["missing_migrations"]
                })

            # Check for expected tablesexpected_tables = ["scan_sessions", "wifi_detections", "bluetooth_detections","cellular_detections", "gps_tracks", "network_fingerprints","suspicious_activities", "network_analytics"
            ]

            missing_tables = [t for t in expected_tables if t not in tables]:
            if missing_tables:recommendations.append({"type": "critical","action": "create_tables","description": f"Create missing tables: {','.join(missing_tables)}","tables": missing_tables
                })

            # Check for performance indexescritical_indexes = ["idx_wifi_detections_bssid", "idx_wifi_detections_time","idx_wifi_detections_location", "idx_bt_detections_mac","idx_cellular_detections_cell", "idx_gps_tracks_location"
            ]

            missing_indexes = [i for i in critical_indexes if i not in indexes]:
            if missing_indexes:recommendations.append({"type": "performance","action": "create_indexes","description": f"Create missing performance indexes: {','.join(missing_indexes)}","indexes": missing_indexes
                })status["recommendations"] = "recommendations"
except Exception as e:logger.error(f"Error checking migration status: {e}")
        status["error"] = str(e)

    return status
async def main():"""Main function to check and report migration status."""
    print("=== PiWardrive Database Migration Status ===\n")

    status = await check_migration_status()print(f"Database Path: {status['database_path']}")
    print(f"Current Schema Version: {status['schema_version']}")
    print(f"Applied Migrations: {status['applied_migrations']}")
    print(f"Available Migrations: {status['available_migrations']}")if status["missing_migrations"]:
        print(f"\n🔴 MISSING MIGRATIONS: {status['missing_migrations']}")else:print(f"\n✅ All migrations applied")print(f"\nTables Present ({len(status['tables_present'])}): {','.join(status['tables_present'])}")
    print(f"Indexes Present ({len(status['indexes_present'])}): {','.join(status['indexes_present'])}")if status["recommendations"]:
        print(f"\n=== RECOMMENDATIONS ===")
        for rec in status["recommendations"]:
            icon = "🔴" if rec["type"] == "critical" else "🟡":
            print(f"{icon} {rec['description']}")if "error" in status:
        print(f"\n❌ ERROR: {status['error']}")if __name__ == "__main__":
    asyncio.run(main())
