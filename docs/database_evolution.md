# Database Schema Evolution and Migration Guide

This guide covers database schema management, migration strategies, and best practices for evolving PiWardrive's database schema safely.

## Overview

PiWardrive uses SQLite as its primary database with support for schema migrations to handle database evolution. The migration system ensures:
- **Zero-downtime upgrades**: Seamless schema updates without data loss
- **Backward compatibility**: Support for rollback scenarios
- **Data integrity**: Validation and constraint enforcement
- **Performance optimization**: Index management and query optimization

## Current Database Schema

### Core Tables

#### health_records
Primary table for storing device health and telemetry data:

```sql
CREATE TABLE health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cpu_temp REAL,
    cpu_percent REAL,
    memory_percent REAL,
    disk_percent REAL,
    network_rx_bytes INTEGER,
    network_tx_bytes INTEGER,
    gps_lat REAL,
    gps_lon REAL,
    gps_accuracy REAL,
    wifi_networks_count INTEGER,
    bluetooth_devices_count INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### wifi_networks
WiFi network scan results:

```sql
CREATE TABLE wifi_networks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bssid TEXT NOT NULL,
    ssid TEXT,
    frequency INTEGER,
    signal_strength INTEGER,
    encryption TEXT,
    channel INTEGER,
    vendor TEXT,
    first_seen TEXT,
    last_seen TEXT,
    gps_lat REAL,
    gps_lon REAL,
    gps_accuracy REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### bluetooth_devices
Bluetooth device discovery results:

```sql
CREATE TABLE bluetooth_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    name TEXT,
    device_type TEXT,
    rssi INTEGER,
    manufacturer TEXT,
    services TEXT, -- JSON array of service UUIDs
    first_seen TEXT,
    last_seen TEXT,
    gps_lat REAL,
    gps_lon REAL,
    gps_accuracy REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### configuration
Application configuration storage:

```sql
CREATE TABLE configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    type TEXT DEFAULT 'string',
    description TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes

Performance-critical indexes:

```sql
-- Health records indexes
CREATE INDEX idx_health_timestamp ON health_records(timestamp);
CREATE INDEX idx_health_created_at ON health_records(created_at);

-- WiFi networks indexes
CREATE INDEX idx_wifi_bssid ON wifi_networks(bssid);
CREATE INDEX idx_wifi_ssid ON wifi_networks(ssid);
CREATE INDEX idx_wifi_last_seen ON wifi_networks(last_seen);
CREATE INDEX idx_wifi_location ON wifi_networks(gps_lat, gps_lon);

-- Bluetooth devices indexes
CREATE INDEX idx_bt_address ON bluetooth_devices(address);
CREATE INDEX idx_bt_name ON bluetooth_devices(name);
CREATE INDEX idx_bt_last_seen ON bluetooth_devices(last_seen);
CREATE INDEX idx_bt_location ON bluetooth_devices(gps_lat, gps_lon);

-- Configuration indexes
CREATE INDEX idx_config_key ON configuration(key);
```

## Migration System

### Migration Framework

PiWardrive uses a migration system based on numbered migration files:

```python
# src/piwardrive/migrations/migration_001.py
from typing import List
from piwardrive.db import DatabaseMigration

class Migration001(DatabaseMigration):
    """Add vendor column to wifi_networks table."""
    
    version = 1
    description = "Add vendor column to wifi_networks table"
    
    def up(self, cursor) -> List[str]:
        """Apply migration."""
        return [
            "ALTER TABLE wifi_networks ADD COLUMN vendor TEXT",
            "CREATE INDEX idx_wifi_vendor ON wifi_networks(vendor)",
        ]
    
    def down(self, cursor) -> List[str]:
        """Rollback migration."""
        return [
            "DROP INDEX IF EXISTS idx_wifi_vendor",
            "ALTER TABLE wifi_networks DROP COLUMN vendor",
        ]
    
    def validate(self, cursor) -> bool:
        """Validate migration was applied correctly."""
        cursor.execute("PRAGMA table_info(wifi_networks)")
        columns = [row[1] for row in cursor.fetchall()]
        return "vendor" in columns
```

### Migration Runner

The migration runner handles applying migrations:

