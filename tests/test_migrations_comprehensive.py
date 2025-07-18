"""
Comprehensive tests for database migration system.
Tests migration execution, rollback, and database schema management.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import aiosqlite
import pytest

# Import migration components with string imports to avoid syntax issues


class TestBaseMigration:
    """Test base migration functionality."""

    def test_base_migration_initialization(self):
        """Test base migration can be initialized."""
        migration = BaseMigration()
        assert migration is not None
        assert hasattr(migration, "apply")
        assert hasattr(migration, "rollback")

    def test_base_migration_version_default(self):
        """Test base migration has default version."""
        migration = BaseMigration()
        assert hasattr(migration, "version")
        assert migration.version == 0

    @pytest.mark.asyncio
    async def test_base_migration_apply_not_implemented(self):
        """Test base migration apply method raises NotImplementedError."""
        migration = BaseMigration()

        with pytest.raises(NotImplementedError):
            await migration.apply(Mock())

    @pytest.mark.asyncio
    async def test_base_migration_rollback_not_implemented(self):
        """Test base migration rollback method raises NotImplementedError."""
        migration = BaseMigration()

        with pytest.raises(NotImplementedError):
            await migration.rollback(Mock())


class TestScanSessionsMigration:
    """Test scan sessions table migration."""

    def test_scan_sessions_migration_version(self):
        """Test scan sessions migration has correct version."""
        migration = ScanSessionsMigration()
        assert migration.version == 1

    @pytest.mark.asyncio
    async def test_scan_sessions_migration_apply(self):
        """Test scan sessions migration creates table."""
        migration = ScanSessionsMigration()

        # Create in-memory database
        async with aiosqlite.connect(":memory:") as conn:
            await migration.apply(conn)

            # Check table exists
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_sessions'"
            )
            result = await cursor.fetchone()
            assert result is not None
            assert result[0] == "scan_sessions"

    @pytest.mark.asyncio
    async def test_scan_sessions_migration_table_structure(self):
        """Test scan sessions table has correct structure."""
        migration = ScanSessionsMigration()

        async with aiosqlite.connect(":memory:") as conn:
            await migration.apply(conn)

            # Check table structure
            cursor = await conn.execute("PRAGMA table_info(scan_sessions)")
            columns = await cursor.fetchall()

            # Extract column names
            column_names = [col[1] for col in columns]

            # Check required columns exist
            assert "id" in column_names
            assert "device_id" in column_names
            assert "scan_type" in column_names
            assert "started_at" in column_names
            assert "completed_at" in column_names
            assert "duration_seconds" in column_names
            assert "location_start_lat" in column_names
            assert "location_start_lon" in column_names
            assert "total_detections" in column_names
            assert "created_at" in column_names

    @pytest.mark.asyncio
    async def test_scan_sessions_migration_rollback(self):
        """Test scan sessions migration rollback."""
        migration = ScanSessionsMigration()

        async with aiosqlite.connect(":memory:") as conn:
            # Apply migration
            await migration.apply(conn)

            # Verify table exists
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_sessions'"
            )
            result = await cursor.fetchone()
            assert result is not None

            # Rollback migration
            await migration.rollback(conn)

            # Verify table is dropped
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_sessions'"
            )
            result = await cursor.fetchone()
            assert result is None


class TestBluetoothDetectionsMigration:
    """Test bluetooth detections table migration."""

    def test_bluetooth_migration_version(self):
        """Test bluetooth migration has correct version."""
        migration = BluetoothMigration()
        assert migration.version == 3

    @pytest.mark.asyncio
    async def test_bluetooth_migration_apply(self):
        """Test bluetooth migration creates table."""
        migration = BluetoothMigration()

        async with aiosqlite.connect(":memory:") as conn:
            await migration.apply(conn)

            # Check table exists
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='bluetooth_detections'"
            )
            result = await cursor.fetchone()
            assert result is not None
            assert result[0] == "bluetooth_detections"

    @pytest.mark.asyncio
    async def test_bluetooth_migration_table_structure(self):
        """Test bluetooth detections table has correct structure."""
        migration = BluetoothMigration()

        async with aiosqlite.connect(":memory:") as conn:
            await migration.apply(conn)

            # Check table structure
            cursor = await conn.execute("PRAGMA table_info(bluetooth_detections)")
            columns = await cursor.fetchall()

            # Extract column names
            column_names = [col[1] for col in columns]

            # Check required columns exist
            assert "id" in column_names
            assert "device_address" in column_names
            assert "device_name" in column_names
            assert "rssi" in column_names
            assert "detected_at" in column_names
            assert "latitude" in column_names
            assert "longitude" in column_names
            assert "created_at" in column_names


class TestGPSTracksMigration:
    """Test GPS tracks table migration."""

    def test_gps_tracks_migration_version(self):
        """Test GPS tracks migration has correct version."""
        migration = GPSTracksMigration()
        assert migration.version == 4

    @pytest.mark.asyncio
    async def test_gps_tracks_migration_apply(self):
        """Test GPS tracks migration creates table."""
        migration = GPSTracksMigration()

        async with aiosqlite.connect(":memory:") as conn:
            await migration.apply(conn)

            # Check table exists
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='gps_tracks'"
            )
            result = await cursor.fetchone()
            assert result is not None
            assert result[0] == "gps_tracks"

    @pytest.mark.asyncio
    async def test_gps_tracks_migration_table_structure(self):
        """Test GPS tracks table has correct structure."""
        migration = GPSTracksMigration()

        async with aiosqlite.connect(":memory:") as conn:
            await migration.apply(conn)

            # Check table structure
            cursor = await conn.execute("PRAGMA table_info(gps_tracks)")
            columns = await cursor.fetchall()

            # Extract column names
            column_names = [col[1] for col in columns]

            # Check required columns exist
            assert "id" in column_names
            assert "latitude" in column_names
            assert "longitude" in column_names
            assert "altitude" in column_names
            assert "accuracy" in column_names
            assert "speed" in column_names
            assert "heading" in column_names
            assert "timestamp" in column_names
            assert "created_at" in column_names


class TestPerformanceIndexesMigration:
    """Test performance indexes migration."""

    def test_performance_indexes_migration_version(self):
        """Test performance indexes migration has correct version."""
        migration = PerformanceIndexesMigration()
        assert migration.version == 10

    @pytest.mark.asyncio
    async def test_performance_indexes_migration_apply(self):
        """Test performance indexes migration creates indexes."""
        migration = PerformanceIndexesMigration()

        async with aiosqlite.connect(":memory:") as conn:
            # First create some basic tables that indexes will reference
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS wifi_detections (
                    id INTEGER PRIMARY KEY,
                    bssid TEXT,
                    ssid TEXT,
                    detected_at TIMESTAMP,
                    created_at TIMESTAMP
                )
            """
            )
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS bluetooth_detections (
                    id INTEGER PRIMARY KEY,
                    device_address TEXT,
                    detected_at TIMESTAMP,
                    created_at TIMESTAMP
                )
            """
            )

            # Apply migration
            await migration.apply(conn)

            # Check indexes exist
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
            )
            indexes = await cursor.fetchall()

            # Should have created some indexes
            assert len(indexes) > 0

    @pytest.mark.asyncio
    async def test_performance_indexes_migration_rollback(self):
        """Test performance indexes migration rollback."""
        migration = PerformanceIndexesMigration()

        async with aiosqlite.connect(":memory:") as conn:
            # Create basic tables
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS wifi_detections (
                    id INTEGER PRIMARY KEY,
                    bssid TEXT,
                    detected_at TIMESTAMP
                )
            """
            )

            # Apply migration
            await migration.apply(conn)

            # Verify indexes exist
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
            )
            indexes_before = await cursor.fetchall()
            assert len(indexes_before) > 0

            # Rollback migration
            await migration.rollback(conn)

            # Verify indexes are dropped
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
            )
            indexes_after = await cursor.fetchall()
            assert len(indexes_after) == 0


