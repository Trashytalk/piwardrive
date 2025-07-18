"""Tests for the coordinator service module."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from piwardrive.services.cluster_manager import ClusterManager, DeviceStatus
from piwardrive.services.coordinator import (
    aggregate_distributed_results,
    coordinate_scanning_tasks,
    manage_device_fleet,
    synchronize_configurations,
)


class TestCoordinateScanning:
    """Test suite for scanning task coordination."""

    @pytest.fixture
    def mock_cluster_manager(self):
        """Create a mock cluster manager."""
        manager = MagicMock(spec=ClusterManager)
        return manager

    @pytest.fixture
    def sample_device(self):
        """Create a sample device for testing."""
        return DeviceStatus(
            id="device-1",
            address="192.168.1.100:8080",
            load=0,
            capabilities=["wifi", "bluetooth"],
        )

    @pytest.fixture
    def sample_tasks(self):
        """Create sample scanning tasks."""
        return [
            {"type": "wifi_scan", "duration": 60, "channels": [1, 6, 11]},
            {"type": "bluetooth_scan", "duration": 30, "power": "high"},
            {"type": "cellular_scan", "duration": 45, "bands": ["GSM", "LTE"]},
        ]

    @pytest.mark.asyncio
    async def test_coordinate_scanning_tasks_success(
        self, mock_cluster_manager, sample_device, sample_tasks
    ):
        """Test successful coordination of scanning tasks."""
        mock_cluster_manager.select_device_for_task.return_value = sample_device

        with patch("piwardrive.services.coordinator._dispatch_task") as mock_dispatch:
            result = await coordinate_scanning_tasks(sample_tasks, mock_cluster_manager)

            assert len(result) == 1
            assert "device-1" in result
            assert len(result["device-1"]) == 3
            assert result["device-1"] == sample_tasks

            # Verify dispatch was called for each task
            assert mock_dispatch.call_count == 3

            # Verify load was incremented
            assert sample_device.load == 3

    @pytest.mark.asyncio
    async def test_coordinate_scanning_tasks_no_devices(
        self, mock_cluster_manager, sample_tasks
    ):
        """Test coordination when no devices are available."""
        mock_cluster_manager.select_device_for_task.return_value = None

        with patch("piwardrive.services.coordinator.logger.warning") as mock_warning:
            result = await coordinate_scanning_tasks(sample_tasks, mock_cluster_manager)

            assert result == {}
            mock_warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_coordinate_scanning_tasks_empty_tasks(self, mock_cluster_manager):
        """Test coordination with empty task list."""
        result = await coordinate_scanning_tasks([], mock_cluster_manager)

        assert result == {}
        mock_cluster_manager.select_device_for_task.assert_not_called()

    @pytest.mark.asyncio
    async def test_coordinate_scanning_tasks_multiple_devices(
        self, mock_cluster_manager, sample_tasks
    ):
        """Test coordination with multiple devices."""
        device1 = DeviceStatus(id="device-1", address="192.168.1.100:8080", load=0)
        device2 = DeviceStatus(id="device-2", address="192.168.1.101:8080", load=0)

        mock_cluster_manager.select_device_for_task.side_effect = [
            device1,
            device2,
            device1,
        ]

        with patch("piwardrive.services.coordinator._dispatch_task") as mock_dispatch:
            result = await coordinate_scanning_tasks(sample_tasks, mock_cluster_manager)

            assert len(result) == 2
            assert "device-1" in result
            assert "device-2" in result
            assert len(result["device-1"]) == 2
            assert len(result["device-2"]) == 1

            assert mock_dispatch.call_count == 3

    @pytest.mark.asyncio
    async def test_dispatch_task_success(self, sample_device, sample_tasks):
        """Test successful task dispatch."""
        from piwardrive.services.coordinator import _dispatch_task

        with patch("aiohttp.ClientSession") as mock_session:
            mock_post = AsyncMock()
            mock_session.return_value.__aenter__.return_value.post = mock_post

            await _dispatch_task(sample_device, sample_tasks[0])

            mock_post.assert_called_once_with(
                "http://192.168.1.100:8080/api/scan", json=sample_tasks[0]
            )

    @pytest.mark.asyncio
    async def test_dispatch_task_failure(self, sample_device, sample_tasks):
        """Test task dispatch failure handling."""
        from piwardrive.services.coordinator import _dispatch_task

        with (
            patch("aiohttp.ClientSession") as mock_session,
            patch("piwardrive.services.coordinator.logger.error") as mock_error,
        ):

            mock_session.return_value.__aenter__.return_value.post.side_effect = (
                Exception("Network error")
            )

            await _dispatch_task(sample_device, sample_tasks[0])

            mock_error.assert_called_once_with(
                "Failed to dispatch task to %s: %s",
                "device-1",
                mock_session.return_value.__aenter__.return_value.post.side_effect,
            )


class TestAggregateResults:
    """Test suite for result aggregation."""

    def test_aggregate_distributed_results_success(self):
        """Test successful aggregation of distributed results."""
        results = [
            [
                {"device_id": "device-1", "ssid": "WiFi-1", "signal": -45},
                {"device_id": "device-1", "ssid": "WiFi-2", "signal": -67},
            ],
            [
                {"device_id": "device-2", "ssid": "WiFi-3", "signal": -52},
            ],
            [
                {"device_id": "device-3", "ssid": "WiFi-4", "signal": -78},
                {"device_id": "device-3", "ssid": "WiFi-5", "signal": -89},
            ],
        ]

        aggregated = aggregate_distributed_results(results)

        assert len(aggregated) == 5
        assert all("device_id" in result for result in aggregated)
        assert all("ssid" in result for result in aggregated)

    def test_aggregate_distributed_results_empty(self):
        """Test aggregation with empty results."""
        aggregated = aggregate_distributed_results([])

        assert aggregated == []

    def test_aggregate_distributed_results_single_device(self):
        """Test aggregation with single device results."""
        results = [
            [
                {"device_id": "device-1", "type": "wifi", "data": "test1"},
                {"device_id": "device-1", "type": "bluetooth", "data": "test2"},
            ]
        ]

        aggregated = aggregate_distributed_results(results)

        assert len(aggregated) == 2
        assert aggregated[0]["device_id"] == "device-1"
        assert aggregated[1]["device_id"] == "device-1"

    def test_aggregate_distributed_results_mixed_types(self):
        """Test aggregation with mixed result types."""
        results = [
            [{"type": "wifi", "ssid": "test"}],
            [{"type": "bluetooth", "device": "phone"}],
            [{"type": "cellular", "cell_id": "123"}],
        ]

        aggregated = aggregate_distributed_results(results)

        assert len(aggregated) == 3
        assert {result["type"] for result in aggregated} == {
            "wifi",
            "bluetooth",
            "cellular",
        }


class TestManageDeviceFleet:
    """Test suite for device fleet management."""

    @pytest.fixture
    def mock_cluster_manager(self):
        """Create a mock cluster manager."""
        manager = MagicMock(spec=ClusterManager)
        manager.discover_devices = AsyncMock()
        manager.collect_health_metrics = AsyncMock()
        return manager

    @pytest.mark.asyncio
    async def test_manage_device_fleet_success(self, mock_cluster_manager):
        """Test successful device fleet management."""
        result = await manage_device_fleet(mock_cluster_manager)

        assert result == mock_cluster_manager
        mock_cluster_manager.discover_devices.assert_called_once()
        mock_cluster_manager.collect_health_metrics.assert_called_once()

    @pytest.mark.asyncio
    async def test_manage_device_fleet_discovery_failure(self, mock_cluster_manager):
        """Test fleet management with discovery failure."""
        mock_cluster_manager.discover_devices.side_effect = Exception(
            "Discovery failed"
        )

        with pytest.raises(Exception, match="Discovery failed"):
            await manage_device_fleet(mock_cluster_manager)

    @pytest.mark.asyncio
    async def test_manage_device_fleet_health_failure(self, mock_cluster_manager):
        """Test fleet management with health collection failure."""
        mock_cluster_manager.collect_health_metrics.side_effect = Exception(
            "Health check failed"
        )

        with pytest.raises(Exception, match="Health check failed"):
            await manage_device_fleet(mock_cluster_manager)


class TestSynchronizeConfigurations:
    """Test suite for configuration synchronization."""

    @pytest.fixture
    def mock_cluster_manager(self):
        """Create a mock cluster manager."""
        manager = MagicMock(spec=ClusterManager)
        return manager

    @pytest.fixture
    def sample_config(self):
        """Create a sample configuration."""
        return {
            "config_version": "1.2.3",
            "scan_interval": 30,
            "max_power": 100,
            "channels": [1, 6, 11],
        }

    @pytest.fixture
    def sample_devices(self):
        """Create sample devices with different config versions."""
        return [
            DeviceStatus(
                id="device-1", address="192.168.1.100:8080", config_version="1.2.2"
            ),
            DeviceStatus(
                id="device-2", address="192.168.1.101:8080", config_version="1.2.3"
            ),
            DeviceStatus(
                id="device-3", address="192.168.1.102:8080", config_version="1.2.1"
            ),
        ]

    @pytest.mark.asyncio
    async def test_synchronize_configurations_success(
        self, mock_cluster_manager, sample_config, sample_devices
    ):
        """Test successful configuration synchronization."""
        mock_cluster_manager.list_devices.return_value = sample_devices

        with (
            patch("piwardrive.core.config.AppConfig.load") as mock_load,
            patch("piwardrive.services.coordinator._push_config") as mock_push,
        ):

            mock_config = MagicMock()
            mock_config.to_dict.return_value = sample_config
            mock_load.return_value = mock_config

            await synchronize_configurations(mock_cluster_manager)

            # Should push config to devices with outdated versions
            assert mock_push.call_count == 2
            mock_push.assert_any_call(sample_devices[0], sample_config)
            mock_push.assert_any_call(sample_devices[2], sample_config)

    @pytest.mark.asyncio
    async def test_synchronize_configurations_all_up_to_date(
        self, mock_cluster_manager, sample_config
    ):
        """Test synchronization when all devices are up to date."""
        devices = [
            DeviceStatus(
                id="device-1", address="192.168.1.100:8080", config_version="1.2.3"
            ),
            DeviceStatus(
                id="device-2", address="192.168.1.101:8080", config_version="1.2.3"
            ),
        ]
        mock_cluster_manager.list_devices.return_value = devices

        with (
            patch("piwardrive.core.config.AppConfig.load") as mock_load,
            patch("piwardrive.services.coordinator._push_config") as mock_push,
        ):

            mock_config = MagicMock()
            mock_config.to_dict.return_value = sample_config
            mock_load.return_value = mock_config

            await synchronize_configurations(mock_cluster_manager)

            mock_push.assert_not_called()

    @pytest.mark.asyncio
    async def test_synchronize_configurations_no_devices(
        self, mock_cluster_manager, sample_config
    ):
        """Test synchronization with no devices."""
        mock_cluster_manager.list_devices.return_value = []

        with (
            patch("piwardrive.core.config.AppConfig.load") as mock_load,
            patch("piwardrive.services.coordinator._push_config") as mock_push,
        ):

            mock_config = MagicMock()
            mock_config.to_dict.return_value = sample_config
            mock_load.return_value = mock_config

            await synchronize_configurations(mock_cluster_manager)

            mock_push.assert_not_called()

    @pytest.mark.asyncio
    async def test_push_config_success(self, sample_config):
        """Test successful configuration push."""
        from piwardrive.services.coordinator import _push_config

        device = DeviceStatus(id="device-1", address="192.168.1.100:8080")

        with patch("aiohttp.ClientSession") as mock_session:
            mock_post = AsyncMock()
            mock_session.return_value.__aenter__.return_value.post = mock_post

            await _push_config(device, sample_config)

            mock_post.assert_called_once_with(
                "http://192.168.1.100:8080/api/config", json=sample_config
            )
            assert device.config_version == "1.2.3"

    @pytest.mark.asyncio
    async def test_push_config_failure(self, sample_config):
        """Test configuration push failure handling."""
        from piwardrive.services.coordinator import _push_config

        device = DeviceStatus(id="device-1", address="192.168.1.100:8080")

        with (
            patch("aiohttp.ClientSession") as mock_session,
            patch("piwardrive.services.coordinator.logger.error") as mock_error,
        ):

            mock_session.return_value.__aenter__.return_value.post.side_effect = (
                Exception("Network error")
            )

            await _push_config(device, sample_config)

            mock_error.assert_called_once_with(
                "Failed to sync config to %s: %s",
                "device-1",
                mock_session.return_value.__aenter__.return_value.post.side_effect,
            )
            # Config version should not be updated on failure
            assert device.config_version is None


class TestCoordinatorModule:
    """Test suite for module-level functionality."""

    def test_module_exports(self):
        """Test that all expected functions and classes are exported."""
        from piwardrive.services.coordinator import __all__

        expected_exports = [
            "cluster_manager",
            "coordinate_scanning_tasks",
            "aggregate_distributed_results",
            "manage_device_fleet",
            "synchronize_configurations",
        ]

        assert set(__all__) == set(expected_exports)

    def test_cluster_manager_instance(self):
        """Test that cluster_manager is a ClusterManager instance."""
        from piwardrive.services.coordinator import cluster_manager

        assert isinstance(cluster_manager, ClusterManager)

    @pytest.mark.asyncio
    async def test_coordinate_scanning_tasks_default_manager(self):
        """Test that coordinate_scanning_tasks uses default manager."""
        from piwardrive.services.coordinator import coordinate_scanning_tasks

        tasks = [{"type": "test"}]

        with patch(
            "piwardrive.services.coordinator.cluster_manager.select_device_for_task"
        ) as mock_select:
            mock_select.return_value = None

            result = await coordinate_scanning_tasks(tasks)

            assert result == {}
            mock_select.assert_called_once()

    @pytest.mark.asyncio
    async def test_manage_device_fleet_default_manager(self):
        """Test that manage_device_fleet uses default manager."""
        from piwardrive.services.coordinator import manage_device_fleet

        with (
            patch(
                "piwardrive.services.coordinator.cluster_manager.discover_devices"
            ) as mock_discover,
            patch(
                "piwardrive.services.coordinator.cluster_manager.collect_health_metrics"
            ) as mock_health,
        ):

            mock_discover.return_value = AsyncMock()
            mock_health.return_value = AsyncMock()

            result = await manage_device_fleet()

            # Should return the actual cluster manager instance
            assert hasattr(result, "discover_devices")
            assert hasattr(result, "collect_health_metrics")
            mock_discover.assert_called_once()
            mock_health.assert_called_once()

    @pytest.mark.asyncio
    async def test_synchronize_configurations_default_manager(self):
        """Test that synchronize_configurations uses default manager."""
        from piwardrive.services.coordinator import synchronize_configurations

        with (
            patch(
                "piwardrive.services.coordinator.cluster_manager.list_devices"
            ) as mock_list,
            patch("piwardrive.core.config.AppConfig.load") as mock_load,
        ):

            mock_list.return_value = []
            mock_config = MagicMock()
            mock_config.to_dict.return_value = {"config_version": "1.0.0"}
            mock_load.return_value = mock_config

            await synchronize_configurations()

            mock_list.assert_called_once()


class TestIntegrationScenarios:
    """Test suite for integration scenarios."""

    @pytest.mark.asyncio
    async def test_full_coordination_workflow(self):
        """Test a complete coordination workflow."""
        # Create mock devices
        device1 = DeviceStatus(id="device-1", address="192.168.1.100:8080", load=0)
        device2 = DeviceStatus(id="device-2", address="192.168.1.101:8080", load=0)

        # Create mock cluster manager
        manager = MagicMock(spec=ClusterManager)
        manager.select_device_for_task.side_effect = [device1, device2, device1]
        manager.discover_devices = AsyncMock()
        manager.collect_health_metrics = AsyncMock()
        manager.list_devices.return_value = [device1, device2]

        # Create sample tasks
        tasks = [
            {"type": "wifi_scan", "duration": 60},
            {"type": "bluetooth_scan", "duration": 30},
            {"type": "cellular_scan", "duration": 45},
        ]

        with (
            patch("piwardrive.services.coordinator._dispatch_task") as mock_dispatch,
            patch("piwardrive.core.config.AppConfig.load") as mock_load,
        ):

            mock_config = MagicMock()
            mock_config.to_dict.return_value = {"config_version": "1.0.0"}
            mock_load.return_value = mock_config

            # Step 1: Manage device fleet
            await manage_device_fleet(manager)

            # Step 2: Synchronize configurations
            await synchronize_configurations(manager)

            # Step 3: Coordinate scanning tasks
            assignments = await coordinate_scanning_tasks(tasks, manager)

            # Verify workflow
            manager.discover_devices.assert_called_once()
            manager.collect_health_metrics.assert_called_once()
            assert len(assignments) == 2
            assert mock_dispatch.call_count == 3

    @pytest.mark.asyncio
    async def test_resilience_to_network_failures(self):
        """Test system resilience to network failures."""
        device = DeviceStatus(id="device-1", address="192.168.1.100:8080", load=0)
        manager = MagicMock(spec=ClusterManager)
        manager.select_device_for_task.return_value = device

        tasks = [{"type": "wifi_scan"}]

        with (
            patch("aiohttp.ClientSession") as mock_session,
            patch("piwardrive.services.coordinator.logger.error") as mock_error,
        ):

            mock_session.return_value.__aenter__.return_value.post.side_effect = (
                Exception("Network error")
            )

            # Should not raise exception, just log error
            result = await coordinate_scanning_tasks(tasks, manager)

            assert result == {"device-1": [{"type": "wifi_scan"}]}
            mock_error.assert_called_once()
            assert device.load == 1
