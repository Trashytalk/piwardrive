#!/usr/bin/env python3
"""
Staging Environment Test Suite for PiWardrive

This module provides comprehensive testing for the staging environment
including functionality, performance, and integration tests.
"""

import asyncio
import os
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Dict, Optional

import aiohttp
import pytest
import requests


@dataclass
class EndpointTest:
    """Test configuration for an API endpoint."""

    path: str
    method: str = "GET"
    expected_status: int = 200
    auth_required: bool = False
    payload: Optional[Dict] = None
    headers: Optional[Dict] = None
    timeout: int = 30


class StagingEnvironmentTester:
    """Main class for staging environment testing."""

    def __init__(self, base_url: str = "http://staging.piwardrive.local"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.timeout = 30

        # Configure auth if needed
        self.auth_token = os.getenv("STAGING_AUTH_TOKEN")
        if self.auth_token:
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})

    def test_health_check(self):
        """Test basic health check endpoint."""
        response = self.session.get(f"{self.base_url}/health")
        assert response.status_code == 200

        health_data = response.json()
        assert health_data.get("status") == "healthy"
        assert "timestamp" in health_data
        assert "version" in health_data

    def test_database_connectivity(self):
        """Test database connectivity."""
        response = self.session.get(f"{self.base_url}/api/health/database")
        assert response.status_code == 200

        db_health = response.json()
        assert db_health.get("status") == "healthy"
        assert "connection_time" in db_health
        assert db_health["connection_time"] < 1.0  # Should connect within 1 second

    def test_critical_endpoints(self):
        """Test all critical API endpoints."""
        critical_endpoints = [
            EndpointTest("/api/wifi/networks", "GET", 200),
            EndpointTest("/api/bluetooth/devices", "GET", 200),
            EndpointTest("/api/status", "GET", 200),
            EndpointTest("/api/config", "GET", 200),
            EndpointTest("/api/health", "GET", 200),
            EndpointTest("/api/metrics", "GET", 200),
            EndpointTest("/api/logs", "GET", 200, auth_required=True),
            EndpointTest("/api/admin/stats", "GET", 200, auth_required=True),
        ]

        for endpoint in critical_endpoints:
            self._test_endpoint(endpoint)

    def _test_endpoint(self, endpoint: EndpointTest):
        """Test a single endpoint."""
        url = f"{self.base_url}{endpoint.path}"
        headers = endpoint.headers or {}

        if endpoint.auth_required and not self.auth_token:
            pytest.skip(f"Skipping {endpoint.path} - no auth token provided")

        response = self.session.request(
            endpoint.method,
            url,
            json=endpoint.payload,
            headers=headers,
            timeout=endpoint.timeout,
        )

        # Check status code
        assert (
            response.status_code == endpoint.expected_status
        ), f"Expected {endpoint.expected_status}, got {response.status_code} for {endpoint.path}"

        # Check response time
        assert (
            response.elapsed.total_seconds() < endpoint.timeout
        ), f"Response time {response.elapsed.total_seconds()}s exceeded timeout {endpoint.timeout}s"

        # Check content type for JSON endpoints
        if endpoint.expected_status == 200 and endpoint.path.startswith("/api/"):
            assert "application/json" in response.headers.get(
                "content-type", ""
            ), f"Expected JSON response for {endpoint.path}"

    def test_external_service_integration(self):
        """Test external service integrations."""
        # Test WiGLE API integration
        response = self.session.get(f"{self.base_url}/api/external/wigle/test")
        if response.status_code != 503:  # Service unavailable is acceptable
            assert response.status_code == 200
            wigle_data = response.json()
            assert "status" in wigle_data

        # Test weather API integration
        response = self.session.get(f"{self.base_url}/api/external/weather/test")
        if response.status_code != 503:
            assert response.status_code == 200
            weather_data = response.json()
            assert "status" in weather_data

    def test_websocket_connectivity(self):
        """Test WebSocket connections."""
        # This would require a WebSocket client library
        # For now, we'll test the WebSocket endpoint availability
        response = self.session.get(f"{self.base_url}/api/websocket/info")
        if response.status_code == 200:
            ws_info = response.json()
            assert "websocket_url" in ws_info
            assert "supported_protocols" in ws_info


@pytest.mark.staging
class TestStagingEnvironment:
    """Staging environment test class."""

    @pytest.fixture(scope="class")
    def staging_tester(self):
        """Create staging environment tester."""
        base_url = os.getenv("STAGING_URL", "http://staging.piwardrive.local")
        return StagingEnvironmentTester(base_url)

    def test_basic_connectivity(self, staging_tester):
        """Test basic connectivity to staging environment."""
        staging_tester.test_health_check()

    def test_database_health(self, staging_tester):
        """Test database health in staging."""
        staging_tester.test_database_connectivity()

    def test_all_endpoints_accessible(self, staging_tester):
        """Test all critical endpoints are accessible."""
        staging_tester.test_critical_endpoints()

    def test_external_integrations(self, staging_tester):
        """Test external service integrations."""
        staging_tester.test_external_service_integration()

    def test_websocket_support(self, staging_tester):
        """Test WebSocket connectivity."""
        staging_tester.test_websocket_connectivity()