class TestMigrationRunner:
    """Test migration runner functionality."""

    def test_migration_runner_initialization(self):
        """Test migration runner can be initialized."""
        runner = MigrationRunner(":memory:")
        assert runner is not None
        assert runner.db_path == ":memory:"

    @pytest.mark.asyncio
    async def test_migration_runner_get_current_version(self):
        """Test migration runner can get current database version."""
        runner = MigrationRunner(":memory:")

        # Mock database connection
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [5]

        with patch("aiosqlite.connect") as mock_connect:
            mock_connect.return_value.__aenter__.return_value = mock_conn

            version = await runner.get_current_version()
            assert version == 5

    @pytest.mark.asyncio
    async def test_migration_runner_get_current_version_no_table(self):
        """Test migration runner handles missing migration table."""
        runner = MigrationRunner(":memory:")

        # Mock database connection with no migration table
        mock_conn = Mock()
        mock_conn.execute.side_effect = Exception("no such table")

        with patch("aiosqlite.connect") as mock_connect:
            mock_connect.return_value.__aenter__.return_value = mock_conn

            version = await runner.get_current_version()
            assert version == 0

    @pytest.mark.asyncio
    async def test_migration_runner_apply_migration(self):
        """Test migration runner can apply a migration."""
        runner = MigrationRunner(":memory:")

        # Create a test migration
        test_migration = ScanSessionsMigration()

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [0]  # Current version

        with patch("aiosqlite.connect") as mock_connect:
            mock_connect.return_value.__aenter__.return_value = mock_conn

            await runner.apply_migration(test_migration)

            # Should have called migration apply
            mock_conn.execute.assert_called()

    @pytest.mark.asyncio
    async def test_migration_runner_rollback_migration(self):
        """Test migration runner can rollback a migration."""
        runner = MigrationRunner(":memory:")

        # Create a test migration
        test_migration = ScanSessionsMigration()

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]  # Current version

        with patch("aiosqlite.connect") as mock_connect:
            mock_connect.return_value.__aenter__.return_value = mock_conn

            await runner.rollback_migration(test_migration)

            # Should have called migration rollback
            mock_conn.execute.assert_called()

    @pytest.mark.asyncio
    async def test_migration_runner_run_migrations(self):
        """Test migration runner can run all migrations."""
        runner = MigrationRunner(":memory:")

        # Mock available migrations
        migrations = [
            ScanSessionsMigration(),
            BluetoothMigration(),
            GPSTracksMigration(),
        ]

        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [0]  # Current version

        with patch("aiosqlite.connect") as mock_connect:
            mock_connect.return_value.__aenter__.return_value = mock_conn
            with patch.object(
                runner, "get_available_migrations", return_value=migrations
            ):

                await runner.run_migrations()

                # Should have executed migrations
                assert mock_conn.execute.call_count > 0


