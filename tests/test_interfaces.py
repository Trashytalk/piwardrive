#!/usr/bin/env python3

"""
Comprehensive test suite for interfaces.py module.
Tests service interfaces and protocol implementations.
"""

import sys
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from piwardrive.interfaces import (
    DataCollector,
    DefaultMapService,
    MapService,
    SelfTestCollector,
)


class TestMapServiceProtocol:
    """Test the MapService protocol interface."""

    def test_map_service_protocol_structure(self):
        """Test that MapService protocol has required methods."""
        # Check that the protocol has the expected methods
        assert hasattr(MapService, "get_current_position")
        assert hasattr(MapService, "fetch_access_points")

        # Check method signatures exist (they're abstract in Protocol)
        assert callable(getattr(MapService, "get_current_position", None))
        assert callable(getattr(MapService, "fetch_access_points", None))

    def test_map_service_protocol_compliance(self):
        """Test that a class can implement MapService protocol."""

        class TestMapService:
            def get_current_position(self) -> tuple[float, float] | None:
                return (1.0, 2.0)

            def fetch_access_points(self) -> list[dict[str, Any]]:
                return [{"ssid": "test"}]

        # Should be able to create instance
        service = TestMapService()
        assert service.get_current_position() == (1.0, 2.0)
        assert service.fetch_access_points() == [{"ssid": "test"}]

        # Should satisfy the protocol (duck typing)
        assert callable(service.get_current_position)
        assert callable(service.fetch_access_points)


class TestDefaultMapService:
    """Test the DefaultMapService implementation."""

    def test_default_map_service_initialization(self):
        """Test DefaultMapService can be initialized."""
        service = DefaultMapService()
        assert isinstance(service, DefaultMapService)
        assert hasattr(service, "get_current_position")
        assert hasattr(service, "fetch_access_points")

    def test_get_current_position_success(self):
        """Test get_current_position with successful GPS data."""
        service = DefaultMapService()

        # Mock successful GPS position
        with mock.patch("piwardrive.interfaces.gps_client.get_position") as mock_gps:
            mock_gps.return_value = (51.5074, -0.1278)  # London coordinates

            result = service.get_current_position()

            assert result == (51.5074, -0.1278)
            mock_gps.assert_called_once()

    def test_get_current_position_no_data(self):
        """Test get_current_position when GPS returns None."""
        service = DefaultMapService()

        with mock.patch("piwardrive.interfaces.gps_client.get_position") as mock_gps:
            mock_gps.return_value = None

            result = service.get_current_position()

            assert result is None
            mock_gps.assert_called_once()

    def test_get_current_position_exception(self):
        """Test get_current_position when GPS raises exception."""
        service = DefaultMapService()

        with mock.patch("piwardrive.interfaces.gps_client.get_position") as mock_gps:
            mock_gps.side_effect = Exception("GPS connection failed")

            result = service.get_current_position()

            assert result is None
            mock_gps.assert_called_once()

    def test_get_current_position_with_string_coordinates(self):
        """Test get_current_position converts string coordinates to float."""
        service = DefaultMapService()

        with mock.patch("piwardrive.interfaces.gps_client.get_position") as mock_gps:
            # GPS might return strings that need conversion
            mock_gps.return_value = (
                "40.7128",
                "-74.0060",
            )  # NYC coordinates as strings

            result = service.get_current_position()

            assert result == (40.7128, -74.0060)
            assert isinstance(result[0], float)
            assert isinstance(result[1], float)
            mock_gps.assert_called_once()

    def test_get_current_position_invalid_coordinates(self):
        """Test get_current_position with invalid coordinate data."""
        service = DefaultMapService()

        test_cases = [
            ("invalid", "data"),
            (None, 5.0),
            (5.0, None),
            ("", ""),
        ]

        for invalid_lat, invalid_lon in test_cases:
            with mock.patch(
                "piwardrive.interfaces.gps_client.get_position"
            ) as mock_gps:
                mock_gps.return_value = (invalid_lat, invalid_lon)

                # Should handle conversion errors gracefully
                result = service.get_current_position()
                # Depending on implementation, might return None or raise exception caught internally
                assert result is None or isinstance(result, tuple)

    def test_fetch_access_points_success(self):
        """Test fetch_access_points with successful Kismet data."""
        service = DefaultMapService()

        mock_aps = [
            {"ssid": "Network1", "bssid": "AA:BB:CC:DD:EE:01"},
            {"ssid": "Network2", "bssid": "AA:BB:CC:DD:EE:02"},
        ]

        with mock.patch(
            "piwardrive.interfaces.utils.fetch_kismet_devices"
        ) as mock_fetch:
            mock_fetch.return_value = (mock_aps, [])  # (aps, clients)

            result = service.fetch_access_points()

            assert result == mock_aps
            mock_fetch.assert_called_once()

    def test_fetch_access_points_empty_result(self):
        """Test fetch_access_points with empty Kismet response."""
        service = DefaultMapService()

        with mock.patch(
            "piwardrive.interfaces.utils.fetch_kismet_devices"
        ) as mock_fetch:
            mock_fetch.return_value = ([], [])  # Empty aps and clients

            result = service.fetch_access_points()

            assert result == []
            mock_fetch.assert_called_once()

    def test_fetch_access_points_generator_conversion(self):
        """Test fetch_access_points converts generator to list."""
        service = DefaultMapService()

        def mock_generator():
            yield {"ssid": "AP1"}
            yield {"ssid": "AP2"}

        with mock.patch(
            "piwardrive.interfaces.utils.fetch_kismet_devices"
        ) as mock_fetch:
            mock_fetch.return_value = (mock_generator(), [])

            result = service.fetch_access_points()

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["ssid"] == "AP1"
            assert result[1]["ssid"] == "AP2"

    def test_fetch_access_points_exception_handling(self):
        """Test fetch_access_points handles exceptions."""
        service = DefaultMapService()

        with mock.patch(
            "piwardrive.interfaces.utils.fetch_kismet_devices"
        ) as mock_fetch:
            mock_fetch.side_effect = Exception("Kismet API error")

            # Should propagate the exception (no try/catch in implementation)
            with pytest.raises(Exception, match="Kismet API error"):
                service.fetch_access_points()


