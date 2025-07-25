# Database Migration Guide

The new persistence layer introduces connection pooling and optional sharding.
Existing databases remain compatible.

## Connection Pool Migration

`DatabaseManager` now manages pooled adapters for SQLite, PostgreSQL and MySQL.
Existing code using the old single-connection pattern should simply call
``DatabaseManager.connect()`` once during startup and ``close()`` on shutdown.
Adapters will handle connection reuse transparently. Metrics are available via
``DatabaseManager.get_metrics()`` for monitoring pool health.

## Migrating Existing Installations

1. Stop all running PiWardrive services to flush buffers:
   ```bash
   python -m piwardrive.persistence --shutdown
   ```
   or terminate the application cleanly.

2. If sharding is enabled via `PW_DB_SHARDS`, rename your current
   `app.db` to `app_0.db` in the configuration directory.

3. Restart the application. The schema will be migrated automatically on
   first connection.

## Backups

Use `piwardrive.persistence.backup_database(path)` to create a backup of the
active shard. This uses SQLite's online backup and can be run while the
application is running.