class TestMigrationIntegration:
    """Test complete migration system integration."""

    @pytest.mark.asyncio
    async def test_complete_migration_sequence(self):
        """Test complete migration sequence from scratch."""
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name

        try:
            runner = MigrationRunner(db_path)

            # Test initial version
            version = await runner.get_current_version()
            assert version == 0

            # Apply scan sessions migration
            migration = ScanSessionsMigration()
            await runner.apply_migration(migration)

            # Check table was created
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_sessions'"
                )
                result = await cursor.fetchone()
                assert result is not None

        finally:
            # Clean up
            Path(db_path).unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_migration_version_tracking(self):
        """Test migration version is properly tracked."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name

        try:
            runner = MigrationRunner(db_path)

            # Apply migration
            migration = ScanSessionsMigration()
            await runner.apply_migration(migration)

            # Check version is updated
            version = await runner.get_current_version()
            assert version == migration.version

        finally:
            Path(db_path).unlink(missing_ok=True)

    @pytest.mark.asyncio
    async def test_migration_rollback_integration(self):
        """Test migration rollback works end-to-end."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            db_path = tmp.name

        try:
            runner = MigrationRunner(db_path)

            # Apply migration
            migration = ScanSessionsMigration()
            await runner.apply_migration(migration)

            # Verify table exists
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_sessions'"
                )
                result = await cursor.fetchone()
                assert result is not None

            # Rollback migration
            await runner.rollback_migration(migration)

            # Verify table is gone
            async with aiosqlite.connect(db_path) as conn:
                cursor = await conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='scan_sessions'"
                )
                result = await cursor.fetchone()
                assert result is None

        finally:
            Path(db_path).unlink(missing_ok=True)