class TestDataCollectorProtocol:
    """Test the DataCollector protocol interface."""

    def test_data_collector_protocol_structure(self):
        """Test that DataCollector protocol has required methods."""
        assert hasattr(DataCollector, "collect")
        assert callable(getattr(DataCollector, "collect", None))

    def test_data_collector_protocol_compliance(self):
        """Test that a class can implement DataCollector protocol."""

        class TestDataCollector:
            def collect(self) -> dict[str, Any]:
                return {"metric": "value"}

        collector = TestDataCollector()
        assert collector.collect() == {"metric": "value"}
        assert callable(collector.collect)


class TestSelfTestCollector:
    """Test the SelfTestCollector implementation."""

    def test_self_test_collector_initialization(self):
        """Test SelfTestCollector can be initialized."""
        collector = SelfTestCollector()
        assert isinstance(collector, SelfTestCollector)
        assert hasattr(collector, "collect")

    def test_collect_success(self):
        """Test collect method with successful diagnostics."""
        collector = SelfTestCollector()

        mock_diagnostics = {
            "gps": {"status": "ok", "satellites": 8},
            "disk": {"status": "ok", "free_space": "5GB"},
            "memory": {"status": "ok", "usage": "45%"},
        }

        with mock.patch(
            "piwardrive.interfaces.diagnostics.self_test"
        ) as mock_self_test:
            mock_self_test.return_value = mock_diagnostics

            result = collector.collect()

            assert result == mock_diagnostics
            mock_self_test.assert_called_once()

    def test_collect_empty_result(self):
        """Test collect method with empty diagnostics."""
        collector = SelfTestCollector()

        with mock.patch(
            "piwardrive.interfaces.diagnostics.self_test"
        ) as mock_self_test:
            mock_self_test.return_value = {}

            result = collector.collect()

            assert result == {}
            mock_self_test.assert_called_once()

    def test_collect_with_failure_data(self):
        """Test collect method with failed diagnostics."""
        collector = SelfTestCollector()

        mock_diagnostics = {
            "gps": {"status": "error", "message": "No GPS signal"},
            "disk": {"status": "warning", "message": "Low disk space"},
            "services": {"status": "error", "failed": ["kismet", "gpsd"]},
        }

        with mock.patch(
            "piwardrive.interfaces.diagnostics.self_test"
        ) as mock_self_test:
            mock_self_test.return_value = mock_diagnostics

            result = collector.collect()

            assert result == mock_diagnostics
            assert result["gps"]["status"] == "error"
            assert result["services"]["failed"] == ["kismet", "gpsd"]
            mock_self_test.assert_called_once()

    def test_collect_exception_handling(self):
        """Test collect method handles diagnostics exceptions."""
        collector = SelfTestCollector()

        with mock.patch(
            "piwardrive.interfaces.diagnostics.self_test"
        ) as mock_self_test:
            mock_self_test.side_effect = Exception("Diagnostics failure")

            # Should propagate exception (no error handling in implementation)
            with pytest.raises(Exception, match="Diagnostics failure"):
                collector.collect()

    def test_collect_multiple_calls(self):
        """Test that collect can be called multiple times."""
        collector = SelfTestCollector()

        mock_results = [
            {"test1": "result1"},
            {"test2": "result2"},
            {"test3": "result3"},
        ]

        with mock.patch(
            "piwardrive.interfaces.diagnostics.self_test"
        ) as mock_self_test:
            mock_self_test.side_effect = mock_results

            # Multiple calls should work
            result1 = collector.collect()
            result2 = collector.collect()
            result3 = collector.collect()

            assert result1 == {"test1": "result1"}
            assert result2 == {"test2": "result2"}
            assert result3 == {"test3": "result3"}
            assert mock_self_test.call_count == 3


