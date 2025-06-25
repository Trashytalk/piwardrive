"""Module tile_maintenance."""
import asyncio
import logging
import os
import sqlite3
import time
import heapq
from piwardrive.scheduler import PollScheduler
from piwardrive import utils
from typing import Optional

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except Exception:  # pragma: no cover - watchdog optional for tests
    Observer = None  # type: ignore
    FileSystemEventHandler = object  # type: ignore


def purge_old_tiles(folder: str, max_age_days: int) -> None:
    """
    Delete files in the specified folder that are older than the given number of days.
    
    Parameters:
        folder (str): Path to the folder containing cached tiles.
        max_age_days (int): Maximum allowed file age in days; files older than this are deleted.
    """
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
    """
    Removes the oldest files in the specified folder to ensure the total cache size does not exceed the given limit in megabytes.
    
    Files are deleted in order of oldest modification time first until the total size is within the specified limit. Subdirectories are processed recursively. Errors during file operations are ignored to ensure robustness.
    """

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
    """
    Return the number of files and total size in bytes for all files within the specified folder and its subdirectories.
    
    Parameters:
        folder (str): Path to the directory to scan.
    
    Returns:
        tuple[int, int]: A tuple containing the file count and the total size in bytes.
    """
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
    """
    Runs the SQLite VACUUM command on the specified MBTiles file to optimize and reduce its disk usage.
    
    Parameters:
        path (str): Path to the MBTiles (SQLite) database file.
    """
    try:
        if os.path.isfile(path):
            with sqlite3.connect(path) as db:
                db.execute("VACUUM")
    except Exception as exc:  # pragma: no cover - database errors
        logging.exception("MBTiles VACUUM failed: %s", exc)


class _TileEventHandler(FileSystemEventHandler):
    """Handle file events for :class:`TileMaintainer`."""

    def __init__(self, maintainer: "TileMaintainer") -> None:
        """
        Initialize the event handler with a reference to the given TileMaintainer instance.
        """
        self.maintainer = maintainer

    def on_any_event(self, _event) -> None:  # pragma: no cover - thin wrapper
        """
        Handles any file system event by triggering a threshold check on the associated TileMaintainer.
        """
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
        """
        Initializes a TileMaintainer to manage tile cache maintenance tasks.
        
        Configures periodic and event-driven maintenance of a tile cache directory, including purging old tiles, enforcing cache size limits, and optionally vacuuming an MBTiles database. Schedules periodic tasks using the provided scheduler and, if enabled and available, starts a file system observer to trigger maintenance on file changes.
        
        Parameters:
            scheduler (PollScheduler): Scheduler used to run periodic maintenance tasks.
            folder (str, optional): Path to the tile cache directory. Defaults to "/mnt/ssd/tiles".
            offline_path (str | None, optional): Path to an offline MBTiles file for vacuuming, if applicable.
            interval (int, optional): Interval in seconds between scheduled maintenance runs. Defaults to 604800 (one week).
            max_age_days (int, optional): Maximum age in days for cached tiles before purging. Defaults to 30.
            limit_mb (int, optional): Maximum allowed cache size in megabytes. Defaults to 512.
            vacuum (bool, optional): Whether to vacuum the MBTiles database during maintenance. Defaults to True.
            trigger_file_count (int, optional): File count threshold to trigger maintenance on file system events. Defaults to 1000.
            start_observer (bool, optional): Whether to start a file system observer for event-driven maintenance. Defaults to True.
        """
        self._folder = folder
        self._offline_path = offline_path
        self._max_age = max_age_days
        self._limit = limit_mb
        self._vacuum = vacuum
        self._trigger_files = trigger_file_count
        self._running = False
        self._observer: Optional[Observer] = None

        if interval > 0:
            scheduler.schedule(
                "tile_maintenance",
                lambda dt: utils.run_async_task(self._run()),
                interval,
            )

        if start_observer and Observer is not None:
            handler = _TileEventHandler(self)
            self._observer = Observer()
            self._observer.schedule(handler, self._folder, recursive=True)
            self._observer.start()

    async def _run(self) -> None:
        """
        Performs tile cache maintenance tasks asynchronously, including purging old tiles, enforcing cache size limits, and optionally vacuuming the MBTiles database.
        """
        try:
            await asyncio.to_thread(purge_old_tiles, self._folder, self._max_age)
            await asyncio.to_thread(enforce_cache_limit, self._folder, self._limit)
            if self._vacuum and self._offline_path:
                await asyncio.to_thread(vacuum_mbtiles, self._offline_path)
        except Exception as exc:  # pragma: no cover - unexpected errors
            logging.exception("Tile maintenance failed: %s", exc)

    def stop(self) -> None:
        """
        Stops the file system observer if it is running, ensuring the observer thread is properly terminated.
        """
        if self._observer is not None:
            self._observer.stop()
            self._observer.join(1)
            self._observer = None

    def check_thresholds(self) -> None:
        """
        Triggers maintenance if the number of files or total size in the tile folder exceeds configured thresholds.
        
        If either the file count or total size surpasses their respective limits and no maintenance is currently running, this method schedules an asynchronous maintenance task and prevents concurrent executions.
        """
        count, size = _folder_stats(self._folder)
        over_files = count >= self._trigger_files
        over_size = size >= self._limit * 1024 * 1024
        if (over_files or over_size) and not self._running:
            self._running = True

            async def _runner() -> None:
                """
                Runs the maintenance task asynchronously and resets the running flag upon completion.
                """
                try:
                    await self._run()
                finally:
                    self._running = False

            utils.run_async_task(_runner())
