#!/usr/bin/env python3

"""
Comprehensive test suite for cache.py module.
Tests Redis-based caching functionality with TTL support.
"""

import json
import sys
from pathlib import Path
from unittest import mock
from unittest.mock import AsyncMock

import pytest

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from piwardrive.cache import RedisCache


class TestRedisCacheInitialization:
    """Test RedisCache initialization and configuration."""

    def test_default_initialization(self):
        """Test RedisCache with default prefix."""
        cache = RedisCache()
        assert cache._prefix == "cache"

    def test_custom_prefix_initialization(self):
        """Test RedisCache with custom prefix."""
        cache = RedisCache(prefix="test_prefix")
        assert cache._prefix == "test_prefix"

    def test_key_method_with_default_prefix(self):
        """Test _key method with default prefix."""
        cache = RedisCache()
        result = cache._key("test_key")
        assert result == "cache:test_key"

    def test_key_method_with_custom_prefix(self):
        """Test _key method with custom prefix."""
        cache = RedisCache(prefix="custom")
        result = cache._key("test_key")
        assert result == "custom:test_key"

    def test_key_method_with_special_characters(self):
        """Test _key method handles special characters."""
        cache = RedisCache(prefix="app")
        test_cases = [
            ("key:with:colons", "app:key:with:colons"),
            ("key-with-dashes", "app:key-with-dashes"),
            ("key_with_underscores", "app:key_with_underscores"),
            ("key.with.dots", "app:key.with.dots"),
            ("key with spaces", "app:key with spaces"),
            ("123numeric", "app:123numeric"),
        ]

        for input_key, expected in test_cases:
            assert cache._key(input_key) == expected


class TestRedisCacheGet:
    """Test RedisCache get functionality."""

    @pytest.mark.asyncio
    async def test_get_with_no_redis_client(self):
        """Test get method when Redis client is None."""
        cache = RedisCache()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=None):
            result = await cache.get("test_key")
            assert result is None

    @pytest.mark.asyncio
    async def test_get_existing_key(self):
        """Test get method with existing key."""
        cache = RedisCache()
        test_data = {"name": "test", "value": 42}
        json_data = json.dumps(test_data)

        mock_client = AsyncMock()
        mock_client.get.return_value = json_data

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            result = await cache.get("test_key")

            assert result == test_data
            mock_client.get.assert_called_once_with("cache:test_key")

    @pytest.mark.asyncio
    async def test_get_nonexistent_key(self):
        """Test get method with nonexistent key."""
        cache = RedisCache()

        mock_client = AsyncMock()
        mock_client.get.return_value = None

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            result = await cache.get("nonexistent_key")

            assert result is None
            mock_client.get.assert_called_once_with("cache:nonexistent_key")

    @pytest.mark.asyncio
    async def test_get_with_custom_prefix(self):
        """Test get method with custom prefix."""
        cache = RedisCache(prefix="myapp")
        test_data = [1, 2, 3]

        mock_client = AsyncMock()
        mock_client.get.return_value = json.dumps(test_data)

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            result = await cache.get("list_key")

            assert result == test_data
            mock_client.get.assert_called_once_with("myapp:list_key")

    @pytest.mark.asyncio
    async def test_get_with_invalid_json(self):
        """Test get method handles invalid JSON gracefully."""
        cache = RedisCache()

        mock_client = AsyncMock()
        mock_client.get.return_value = "invalid json data"

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            # Should not raise an exception, but will return None due to JSON decode error
            with pytest.raises(json.JSONDecodeError):
                await cache.get("invalid_key")

    @pytest.mark.asyncio
    async def test_get_with_various_data_types(self):
        """Test get method with various JSON-serializable data types."""
        cache = RedisCache()

        test_cases = [
            ("string_key", "simple string", '"simple string"'),
            ("number_key", 42, "42"),
            ("float_key", 3.14, "3.14"),
            ("bool_key", True, "true"),
            ("null_key", None, "null"),
            ("list_key", [1, 2, 3], "[1, 2, 3]"),
            ("dict_key", {"a": 1, "b": 2}, '{"a": 1, "b": 2}'),
        ]

        for key, expected_value, json_data in test_cases:
            mock_client = AsyncMock()
            mock_client.get.return_value = json_data

            with mock.patch(
                "piwardrive.cache._get_redis_client", return_value=mock_client
            ):
                result = await cache.get(key)
                assert result == expected_value


