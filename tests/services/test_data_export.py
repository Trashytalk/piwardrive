"""Tests for the data_export service module."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from piwardrive.services.data_export import (
    export_bluetooth_detections,
    export_cellular_detections,
    export_gps_tracks,
    export_wifi_detections,
)


class TestDataExportFunctions:
    """Test suite for data export functions."""

    @pytest.fixture
    def mock_persistence(self):
        """Mock persistence connection."""
        with patch(
            "piwardrive.services.data_export.persistence._get_conn"
        ) as mock_conn:
            mock_context = AsyncMock()
            mock_conn.return_value.__aenter__.return_value = mock_context
            yield mock_context

    @pytest.fixture
    def mock_export(self):
        """Mock export.export_records function."""
        with patch(
            "piwardrive.services.data_export.export.export_records"
        ) as mock_export:
            yield mock_export

    @pytest.fixture
    def sample_wifi_data(self):
        """Sample WiFi detection data."""
        return [
            {
                "id": 1,
                "ssid": "HomeNetwork",
                "bssid": "00:11:22:33:44:55",
                "signal_strength": -45,
                "timestamp": "2023-01-01T10:00:00Z",
                "channel": 6,
                "encryption": "WPA2",
            },
            {
                "id": 2,
                "ssid": "CoffeeShop",
                "bssid": "66:77:88:99:AA:BB",
                "signal_strength": -67,
                "timestamp": "2023-01-01T10:05:00Z",
                "channel": 11,
                "encryption": "Open",
            },
        ]

    @pytest.fixture
    def sample_bluetooth_data(self):
        """Sample Bluetooth detection data."""
        return [
            {
                "id": 1,
                "device_name": "iPhone",
                "mac_address": "AA:BB:CC:DD:EE:FF",
                "device_type": "phone",
                "timestamp": "2023-01-01T10:00:00Z",
                "rssi": -55,
            },
            {
                "id": 2,
                "device_name": "Headphones",
                "mac_address": "11:22:33:44:55:66",
                "device_type": "audio",
                "timestamp": "2023-01-01T10:05:00Z",
                "rssi": -78,
            },
        ]

    @pytest.fixture
    def sample_cellular_data(self):
        """Sample cellular detection data."""
        return [
            {
                "id": 1,
                "cell_id": "12345",
                "lac": "678",
                "mcc": "310",
                "mnc": "410",
                "technology": "LTE",
                "timestamp": "2023-01-01T10:00:00Z",
                "signal_strength": -85,
            },
            {
                "id": 2,
                "cell_id": "67890",
                "lac": "123",
                "mcc": "310",
                "mnc": "260",
                "technology": "GSM",
                "timestamp": "2023-01-01T10:05:00Z",
                "signal_strength": -95,
            },
        ]

    @pytest.fixture
    def sample_gps_data(self):
        """Sample GPS track data."""
        return [
            {
                "lat": 40.7128,
                "lon": -74.0060,
                "timestamp": "2023-01-01T10:00:00Z",
            },
            {
                "lat": 40.7580,
                "lon": -73.9855,
                "timestamp": "2023-01-01T10:05:00Z",
            },
        ]

    @pytest.mark.asyncio
    async def test_export_wifi_detections_csv(
        self, mock_persistence, mock_export, sample_wifi_data
    ):
        """Test WiFi detections export to CSV format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_wifi_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_wifi_detections("/tmp/wifi.csv", "csv")

        # Verify database query
        mock_persistence.execute.assert_called_once_with(
            "SELECT * FROM wifi_detections"
        )

        # Verify export call
        mock_export.assert_called_once_with(sample_wifi_data, "/tmp/wifi.csv", "csv")

    @pytest.mark.asyncio
    async def test_export_wifi_detections_json(
        self, mock_persistence, mock_export, sample_wifi_data
    ):
        """Test WiFi detections export to JSON format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_wifi_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_wifi_detections("/tmp/wifi.json", "json")

        # Verify export call with JSON format
        mock_export.assert_called_once_with(sample_wifi_data, "/tmp/wifi.json", "json")

    @pytest.mark.asyncio
    async def test_export_wifi_detections_default_format(
        self, mock_persistence, mock_export, sample_wifi_data
    ):
        """Test WiFi detections export with default format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_wifi_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_wifi_detections("/tmp/wifi.csv")

        # Verify default format is CSV
        mock_export.assert_called_once_with(sample_wifi_data, "/tmp/wifi.csv", "csv")

    @pytest.mark.asyncio
    async def test_export_bluetooth_detections_csv(
        self, mock_persistence, mock_export, sample_bluetooth_data
    ):
        """Test Bluetooth detections export to CSV format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_bluetooth_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_bluetooth_detections("/tmp/bluetooth.csv", "csv")

        # Verify database query
        mock_persistence.execute.assert_called_once_with(
            "SELECT * FROM bluetooth_detections"
        )

        # Verify export call
        mock_export.assert_called_once_with(
            sample_bluetooth_data, "/tmp/bluetooth.csv", "csv"
        )

    @pytest.mark.asyncio
    async def test_export_bluetooth_detections_default_format(
        self, mock_persistence, mock_export, sample_bluetooth_data
    ):
        """Test Bluetooth detections export with default format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_bluetooth_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_bluetooth_detections("/tmp/bluetooth.csv")

        # Verify default format is CSV
        mock_export.assert_called_once_with(
            sample_bluetooth_data, "/tmp/bluetooth.csv", "csv"
        )

    @pytest.mark.asyncio
    async def test_export_cellular_detections_csv(
        self, mock_persistence, mock_export, sample_cellular_data
    ):
        """Test cellular detections export to CSV format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_cellular_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_cellular_detections("/tmp/cellular.csv", "csv")

        # Verify database query
        mock_persistence.execute.assert_called_once_with(
            "SELECT * FROM cellular_detections"
        )

        # Verify export call
        mock_export.assert_called_once_with(
            sample_cellular_data, "/tmp/cellular.csv", "csv"
        )

    @pytest.mark.asyncio
    async def test_export_cellular_detections_default_format(
        self, mock_persistence, mock_export, sample_cellular_data
    ):
        """Test cellular detections export with default format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_cellular_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_cellular_detections("/tmp/cellular.csv")

        # Verify default format is CSV
        mock_export.assert_called_once_with(
            sample_cellular_data, "/tmp/cellular.csv", "csv"
        )

    @pytest.mark.asyncio
    async def test_export_gps_tracks_kml(
        self, mock_persistence, mock_export, sample_gps_data
    ):
        """Test GPS tracks export to KML format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_gps_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_gps_tracks("/tmp/tracks.kml", "kml")

        # Verify database query
        expected_query = (
            "SELECT latitude AS lat, longitude AS lon, timestamp FROM gps_tracks"
        )
        mock_persistence.execute.assert_called_once_with(expected_query)

        # Verify export call
        mock_export.assert_called_once_with(sample_gps_data, "/tmp/tracks.kml", "kml")

    @pytest.mark.asyncio
    async def test_export_gps_tracks_default_format(
        self, mock_persistence, mock_export, sample_gps_data
    ):
        """Test GPS tracks export with default format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_gps_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_gps_tracks("/tmp/tracks.kml")

        # Verify default format is KML
        mock_export.assert_called_once_with(sample_gps_data, "/tmp/tracks.kml", "kml")

    @pytest.mark.asyncio
    async def test_export_gps_tracks_csv(
        self, mock_persistence, mock_export, sample_gps_data
    ):
        """Test GPS tracks export to CSV format."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: row) for row in sample_gps_data
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_gps_tracks("/tmp/tracks.csv", "csv")

        # Verify export call with CSV format
        mock_export.assert_called_once_with(sample_gps_data, "/tmp/tracks.csv", "csv")

    @pytest.mark.asyncio
    async def test_export_empty_data(self, mock_persistence, mock_export):
        """Test export with empty data."""
        # Setup mock database response with empty data
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = []
        mock_persistence.execute.return_value = mock_cursor

        # Mock dict() constructor for rows
        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_wifi_detections("/tmp/empty.csv")

        # Verify export call with empty data
        mock_export.assert_called_once_with([], "/tmp/empty.csv", "csv")

    @pytest.mark.asyncio
    async def test_database_connection_error(self, mock_export):
        """Test handling of database connection errors."""
        with patch(
            "piwardrive.services.data_export.persistence._get_conn"
        ) as mock_conn:
            mock_conn.side_effect = Exception("Database connection failed")

            with pytest.raises(Exception, match="Database connection failed"):
                await export_wifi_detections("/tmp/wifi.csv")

            # Export should not be called if database connection fails
            mock_export.assert_not_called()

    @pytest.mark.asyncio
    async def test_export_function_error(self, mock_persistence, mock_export):
        """Test handling of export function errors."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: {"id": 1, "test": "data"})
        ]
        mock_persistence.execute.return_value = mock_cursor

        # Mock export function to raise an error
        mock_export.side_effect = Exception("Export failed")

        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            with pytest.raises(Exception, match="Export failed"):
                await export_wifi_detections("/tmp/wifi.csv")

    @pytest.mark.asyncio
    async def test_fetch_all_private_function(self, mock_persistence):
        """Test the private _fetch_all function."""
        from piwardrive.services.data_export import _fetch_all

        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: {"id": 1, "name": "test1"}),
            MagicMock(_asdict=lambda: {"id": 2, "name": "test2"}),
        ]
        mock_persistence.execute.return_value = mock_cursor

        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            result = await _fetch_all("SELECT * FROM test_table")

        assert result == [
            {"id": 1, "name": "test1"},
            {"id": 2, "name": "test2"},
        ]

        # Verify database query
        mock_persistence.execute.assert_called_once_with("SELECT * FROM test_table")


