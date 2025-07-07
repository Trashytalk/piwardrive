"""
Comprehensive tests for persistence layer and database operations.
Tests database connections, health records, app state, and data integrity.
"""

import os
import pytest
import asyncio
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
from typing import List, Dict, Any

from piwardrive.core.persistence import (
    HealthRecord,
    AppState,
    DashboardSettings,
    save_health_record,
    load_recent_health,
    save_app_state,
    load_app_state,
    save_dashboard_settings,
    load_dashboard_settings,
    purge_old_health,
    get_database_stats,
    _db_path,
    _acquire_connection,
    _release_connection,
    init_database,
    migrate_database,
    ShardManager,
    LATEST_VERSION,
    _filter_invalid,
    _flush_health_buffer,
    bulk_insert_health_records,
    get_health_record_count,
    vacuum_database,
    backup_database,
    restore_database
)


class TestDatabaseConnection:
    """Test database connection management."""
    
    @pytest.mark.asyncio
    async def test_database_initialization(self, tmp_path):
        """Test database initialization creates proper schema."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            # Initialize database
            await init_database()
            
            # Verify database file was created
            db_file = tmp_path / "test.db"
            assert db_file.exists()
            
            # Verify schema was created
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            
            # Check for main tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            assert 'health_records' in tables
            assert 'app_state' in tables
            assert 'dashboard_settings' in tables
            assert 'schema_version' in tables
            
            conn.close()
            
    @pytest.mark.asyncio
    async def test_connection_pool_management(self, tmp_path):
        """Test database connection pool acquire/release."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            # Initialize database
            await init_database()
            
            # Acquire connection
            conn = await _acquire_connection()
            assert conn is not None
            
            # Test connection works
            async with conn.execute("SELECT 1") as cursor:
                result = await cursor.fetchone()
                assert result[0] == 1
            
            # Release connection
            await _release_connection(conn)
            
    @pytest.mark.asyncio
    async def test_database_migration(self, tmp_path):
        """Test database schema migration."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            # Initialize database
            await init_database()
            
            # Run migration
            await migrate_database()
            
            # Verify version table
            conn = sqlite3.connect(str(tmp_path / "test.db"))
            cursor = conn.cursor()
            
            cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
            result = cursor.fetchone()
            assert result[0] == LATEST_VERSION
            
            conn.close()
            
    def test_shard_manager(self):
        """Test database sharding functionality."""
        # Test single shard
        shard_mgr = ShardManager(shards=1)
        assert shard_mgr.shards == 1
        
        path1 = shard_mgr.db_path("key1")
        path2 = shard_mgr.db_path("key2")
        assert path1 == path2  # Same path for single shard
        
        # Test multiple shards
        shard_mgr = ShardManager(shards=3)
        assert shard_mgr.shards == 3
        
        paths = [shard_mgr.db_path(f"key{i}") for i in range(10)]
        unique_paths = set(paths)
        assert len(unique_paths) <= 3  # Should distribute across shards
        
    def test_filter_invalid_records(self):
        """Test filtering of invalid records."""
        records = [
            {"timestamp": "2024-01-01", "value": 10},
            {"timestamp": None, "value": 20},  # Invalid - None timestamp
            {"timestamp": "2024-01-02", "value": None},  # Invalid - None value
            {"timestamp": "2024-01-03", "value": 30},
            {"other_field": "test"}  # Invalid - missing required fields
        ]
        
        required_fields = ["timestamp", "value"]
        valid_records = _filter_invalid(records, required_fields)
        
        assert len(valid_records) == 2
        assert valid_records[0]["timestamp"] == "2024-01-01"
        assert valid_records[1]["timestamp"] == "2024-01-03"


class TestHealthRecords:
    """Test health record operations."""
    
    @pytest.mark.asyncio
    async def test_save_and_load_health_record(self, tmp_path):
        """Test saving and loading health records."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create test health record
            record = HealthRecord(
                timestamp="2024-01-01T12:00:00",
                cpu_temp=55.5,
                cpu_percent=25.0,
                memory_percent=60.0,
                disk_percent=40.0
            )
            
            # Save record
            await save_health_record(record)
            
            # Load recent records
            records = await load_recent_health(1)
            
            # Verify record
            assert len(records) == 1
            assert records[0].cpu_temp == 55.5
            assert records[0].cpu_percent == 25.0
            assert records[0].memory_percent == 60.0
            assert records[0].disk_percent == 40.0
            
    @pytest.mark.asyncio
    async def test_load_multiple_health_records(self, tmp_path):
        """Test loading multiple health records."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create multiple test records
            records = [
                HealthRecord(f"2024-01-01T{12+i:02d}:00:00", 50.0+i, 20.0+i, 60.0+i, 30.0+i)
                for i in range(5)
            ]
            
            # Save all records
            for record in records:
                await save_health_record(record)
            
            # Load recent records
            loaded_records = await load_recent_health(3)
            
            # Verify we got the most recent 3 records
            assert len(loaded_records) == 3
            
            # Verify order (most recent first)
            assert loaded_records[0].cpu_temp == 54.0  # Last saved
            assert loaded_records[1].cpu_temp == 53.0
            assert loaded_records[2].cpu_temp == 52.0
            
    @pytest.mark.asyncio
    async def test_bulk_insert_health_records(self, tmp_path):
        """Test bulk insertion of health records."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create multiple records
            records = [
                HealthRecord(f"2024-01-01T{12+i:02d}:00:00", 50.0+i, 20.0+i, 60.0+i, 30.0+i)
                for i in range(100)
            ]
            
            # Bulk insert
            await bulk_insert_health_records(records)
            
            # Verify all records were inserted
            count = await get_health_record_count()
            assert count == 100
            
            # Verify data integrity
            loaded_records = await load_recent_health(5)
            assert len(loaded_records) == 5
            assert loaded_records[0].cpu_temp == 149.0  # Last record
            
    @pytest.mark.asyncio
    async def test_purge_old_health_records(self, tmp_path):
        """Test purging old health records."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create records with different timestamps
            base_time = datetime.now()
            records = []
            
            # Create old records (30 days ago)
            for i in range(5):
                timestamp = (base_time - timedelta(days=30, hours=i)).isoformat()
                records.append(HealthRecord(timestamp, 50.0, 20.0, 60.0, 30.0))
            
            # Create recent records (1 day ago)
            for i in range(5):
                timestamp = (base_time - timedelta(days=1, hours=i)).isoformat()
                records.append(HealthRecord(timestamp, 55.0, 25.0, 65.0, 35.0))
            
            # Save all records
            for record in records:
                await save_health_record(record)
            
            # Verify all records exist
            all_records = await load_recent_health(20)
            assert len(all_records) == 10
            
            # Purge records older than 7 days
            deleted_count = await purge_old_health(days=7)
            assert deleted_count == 5
            
            # Verify only recent records remain
            remaining_records = await load_recent_health(20)
            assert len(remaining_records) == 5
            
            # Verify remaining records are the recent ones
            for record in remaining_records:
                assert record.cpu_temp == 55.0  # Recent record temperature
                
    @pytest.mark.asyncio
    async def test_health_buffer_flush(self, tmp_path):
        """Test health record buffer flushing."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Mock buffer with records
            buffer_records = [
                {
                    "timestamp": "2024-01-01T12:00:00",
                    "cpu_temp": 55.0,
                    "cpu_percent": 25.0,
                    "memory_percent": 60.0,
                    "disk_percent": 40.0
                },
                {
                    "timestamp": "2024-01-01T12:01:00",
                    "cpu_temp": 56.0,
                    "cpu_percent": 26.0,
                    "memory_percent": 61.0,
                    "disk_percent": 41.0
                }
            ]
            
            with patch('piwardrive.core.persistence._HEALTH_BUFFER', buffer_records):
                # Flush buffer
                await _flush_health_buffer()
                
                # Verify records were inserted
                records = await load_recent_health(5)
                assert len(records) == 2
                
                # Verify buffer was cleared
                assert len(buffer_records) == 0


