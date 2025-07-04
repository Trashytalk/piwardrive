from __future__ import annotations

import pickle
from typing import Any

from .core.utils import _get_redis_client


class RedisCache:
    """Lightweight async Redis cache with optional TTL."""

    def __init__(self, prefix: str = "cache") -> None:
        self._prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> Any:
        cli = _get_redis_client()
        if cli is None:
            return None
        data = await cli.get(self._key(key))
        return pickle.loads(data) if data else None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        cli = _get_redis_client()
        if cli is None:
            return
        data = pickle.dumps(value)
        await cli.set(self._key(key), data, ex=ttl)

    async def invalidate(self, key: str) -> None:
        cli = _get_redis_client()
        if cli is None:
            return
        await cli.delete(self._key(key))

    async def clear(self) -> None:
        cli = _get_redis_client()
        if cli is None:
            return
        keys = await cli.keys(f"{self._prefix}:*")
        if keys:
            await cli.delete(*keys)


__all__ = ["RedisCache"]