class TestDataExportModule:
    """Test suite for module-level functionality."""

    def test_module_exports(self):
        """Test that all expected functions are exported."""
        from piwardrive.services.data_export import __all__

        expected_exports = [
            "export_wifi_detections",
            "export_bluetooth_detections",
            "export_cellular_detections",
            "export_gps_tracks",
        ]

        assert set(__all__) == set(expected_exports)

    def test_all_functions_are_async(self):
        """Test that all exported functions are async."""
        import inspect

        from piwardrive.services.data_export import (
            export_bluetooth_detections,
            export_cellular_detections,
            export_gps_tracks,
            export_wifi_detections,
        )

        functions = [
            export_wifi_detections,
            export_bluetooth_detections,
            export_cellular_detections,
            export_gps_tracks,
        ]

        for func in functions:
            assert inspect.iscoroutinefunction(func), f"{func.__name__} should be async"

    def test_function_signatures(self):
        """Test that functions have correct signatures."""
        import inspect

        from piwardrive.services.data_export import (
            export_bluetooth_detections,
            export_cellular_detections,
            export_gps_tracks,
            export_wifi_detections,
        )

        # Test WiFi function signature
        sig = inspect.signature(export_wifi_detections)
        assert "path" in sig.parameters
        assert "fmt" in sig.parameters
        assert sig.parameters["fmt"].default == "csv"

        # Test Bluetooth function signature
        sig = inspect.signature(export_bluetooth_detections)
        assert "path" in sig.parameters
        assert "fmt" in sig.parameters
        assert sig.parameters["fmt"].default == "csv"

        # Test cellular function signature
        sig = inspect.signature(export_cellular_detections)
        assert "path" in sig.parameters
        assert "fmt" in sig.parameters
        assert sig.parameters["fmt"].default == "csv"

        # Test GPS function signature
        sig = inspect.signature(export_gps_tracks)
        assert "path" in sig.parameters
        assert "fmt" in sig.parameters
        assert sig.parameters["fmt"].default == "kml"


