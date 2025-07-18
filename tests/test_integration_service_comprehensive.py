#!/usr/bin/env python3
"""Comprehensive test suite for piwardrive.services.integration_service module.

This test suite provides complete coverage for the integration_service module including:
- APIClient functionality
- STIX/TAXII integration
- Elasticsearch integration
- Grafana metrics
- Webhook broadcasting
- IntegrationMonitor
- Error handling and edge cases
"""

import asyncio
import json
import unittest.mock as mock
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from piwardrive.services import integration_service


class TestAPIClient:
    """Test suite for APIClient class."""

    def test_init_default_params(self):
        """Test APIClient initialization with default parameters."""
        client = integration_service.APIClient()

        assert client.token is None
        assert hasattr(client, "rate_limiter")

    def test_init_with_token(self):
        """Test APIClient initialization with token."""
        token = "test_token_123"
        client = integration_service.APIClient(token=token)

        assert client.token == token
        assert hasattr(client, "rate_limiter")

    @pytest.mark.asyncio
    async def test_request_with_token_auth(self):
        """Test making requests with token authentication."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}

        client = integration_service.APIClient(token="test_token")

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(client.rate_limiter, "should_allow") as mock_rate_check:
                mock_rate_check.return_value = True

                response = await client.request("GET", "https://api.example.com/data")

                # Verify request was made with correct authentication
                mock_async_client.request.assert_called_once()
                call_args = mock_async_client.request.call_args
                assert call_args[0][0] == "GET"
                assert call_args[0][1] == "https://api.example.com/data"
                assert call_args[1]["headers"]["Authorization"] == "Bearer test_token"

                assert response == mock_response

    @pytest.mark.asyncio
    async def test_request_rate_limit_exceeded(self):
        """Test request when rate limit is exceeded."""
        client = integration_service.APIClient()

        with patch.object(client.rate_limiter, "should_allow") as mock_rate_check:
            mock_rate_check.return_value = False

            with pytest.raises(RuntimeError, match="rate limit exceeded"):
                await client.request("GET", "https://api.example.com/data")


class TestSTIXTAXII:
    """Test suite for STIX/TAXII integration."""

    @pytest.mark.asyncio
    async def test_fetch_stix_taxii_success(self):
        """Test successful STIX/TAXII fetch."""
        client = integration_service.APIClient()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "objects": [
                {"type": "indicator", "id": "indicator-1", "pattern": "test"},
                {"type": "malware", "id": "malware-1", "name": "test-malware"},
            ]
        }

        with patch.object(
            client, "request", return_value=mock_response
        ) as mock_request:
            result = await integration_service.fetch_stix_taxii(
                "https://taxii.example.com", "indicators", client
            )

            # Verify correct endpoint was called
            mock_request.assert_called_once_with(
                "GET", "https://taxii.example.com/collections/indicators/objects"
            )

            # Verify result contains expected objects
            assert len(result) == 2
            assert result[0]["type"] == "indicator"
            assert result[1]["type"] == "malware"


class TestElasticsearch:
    """Test suite for Elasticsearch integration."""

    @pytest.mark.asyncio
    async def test_send_to_elasticsearch_success(self):
        """Test successful Elasticsearch send."""
        client = integration_service.APIClient()

        mock_response = MagicMock()
        mock_response.status_code = 200

        records = [{"id": 1, "message": "test1"}, {"id": 2, "message": "test2"}]

        with patch.object(
            client, "request", return_value=mock_response
        ) as mock_request:
            await integration_service.send_to_elasticsearch(
                "https://es.example.com", "test-index", records, client
            )

            # Verify correct endpoint and method
            mock_request.assert_called_once_with(
                "POST",
                "https://es.example.com/_bulk",
                content=mock.ANY,
                headers={"Content-Type": "application/x-ndjson"},
            )


class TestGrafana:
    """Test suite for Grafana metrics integration."""

    @pytest.mark.asyncio
    async def test_push_metrics_to_grafana_success(self):
        """Test successful Grafana metrics push."""
        client = integration_service.APIClient()

        mock_response = MagicMock()
        mock_response.status_code = 200

        metrics = {"cpu_usage": 75.5, "memory_usage": 60.2, "disk_usage": 45.8}

        with patch.object(
            client, "request", return_value=mock_response
        ) as mock_request:
            await integration_service.push_metrics_to_grafana(
                "https://grafana.example.com/api/metrics", metrics, client
            )

            # Verify correct request
            mock_request.assert_called_once_with(
                "POST", "https://grafana.example.com/api/metrics", json=metrics
            )


class TestWebhooks:
    """Test suite for webhook broadcasting."""

    @pytest.mark.asyncio
    async def test_broadcast_webhooks_success(self):
        """Test successful webhook broadcasting."""
        urls = [
            "https://webhook1.example.com",
            "https://webhook2.example.com",
            "https://webhook3.example.com",
        ]

        payload = {"event": "test", "data": {"id": 123}}

        with patch("httpx.AsyncClient") as mock_client:
            mock_http = AsyncMock()
            mock_http.post = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_http

            await integration_service.broadcast_webhooks(urls, payload)

            # Verify all URLs were called
            assert mock_http.post.call_count == 3

            # Verify correct payload was sent
            for call in mock_http.post.call_args_list:
                assert call[1]["json"] == payload


class TestIntegrationMonitor:
    """Test suite for IntegrationMonitor class."""

    def test_init(self):
        """Test IntegrationMonitor initialization."""
        monitor = integration_service.IntegrationMonitor()

        assert monitor.status == {}

    def test_update_success(self):
        """Test updating integration status with success."""
        monitor = integration_service.IntegrationMonitor()

        monitor.update("elasticsearch", True, "Connection successful")

        status = monitor.status["elasticsearch"]
        assert status["ok"] is True
        assert status["message"] == "Connection successful"
        assert "timestamp" in status
        assert isinstance(status["timestamp"], str)

    def test_get_status_with_integrations(self):
        """Test getting status with tracked integrations."""
        monitor = integration_service.IntegrationMonitor()

        monitor.update("elasticsearch", True, "OK")
        monitor.update("grafana", False, "Error")

        status = monitor.get_status()

        assert len(status) == 2
        assert "elasticsearch" in status
        assert "grafana" in status
        assert status["elasticsearch"]["ok"] is True
        assert status["grafana"]["ok"] is False


if __name__ == "__main__":
    pytest.main([__file__])

    @pytest.mark.asyncio
    async def test_request_with_token_auth(self):
        """Test making requests with token authentication."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}

        client = integration_service.APIClient(token="test_token")

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                response = await client.request("GET", "https://api.example.com/data")

                # Verify request was made with correct authentication
                mock_async_client.request.assert_called_once()
                call_args = mock_async_client.request.call_args
                assert call_args[0][0] == "GET"
                assert call_args[0][1] == "https://api.example.com/data"
                assert call_args[1]["headers"]["Authorization"] == "Bearer test_token"

                assert response == mock_response

    @pytest.mark.asyncio
    async def test_request_without_token(self):
        """Test making requests without token authentication."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        client = integration_service.APIClient()

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                response = await client.request("GET", "https://api.example.com/data")

                # Verify request was made without authentication header
                mock_async_client.request.assert_called_once()
                call_args = mock_async_client.request.call_args
                assert "headers" not in call_args[
                    1
                ] or "Authorization" not in call_args[1].get("headers", {})

                assert response == mock_response

    @pytest.mark.asyncio
    async def test_request_with_rate_limit_exceeded(self):
        """Test request when rate limit is exceeded."""
        client = integration_service.APIClient()

        with patch.object(client.rate_limiter, "check_rate_limit") as mock_rate_check:
            mock_rate_check.return_value = False

            with pytest.raises(RuntimeError, match="Rate limit exceeded"):
                await client.request("GET", "https://api.example.com/data")

    @pytest.mark.asyncio
    async def test_request_with_custom_headers(self):
        """Test request with custom headers."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        client = integration_service.APIClient(token="test_token")

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                custom_headers = {"X-Custom-Header": "custom_value"}
                response = await client.request(
                    "GET", "https://api.example.com/data", headers=custom_headers
                )

                # Verify both auth and custom headers are present
                call_args = mock_async_client.request.call_args
                expected_headers = {
                    "Authorization": "Bearer test_token",
                    "X-Custom-Header": "custom_value",
                }
                assert call_args[1]["headers"] == expected_headers

    @pytest.mark.asyncio
    async def test_request_with_json_data(self):
        """Test request with JSON data."""
        mock_response = MagicMock()
        mock_response.status_code = 201

        client = integration_service.APIClient()

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                json_data = {"key": "value", "number": 42}
                response = await client.request(
                    "POST", "https://api.example.com/data", json=json_data
                )

                # Verify JSON data was passed correctly
                call_args = mock_async_client.request.call_args
                assert call_args[1]["json"] == json_data

    @pytest.mark.asyncio
    async def test_request_http_error(self):
        """Test request with HTTP error."""
        client = integration_service.APIClient()

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.side_effect = httpx.HTTPStatusError(
                "Not Found", request=MagicMock(), response=MagicMock()
            )
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                with pytest.raises(httpx.HTTPStatusError):
                    await client.request("GET", "https://api.example.com/nonexistent")

    @pytest.mark.asyncio
    async def test_request_network_error(self):
        """Test request with network error."""
        client = integration_service.APIClient()

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.side_effect = httpx.NetworkError(
                "Connection failed"
            )
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                with pytest.raises(httpx.NetworkError):
                    await client.request("GET", "https://api.example.com/data")

    @pytest.mark.asyncio
    async def test_request_timeout(self):
        """Test request with timeout."""
        client = integration_service.APIClient()

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.side_effect = httpx.TimeoutException(
                "Request timeout"
            )
            mock_client.return_value.__aenter__.return_value = mock_async_client

            with patch.object(
                client.rate_limiter, "check_rate_limit"
            ) as mock_rate_check:
                mock_rate_check.return_value = True

                with pytest.raises(httpx.TimeoutException):
                    await client.request("GET", "https://api.example.com/data")

    @pytest.mark.asyncio
    async def test_multiple_requests_rate_limiting(self):
        """Test multiple requests with rate limiting."""
        client = integration_service.APIClient(max_rate=2, window=60)

        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("httpx.AsyncClient") as mock_client:
            mock_async_client = AsyncMock()
            mock_async_client.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_async_client

            # Mock rate limiter to allow first two requests, then deny
            rate_check_results = [True, True, False]
            with patch.object(
                client.rate_limiter, "check_rate_limit", side_effect=rate_check_results
            ):

                # First two requests should succeed
                response1 = await client.request("GET", "https://api.example.com/data1")
                response2 = await client.request("GET", "https://api.example.com/data2")

                assert response1 == mock_response
                assert response2 == mock_response

                # Third request should fail due to rate limit
                with pytest.raises(RuntimeError, match="Rate limit exceeded"):
                    await client.request("GET", "https://api.example.com/data3")


