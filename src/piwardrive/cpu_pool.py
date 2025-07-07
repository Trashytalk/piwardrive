"""CPU-intensive task processing pool for PiWardrive.

This module provides a process pool executor for CPU-bound tasks such as
signal processing, data analysis, and cryptographic operations that can
benefit from multi-core processing.
"""
from __future__ import annotations

import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable

_CPU_POOL: ProcessPoolExecutor | None = None


def get_cpu_pool() -> ProcessPoolExecutor:
    """Return a global :class:`ProcessPoolExecutor`."""
    global _CPU_POOL
    if _CPU_POOL is None:
        size = int(os.getenv("PW_CPU_POOL_SIZE", os.cpu_count() or 1))
        _CPU_POOL = ProcessPoolExecutor(max_workers=size)
    return _CPU_POOL


async def run_cpu_bound(func: Callable[..., Any], *args: Any) -> Any:
    """Run ``func`` in the shared process pool and return the result."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(get_cpu_pool(), func, *args)


def shutdown_cpu_pool() -> None:
    """Clean up the global process pool."""
    global _CPU_POOL
    if _CPU_POOL is not None:
        _CPU_POOL.shutdown()
        _CPU_POOL = None


__all__ = ["get_cpu_pool", "run_cpu_bound", "shutdown_cpu_pool"]