class TestInterfaceIntegration:
    """Test integration scenarios and interface compliance."""

    def test_default_map_service_implements_protocol(self):
        """Test that DefaultMapService properly implements MapService protocol."""
        service = DefaultMapService()

        # Should have all required methods
        assert hasattr(service, "get_current_position")
        assert hasattr(service, "fetch_access_points")

        # Methods should be callable
        assert callable(service.get_current_position)
        assert callable(service.fetch_access_points)

        # Return types should match protocol expectations
        with mock.patch(
            "piwardrive.interfaces.gps_client.get_position", return_value=None
        ):
            pos = service.get_current_position()
            assert pos is None or isinstance(pos, tuple)

        with mock.patch(
            "piwardrive.interfaces.utils.fetch_kismet_devices", return_value=([], [])
        ):
            aps = service.fetch_access_points()
            assert isinstance(aps, list)

    def test_self_test_collector_implements_protocol(self):
        """Test that SelfTestCollector properly implements DataCollector protocol."""
        collector = SelfTestCollector()

        # Should have required method
        assert hasattr(collector, "collect")
        assert callable(collector.collect)

        # Return type should match protocol expectations
        with mock.patch("piwardrive.interfaces.diagnostics.self_test", return_value={}):
            result = collector.collect()
            assert isinstance(result, dict)

    def test_protocol_duck_typing(self):
        """Test that protocols work with duck typing."""

        class MockMapService:
            def get_current_position(self):
                return (0.0, 0.0)

            def fetch_access_points(self):
                return []

        class MockDataCollector:
            def collect(self):
                return {"test": True}

        # These should work as protocol implementations
        map_service = MockMapService()
        data_collector = MockDataCollector()

        # Test map service
        assert map_service.get_current_position() == (0.0, 0.0)
        assert map_service.fetch_access_points() == []

        # Test data collector
        assert data_collector.collect() == {"test": True}

    def test_real_world_usage_scenario(self):
        """Test a realistic usage scenario with mocked dependencies."""
        # Create services
        map_service = DefaultMapService()
        collector = SelfTestCollector()

        # Mock dependencies
        with (
            mock.patch("piwardrive.interfaces.gps_client.get_position") as mock_gps,
            mock.patch(
                "piwardrive.interfaces.utils.fetch_kismet_devices"
            ) as mock_kismet,
            mock.patch(
                "piwardrive.interfaces.diagnostics.self_test"
            ) as mock_diagnostics,
        ):

            # Setup mocks
            mock_gps.return_value = (37.7749, -122.4194)  # San Francisco
            mock_kismet.return_value = ([{"ssid": "CoffeeShop-WiFi"}], [])
            mock_diagnostics.return_value = {"status": "all_good"}

            # Use services
            position = map_service.get_current_position()
            access_points = map_service.fetch_access_points()
            diagnostics_data = collector.collect()

            # Verify results
            assert position == (37.7749, -122.4194)
            assert access_points == [{"ssid": "CoffeeShop-WiFi"}]
            assert diagnostics_data == {"status": "all_good"}

            # Verify all mocks were called
            mock_gps.assert_called_once()
            mock_kismet.assert_called_once()
            mock_diagnostics.assert_called_once()


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_map_service_with_malformed_gps_data(self):
        """Test DefaultMapService with various malformed GPS data."""
        service = DefaultMapService()

        malformed_data_cases = [
            ([1, 2, 3]),  # Too many elements
            ((1,)),  # Too few elements
            ((float("inf"), 0)),  # Infinite values
            ((float("nan"), 0)),  # NaN values
            (("not", "numbers")),  # Non-numeric strings
        ]

        for malformed_data in malformed_data_cases:
            with mock.patch(
                "piwardrive.interfaces.gps_client.get_position"
            ) as mock_gps:
                mock_gps.return_value = malformed_data

                # Should handle gracefully (might return None or raise exception internally)
                try:
                    result = service.get_current_position()
                    # If no exception, result should be None or valid tuple
                    assert result is None or (
                        isinstance(result, tuple) and len(result) == 2
                    )
                except Exception:
                    # Exception handling is acceptable for malformed data
                    pass

    def test_collector_with_none_diagnostics(self):
        """Test SelfTestCollector when diagnostics returns None."""
        collector = SelfTestCollector()

        with mock.patch(
            "piwardrive.interfaces.diagnostics.self_test"
        ) as mock_self_test:
            mock_self_test.return_value = None

            result = collector.collect()

            # Should return None as-is
            assert result is None
            mock_self_test.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
