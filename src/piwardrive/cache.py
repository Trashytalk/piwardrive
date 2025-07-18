"""Redis-based caching system for PiWardrive.

This module provides a lightweight Redis cache implementation with TTL support
for efficient data caching and retrieval.
"""

from __future__ import annotations

import json
from typing import Any

from .core.utils import _get_redis_client


class RedisCache:
    """Lightweight async Redis cache with optional TTL."""

    def __init__(self, prefix: str = "cache") -> None:
        """Initialize the Redis cache.

        Args:
            prefix: Key prefix for cache entries.
        """
        self._prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> Any:
        """Get a value from cache.

        Args:
            key: Cache key to retrieve.

        Returns:
            The cached value or None if not found.
        """
        cli = _get_redis_client()
        if cli is None:
            return None
        data = await cli.get(self._key(key))
        return json.loads(data) if data else None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set a value in cache.

        Args:
            key: Cache key to set.
            value: Value to cache.
            ttl: Time to live in seconds (optional).
        """
        cli = _get_redis_client()
        if cli is None:
            return
        data = json.dumps(value)
        await cli.set(self._key(key), data, ex=ttl)

    async def invalidate(self, key: str) -> None:
        """Remove a key from cache.

        Args:
            key: Cache key to invalidate.
        """
        cli = _get_redis_client()
        if cli is None:
            return
        await cli.delete(self._key(key))

    async def clear(self) -> None:
        """Clear all cache entries with this prefix."""
        cli = _get_redis_client()
        if cli is None:
            return
        keys = await cli.keys(f"{self._prefix}:*")
        if keys:
            await cli.delete(*keys)


__all__ = ["RedisCache"]