class TestAppState:
    """Test application state persistence."""
    
    @pytest.mark.asyncio
    async def test_save_and_load_app_state(self, tmp_path):
        """Test saving and loading application state."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create test app state
            state = AppState(
                last_screen="Dashboard",
                last_start="2024-01-01T12:00:00",
                first_run=False
            )
            
            # Save state
            await save_app_state(state)
            
            # Load state
            loaded_state = await load_app_state()
            
            # Verify state
            assert loaded_state.last_screen == "Dashboard"
            assert loaded_state.last_start == "2024-01-01T12:00:00"
            assert loaded_state.first_run is False
            
    @pytest.mark.asyncio
    async def test_app_state_first_run_detection(self, tmp_path):
        """Test first run detection when no state exists."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Load state when no state exists
            loaded_state = await load_app_state()
            
            # Should return defaults for first run
            assert loaded_state.first_run is True
            assert loaded_state.last_screen == "Dashboard"  # Default
            assert loaded_state.last_start is not None
            
    @pytest.mark.asyncio
    async def test_app_state_update(self, tmp_path):
        """Test updating application state."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Save initial state
            initial_state = AppState(
                last_screen="Map",
                last_start="2024-01-01T12:00:00",
                first_run=True
            )
            await save_app_state(initial_state)
            
            # Update state
            updated_state = AppState(
                last_screen="Analytics",
                last_start="2024-01-01T13:00:00",
                first_run=False
            )
            await save_app_state(updated_state)
            
            # Load state
            loaded_state = await load_app_state()
            
            # Verify updated values
            assert loaded_state.last_screen == "Analytics"
            assert loaded_state.last_start == "2024-01-01T13:00:00"
            assert loaded_state.first_run is False


class TestDashboardSettings:
    """Test dashboard settings persistence."""
    
    @pytest.mark.asyncio
    async def test_save_and_load_dashboard_settings(self, tmp_path):
        """Test saving and loading dashboard settings."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create test dashboard settings
            settings = DashboardSettings(
                layout=[
                    {"widget": "SystemStats", "position": [0, 0], "size": [2, 2]},
                    {"widget": "MapView", "position": [2, 0], "size": [4, 4]}
                ],
                widgets=["SystemStats", "MapView", "GPSStatus"]
            )
            
            # Save settings
            await save_dashboard_settings(settings)
            
            # Load settings
            loaded_settings = await load_dashboard_settings()
            
            # Verify settings
            assert loaded_settings.layout == settings.layout
            assert loaded_settings.widgets == settings.widgets
            
    @pytest.mark.asyncio
    async def test_dashboard_settings_defaults(self, tmp_path):
        """Test dashboard settings defaults when no settings exist."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Load settings when none exist
            loaded_settings = await load_dashboard_settings()
            
            # Should return defaults
            assert loaded_settings.layout == []
            assert loaded_settings.widgets == []
            
    @pytest.mark.asyncio
    async def test_dashboard_settings_complex_layout(self, tmp_path):
        """Test dashboard settings with complex layout data."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create complex layout
            settings = DashboardSettings(
                layout=[
                    {
                        "widget": "SystemStats",
                        "position": [0, 0],
                        "size": [2, 2],
                        "config": {
                            "refresh_interval": 5000,
                            "show_temperature": True,
                            "alert_thresholds": {
                                "cpu": 80,
                                "memory": 90,
                                "temperature": 70
                            }
                        }
                    },
                    {
                        "widget": "NetworkMap",
                        "position": [2, 0],
                        "size": [6, 4],
                        "config": {
                            "show_access_points": True,
                            "show_bluetooth": False,
                            "clustering": True,
                            "auto_refresh": True
                        }
                    }
                ],
                widgets=[
                    "SystemStats",
                    "NetworkMap",
                    "GPSStatus",
                    "SecurityAlerts",
                    "BatteryStatus"
                ]
            )
            
            # Save and load
            await save_dashboard_settings(settings)
            loaded_settings = await load_dashboard_settings()
            
            # Verify complex data integrity
            assert len(loaded_settings.layout) == 2
            assert loaded_settings.layout[0]["config"]["refresh_interval"] == 5000
            assert loaded_settings.layout[1]["config"]["show_access_points"] is True
            assert len(loaded_settings.widgets) == 5


