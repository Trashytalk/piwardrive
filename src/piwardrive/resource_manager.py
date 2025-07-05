import asyncio
import sqlite3
import weakref
from contextlib import contextmanager
from typing import Any, Callable, Iterable


class ResourceManager:
    """Central manager for process resources."""

    def __init__(self) -> None:
        self._finalizers: list[weakref.finalize] = []
        self._tasks: "weakref.WeakSet[asyncio.Task[Any]]" = weakref.WeakSet()

    def register(
        self, obj: Any, cleanup: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> None:
        """Register ``cleanup`` to run when ``obj`` is garbage collected."""
        self._finalizers.append(weakref.finalize(obj, cleanup, *args, **kwargs))

    @contextmanager
    def open_file(self, path: str, mode: str = "r", **kwargs: Any) -> Iterable[Any]:
        fh = open(path, mode, **kwargs)
        self.register(fh, fh.close)
        try:
            yield fh
        finally:
            fh.close()

    @contextmanager
    def open_db(self, path: str, **kwargs: Any) -> Iterable[sqlite3.Connection]:
        conn = sqlite3.connect(path, **kwargs)
        try:
            yield conn
        finally:
            conn.close()

    def add_task(self, task: asyncio.Task[Any]) -> None:
        """Track ``task`` and ensure it is cancelled when finalized."""
        self._tasks.add(task)
        self.register(task, self._cancel_task, task)

    async def cancel_all(self) -> None:
        """Cancel all tracked tasks and wait for completion."""
        tasks = [t for t in self._tasks if not t.done()]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self._tasks.clear()

    def cleanup(self) -> None:
        """Run registered cleanup callbacks immediately."""
        for fin in self._finalizers:
            fin()
        self._finalizers.clear()

    @staticmethod
    def _cancel_task(task: asyncio.Task[Any]) -> None:
        if not task.done():
            task.cancel()
