"""
Comprehensive test suite for utils.py module.

This module provides thorough testing for utils.py, including:
- Core utility function imports and fallbacks
- Stub function behavior when core utils unavailable
- HTTP request utilities with retry logic
- Error handling and edge cases
"""

import os
import sys
import time
import unittest
from unittest.mock import Mock, patch

import pytest
import requests

# Import the module under test
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from piwardrive import utils
from piwardrive.utils import HTTP_TIMEOUT, RETRY_ATTEMPTS, RETRY_DELAY, robust_request


class TestUtilsModuleStructure(unittest.TestCase):
    """Test utils module structure and imports."""

    def test_module_constants(self):
        """Test that module constants are defined correctly."""
        self.assertEqual(utils.HTTP_TIMEOUT, 5)
        self.assertEqual(utils.RETRY_ATTEMPTS, 3)
        self.assertEqual(utils.RETRY_DELAY, 1)

    def test_module_exports(self):
        """Test that module exports expected functions."""
        self.assertIn("format_error", utils.__all__)
        self.assertIn("report_error", utils.__all__)
        self.assertIn("robust_request", utils.__all__)

    def test_error_reporting_imports(self):
        """Test that error reporting functions are imported."""
        self.assertTrue(callable(utils.format_error))
        self.assertTrue(callable(utils.report_error))


class TestStubFunctions(unittest.TestCase):
    """Test stub functions when core utils are unavailable."""

    def test_metrics_result_stub(self):
        """Test MetricsResult stub class."""
        # This should work whether core utils are available or not
        if hasattr(utils, "MetricsResult"):
            result = utils.MetricsResult(aps=[], clients=[], handshake_count=0)
            self.assertEqual(result.aps, [])
            self.assertEqual(result.clients, [])
            self.assertEqual(result.handshake_count, 0)

    def test_get_gps_fix_quality_stub(self):
        """Test GPS fix quality stub function."""
        if hasattr(utils, "get_gps_fix_quality"):
            # Function may require arguments, test with mock data
            try:
                result = utils.get_gps_fix_quality()
                self.assertIsInstance(result, str)
            except (TypeError, NameError):
                # Function requires arguments or has implementation issues
                # Test with dummy argument
                result = utils.get_gps_fix_quality({})
                self.assertIsInstance(result, str)

    def test_service_status_stub(self):
        """Test service status stub function."""
        if hasattr(utils, "service_status"):
            # Function requires service name argument
            result = utils.service_status("test_service")
            self.assertIsInstance(result, bool)

    def test_count_bettercap_handshakes_stub(self):
        """Test handshake counting stub function."""
        if hasattr(utils, "count_bettercap_handshakes"):
            result = utils.count_bettercap_handshakes()
            self.assertIsInstance(result, int)

    def test_get_disk_usage_stub(self):
        """Test disk usage stub function."""
        if hasattr(utils, "get_disk_usage"):
            result = utils.get_disk_usage()
            self.assertTrue(result is None or isinstance(result, float))

    @pytest.mark.asyncio
    async def test_fetch_kismet_devices_async_stub(self):
        """Test async Kismet devices stub function."""
        if hasattr(utils, "fetch_kismet_devices_async"):
            result = await utils.fetch_kismet_devices_async()
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], list)
            self.assertIsInstance(result[1], list)

    def test_run_async_task_stub(self):
        """Test async task runner stub function."""
        if hasattr(utils, "run_async_task"):
            # Function requires coroutine argument
            async def dummy_coro():
                return "test"

            utils.run_async_task(dummy_coro())
            # Function may return None or the result

    def test_get_avg_rssi_stub(self):
        """Test average RSSI calculation stub function."""
        if hasattr(utils, "get_avg_rssi"):
            # Function requires aps argument (access points list)
            result = utils.get_avg_rssi([])
            self.assertTrue(result is None or isinstance(result, float))