class TestIntegrationScenarios:
    """Test suite for integration scenarios."""

    @pytest.mark.asyncio
    async def test_export_all_data_types(self, mock_persistence, mock_export):
        """Test exporting all data types in sequence."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: {"id": 1, "data": "test"})
        ]
        mock_persistence.execute.return_value = mock_cursor

        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            # Export all data types
            await export_wifi_detections("/tmp/wifi.csv")
            await export_bluetooth_detections("/tmp/bluetooth.csv")
            await export_cellular_detections("/tmp/cellular.csv")
            await export_gps_tracks("/tmp/gps.kml")

        # Verify all export calls were made
        assert mock_export.call_count == 4
        export_calls = mock_export.call_args_list

        # Check file paths and formats
        assert export_calls[0][0][1] == "/tmp/wifi.csv"
        assert export_calls[0][0][2] == "csv"
        assert export_calls[1][0][1] == "/tmp/bluetooth.csv"
        assert export_calls[1][0][2] == "csv"
        assert export_calls[2][0][1] == "/tmp/cellular.csv"
        assert export_calls[2][0][2] == "csv"
        assert export_calls[3][0][1] == "/tmp/gps.kml"
        assert export_calls[3][0][2] == "kml"

    @pytest.mark.asyncio
    async def test_export_multiple_formats(self, mock_persistence, mock_export):
        """Test exporting same data to multiple formats."""
        # Setup mock database response
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            MagicMock(_asdict=lambda: {"id": 1, "ssid": "test"})
        ]
        mock_persistence.execute.return_value = mock_cursor

        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            # Export same data to different formats
            await export_wifi_detections("/tmp/wifi.csv", "csv")
            await export_wifi_detections("/tmp/wifi.json", "json")
            await export_wifi_detections("/tmp/wifi.xml", "xml")

        # Verify all export calls were made with different formats
        assert mock_export.call_count == 3
        export_calls = mock_export.call_args_list

        assert export_calls[0][0][2] == "csv"
        assert export_calls[1][0][2] == "json"
        assert export_calls[2][0][2] == "xml"

    @pytest.mark.asyncio
    async def test_large_dataset_export(self, mock_persistence, mock_export):
        """Test exporting large datasets."""
        # Setup mock database response with large dataset
        large_data = [
            MagicMock(_asdict=lambda i=i: {"id": i, "ssid": f"network_{i}"})
            for i in range(1000)
        ]
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = large_data
        mock_persistence.execute.return_value = mock_cursor

        with patch("builtins.dict", side_effect=lambda r: r._asdict()):
            await export_wifi_detections("/tmp/large_wifi.csv")

        # Verify export was called with large dataset
        mock_export.assert_called_once()
        exported_data = mock_export.call_args[0][0]
        assert len(exported_data) == 1000