```python
# src/piwardrive/db/migrations.py
import asyncio
import logging
from typing import List, Type
from pathlib import Path

class MigrationRunner:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    async def get_current_version(self) -> int:
        """Get current database schema version."""
        async with aiosqlite.connect(self.db_path) as conn:
            try:
                cursor = await conn.execute(
                    "SELECT version FROM schema_version ORDER BY version DESC LIMIT 1"
                )
                row = await cursor.fetchone()
                return row[0] if row else 0
            except sqlite3.OperationalError:
                # schema_version table doesn't exist
                return 0
    
    async def apply_migrations(self, target_version: int = None) -> None:
        """Apply migrations up to target version."""
        current_version = await self.get_current_version()
        migrations = self.load_migrations()
        
        if target_version is None:
            target_version = max(m.version for m in migrations)
        
        for migration in sorted(migrations, key=lambda m: m.version):
            if migration.version > current_version and migration.version <= target_version:
                await self.apply_migration(migration)
    
    async def apply_migration(self, migration: DatabaseMigration) -> None:
        """Apply a single migration."""
        async with aiosqlite.connect(self.db_path) as conn:
            try:
                await conn.execute("BEGIN TRANSACTION")
                
                # Apply migration
                cursor = await conn.cursor()
                for sql in migration.up(cursor):
                    await conn.execute(sql)
                
                # Validate migration
                if not migration.validate(cursor):
                    raise Exception(f"Migration {migration.version} validation failed")
                
                # Record migration
                await conn.execute(
                    "INSERT INTO schema_version (version, description, applied_at) VALUES (?, ?, ?)",
                    (migration.version, migration.description, datetime.utcnow().isoformat())
                )
                
                await conn.commit()
                self.logger.info(f"Applied migration {migration.version}: {migration.description}")
                
            except Exception as e:
                await conn.rollback()
                self.logger.error(f"Migration {migration.version} failed: {e}")
                raise
```

### Schema Versioning

Track schema versions:

```sql
CREATE TABLE schema_version (
    version INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    applied_at TEXT NOT NULL,
    checksum TEXT
);
```

## Migration Best Practices

### Safe Migration Patterns

#### Adding Columns
```sql
-- Safe: Adding nullable columns
ALTER TABLE wifi_networks ADD COLUMN vendor TEXT;

-- Safe: Adding columns with defaults
ALTER TABLE wifi_networks ADD COLUMN confidence_score INTEGER DEFAULT 0;
```

#### Adding Indexes
```sql
-- Safe: Adding indexes (non-blocking in SQLite)
CREATE INDEX idx_wifi_vendor ON wifi_networks(vendor);
CREATE INDEX IF NOT EXISTS idx_wifi_vendor ON wifi_networks(vendor);
```

#### Renaming Columns (SQLite 3.25+)
```sql
-- Modern SQLite approach
ALTER TABLE wifi_networks RENAME COLUMN old_name TO new_name;
```

#### Complex Schema Changes
For complex changes, use the recreation pattern:

```python
def complex_table_migration(cursor):
    """Example of complex table restructuring."""
    return [
        # Create new table with desired schema
        """CREATE TABLE wifi_networks_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bssid TEXT NOT NULL,
            ssid TEXT,
            frequency INTEGER,
            signal_strength INTEGER,
            encryption TEXT,
            channel INTEGER,
            vendor TEXT,
            confidence_score INTEGER DEFAULT 0,
            first_seen TEXT,
            last_seen TEXT,
            gps_lat REAL,
            gps_lon REAL,
            gps_accuracy REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""",
        
        # Copy data from old table
        """INSERT INTO wifi_networks_new (
            id, bssid, ssid, frequency, signal_strength, encryption,
            channel, first_seen, last_seen, gps_lat, gps_lon, gps_accuracy, created_at
        ) SELECT 
            id, bssid, ssid, frequency, signal_strength, encryption,
            channel, first_seen, last_seen, gps_lat, gps_lon, gps_accuracy, created_at
        FROM wifi_networks""",
        
        # Drop old table
        "DROP TABLE wifi_networks",
        
        # Rename new table
        "ALTER TABLE wifi_networks_new RENAME TO wifi_networks",
        
        # Recreate indexes
        "CREATE INDEX idx_wifi_bssid ON wifi_networks(bssid)",
        "CREATE INDEX idx_wifi_ssid ON wifi_networks(ssid)",
        "CREATE INDEX idx_wifi_last_seen ON wifi_networks(last_seen)",
        "CREATE INDEX idx_wifi_location ON wifi_networks(gps_lat, gps_lon)",
        "CREATE INDEX idx_wifi_vendor ON wifi_networks(vendor)",
    ]
```