class TestRedisCacheSet:
    """Test RedisCache set functionality."""

    @pytest.mark.asyncio
    async def test_set_with_no_redis_client(self):
        """Test set method when Redis client is None."""
        cache = RedisCache()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=None):
            # Should not raise an exception
            await cache.set("test_key", "test_value")

    @pytest.mark.asyncio
    async def test_set_without_ttl(self):
        """Test set method without TTL."""
        cache = RedisCache()
        test_value = {"name": "test", "active": True}

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("test_key", test_value)

            mock_client.set.assert_called_once_with(
                "cache:test_key", json.dumps(test_value), ex=None
            )

    @pytest.mark.asyncio
    async def test_set_with_ttl(self):
        """Test set method with TTL."""
        cache = RedisCache()
        test_value = "expires soon"
        ttl = 300  # 5 minutes

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("temp_key", test_value, ttl=ttl)

            mock_client.set.assert_called_once_with(
                "cache:temp_key", json.dumps(test_value), ex=ttl
            )

    @pytest.mark.asyncio
    async def test_set_with_custom_prefix(self):
        """Test set method with custom prefix."""
        cache = RedisCache(prefix="session")
        test_value = {"user_id": 123, "role": "admin"}

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("user_data", test_value, ttl=3600)

            mock_client.set.assert_called_once_with(
                "session:user_data", json.dumps(test_value), ex=3600
            )

    @pytest.mark.asyncio
    async def test_set_with_various_data_types(self):
        """Test set method with various data types."""
        cache = RedisCache()

        test_cases = [
            ("string", "hello world"),
            ("integer", 42),
            ("float", 3.14159),
            ("boolean", True),
            ("none", None),
            ("list", [1, "two", 3.0, True]),
            ("dict", {"nested": {"deep": {"value": 123}}}),
            ("empty_list", []),
            ("empty_dict", {}),
        ]

        for key, value in test_cases:
            mock_client = AsyncMock()

            with mock.patch(
                "piwardrive.cache._get_redis_client", return_value=mock_client
            ):
                await cache.set(key, value)

                expected_json = json.dumps(value)
                mock_client.set.assert_called_once_with(
                    f"cache:{key}", expected_json, ex=None
                )


class TestRedisCacheInvalidate:
    """Test RedisCache invalidate functionality."""

    @pytest.mark.asyncio
    async def test_invalidate_with_no_redis_client(self):
        """Test invalidate method when Redis client is None."""
        cache = RedisCache()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=None):
            # Should not raise an exception
            await cache.invalidate("test_key")

    @pytest.mark.asyncio
    async def test_invalidate_existing_key(self):
        """Test invalidate method with existing key."""
        cache = RedisCache()

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.invalidate("test_key")

            mock_client.delete.assert_called_once_with("cache:test_key")

    @pytest.mark.asyncio
    async def test_invalidate_with_custom_prefix(self):
        """Test invalidate method with custom prefix."""
        cache = RedisCache(prefix="temp")

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.invalidate("expired_key")

            mock_client.delete.assert_called_once_with("temp:expired_key")

    @pytest.mark.asyncio
    async def test_invalidate_nonexistent_key(self):
        """Test invalidate method with nonexistent key."""
        cache = RedisCache()

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.invalidate("nonexistent_key")

            # Should still call delete (Redis handles nonexistent keys gracefully)
            mock_client.delete.assert_called_once_with("cache:nonexistent_key")


class TestRedisCacheClear:
    """Test RedisCache clear functionality."""

    @pytest.mark.asyncio
    async def test_clear_with_no_redis_client(self):
        """Test clear method when Redis client is None."""
        cache = RedisCache()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=None):
            # Should not raise an exception
            await cache.clear()

    @pytest.mark.asyncio
    async def test_clear_with_matching_keys(self):
        """Test clear method when matching keys exist."""
        cache = RedisCache(prefix="test")

        mock_client = AsyncMock()
        mock_client.keys.return_value = ["test:key1", "test:key2", "test:key3"]

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.clear()

            mock_client.keys.assert_called_once_with("test:*")
            mock_client.delete.assert_called_once_with(
                "test:key1", "test:key2", "test:key3"
            )

    @pytest.mark.asyncio
    async def test_clear_with_no_matching_keys(self):
        """Test clear method when no matching keys exist."""
        cache = RedisCache(prefix="empty")

        mock_client = AsyncMock()
        mock_client.keys.return_value = []

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.clear()

            mock_client.keys.assert_called_once_with("empty:*")
            mock_client.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_clear_default_prefix(self):
        """Test clear method with default prefix."""
        cache = RedisCache()  # Default prefix is "cache"

        mock_client = AsyncMock()
        mock_client.keys.return_value = ["cache:data1", "cache:data2"]

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.clear()

            mock_client.keys.assert_called_once_with("cache:*")
            mock_client.delete.assert_called_once_with("cache:data1", "cache:data2")


