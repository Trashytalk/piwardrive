from __future__ import annotations

import time
from typing import Any, Awaitable, Callable


class CircuitBreaker:
    """Simple circuit breaker for async functions."""

    def __init__(self, max_failures: int = 3, reset_timeout: float = 30.0) -> None:
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure = 0.0
        self.open = False

    async def call(
        self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any
    ) -> Any:
        if self.open and time.time() - self.last_failure < self.reset_timeout:
            raise RuntimeError("Circuit open")
        try:
            result = await func(*args, **kwargs)
        except Exception:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.max_failures:
                self.open = True
            raise
        else:
            self.failures = 0
            self.open = False
            return result


__all__ = ["CircuitBreaker"]
