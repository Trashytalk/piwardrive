from __future__ import annotations

"""Filesystem watcher for configuration changes."""

import os
from typing import Any, Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer as _Observer


class _ConfigHandler(FileSystemEventHandler):
    """Handle file events for :func:`watch_config`."""

    _path: str
    _callback: Callable[[], None]

    def __init__(self, path: str, callback: Callable[[], None]) -> None:
        super().__init__()
        self._path = os.path.abspath(path)
        self._callback = callback

    def on_modified(self, event: Any) -> None:  # noqa: V105 - Watchdog callback
        """Watchdog callback for modifications to the watched file."""
        if os.path.abspath(event.src_path) == self._path:
            self._callback()

    def on_created(self, event: Any) -> None:  # noqa: V105 - Watchdog callback
        """Watchdog callback for creation of the watched file."""
        if os.path.abspath(event.src_path) == self._path:
            self._callback()


def watch_config(path: str, callback: Callable[[], None]) -> Any:
    """Start watching ``path`` and invoke ``callback`` on changes."""
    observer = _Observer()
    handler = _ConfigHandler(path, callback)
    observer.schedule(handler, os.path.dirname(path) or ".", recursive=False)
    observer.start()
    return observer


__all__ = ["watch_config"]