class TestDatabaseMaintenance:
    """Test database maintenance operations."""
    
    @pytest.mark.asyncio
    async def test_database_vacuum(self, tmp_path):
        """Test database vacuum operation."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Add some data
            records = [
                HealthRecord(f"2024-01-01T{12+i:02d}:00:00", 50.0+i, 20.0, 60.0, 30.0)
                for i in range(100)
            ]
            for record in records:
                await save_health_record(record)
            
            # Delete some data
            await purge_old_health(days=0)  # Delete everything
            
            # Get file size before vacuum
            db_file = Path(tmp_path / "test.db")
            size_before = db_file.stat().st_size
            
            # Vacuum database
            await vacuum_database()
            
            # Verify vacuum completed (size might change, but file should still exist)
            assert db_file.exists()
            size_after = db_file.stat().st_size
            # Size might be smaller after vacuum, but could be same if no fragmentation
            assert size_after > 0
            
    @pytest.mark.asyncio
    async def test_database_backup(self, tmp_path):
        """Test database backup operation."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Add some test data
            record = HealthRecord("2024-01-01T12:00:00", 55.0, 25.0, 60.0, 40.0)
            await save_health_record(record)
            
            state = AppState("Dashboard", "2024-01-01T12:00:00", False)
            await save_app_state(state)
            
            # Create backup
            backup_path = tmp_path / "backup.db"
            await backup_database(str(backup_path))
            
            # Verify backup file was created
            assert backup_path.exists()
            assert backup_path.stat().st_size > 0
            
            # Verify backup contains data
            backup_conn = sqlite3.connect(str(backup_path))
            cursor = backup_conn.cursor()
            
            # Check health records
            cursor.execute("SELECT COUNT(*) FROM health_records")
            health_count = cursor.fetchone()[0]
            assert health_count == 1
            
            # Check app state
            cursor.execute("SELECT COUNT(*) FROM app_state")
            state_count = cursor.fetchone()[0]
            assert state_count == 1
            
            backup_conn.close()
            
    @pytest.mark.asyncio
    async def test_database_restore(self, tmp_path):
        """Test database restore operation."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            # Create backup database with data
            backup_path = tmp_path / "backup.db"
            backup_conn = sqlite3.connect(str(backup_path))
            cursor = backup_conn.cursor()
            
            # Create schema
            cursor.execute("""
                CREATE TABLE health_records (
                    timestamp TEXT PRIMARY KEY,
                    cpu_temp REAL,
                    cpu_percent REAL,
                    memory_percent REAL,
                    disk_percent REAL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE app_state (
                    id INTEGER PRIMARY KEY,
                    last_screen TEXT,
                    last_start TEXT,
                    first_run BOOLEAN
                )
            """)
            
            # Insert test data
            cursor.execute("""
                INSERT INTO health_records VALUES (?, ?, ?, ?, ?)
            """, ("2024-01-01T12:00:00", 55.0, 25.0, 60.0, 40.0))
            
            cursor.execute("""
                INSERT INTO app_state VALUES (?, ?, ?, ?)
            """, (1, "Dashboard", "2024-01-01T12:00:00", 0))
            
            backup_conn.commit()
            backup_conn.close()
            
            # Initialize target database
            await init_database()
            
            # Restore from backup
            await restore_database(str(backup_path))
            
            # Verify data was restored
            records = await load_recent_health(10)
            assert len(records) == 1
            assert records[0].cpu_temp == 55.0
            
            state = await load_app_state()
            assert state.last_screen == "Dashboard"
            
    @pytest.mark.asyncio
    async def test_get_database_stats(self, tmp_path):
        """Test database statistics retrieval."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Add some test data
            records = [
                HealthRecord(f"2024-01-01T{12+i:02d}:00:00", 50.0, 20.0, 60.0, 30.0)
                for i in range(10)
            ]
            for record in records:
                await save_health_record(record)
            
            # Get database stats
            stats = await get_database_stats()
            
            # Verify stats
            assert "health_records" in stats
            assert "app_state" in stats
            assert "dashboard_settings" in stats
            assert "total_size" in stats
            
            assert stats["health_records"]["count"] == 10
            assert stats["total_size"] > 0


class TestDatabaseErrorHandling:
    """Test database error handling and edge cases."""
    
    @pytest.mark.asyncio
    async def test_database_connection_failure(self, tmp_path):
        """Test handling of database connection failures."""
        with patch('piwardrive.core.persistence._db_path', return_value="/invalid/path/db.sqlite"):
            # Should handle connection failure gracefully
            try:
                await init_database()
            except Exception as e:
                assert "database" in str(e).lower() or "permission" in str(e).lower()
                
    @pytest.mark.asyncio
    async def test_invalid_health_record_data(self, tmp_path):
        """Test handling of invalid health record data."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Try to save record with invalid data
            invalid_record = HealthRecord(
                timestamp="invalid_timestamp",
                cpu_temp=None,  # Invalid
                cpu_percent="not_a_number",  # Invalid
                memory_percent=60.0,
                disk_percent=40.0
            )
            
            # Should handle invalid data gracefully
            try:
                await save_health_record(invalid_record)
            except Exception as e:
                # Expected to fail with invalid data
                assert "constraint" in str(e).lower() or "type" in str(e).lower()
                
    @pytest.mark.asyncio
    async def test_database_corruption_recovery(self, tmp_path):
        """Test recovery from database corruption."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Corrupt the database file
            db_file = tmp_path / "test.db"
            with open(db_file, 'w') as f:
                f.write("corrupted data")
            
            # Try to reinitialize - should handle corruption
            try:
                await init_database()
            except Exception as e:
                # Expected to fail with corrupted database
                assert "database" in str(e).lower() or "malformed" in str(e).lower()
                
    @pytest.mark.asyncio
    async def test_concurrent_database_access(self, tmp_path):
        """Test concurrent database access scenarios."""
        with patch('piwardrive.core.persistence._db_path', return_value=str(tmp_path / "test.db")):
            await init_database()
            
            # Create multiple concurrent tasks
            async def save_records(start_idx):
                for i in range(5):
                    record = HealthRecord(
                        f"2024-01-01T{12+start_idx+i:02d}:00:00",
                        50.0 + start_idx + i,
                        20.0,
                        60.0,
                        30.0
                    )
                    await save_health_record(record)
            
            # Run multiple tasks concurrently
            tasks = [save_records(i * 10) for i in range(3)]
            await asyncio.gather(*tasks)
            
            # Verify all records were saved
            records = await load_recent_health(50)
            assert len(records) == 15
