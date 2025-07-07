"""Background task queue system for PiWardrive.

This module provides a simple asyncio-based task queue for handling
background jobs and worker pools in an asynchronous environment.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable


class BackgroundTaskQueue:
    """Simple asyncio-based worker pool for background jobs."""

    def __init__(self, workers: int = 1) -> None:
        """Initialize the background task queue.
        
        Args:
            workers: Number of worker tasks to spawn.
        """
        self._queue: asyncio.Queue[Callable[[], Awaitable[Any]]] = asyncio.Queue()
        self._tasks: list[asyncio.Task[None]] = []
        self._running = False
        self.workers = workers

    async def _worker(self) -> None:
        while self._running:
            job = await self._queue.get()
            try:
                await job()
            except Exception as exc:  # pragma: no cover - background errors
                logging.exception("Background task failed: %s", exc)
            finally:
                self._queue.task_done()

    async def start(self) -> None:
        """Start the task queue workers."""
        if self._running:
            return
        self._running = True
        for _ in range(self.workers):
            self._tasks.append(asyncio.create_task(self._worker()))

    async def stop(self) -> None:
        """Stop the task queue workers."""
        self._running = False
        await self._queue.join()
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    def enqueue(self, func: Callable[[], Awaitable[Any]]) -> None:
        """Queue ``func`` to be executed by a worker."""
        self._queue.put_nowait(func)


class PriorityTaskQueue:
    """Worker pool processing jobs based on priority."""

    def __init__(self, workers: int = 1) -> None:
        """Initialize the priority task queue.
        
        Args:
            workers: Number of worker tasks to spawn.
        """
        self._queue: asyncio.PriorityQueue[tuple[int, Callable[[], Awaitable[Any]]]] = (
            asyncio.PriorityQueue()
        )
        self._tasks: list[asyncio.Task[None]] = []
        self._running = False
        self.workers = workers

    async def _worker(self) -> None:
        while self._running:
            priority, job = await self._queue.get()
            try:
                await job()
            except Exception as exc:  # pragma: no cover - background errors
                logging.exception("Background task failed: %s", exc)
            finally:
                self._queue.task_done()

    async def start(self) -> None:
        """Start the priority task queue workers."""
        if self._running:
            return
        self._running = True
        for _ in range(self.workers):
            self._tasks.append(asyncio.create_task(self._worker()))

    async def stop(self) -> None:
        """Stop the priority task queue workers."""
        self._running = False
        await self._queue.join()
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    def enqueue(self, func: Callable[[], Awaitable[Any]], priority: int = 0) -> None:
        """Queue a function with priority (lower numbers = higher priority).
        
        Args:
            func: Function to execute.
            priority: Task priority (lower numbers execute first).
        """
        self._queue.put_nowait((priority, func))


__all__ = ["BackgroundTaskQueue", "PriorityTaskQueue"]
