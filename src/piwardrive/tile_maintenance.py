import asyncio
import logging
import os
import sqlite3
import time
import heapq
from scheduler import PollScheduler
import utils


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


def vacuum_mbtiles(path: str) -> None:
    """Run VACUUM on an MBTiles file to compress it."""
    try:
        if os.path.isfile(path):
            with sqlite3.connect(path) as db:
                db.execute("VACUUM")
    except Exception as exc:  # pragma: no cover - database errors
        logging.exception("MBTiles VACUUM failed: %s", exc)


class TileMaintainer:
    """Background task for periodic tile cache maintenance."""

    def __init__(
        self,
        scheduler: PollScheduler,
        *,
        folder: str = "/mnt/ssd/tiles",
        offline_path: str | None = None,
        interval: int = 86400,
        max_age_days: int = 30,
        limit_mb: int = 512,
        vacuum: bool = True,
    ) -> None:
        self._folder = folder
        self._offline_path = offline_path
        self._max_age = max_age_days
        self._limit = limit_mb
        self._vacuum = vacuum
        scheduler.schedule(
            "tile_maintenance",
            lambda dt: utils.run_async_task(self._run()),
            interval,
        )

    async def _run(self) -> None:
        try:
            await asyncio.to_thread(purge_old_tiles, self._folder, self._max_age)
            await asyncio.to_thread(enforce_cache_limit, self._folder, self._limit)
            if self._vacuum and self._offline_path:
                await asyncio.to_thread(vacuum_mbtiles, self._offline_path)
        except Exception as exc:  # pragma: no cover - unexpected errors
            logging.exception("Tile maintenance failed: %s", exc)