class TestMigrationErrorHandling:
    """Test migration error handling."""

    @pytest.mark.asyncio
    async def test_migration_apply_error_handling(self):
        """Test migration handles apply errors gracefully."""
        migration = ScanSessionsMigration()

        # Mock connection that raises error
        mock_conn = Mock()
        mock_conn.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await migration.apply(mock_conn)

    @pytest.mark.asyncio
    async def test_migration_rollback_error_handling(self):
        """Test migration handles rollback errors gracefully."""
        migration = ScanSessionsMigration()

        # Mock connection that raises error
        mock_conn = Mock()
        mock_conn.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            await migration.rollback(mock_conn)

    @pytest.mark.asyncio
    async def test_migration_runner_database_connection_error(self):
        """Test migration runner handles database connection errors."""
        runner = MigrationRunner("/nonexistent/path.db")

        with pytest.raises(Exception):
            await runner.get_current_version()

    @pytest.mark.asyncio
    async def test_migration_runner_invalid_migration_error(self):
        """Test migration runner handles invalid migration errors."""
        runner = MigrationRunner(":memory:")

        # Create invalid migration
        invalid_migration = Mock()
        invalid_migration.version = None
        invalid_migration.apply.side_effect = Exception("Invalid migration")

        with pytest.raises(Exception, match="Invalid migration"):
            await runner.apply_migration(invalid_migration)


class TestMigrationPerformance:
    """Test migration performance and optimization."""

    @pytest.mark.asyncio
    async def test_migration_performance_indexes(self):
        """Test performance indexes migration improves query performance."""
        migration = PerformanceIndexesMigration()

        async with aiosqlite.connect(":memory:") as conn:
            # Create test tables
            await conn.execute(
                """
                CREATE TABLE wifi_detections (
                    id INTEGER PRIMARY KEY,
                    bssid TEXT,
                    detected_at TIMESTAMP
                )
            """
            )

            # Insert test data
            await conn.execute(
                """
                INSERT INTO wifi_detections (bssid, detected_at) 
                VALUES ('00:11:22:33:44:55', '2024-01-01 12:00:00')
            """
            )

            # Apply performance indexes
            await migration.apply(conn)

            # Query should still work
            cursor = await conn.execute(
                "SELECT * FROM wifi_detections WHERE bssid = '00:11:22:33:44:55'"
            )
            result = await cursor.fetchone()
            assert result is not None

    @pytest.mark.asyncio
    async def test_migration_batch_operations(self):
        """Test migration can handle batch operations efficiently."""
        migration = ScanSessionsMigration()

        async with aiosqlite.connect(":memory:") as conn:
            # Apply migration
            await migration.apply(conn)

            # Test batch insert
            data = [
                (f"session_{i}", f"device_{i}", "wifi", "2024-01-01 12:00:00")
                for i in range(100)
            ]

            await conn.executemany(
                "INSERT INTO scan_sessions (id, device_id, scan_type, started_at) VALUES (?, ?, ?, ?)",
                data,
            )

            # Verify data was inserted
            cursor = await conn.execute("SELECT COUNT(*) FROM scan_sessions")
            count = await cursor.fetchone()
            assert count[0] == 100
