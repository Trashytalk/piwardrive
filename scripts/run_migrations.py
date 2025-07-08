#!/usr/bin/env python3
"""Comprehensive migration runner for PiWardrive database."""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
:
try:
    from piwardrive.core.persistence import _get_conn
from piwardrive.migrations.runner import (
        run_pending_migrations,)
        check_migration_statusexcept ImportError as e:print(f"Import error: {e}")
print("Installing dependencies...")import subprocesssubprocess.run([sys.executable, "-m", "pip", "install", "aiosqlite"])
from piwardrive.core.persistence import _get_conn
from piwardrive.migrations.runner import (
        run_pending_migrations,)
        check_migration_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
async def run_comprehensive_migration():"""Run comprehensive database migration."""
    logger.info("Starting comprehensive database migration...")

    async with _get_conn() as conn:
        # Check current migration status
        status = await check_migration_status(conn)logger.info(f"Migration Status:")
        logger.info(f"  Applied: {status['applied']}")
        logger.info(f"  Available: {status['available']}")
        logger.info(f"  Pending: {status['pending']}")
if status['unknown']:logger.warning(f"  Unknown migrations in database: {status['unknown']}")
if not status['pending']:logger.info("✅ All migrations are already applied")
            return 0
# Run pending migrationslogger.info(f"Applying {len(status['pending'])} pending migrations...")
        applied_count = await run_pending_migrations(conn)logger.info(f"✅ Successfully applied {applied_count} migrations")
        return applied_count
async def main():"""Main migration function."""
    print("=== PiWardrive Database Migration ===\n")

    try:
        applied_count = await run_comprehensive_migration()
if applied_count > 0:print(f"✅ Successfully applied {applied_count} migrations")else:print("✅ Database is already up to date")print("\n=== Migration completed successfully! ===")
except Exception as e:print(f"❌ Migration failed: {e}")
import traceback
        traceback.print_exc()
sys.exit(1)if __name__ == "__main__":
    asyncio.run(main())
