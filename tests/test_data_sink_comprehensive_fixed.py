#!/usr/bin/env python3
"""Comprehensive test suite for piwardrive.data_sink module.

This test suite provides complete coverage for the data_sink module including:
- S3 upload functionality
- InfluxDB write operations
- PostgreSQL write operations
- Error handling and edge cases
- Async operations
- External service integration
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from piwardrive import data_sink


class TestS3Upload:
    """Test S3 upload functionality."""

    @pytest.mark.asyncio
    async def test_upload_to_s3_success(self):
        """Test successful S3 upload."""
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3") as mock_upload:
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.return_value = None

                await data_sink.upload_to_s3(
                    path="/test/path",
                    bucket="test-bucket",
                    key="test-key",
                    profile="test-profile",
                )

                mock_to_thread.assert_called_once_with(
                    mock_upload, "/test/path", "test-bucket", "test-key", "test-profile"
                )

    @pytest.mark.asyncio
    async def test_upload_to_s3_without_profile(self):
        """Test S3 upload without profile."""
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3") as mock_upload:
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.return_value = None

                await data_sink.upload_to_s3(
                    path="/test/path", bucket="test-bucket", key="test-key"
                )

                mock_to_thread.assert_called_once_with(
                    mock_upload, "/test/path", "test-bucket", "test-key", None
                )

    @pytest.mark.asyncio
    async def test_upload_to_s3_exception(self):
        """Test S3 upload with exception."""
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3") as mock_upload:
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.side_effect = Exception("Upload failed")

                with pytest.raises(Exception, match="Upload failed"):
                    await data_sink.upload_to_s3(
                        path="/test/path", bucket="test-bucket", key="test-key"
                    )

    @pytest.mark.asyncio
    async def test_upload_to_s3_empty_params(self):
        """Test S3 upload with empty parameters."""
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3") as mock_upload:
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.return_value = None

                await data_sink.upload_to_s3(path="", bucket="", key="")

                mock_to_thread.assert_called_once_with(mock_upload, "", "", "", None)


class TestInfluxDBWrite:
    """Test InfluxDB write functionality."""

    @pytest.mark.asyncio
    async def test_write_influxdb_success(self):
        """Test successful InfluxDB write."""
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()

        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session

            records = [
                "measurement1,tag1=value1 field1=10 1000000000",
                "measurement2,tag2=value2 field2=20 1000000001",
            ]

            await data_sink.write_influxdb(
                url="http://localhost:8086",
                token="test-token",
                org="test-org",
                bucket="test-bucket",
                records=records,
            )

            # Verify session post was called with correct parameters
            mock_session.post.assert_called_once()
            call_args = mock_session.post.call_args
            assert call_args[0][0] == "http://localhost:8086/api/v2/write"
            assert call_args[1]["params"] == {
                "org": "test-org",
                "bucket": "test-bucket",
                "precision": "s",
            }
            assert call_args[1]["headers"] == {"Authorization": "Token test-token"}

            mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_influxdb_aiohttp_not_available(self):
        """Test InfluxDB write when aiohttp is not available."""
        original_import = __builtins__["__import__"]

        def mock_import(name, *args, **kwargs):
            if name == "aiohttp":
                raise ImportError("No module named 'aiohttp'")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(
                RuntimeError, match="aiohttp required for InfluxDB uploads"
            ):
                await data_sink.write_influxdb(
                    url="http://localhost:8086",
                    token="test-token",
                    org="test-org",
                    bucket="test-bucket",
                    records=["measurement,tag=value field=123 1234567890"],
                )

    @pytest.mark.asyncio
    async def test_write_influxdb_http_error(self):
        """Test InfluxDB write with HTTP error."""
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 400 Bad Request")

        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session

            with pytest.raises(Exception, match="HTTP 400 Bad Request"):
                await data_sink.write_influxdb(
                    url="http://localhost:8086",
                    token="test-token",
                    org="test-org",
                    bucket="test-bucket",
                    records=["measurement,tag=value field=123 1234567890"],
                )

    @pytest.mark.asyncio
    async def test_write_influxdb_url_normalization(self):
        """Test InfluxDB write with URL normalization."""
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()

        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session

            # Test with trailing slash
            await data_sink.write_influxdb(
                url="http://localhost:8086/",
                token="test-token",
                org="test-org",
                bucket="test-bucket",
                records=["measurement,tag=value field=123 1234567890"],
            )

            # Verify URL was normalized (trailing slash removed)
            call_args = mock_session.post.call_args
            assert call_args[0][0] == "http://localhost:8086/api/v2/write"

    @pytest.mark.asyncio
    async def test_write_influxdb_empty_records(self):
        """Test InfluxDB write with empty records."""
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()

        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session

            await data_sink.write_influxdb(
                url="http://localhost:8086",
                token="test-token",
                org="test-org",
                bucket="test-bucket",
                records=[],
            )

            # Verify empty data was sent
            call_args = mock_session.post.call_args
            assert call_args[1]["data"] == b""


class TestPostgresWrite:
    """Test PostgreSQL write functionality."""

    @pytest.mark.asyncio
    async def test_write_postgres_success(self):
        """Test successful PostgreSQL write."""
        mock_conn = AsyncMock()
        mock_conn.executemany = AsyncMock()
        mock_conn.close = AsyncMock()

        with patch("asyncpg.connect", return_value=mock_conn):
            rows = [
                {"id": 1, "name": "test1", "value": 10},
                {"id": 2, "name": "test2", "value": 20},
            ]

            await data_sink.write_postgres(
                dsn="postgresql://user:pass@localhost/db", table="test_table", rows=rows
            )

            # Verify connection was established
            mock_conn.executemany.assert_called_once()
            mock_conn.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_postgres_asyncpg_not_available(self):
        """Test PostgreSQL write when asyncpg is not available."""
        original_import = __builtins__["__import__"]

        def mock_import(name, *args, **kwargs):
            if name == "asyncpg":
                raise ImportError("No module named 'asyncpg'")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(
                RuntimeError, match="asyncpg required for Postgres uploads"
            ):
                await data_sink.write_postgres(
                    dsn="postgresql://user:pass@localhost/db",
                    table="test_table",
                    rows=[{"id": 1, "name": "test"}],
                )

    @pytest.mark.asyncio
    async def test_write_postgres_empty_rows(self):
        """Test PostgreSQL write with empty rows."""
        # Should return early without connecting to database
        with patch("asyncpg.connect") as mock_connect:
            await data_sink.write_postgres(
                dsn="postgresql://user:pass@localhost/db", table="test_table", rows=[]
            )

            # Verify no connection was attempted
            mock_connect.assert_not_called()

    @pytest.mark.asyncio
    async def test_write_postgres_connection_error(self):
        """Test PostgreSQL write with connection error."""
        with patch("asyncpg.connect", side_effect=Exception("Connection failed")):
            with pytest.raises(Exception, match="Connection failed"):
                await data_sink.write_postgres(
                    dsn="postgresql://user:pass@localhost/db",
                    table="test_table",
                    rows=[{"id": 1, "name": "test"}],
                )

    @pytest.mark.asyncio
    async def test_write_postgres_executemany_error(self):
        """Test PostgreSQL write with executemany error."""
        mock_conn = AsyncMock()
        mock_conn.executemany.side_effect = Exception("Query failed")
        mock_conn.close = AsyncMock()

        with patch("asyncpg.connect", return_value=mock_conn):
            with pytest.raises(Exception, match="Query failed"):
                await data_sink.write_postgres(
                    dsn="postgresql://user:pass@localhost/db",
                    table="test_table",
                    rows=[{"id": 1, "name": "test"}],
                )

            # Verify connection was closed even after error
            mock_conn.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_write_postgres_query_construction(self):
        """Test PostgreSQL query construction."""
        mock_conn = AsyncMock()
        mock_conn.executemany = AsyncMock()
        mock_conn.close = AsyncMock()

        with patch("asyncpg.connect", return_value=mock_conn):
            rows = [
                {"id": 1, "name": "test1", "value": 10},
                {"id": 2, "name": "test2", "value": 20},
            ]

            await data_sink.write_postgres(
                dsn="postgresql://user:pass@localhost/db", table="test_table", rows=rows
            )

            # Verify query construction
            call_args = mock_conn.executemany.call_args
            query = call_args[0][0]
            values = call_args[0][1]

            assert "INSERT INTO test_table" in query
            assert "id, name, value" in query
            assert "$1, $2, $3" in query
            assert values == [(1, "test1", 10), (2, "test2", 20)]


class TestIntegration:
    """Integration tests for data_sink module."""

    @pytest.mark.asyncio
    async def test_s3_upload_integration(self):
        """Test S3 upload integration."""
        # This would typically test with real S3 service
        # For now, we'll just verify the interface works
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3"):
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.return_value = None

                await data_sink.upload_to_s3("test", "bucket", "key")
                assert mock_to_thread.called

    @pytest.mark.asyncio
    async def test_influxdb_integration(self):
        """Test InfluxDB integration."""
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()

        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session

            await data_sink.write_influxdb(
                "http://localhost:8086", "token", "org", "bucket", ["test"]
            )

            assert mock_session.post.called

    @pytest.mark.asyncio
    async def test_postgres_integration(self):
        """Test PostgreSQL integration."""
        mock_conn = AsyncMock()
        mock_conn.executemany = AsyncMock()
        mock_conn.close = AsyncMock()

        with patch("asyncpg.connect", return_value=mock_conn):
            await data_sink.write_postgres("postgresql://test", "table", [{"id": 1}])

            assert mock_conn.executemany.called
            assert mock_conn.close.called


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent data sink operations."""
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3"):
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.return_value = None

                # Test concurrent S3 uploads
                tasks = [
                    data_sink.upload_to_s3(f"path{i}", "bucket", f"key{i}")
                    for i in range(5)
                ]

                await asyncio.gather(*tasks)
                assert mock_to_thread.call_count == 5

    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test timeout handling in async operations."""
        with patch("piwardrive.data_sink.cloud_export.upload_to_s3"):
            with patch("asyncio.to_thread") as mock_to_thread:
                mock_to_thread.side_effect = asyncio.TimeoutError("Operation timed out")

                with pytest.raises(asyncio.TimeoutError):
                    await data_sink.upload_to_s3("test", "bucket", "key")


if __name__ == "__main__":
    pytest.main([__file__])