class TestRedisCacheIntegration:
    """Test integration scenarios and real-world usage patterns."""

    @pytest.mark.asyncio
    async def test_cache_roundtrip(self):
        """Test complete cache roundtrip: set, get, invalidate."""
        cache = RedisCache(prefix="integration")
        test_data = {
            "user": {"id": 123, "name": "Alice"},
            "permissions": ["read", "write"],
            "active": True,
        }

        mock_client = AsyncMock()

        # Mock the set operation
        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("user:123", test_data, ttl=1800)

            mock_client.set.assert_called_with(
                "integration:user:123", json.dumps(test_data), ex=1800
            )

        # Mock the get operation
        mock_client.get.return_value = json.dumps(test_data)
        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            result = await cache.get("user:123")
            assert result == test_data
            mock_client.get.assert_called_with("integration:user:123")

        # Mock the invalidate operation
        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.invalidate("user:123")
            mock_client.delete.assert_called_with("integration:user:123")

    @pytest.mark.asyncio
    async def test_multiple_cache_instances(self):
        """Test multiple cache instances with different prefixes."""
        user_cache = RedisCache(prefix="users")
        session_cache = RedisCache(prefix="sessions")

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            # Set data in different caches
            await user_cache.set("123", {"name": "Alice"})
            await session_cache.set("abc", {"user_id": 123})

            # Verify correct prefixes are used
            assert mock_client.set.call_count == 2
            calls = mock_client.set.call_args_list

            # Check first call (user cache)
            assert calls[0][0][0] == "users:123"

            # Check second call (session cache)
            assert calls[1][0][0] == "sessions:abc"

    @pytest.mark.asyncio
    async def test_cache_with_unicode_data(self):
        """Test cache operations with Unicode data."""
        cache = RedisCache(prefix="unicode")
        unicode_data = {
            "emoji": "🚀🌟💫",
            "chinese": "你好世界",
            "arabic": "مرحبا بالعالم",
            "special": "Café naïve résumé",
        }

        mock_client = AsyncMock()

        # Test setting Unicode data
        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("unicode_test", unicode_data)

            expected_json = json.dumps(unicode_data)
            mock_client.set.assert_called_once_with(
                "unicode:unicode_test", expected_json, ex=None
            )

        # Test getting Unicode data
        mock_client.get.return_value = json.dumps(unicode_data, ensure_ascii=False)
        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            result = await cache.get("unicode_test")
            assert result == unicode_data

    @pytest.mark.asyncio
    async def test_cache_error_handling(self):
        """Test cache behavior when Redis operations fail."""
        cache = RedisCache()

        # Test when Redis client raises an exception
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Redis connection failed")
        mock_client.set.side_effect = Exception("Redis connection failed")
        mock_client.delete.side_effect = Exception("Redis connection failed")

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            # These should raise exceptions as the cache doesn't handle Redis errors
            with pytest.raises(Exception):
                await cache.get("test")

            with pytest.raises(Exception):
                await cache.set("test", "value")

            with pytest.raises(Exception):
                await cache.invalidate("test")


class TestRedisCacheEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.asyncio
    async def test_empty_key_handling(self):
        """Test cache operations with empty keys."""
        cache = RedisCache()

        mock_client = AsyncMock()
        mock_client.get.return_value = json.dumps("empty key value")

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            # Empty string key
            await cache.set("", "empty key value")
            mock_client.set.assert_called_with(
                "cache:", json.dumps("empty key value"), ex=None
            )

            result = await cache.get("")
            mock_client.get.assert_called_with("cache:")
            assert result == "empty key value"

            await cache.invalidate("")
            mock_client.delete.assert_called_with("cache:")

    @pytest.mark.asyncio
    async def test_very_long_key(self):
        """Test cache operations with very long keys."""
        cache = RedisCache()
        long_key = "x" * 1000  # Very long key

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set(long_key, "value")
            expected_key = f"cache:{long_key}"
            mock_client.set.assert_called_with(
                expected_key, json.dumps("value"), ex=None
            )

    @pytest.mark.asyncio
    async def test_zero_ttl(self):
        """Test cache set operation with zero TTL."""
        cache = RedisCache()

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("zero_ttl", "value", ttl=0)
            mock_client.set.assert_called_with(
                "cache:zero_ttl", json.dumps("value"), ex=0
            )

    @pytest.mark.asyncio
    async def test_negative_ttl(self):
        """Test cache set operation with negative TTL."""
        cache = RedisCache()

        mock_client = AsyncMock()

        with mock.patch("piwardrive.cache._get_redis_client", return_value=mock_client):
            await cache.set("negative_ttl", "value", ttl=-1)
            mock_client.set.assert_called_with(
                "cache:negative_ttl", json.dumps("value"), ex=-1
            )


if __name__ == "__main__":
    pytest.main([__file__])
