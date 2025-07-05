#!/usr/bin/env python3
"""
Simple database migration status checker.
"""

import asyncio
import logging
import os
import sqlite3
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_database_status(db_path: str) -> Dict[str, Any]:
    """Check current database status without complex imports."""
    status = {
        "database_path": db_path,
        "database_exists": os.path.exists(db_path),
        "schema_version": 0,
        "tables_present": [],
        "indexes_present": [],
        "migration_table_exists": False,
        "applied_migrations": [],
        "recommendations": []
    }

    if not status["database_exists"]:
        status["recommendations"].append({
            "type": "critical",
            "description": "Database does not exist - needs initialization"
        })
        return status

    try:
        # Use synchronous sqlite3 for simplicity
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Check for migration table
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='schema_migrations'
        """)
        if cursor.fetchone():
            status["migration_table_exists"] = True

            # Get applied migrations
            cursor.execute("SELECT version FROM schema_migrations ORDER BY version")
            status["applied_migrations"] = [row[0] for row in cursor.fetchall()]

        # Check schema version
        try:
            cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
            result = cursor.fetchone()
            status["schema_version"] = result[0] if result else 0
        except sqlite3.OperationalError:
            status["schema_version"] = 0

        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        status["tables_present"] = [row[0] for row in cursor.fetchall()]

        # Get all indexes
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        status["indexes_present"] = [row[0] for row in cursor.fetchall()]

        # Check for expected tables
        expected_tables = [
            "scan_sessions", "wifi_detections", "bluetooth_detections",
            "cellular_detections", "gps_tracks", "network_fingerprints",
            "suspicious_activities", "network_analytics"
        ]

        missing_tables = [t for t in expected_tables if t not in status["tables_present"]]
        if missing_tables:
            status["recommendations"].append({
                "type": "critical",
                "description": f"Missing tables: {', '.join(missing_tables)}"
            })

        # Check for critical indexes
        critical_indexes = [
            "idx_wifi_detections_bssid", "idx_wifi_detections_time",
            "idx_wifi_detections_location", "idx_bt_detections_mac",
            "idx_cellular_detections_cell", "idx_gps_tracks_location"
        ]

        missing_indexes = [i for i in critical_indexes if i not in status["indexes_present"]]
        if missing_indexes:
            status["recommendations"].append({
                "type": "performance",
                "description": f"Missing indexes: {', '.join(missing_indexes)}"
            })

        conn.close()

    except Exception as e:
        logger.error(f"Error checking database: {e}")
        status["error"] = str(e)

    return status

async def main():
    """Main function to check database status."""
    print("=== PiWardrive Database Status Check ===\n")

    # Try to find the database
    possible_paths = [
        os.path.expanduser("~/.config/piwardrive/app.db"),
        os.path.join(os.getcwd(), "app.db"),
        os.path.join(os.getcwd(), "data", "app.db")
    ]

    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break

    if not db_path:
        db_path = possible_paths[0]  # Use default location

    status = await check_database_status(db_path)

    print(f"Database Path: {status['database_path']}")
    print(f"Database Exists: {status['database_exists']}")
    print(f"Schema Version: {status['schema_version']}")
    print(f"Migration Table Exists: {status['migration_table_exists']}")

    if status["applied_migrations"]:
        print(f"Applied Migrations: {status['applied_migrations']}")

    print(f"\nTables Present ({len(status['tables_present'])}): {',
        '.join(status['tables_present'])}")
    print(f"Indexes Present ({len(status['indexes_present'])}): {',
        '.join(status['indexes_present'])}")

    if status["recommendations"]:
        print(f"\n=== RECOMMENDATIONS ===")
        for rec in status["recommendations"]:
            icon = "🔴" if rec["type"] == "critical" else "🟡"
            print(f"{icon} {rec['description']}")

    if "error" in status:
        print(f"\n❌ ERROR: {status['error']}")

if __name__ == "__main__":
    asyncio.run(main())
