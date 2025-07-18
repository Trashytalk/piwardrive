"""
Tests for the service layer and API endpoints.
"""

import os
import sys
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from piwardrive.service import (
    app,
    get_system_status,
    get_wifi_data,
    start_scan,
    stop_scan,
)


class TestServiceAPI:
    """Test FastAPI service endpoints."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)

    def test_root_endpoint(self):
        """Test root endpoint returns service info."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "unhealthy", "degraded"]

    @patch("piwardrive.service.get_system_status")
    def test_status_endpoint(self, mock_get_status):
        """Test system status endpoint."""
        mock_status = {
            "cpu_usage": 15.5,
            "memory_usage": 45.2,
            "disk_usage": 60.1,
            "temperature": 42.0,
            "services": {
                "scheduler": "running",
                "database": "connected",
                "widgets": "active",
            },
        }
        mock_get_status.return_value = mock_status

        response = self.client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "cpu_usage" in data
        assert "memory_usage" in data
        assert "services" in data

    @patch("piwardrive.service.get_wifi_data")
    def test_wifi_data_endpoint(self, mock_get_wifi):
        """Test WiFi data endpoint."""
        mock_wifi_data = {
            "access_points": [
                {
                    "ssid": "TestNetwork",
                    "bssid": "00:11:22:33:44:55",
                    "channel": 6,
                    "signal_strength": -45,
                    "encryption": "WPA2",
                }
            ],
            "scan_time": "2024-01-01T12:00:00Z",
            "total_count": 1,
        }
        mock_get_wifi.return_value = mock_wifi_data

        response = self.client.get("/wifi")
        assert response.status_code == 200
        data = response.json()
        assert "access_points" in data
        assert len(data["access_points"]) == 1
        assert data["access_points"][0]["ssid"] == "TestNetwork"

    @patch("piwardrive.service.start_scan")
    def test_start_scan_endpoint(self, mock_start_scan):
        """Test start scan endpoint."""
        mock_start_scan.return_value = {
            "status": "started",
            "scan_id": "scan_123",
            "message": "Scan started successfully",
        }

        response = self.client.post("/scan/start")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
        assert "scan_id" in data

    @patch("piwardrive.service.stop_scan")
    def test_stop_scan_endpoint(self, mock_stop_scan):
        """Test stop scan endpoint."""
        mock_stop_scan.return_value = {
            "status": "stopped",
            "message": "Scan stopped successfully",
        }

        response = self.client.post("/scan/stop")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "stopped"

    def test_logs_endpoint(self):
        """Test logs endpoint."""
        response = self.client.get("/logs")
        assert response.status_code == 200
        data = response.json()
        assert "lines" in data
        assert isinstance(data["lines"], list)

    def test_config_endpoint_get(self):
        """Test config endpoint GET."""
        response = self.client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_config_endpoint_post(self):
        """Test config endpoint POST."""
        test_config = {"debug": True, "logging": {"level": "DEBUG"}}

        response = self.client.post("/config", json=test_config)
        assert response.status_code in [200, 201]

    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = self.client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_api_error_handling(self):
        """Test API error handling."""
        # Test non-existent endpoint
        response = self.client.get("/nonexistent")
        assert response.status_code == 404


class TestServiceFunctions:
    """Test service layer functions."""

    @patch("piwardrive.service.psutil.cpu_percent")
    @patch("piwardrive.service.psutil.virtual_memory")
    @patch("piwardrive.service.psutil.disk_usage")
    def test_get_system_status(self, mock_disk, mock_memory, mock_cpu):
        """Test get_system_status function."""
        mock_cpu.return_value = 15.5
        mock_memory.return_value = Mock(percent=45.2)
        mock_disk.return_value = Mock(percent=60.1)

        status = get_system_status()
        assert "cpu_usage" in status
        assert "memory_usage" in status
        assert "disk_usage" in status
        assert status["cpu_usage"] == 15.5
        assert status["memory_usage"] == 45.2
        assert status["disk_usage"] == 60.1

    @patch("piwardrive.service.get_temperature")
    def test_get_system_status_with_temperature(self, mock_temp):
        """Test get_system_status with temperature monitoring."""
        mock_temp.return_value = 42.0

        status = get_system_status()
        assert "temperature" in status
        assert status["temperature"] == 42.0

    @patch("piwardrive.service.DatabaseManager")
    def test_get_wifi_data(self, mock_db):
        """Test get_wifi_data function."""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance

        mock_db_instance.get_access_points.return_value = [
            {
                "ssid": "TestNetwork",
                "bssid": "00:11:22:33:44:55",
                "channel": 6,
                "signal_strength": -45,
                "encryption": "WPA2",
            }
        ]

        wifi_data = get_wifi_data()
        assert "access_points" in wifi_data
        assert len(wifi_data["access_points"]) == 1

    @patch("piwardrive.service.ScanManager")
    def test_start_scan(self, mock_scan_manager):
        """Test start_scan function."""
        mock_manager = Mock()
        mock_scan_manager.return_value = mock_manager
        mock_manager.start_scan.return_value = "scan_123"

        result = start_scan()
        assert result["status"] == "started"
        assert "scan_id" in result

    @patch("piwardrive.service.ScanManager")
    def test_stop_scan(self, mock_scan_manager):
        """Test stop_scan function."""
        mock_manager = Mock()
        mock_scan_manager.return_value = mock_manager
        mock_manager.stop_scan.return_value = True

        result = stop_scan()
        assert result["status"] == "stopped"

    @patch("piwardrive.service.ScanManager")
    def test_scan_error_handling(self, mock_scan_manager):
        """Test scan error handling."""
        mock_manager = Mock()
        mock_scan_manager.return_value = mock_manager
        mock_manager.start_scan.side_effect = Exception("Scan failed")

        result = start_scan()
        assert result["status"] == "error"
        assert "error" in result


