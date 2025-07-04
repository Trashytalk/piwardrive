from __future__ import annotations

from typing import Any, AsyncIterator, Iterable


class DatabaseAdapter:
    """Abstract database adapter interface."""

    async def connect(self) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def execute(self, query: str, *args: Any) -> None:
        raise NotImplementedError

    async def executemany(self, query: str, args_iter: Iterable[Iterable[Any]]) -> None:
        raise NotImplementedError

    async def fetchall(self, query: str, *args: Any) -> list[dict[str, Any]]:
        raise NotImplementedError

    async def transaction(self) -> AsyncIterator[None]:
        """Context manager for transactions."""
        raise NotImplementedError
