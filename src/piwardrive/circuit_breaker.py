"""Circuit breaker pattern implementation for PiWardrive.

This module provides a simple circuit breaker implementation to prevent
cascading failures in asynchronous operations.
"""

from __future__ import annotations

import time
from typing import Any, Awaitable, Callable


class CircuitBreaker:
    """Simple circuit breaker for async functions."""

    def __init__(self, max_failures: int = 3, reset_timeout: float = 30.0) -> None:
        """Initialize the circuit breaker.
        
        Args:
            max_failures: Maximum number of failures before opening circuit.
            reset_timeout: Time in seconds before attempting to reset.
        """
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure = 0.0
        self.open = False

    async def call(
        self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any
    ) -> Any:
        """Call a function through the circuit breaker.
        
        Args:
            func: The async function to call.
            args: Positional arguments for the function.
            kwargs: Keyword arguments for the function.
            
        Returns:
            The result of the function call.
            
        Raises:
            RuntimeError: If the circuit is open.
        """
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
