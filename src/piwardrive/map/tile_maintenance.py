"""Module tile_maintenance."""

import asyncio
import heapq
import logging
import os
import sqlite3
import time
from concurrent.futures import Future
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Optional,
    TypeVar,
    cast,
)

from piwardrive.scheduler import PollScheduler

T = TypeVar("T")


def _run_async(
    coro: Coroutine[Any, Any, T], callback: Callable[[T], None] | None = None
) -> Future[T]:
    """Execute ``coro`` in the current or new event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        result = asyncio.run(coro)
        fut: Future[T] = Future()
        fut.set_result(result)
        if callback is not None:
            callback(result)
        return fut
    else:
        task = loop.create_task(coro)
        if callback is not None:
            task.add_done_callback(lambda f: callback(f.result()))
        return cast(Future[T], task)


if TYPE_CHECKING:  # pragma: no cover - type hints only
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
else:
    try:
        from watchdog.events import \
            FileSystemEventHandler as _FileSystemEventHandler
        from watchdog.observers import Observer as _Observer
    except Exception:  # pragma: no cover - watchdog optional for tests
        from typing import Any as _Observer  # type: ignore

        _FileSystemEventHandler = object  # type: ignore

    from typing import Any

    FileSystemEventHandler = _FileSystemEventHandler
    Observer = cast(Any, _Observer)


def purge_old_tiles(folder: str, max_age_days: int) -> None:
    """Delete cached tiles older than ``max_age_days`` days."""
    cutoff = time.time() - max_age_days * 86400
    try:
        if not os.path.isdir(folder):
            return
        for root, _, files in os.walk(folder):
            for f in files:
                path = os.path.join(root, f)
                if os.path.getmtime(path) < cutoff:
                    os.remove(path)
    except Exception as exc:  # pragma: no cover - filesystem errors
        logging.exception("Tile purge failed: %s", exc)


def enforce_cache_limit(folder: str, limit_mb: int) -> None:
    """Ensure tile cache does not exceed ``limit_mb`` megabytes."""
    try:
        if not os.path.isdir(folder):
            return

        max_bytes = limit_mb * 1024 * 1024
        total = 0
        stack = [folder]
        heap: list[tuple[float, int, str]] = []

        while stack:
            base = stack.pop()
            try:
                with os.scandir(base) as entries:
                    for entry in entries:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry.path)
                        elif entry.is_file(follow_symlinks=False):
                            stat = entry.stat()
                            size = stat.st_size
                            total += size
                            heapq.heappush(heap, (stat.st_mtime, size, entry.path))
                            while heap and total > max_bytes:
                                mtime, sz, path = heapq.heappop(heap)
                                try:
                                    os.remove(path)
                                except OSError:
                                    pass
                                total -= sz
            except OSError:
                continue

        while heap and total > max_bytes:
            mtime, sz, path = heapq.heappop(heap)
            try:
                os.remove(path)
            except OSError:
                pass
            total -= sz
    except Exception as exc:  # pragma: no cover - filesystem errors
        logging.exception("Cache limit enforcement failed: %s", exc)


def _folder_stats(folder: str) -> tuple[int, int]:
    """Return ``(file_count, total_bytes)`` for ``folder``."""
    count = 0
    size = 0
    if not os.path.isdir(folder):
        return count, size
    stack = [folder]
    while stack:
        base = stack.pop()
        try:
            with os.scandir(base) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        stack.append(entry.path)
                    elif entry.is_file(follow_symlinks=False):
                        stat = entry.stat()
                        count += 1
                        size += stat.st_size
        except OSError:
            continue
    return count, size


def vacuum_mbtiles(path: str) -> None:
    """Run VACUUM on an MBTiles file to compress it."""
    try:
        if os.path.isfile(path):
            with sqlite3.connect(path) as db:
                db.execute("VACUUM")
    except Exception as exc:  # pragma: no cover - database errors
        logging.exception("MBTiles VACUUM failed: %s", exc)


class _TileEventHandler(FileSystemEventHandler):
    """Handle file events for :class:`TileMaintainer`."""

    maintainer: "TileMaintainer"

    def __init__(self, maintainer: "TileMaintainer") -> None:
        self.maintainer = maintainer

    def on_any_event(self, _event: object) -> None:  # pragma: no cover - thin wrapper
        self.maintainer.check_thresholds()


class TileMaintainer:
    """Maintain cached tiles using ``watchdog`` and periodic checks."""

    def __init__(
        self,
        scheduler: PollScheduler,
        *,
        folder: str = "/mnt/ssd/tiles",
        offline_path: str | None = None,
        interval: int = 604800,
        max_age_days: int = 30,
        limit_mb: int = 512,
        vacuum: bool = True,
        trigger_file_count: int = 1000,
        start_observer: bool = True,
    ) -> None:
        self._folder = folder
        self._offline_path = offline_path
        self._max_age = max_age_days
        self._limit = limit_mb
        self._vacuum = vacuum
        self._trigger_files = trigger_file_count
        self._running = False
        self._observer: Optional[Any] = None

        if interval > 0:
            scheduler.schedule(
                "tile_maintenance",
                lambda dt: _run_async(self._run()),
                interval,
            )

        if start_observer and Observer is not None:
            handler = _TileEventHandler(self)
            self._observer = Observer()
            self._observer.schedule(handler, self._folder, recursive=True)
            self._observer.start()

    async def _run(self) -> None:
        try:
            await asyncio.to_thread(purge_old_tiles, self._folder, self._max_age)
            await asyncio.to_thread(enforce_cache_limit, self._folder, self._limit)
            if self._vacuum and self._offline_path:
                await asyncio.to_thread(vacuum_mbtiles, self._offline_path)
        except Exception as exc:  # pragma: no cover - unexpected errors
            logging.exception("Tile maintenance failed: %s", exc)

    def stop(self) -> None:
        """Stop the ``watchdog`` observer if running."""
        if self._observer is not None:
            self._observer.stop()
            self._observer.join(1)
            self._observer = None

    def check_thresholds(self) -> None:
        """Run maintenance if file count or size exceed limits."""
        count, size = _folder_stats(self._folder)
        over_files = count >= self._trigger_files
        over_size = size >= self._limit * 1024 * 1024
        if (over_files or over_size) and not self._running:
            self._running = True

            async def _runner() -> None:
                try:
                    await self._run()
                finally:
                    self._running = False

            _run_async(_runner())