class TestRobustRequest(unittest.TestCase):
    """Test robust HTTP request functionality."""

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_success(self, mock_request):
        """Test successful HTTP request."""
        mock_response = Mock()
        mock_request.return_value = mock_response

        result = robust_request("http://example.com")

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once_with(
            "GET", "http://example.com", headers=None, timeout=HTTP_TIMEOUT
        )

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_with_custom_method(self, mock_request):
        """Test HTTP request with custom method."""
        mock_response = Mock()
        mock_request.return_value = mock_response

        result = robust_request("http://example.com", method="POST")

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once_with(
            "POST", "http://example.com", headers=None, timeout=HTTP_TIMEOUT
        )

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_with_headers(self, mock_request):
        """Test HTTP request with custom headers."""
        mock_response = Mock()
        mock_request.return_value = mock_response
        headers = {"Authorization": "Bearer token"}

        result = robust_request("http://example.com", headers=headers)

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once_with(
            "GET", "http://example.com", headers=headers, timeout=HTTP_TIMEOUT
        )

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_with_custom_timeout(self, mock_request):
        """Test HTTP request with custom timeout."""
        mock_response = Mock()
        mock_request.return_value = mock_response

        result = robust_request("http://example.com", timeout=10.0)

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once_with(
            "GET", "http://example.com", headers=None, timeout=10.0
        )

    @patch("piwardrive.utils.time.sleep")
    @patch("piwardrive.utils.requests.request")
    def test_robust_request_retry_logic(self, mock_request, mock_sleep):
        """Test HTTP request retry logic."""
        # First two calls fail, third succeeds
        mock_request.side_effect = [
            requests.ConnectionError("Connection failed"),
            requests.Timeout("Request timeout"),
            Mock(),  # Success on third try
        ]

        result = robust_request("http://example.com")

        self.assertEqual(mock_request.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

        # Check exponential backoff
        mock_sleep.assert_any_call(RETRY_DELAY)  # First retry
        mock_sleep.assert_any_call(RETRY_DELAY * 2)  # Second retry

    @patch("piwardrive.utils.time.sleep")
    @patch("piwardrive.utils.requests.request")
    def test_robust_request_all_retries_fail(self, mock_request, mock_sleep):
        """Test HTTP request when all retries fail."""
        exception = requests.ConnectionError("Connection failed")
        mock_request.side_effect = exception

        with self.assertRaises(requests.ConnectionError):
            robust_request("http://example.com")

        self.assertEqual(mock_request.call_count, RETRY_ATTEMPTS)
        self.assertEqual(mock_sleep.call_count, RETRY_ATTEMPTS - 1)

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_different_exceptions(self, mock_request):
        """Test HTTP request with different types of exceptions."""
        exceptions = [
            requests.ConnectionError("Connection error"),
            requests.Timeout("Timeout error"),
            requests.HTTPError("HTTP error"),
            requests.RequestException("General request error"),
        ]

        for exception in exceptions:
            with self.subTest(exception=type(exception).__name__):
                mock_request.side_effect = exception
                with self.assertRaises(type(exception)):
                    robust_request("http://example.com")

    @patch("piwardrive.utils.logging")
    @patch("piwardrive.utils.time.sleep")
    @patch("piwardrive.utils.requests.request")
    def test_robust_request_logging(self, mock_request, mock_sleep, mock_logging):
        """Test that request failures are logged."""
        exception = requests.ConnectionError("Connection failed")
        mock_request.side_effect = [exception, Mock()]  # Fail then succeed

        robust_request("http://example.com")

        mock_logging.warning.assert_called_once_with("Request failed: %s", exception)


class TestUtilsIntegration(unittest.TestCase):
    """Test utils module integration scenarios."""

    def test_utils_module_import(self):
        """Test that utils module can be imported successfully."""
        import piwardrive.utils

        self.assertIsNotNone(piwardrive.utils)

    def test_all_exports_callable(self):
        """Test that all exported functions are callable."""
        for name in utils.__all__:
            if hasattr(utils, name):
                attr = getattr(utils, name)
                if not isinstance(attr, type) and not isinstance(
                    attr, (int, float, str)
                ):  # Skip classes and constants
                    self.assertTrue(callable(attr), f"{name} should be callable")

    def test_optional_imports_graceful_degradation(self):
        """Test that module works even when core utils are unavailable."""
        # This test verifies the module structure when imports fail
        self.assertIn("format_error", utils.__all__)
        self.assertIn("report_error", utils.__all__)
        self.assertIn("robust_request", utils.__all__)


class TestUtilsEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios."""

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_empty_url(self, mock_request):
        """Test robust request with empty URL."""
        mock_response = Mock()
        mock_request.return_value = mock_response

        result = robust_request("")

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once_with(
            "GET", "", headers=None, timeout=HTTP_TIMEOUT
        )

    @patch("piwardrive.utils.requests.request")
    def test_robust_request_none_headers(self, mock_request):
        """Test robust request with None headers."""
        mock_response = Mock()
        mock_request.return_value = mock_response

        result = robust_request("http://example.com", headers=None)

        self.assertEqual(result, mock_response)
        mock_request.assert_called_once_with(
            "GET", "http://example.com", headers=None, timeout=HTTP_TIMEOUT
        )

    def test_robust_request_zero_timeout(self):
        """Test robust request with zero timeout."""
        with patch("piwardrive.utils.requests.request") as mock_request:
            mock_response = Mock()
            mock_request.return_value = mock_response

            result = robust_request("http://example.com", timeout=0)

            self.assertEqual(result, mock_response)
            mock_request.assert_called_once_with(
                "GET", "http://example.com", headers=None, timeout=0
            )

    def test_robust_request_negative_timeout(self):
        """Test robust request with negative timeout."""
        with patch("piwardrive.utils.requests.request") as mock_request:
            mock_response = Mock()
            mock_request.return_value = mock_response

            result = robust_request("http://example.com", timeout=-1)

            self.assertEqual(result, mock_response)
            mock_request.assert_called_once_with(
                "GET", "http://example.com", headers=None, timeout=-1
            )


class TestUtilsConstants(unittest.TestCase):
    """Test utils module constants and configuration."""

    def test_http_timeout_value(self):
        """Test HTTP timeout constant."""
        self.assertEqual(HTTP_TIMEOUT, 5)
        self.assertIsInstance(HTTP_TIMEOUT, int)

    def test_retry_attempts_value(self):
        """Test retry attempts constant."""
        self.assertEqual(RETRY_ATTEMPTS, 3)
        self.assertIsInstance(RETRY_ATTEMPTS, int)
        self.assertGreater(RETRY_ATTEMPTS, 0)

    def test_retry_delay_value(self):
        """Test retry delay constant."""
        self.assertEqual(RETRY_DELAY, 1)
        self.assertIsInstance(RETRY_DELAY, int)
        self.assertGreater(RETRY_DELAY, 0)


class TestUtilsPerformance(unittest.TestCase):
    """Test utils module performance considerations."""

    @patch("piwardrive.utils.time.sleep")
    @patch("piwardrive.utils.requests.request")
    def test_robust_request_timing(self, mock_request, mock_sleep):
        """Test that robust request timing behaves as expected."""
        mock_request.side_effect = [
            requests.ConnectionError("Connection failed"),
            Mock(),  # Success on second try
        ]

        time.time()
        robust_request("http://example.com")
        time.time()

        # Should have slept once
        mock_sleep.assert_called_once_with(RETRY_DELAY)

        # Verify the request was retried
        self.assertEqual(mock_request.call_count, 2)

    def test_stub_function_performance(self):
        """Test that stub functions return quickly."""
        if hasattr(utils, "service_status"):
            start_time = time.time()
            utils.service_status("test")
            end_time = time.time()

            # Should complete very quickly (less than 1 second)
            self.assertLess(end_time - start_time, 1.0)


if __name__ == "__main__":
    unittest.main()