class TestDataSynchronizer:
    """Test suite for DataSynchronizer class."""

    def test_init(self):
        """Test DataSynchronizer initialization."""
        sync = integration_service.DataSynchronizer()

        assert sync.pending_uploads == []
        assert sync.batch_size == 100
        assert sync.max_retries == 3

    def test_init_with_custom_params(self):
        """Test DataSynchronizer initialization with custom parameters."""
        sync = integration_service.DataSynchronizer(batch_size=50, max_retries=5)

        assert sync.batch_size == 50
        assert sync.max_retries == 5

    def test_add_item(self):
        """Test adding items to sync queue."""
        sync = integration_service.DataSynchronizer()

        item1 = {"id": 1, "data": "test1"}
        item2 = {"id": 2, "data": "test2"}

        sync.add_item(item1)
        sync.add_item(item2)

        assert len(sync.pending_uploads) == 2
        assert sync.pending_uploads[0] == item1
        assert sync.pending_uploads[1] == item2

    def test_add_items_batch(self):
        """Test adding multiple items at once."""
        sync = integration_service.DataSynchronizer()

        items = [
            {"id": 1, "data": "test1"},
            {"id": 2, "data": "test2"},
            {"id": 3, "data": "test3"},
        ]

        sync.add_items(items)

        assert len(sync.pending_uploads) == 3
        assert sync.pending_uploads == items

    @pytest.mark.asyncio
    async def test_sync_empty_queue(self):
        """Test syncing with empty queue."""
        sync = integration_service.DataSynchronizer()
        client = integration_service.APIClient()

        result = await sync.sync_to_endpoint(client, "https://api.example.com/upload")

        assert result == {"uploaded": 0, "failed": 0, "errors": []}

    @pytest.mark.asyncio
    async def test_sync_successful_upload(self):
        """Test successful sync upload."""
        sync = integration_service.DataSynchronizer(batch_size=2)
        client = integration_service.APIClient()

        # Add test items
        items = [
            {"id": 1, "data": "test1"},
            {"id": 2, "data": "test2"},
            {"id": 3, "data": "test3"},
        ]
        sync.add_items(items)

        # Mock successful API responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}

        with patch.object(
            client, "request", return_value=mock_response
        ) as mock_request:
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Should make 2 requests (batch_size=2, so 2 items + 1 item)
            assert mock_request.call_count == 2
            assert result["uploaded"] == 3
            assert result["failed"] == 0
            assert result["errors"] == []

            # Queue should be empty after successful upload
            assert len(sync.pending_uploads) == 0

    @pytest.mark.asyncio
    async def test_sync_partial_failure(self):
        """Test sync with partial failure."""
        sync = integration_service.DataSynchronizer(batch_size=1)
        client = integration_service.APIClient()

        # Add test items
        items = [
            {"id": 1, "data": "test1"},
            {"id": 2, "data": "test2"},
        ]
        sync.add_items(items)

        # Mock responses: first succeeds, second fails
        mock_success = MagicMock()
        mock_success.status_code = 200
        mock_success.json.return_value = {"status": "success"}

        mock_failure = MagicMock()
        mock_failure.status_code = 500
        mock_failure.json.return_value = {"error": "Internal server error"}

        with patch.object(
            client, "request", side_effect=[mock_success, mock_failure]
        ) as mock_request:
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            assert mock_request.call_count == 2
            assert result["uploaded"] == 1
            assert result["failed"] == 1
            assert len(result["errors"]) == 1

            # Failed items should remain in queue
            assert len(sync.pending_uploads) == 1

    @pytest.mark.asyncio
    async def test_sync_with_retries(self):
        """Test sync with retry logic."""
        sync = integration_service.DataSynchronizer(batch_size=1, max_retries=2)
        client = integration_service.APIClient()

        # Add test item
        item = {"id": 1, "data": "test1"}
        sync.add_item(item)

        # Mock responses: fail twice, then succeed
        mock_failure = MagicMock()
        mock_failure.status_code = 500
        mock_failure.json.return_value = {"error": "Server error"}

        mock_success = MagicMock()
        mock_success.status_code = 200
        mock_success.json.return_value = {"status": "success"}

        with patch.object(
            client, "request", side_effect=[mock_failure, mock_failure, mock_success]
        ) as mock_request:
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Should make 3 requests (2 failures + 1 success)
            assert mock_request.call_count == 3
            assert result["uploaded"] == 1
            assert result["failed"] == 0
            assert result["errors"] == []

            # Queue should be empty after successful retry
            assert len(sync.pending_uploads) == 0

    @pytest.mark.asyncio
    async def test_sync_max_retries_exceeded(self):
        """Test sync when max retries are exceeded."""
        sync = integration_service.DataSynchronizer(batch_size=1, max_retries=2)
        client = integration_service.APIClient()

        # Add test item
        item = {"id": 1, "data": "test1"}
        sync.add_item(item)

        # Mock responses: always fail
        mock_failure = MagicMock()
        mock_failure.status_code = 500
        mock_failure.json.return_value = {"error": "Server error"}

        with patch.object(client, "request", return_value=mock_failure) as mock_request:
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Should make 3 requests (1 initial + 2 retries)
            assert mock_request.call_count == 3
            assert result["uploaded"] == 0
            assert result["failed"] == 1
            assert len(result["errors"]) == 1

            # Failed item should remain in queue
            assert len(sync.pending_uploads) == 1

    @pytest.mark.asyncio
    async def test_sync_network_error(self):
        """Test sync with network error."""
        sync = integration_service.DataSynchronizer(batch_size=1)
        client = integration_service.APIClient()

        # Add test item
        item = {"id": 1, "data": "test1"}
        sync.add_item(item)

        with patch.object(
            client, "request", side_effect=httpx.NetworkError("Connection failed")
        ):
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            assert result["uploaded"] == 0
            assert result["failed"] == 1
            assert len(result["errors"]) == 1
            assert "Connection failed" in result["errors"][0]

            # Failed item should remain in queue
            assert len(sync.pending_uploads) == 1

    def test_get_queue_status(self):
        """Test getting queue status."""
        sync = integration_service.DataSynchronizer()

        # Initially empty
        status = sync.get_queue_status()
        assert status == {"pending": 0, "total_size": 0}

        # Add items
        items = [{"id": i, "data": f"test{i}"} for i in range(5)]
        sync.add_items(items)

        status = sync.get_queue_status()
        assert status["pending"] == 5
        assert status["total_size"] > 0  # Should have some size

    def test_clear_queue(self):
        """Test clearing the queue."""
        sync = integration_service.DataSynchronizer()

        # Add items
        items = [{"id": i, "data": f"test{i}"} for i in range(5)]
        sync.add_items(items)

        assert len(sync.pending_uploads) == 5

        sync.clear_queue()

        assert len(sync.pending_uploads) == 0