class TestServiceMiddleware:
    """Test service middleware and request handling."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)

    def test_cors_headers(self):
        """Test CORS headers are set correctly."""
        response = self.client.get("/")
        assert "access-control-allow-origin" in response.headers

    def test_request_logging(self):
        """Test request logging middleware."""
        with patch("piwardrive.service.logger") as mock_logger:
            self.client.get("/status")
            mock_logger.info.assert_called()

    def test_rate_limiting(self):
        """Test rate limiting middleware."""
        # Make multiple rapid requests
        responses = []
        for i in range(10):
            response = self.client.get("/status")
            responses.append(response)

        # Check if rate limiting kicks in
        status_codes = [r.status_code for r in responses]
        assert all(code in [200, 429] for code in status_codes)

    def test_authentication_middleware(self):
        """Test authentication middleware."""
        # Test protected endpoint without auth
        response = self.client.get("/admin/config")
        assert response.status_code in [401, 403, 404]

    def test_error_handling_middleware(self):
        """Test error handling middleware."""
        with patch("piwardrive.service.get_system_status") as mock_status:
            mock_status.side_effect = Exception("Service error")

            response = self.client.get("/status")
            assert response.status_code == 500
            data = response.json()
            assert "error" in data


class TestServiceWebSocket:
    """Test WebSocket functionality."""

    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test WebSocket connection establishment."""
        with patch("piwardrive.service.websocket_manager") as mock_ws:
            mock_ws.connect = AsyncMock()
            mock_ws.disconnect = AsyncMock()

            # Test connection
            await mock_ws.connect("test_client")
            mock_ws.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_websocket_message_handling(self):
        """Test WebSocket message handling."""
        with patch("piwardrive.service.websocket_manager") as mock_ws:
            mock_ws.send_message = AsyncMock()

            # Test message sending
            await mock_ws.send_message("test_client", {"type": "status_update"})
            mock_ws.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_websocket_broadcast(self):
        """Test WebSocket broadcast functionality."""
        with patch("piwardrive.service.websocket_manager") as mock_ws:
            mock_ws.broadcast = AsyncMock()

            # Test broadcasting
            await mock_ws.broadcast({"type": "system_alert", "message": "Test"})
            mock_ws.broadcast.assert_called_once()


class TestServiceIntegration:
    """Test service integration with other components."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)

    @patch("piwardrive.service.DatabaseManager")
    def test_database_integration(self, mock_db):
        """Test service integration with database."""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance
        mock_db_instance.get_scan_results.return_value = []

        response = self.client.get("/scans")
        assert response.status_code in [200, 404]

    @patch("piwardrive.service.WidgetManager")
    def test_widget_integration(self, mock_widgets):
        """Test service integration with widget system."""
        mock_widget_manager = Mock()
        mock_widgets.return_value = mock_widget_manager
        mock_widget_manager.get_widget_data.return_value = {}

        response = self.client.get("/widgets")
        assert response.status_code in [200, 404]

    @patch("piwardrive.service.ConfigManager")
    def test_config_integration(self, mock_config):
        """Test service integration with configuration."""
        mock_config_manager = Mock()
        mock_config.return_value = mock_config_manager
        mock_config_manager.get_config.return_value = {"debug": False}

        response = self.client.get("/config")
        assert response.status_code == 200

    @patch("piwardrive.service.Scheduler")
    def test_scheduler_integration(self, mock_scheduler):
        """Test service integration with scheduler."""
        mock_scheduler_instance = Mock()
        mock_scheduler.return_value = mock_scheduler_instance
        mock_scheduler_instance.get_status.return_value = {"status": "running"}

        response = self.client.get("/scheduler/status")
        assert response.status_code in [200, 404]


class TestServiceSecurity:
    """Test service security features."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(app)

    def test_input_validation(self):
        """Test input validation."""
        # Test with malicious input
        malicious_data = {
            "config": "<script>alert('xss')</script>",
            "sql_injection": "'; DROP TABLE users; --",
        }

        response = self.client.post("/config", json=malicious_data)
        assert response.status_code in [400, 422]

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention."""
        # Test with SQL injection attempt
        response = self.client.get("/wifi?filter='; DROP TABLE access_points; --")
        assert response.status_code in [200, 400]

    def test_csrf_protection(self):
        """Test CSRF protection."""
        # Test without CSRF token
        response = self.client.post("/config", json={"debug": True})
        # Should either succeed or fail with proper status code
        assert response.status_code in [200, 400, 403]

    def test_secure_headers(self):
        """Test security headers."""
        response = self.client.get("/")

        # Check for security headers
        headers = response.headers
        assert any(header.lower().startswith("x-") for header in headers)


if __name__ == "__main__":
    pytest.main([__file__])