### Data Migration Patterns

#### Populating New Columns
```python
def populate_vendor_column(cursor):
    """Populate vendor column from existing data."""
    return [
        # Add vendor column
        "ALTER TABLE wifi_networks ADD COLUMN vendor TEXT",
        
        # Update with vendor lookup
        """UPDATE wifi_networks 
           SET vendor = (
               SELECT vendor_name 
               FROM oui_lookup 
               WHERE wifi_networks.bssid LIKE oui_lookup.prefix || '%'
           )""",
    ]
```

#### Data Transformation
```python
def transform_encryption_data(cursor):
    """Transform encryption data format."""
    return [
        # Add new column
        "ALTER TABLE wifi_networks ADD COLUMN encryption_type TEXT",
        
        # Transform existing data
        """UPDATE wifi_networks 
           SET encryption_type = CASE 
               WHEN encryption LIKE '%WPA3%' THEN 'WPA3'
               WHEN encryption LIKE '%WPA2%' THEN 'WPA2'
               WHEN encryption LIKE '%WPA%' THEN 'WPA'
               WHEN encryption LIKE '%WEP%' THEN 'WEP'
               ELSE 'Open'
           END""",
    ]
```

## Performance Considerations

### Index Management

Monitor and optimize indexes:

```python
async def analyze_query_performance():
    """Analyze query performance and suggest indexes."""
    async with aiosqlite.connect(db_path) as conn:
        # Enable query planner
        await conn.execute("PRAGMA compile_options")
        
        # Analyze table statistics
        await conn.execute("ANALYZE")
        
        # Check index usage
        cursor = await conn.execute("""
            SELECT name, tbl_name, sql 
            FROM sqlite_master 
            WHERE type='index' AND tbl_name IN ('wifi_networks', 'bluetooth_devices')
        """)
        indexes = await cursor.fetchall()
        
        return indexes
```

### Maintenance Operations

Regular maintenance tasks:

```python
async def maintenance_tasks():
    """Perform regular database maintenance."""
    async with aiosqlite.connect(db_path) as conn:
        # Vacuum database to reclaim space
        await conn.execute("VACUUM")
        
        # Update table statistics
        await conn.execute("ANALYZE")
        
        # Check database integrity
        cursor = await conn.execute("PRAGMA integrity_check")
        integrity = await cursor.fetchall()
        
        return integrity
```

## Testing Migrations

### Migration Testing Framework

```python
# tests/test_migrations.py
import pytest
import tempfile
import os
from piwardrive.db.migrations import MigrationRunner

@pytest.mark.asyncio
async def test_migration_001():
    """Test migration 001 applies correctly."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    try:
        # Create initial schema
        runner = MigrationRunner(db_path)
        await runner.apply_migrations(target_version=0)
        
        # Apply migration
        await runner.apply_migrations(target_version=1)
        
        # Verify migration applied
        async with aiosqlite.connect(db_path) as conn:
            cursor = await conn.execute("PRAGMA table_info(wifi_networks)")
            columns = [row[1] for row in cursor.fetchall()]
            assert "vendor" in columns
            
    finally:
        os.unlink(db_path)
```

### Data Integrity Testing

```python
async def test_data_integrity_after_migration():
    """Test data integrity is preserved during migration."""
    # Create test data
    test_data = [
        ('00:11:22:33:44:55', 'TestNetwork', 2437, -50),
        ('AA:BB:CC:DD:EE:FF', 'AnotherNetwork', 5180, -60),
    ]
    
    # Insert test data
    async with aiosqlite.connect(db_path) as conn:
        for bssid, ssid, freq, signal in test_data:
            await conn.execute(
                "INSERT INTO wifi_networks (bssid, ssid, frequency, signal_strength) VALUES (?, ?, ?, ?)",
                (bssid, ssid, freq, signal)
            )
    
    # Apply migration
    await runner.apply_migrations()
    
    # Verify data integrity
    async with aiosqlite.connect(db_path) as conn:
        cursor = await conn.execute("SELECT bssid, ssid, frequency, signal_strength FROM wifi_networks")
        migrated_data = await cursor.fetchall()
        
        assert len(migrated_data) == len(test_data)
        for original, migrated in zip(test_data, migrated_data):
            assert original == migrated
```