class TestIntegrationServiceUtilities:
    """Test suite for utility functions."""

    def test_format_timestamp(self):
        """Test timestamp formatting."""
        dt = datetime(2023, 1, 1, 12, 0, 0)

        formatted = integration_service.format_timestamp(dt)

        assert isinstance(formatted, str)
        assert "2023-01-01" in formatted
        assert "12:00:00" in formatted

    def test_parse_response_json(self):
        """Test parsing JSON response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "data": {"id": 123}}

        result = integration_service.parse_response_json(mock_response)

        assert result == {"status": "success", "data": {"id": 123}}

    def test_parse_response_json_invalid(self):
        """Test parsing invalid JSON response."""
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with pytest.raises(json.JSONDecodeError):
            integration_service.parse_response_json(mock_response)

    def test_build_query_params(self):
        """Test building query parameters."""
        params = {"limit": 10, "offset": 20, "filter": "active", "sort": "created_at"}

        query_string = integration_service.build_query_params(params)

        assert isinstance(query_string, str)
        assert "limit=10" in query_string
        assert "offset=20" in query_string
        assert "filter=active" in query_string
        assert "sort=created_at" in query_string

    def test_build_query_params_empty(self):
        """Test building query parameters with empty dict."""
        result = integration_service.build_query_params({})

        assert result == ""

    def test_build_query_params_none_values(self):
        """Test building query parameters with None values."""
        params = {"limit": 10, "offset": None, "filter": "active", "sort": None}

        query_string = integration_service.build_query_params(params)

        # None values should be excluded
        assert "limit=10" in query_string
        assert "filter=active" in query_string
        assert "offset" not in query_string
        assert "sort" not in query_string


class TestIntegrationServiceIntegration:
    """Integration tests for the integration service."""

    @pytest.mark.asyncio
    async def test_end_to_end_sync(self):
        """Test end-to-end synchronization flow."""
        # Create client and synchronizer
        client = integration_service.APIClient(token="test_token")
        sync = integration_service.DataSynchronizer(batch_size=2)

        # Add test data
        items = [
            {"id": 1, "data": "test1"},
            {"id": 2, "data": "test2"},
            {"id": 3, "data": "test3"},
        ]
        sync.add_items(items)

        # Mock successful API responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}

        with patch.object(
            client, "request", return_value=mock_response
        ) as mock_request:
            # Perform sync
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Verify results
            assert result["uploaded"] == 3
            assert result["failed"] == 0
            assert len(sync.pending_uploads) == 0

            # Verify API calls
            assert mock_request.call_count == 2  # 2 batches

    @pytest.mark.asyncio
    async def test_concurrent_sync_operations(self):
        """Test concurrent synchronization operations."""
        client = integration_service.APIClient()
        sync1 = integration_service.DataSynchronizer(batch_size=1)
        sync2 = integration_service.DataSynchronizer(batch_size=1)

        # Add different data to each synchronizer
        sync1.add_item({"id": 1, "data": "sync1"})
        sync2.add_item({"id": 2, "data": "sync2"})

        # Mock responses
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}

        with patch.object(
            client, "request", return_value=mock_response
        ) as mock_request:
            # Run concurrent syncs
            results = await asyncio.gather(
                sync1.sync_to_endpoint(client, "https://api.example.com/upload1"),
                sync2.sync_to_endpoint(client, "https://api.example.com/upload2"),
            )

            # Both should succeed
            assert results[0]["uploaded"] == 1
            assert results[1]["uploaded"] == 1
            assert mock_request.call_count == 2


class TestIntegrationServiceErrorHandling:
    """Test error handling in integration service."""

    @pytest.mark.asyncio
    async def test_malformed_response_handling(self):
        """Test handling of malformed API responses."""
        client = integration_service.APIClient()
        sync = integration_service.DataSynchronizer()

        sync.add_item({"id": 1, "data": "test"})

        # Mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with patch.object(client, "request", return_value=mock_response):
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Should handle JSON decode error gracefully
            assert result["uploaded"] == 0
            assert result["failed"] == 1
            assert len(result["errors"]) == 1

    @pytest.mark.asyncio
    async def test_authentication_error_handling(self):
        """Test handling of authentication errors."""
        client = integration_service.APIClient(token="invalid_token")
        sync = integration_service.DataSynchronizer()

        sync.add_item({"id": 1, "data": "test"})

        # Mock 401 response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}

        with patch.object(client, "request", return_value=mock_response):
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Should handle auth error
            assert result["uploaded"] == 0
            assert result["failed"] == 1
            assert len(result["errors"]) == 1

    @pytest.mark.asyncio
    async def test_connection_timeout_handling(self):
        """Test handling of connection timeouts."""
        client = integration_service.APIClient()
        sync = integration_service.DataSynchronizer()

        sync.add_item({"id": 1, "data": "test"})

        with patch.object(
            client, "request", side_effect=httpx.TimeoutException("Request timeout")
        ):
            result = await sync.sync_to_endpoint(
                client, "https://api.example.com/upload"
            )

            # Should handle timeout gracefully
            assert result["uploaded"] == 0
            assert result["failed"] == 1
            assert len(result["errors"]) == 1
            assert "timeout" in result["errors"][0].lower()


if __name__ == "__main__":
    pytest.main([__file__])