@pytest.mark.staging
@pytest.mark.performance
class TestStagingPerformance:
    """Staging environment performance tests."""

    @pytest.fixture(scope="class")
    def staging_url(self):
        """Get staging URL."""
        return os.getenv("STAGING_URL", "http://staging.piwardrive.local")

    def test_api_response_times(self, staging_url):
        """Test API response times meet requirements."""
        endpoints = [
            "/api/wifi/networks",
            "/api/bluetooth/devices",
            "/api/status",
            "/health",
        ]

        for endpoint in endpoints:
            start_time = time.perf_counter()
            response = requests.get(f"{staging_url}{endpoint}", timeout=10)
            end_time = time.perf_counter()

            assert response.status_code in [200, 401], f"Endpoint {endpoint} failed"
            assert (
                end_time - start_time
            ) < 2.0, f"Endpoint {endpoint} too slow: {end_time - start_time}s"

    def test_concurrent_request_handling(self, staging_url):
        """Test concurrent request handling."""

        def make_request():
            try:
                response = requests.get(f"{staging_url}/api/status", timeout=10)
                return response.status_code == 200
            except:
                return False

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [f.result() for f in futures]

        success_count = sum(1 for r in results if r)
        success_rate = success_count / len(results)

        assert success_rate >= 0.90, f"Success rate too low: {success_rate:.2%}"

    def test_database_performance(self, staging_url):
        """Test database query performance."""
        start_time = time.perf_counter()
        response = requests.get(f"{staging_url}/api/health/database", timeout=10)
        end_time = time.perf_counter()

        assert response.status_code == 200
        db_health = response.json()

        # Check response time
        response_time = end_time - start_time
        assert response_time < 1.0, f"Database health check too slow: {response_time}s"

        # Check reported connection time
        if "connection_time" in db_health:
            assert (
                db_health["connection_time"] < 0.5
            ), f"Database connection too slow: {db_health['connection_time']}s"

    def test_memory_usage(self, staging_url):
        """Test memory usage is within acceptable limits."""
        response = requests.get(f"{staging_url}/api/system/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            if "memory_usage_percent" in stats:
                assert (
                    stats["memory_usage_percent"] < 85.0
                ), f"Memory usage too high: {stats['memory_usage_percent']}%"

    def test_load_testing(self, staging_url):
        """Perform basic load testing."""

        async def make_async_request(session, url):
            try:
                async with session.get(url, timeout=10) as response:
                    return response.status == 200
            except:
                return False

        async def run_load_test():
            async with aiohttp.ClientSession() as session:
                tasks = []
                for _ in range(100):
                    task = make_async_request(session, f"{staging_url}/api/status")
                    tasks.append(task)

                results = await asyncio.gather(*tasks)
                return results

        # Run the async load test
        results = asyncio.run(run_load_test())
        success_count = sum(1 for r in results if r)
        success_rate = success_count / len(results)

        assert (
            success_rate >= 0.85
        ), f"Load test success rate too low: {success_rate:.2%}"


@pytest.mark.staging
@pytest.mark.integration
class TestStagingIntegration:
    """Staging environment integration tests."""

    @pytest.fixture(scope="class")
    def staging_url(self):
        """Get staging URL."""
        return os.getenv("STAGING_URL", "http://staging.piwardrive.local")

    def test_full_wifi_scan_workflow(self, staging_url):
        """Test complete WiFi scanning workflow."""
        # Start a scan
        response = requests.post(f"{staging_url}/api/wifi/scan/start", timeout=30)
        if response.status_code == 200:
            scan_id = response.json().get("scan_id")

            # Wait for scan to complete
            timeout = 60
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{staging_url}/api/wifi/scan/{scan_id}/status", timeout=10
                )
                if status_response.status_code == 200:
                    status = status_response.json()
                    if status.get("status") == "completed":
                        break
                time.sleep(2)

            # Get scan results
            results_response = requests.get(
                f"{staging_url}/api/wifi/scan/{scan_id}/results", timeout=10
            )
            assert results_response.status_code == 200

            results = results_response.json()
            assert "networks" in results
            assert isinstance(results["networks"], list)

    def test_bluetooth_scan_workflow(self, staging_url):
        """Test complete Bluetooth scanning workflow."""
        # Start a Bluetooth scan
        response = requests.post(f"{staging_url}/api/bluetooth/scan/start", timeout=30)
        if response.status_code == 200:
            scan_id = response.json().get("scan_id")

            # Wait for scan to complete
            timeout = 60
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{staging_url}/api/bluetooth/scan/{scan_id}/status", timeout=10
                )
                if status_response.status_code == 200:
                    status = status_response.json()
                    if status.get("status") == "completed":
                        break
                time.sleep(2)

            # Get scan results
            results_response = requests.get(
                f"{staging_url}/api/bluetooth/scan/{scan_id}/results", timeout=10
            )
            assert results_response.status_code == 200

            results = results_response.json()
            assert "devices" in results
            assert isinstance(results["devices"], list)

    def test_data_export_workflow(self, staging_url):
        """Test data export functionality."""
        # Request data export
        export_request = {
            "format": "json",
            "date_range": {"start": "2024-01-01", "end": "2024-12-31"},
            "data_types": ["wifi", "bluetooth"],
        }

        response = requests.post(
            f"{staging_url}/api/export/request", json=export_request, timeout=30
        )

        if response.status_code == 200:
            export_id = response.json().get("export_id")

            # Wait for export to complete
            timeout = 120
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_response = requests.get(
                    f"{staging_url}/api/export/{export_id}/status", timeout=10
                )
                if status_response.status_code == 200:
                    status = status_response.json()
                    if status.get("status") == "completed":
                        break
                time.sleep(5)

            # Check export file availability
            download_response = requests.get(
                f"{staging_url}/api/export/{export_id}/download", timeout=30
            )
            assert download_response.status_code == 200
            assert len(download_response.content) > 0


if __name__ == "__main__":
    # Run staging tests
    pytest.main([__file__, "-v", "-m", "staging", "--tb=short"])