## Rollback Strategies

### Automatic Rollback

```python
async def safe_migration_with_rollback(migration: DatabaseMigration):
    """Apply migration with automatic rollback on failure."""
    backup_path = f"{db_path}.backup"
    
    try:
        # Create backup
        shutil.copy2(db_path, backup_path)
        
        # Apply migration
        await runner.apply_migration(migration)
        
        # Verify migration
        if not await verify_migration(migration):
            raise Exception("Migration verification failed")
            
    except Exception as e:
        # Rollback to backup
        shutil.copy2(backup_path, db_path)
        logger.error(f"Migration failed, rolled back: {e}")
        raise
    finally:
        # Clean up backup
        if os.path.exists(backup_path):
            os.unlink(backup_path)
```

### Manual Rollback

```python
async def rollback_migration(version: int):
    """Manually rollback to a specific version."""
    current_version = await runner.get_current_version()
    
    if version >= current_version:
        raise ValueError("Cannot rollback to current or future version")
    
    # Get migrations to rollback
    migrations = runner.load_migrations()
    rollback_migrations = [
        m for m in migrations 
        if m.version > version and m.version <= current_version
    ]
    
    # Apply rollbacks in reverse order
    for migration in sorted(rollback_migrations, key=lambda m: m.version, reverse=True):
        await runner.rollback_migration(migration)
```

## Monitoring and Alerting

### Schema Change Monitoring

```python
async def monitor_schema_changes():
    """Monitor database schema changes."""
    async with aiosqlite.connect(db_path) as conn:
        # Check for schema drift
        cursor = await conn.execute("""
            SELECT name, sql FROM sqlite_master 
            WHERE type IN ('table', 'index') 
            ORDER BY name
        """)
        current_schema = await cursor.fetchall()
        
        # Compare with expected schema
        expected_schema = load_expected_schema()
        
        if current_schema != expected_schema:
            await send_alert("Schema drift detected")
```

### Performance Monitoring

```python
async def monitor_database_performance():
    """Monitor database performance metrics."""
    async with aiosqlite.connect(db_path) as conn:
        # Check database size
        cursor = await conn.execute("PRAGMA page_count")
        page_count = (await cursor.fetchone())[0]
        
        cursor = await conn.execute("PRAGMA page_size")
        page_size = (await cursor.fetchone())[0]
        
        db_size = page_count * page_size
        
        # Check query performance
        slow_queries = await identify_slow_queries()
        
        return {
            'db_size': db_size,
            'slow_queries': slow_queries,
            'index_usage': await analyze_index_usage()
        }
```

## Best Practices Summary

### Do's

1. **Always backup before migrations**: Create database backups before applying migrations
2. **Test migrations thoroughly**: Test on development data before production
3. **Use transactions**: Wrap migrations in transactions for atomicity
4. **Validate migrations**: Implement validation functions for all migrations
5. **Monitor performance**: Track database performance before and after migrations
6. **Version control**: Store migrations in version control with clear descriptions

### Don'ts

1. **Don't drop columns directly**: SQLite doesn't support dropping columns easily
2. **Don't ignore foreign keys**: Consider foreign key constraints during migrations
3. **Don't skip validation**: Always validate migration results
4. **Don't rush migrations**: Take time to plan and test complex schema changes
5. **Don't ignore rollback**: Always implement rollback procedures

### Schema Evolution Strategy

1. **Additive changes first**: Prefer adding new columns/tables over modifying existing ones
2. **Gradual deprecation**: Deprecate old columns/tables gradually
3. **Backward compatibility**: Maintain backward compatibility where possible
4. **Performance testing**: Test performance impact of schema changes
5. **Documentation**: Document all schema changes and their rationale

## Troubleshooting

### Common Issues

1. **Migration fails**: Check logs, verify SQL syntax, ensure proper permissions
2. **Data corruption**: Restore from backup, investigate root cause
3. **Performance degradation**: Analyze query plans, rebuild indexes
4. **Deadlocks**: Review transaction scope, implement retry logic

### Recovery Procedures

1. **Backup restoration**: Restore from known good backup
2. **Schema repair**: Rebuild corrupted tables/indexes
3. **Data recovery**: Use SQLite recovery tools if needed
4. **Consistency checks**: Run integrity checks after recovery

For more information, see the [Database Administration Guide](database_administration.md) and [Performance Tuning Guide](performance_tuning.md).
