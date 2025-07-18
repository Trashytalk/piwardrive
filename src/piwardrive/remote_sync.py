"""Backward compatibility wrapper around the :mod:`remote_sync` package.

This module provides compatibility for older import patterns while redirecting
to the new remote_sync package implementation.
"""

from __future__ import annotations

import logging
import sqlite3
from typing import Tuple

import remote_sync as _impl
from remote_sync import DEFAULT_RETRIES, DEFAULT_TIMEOUT

# Re-export commonly used modules to keep older imports working.
asyncio = _impl.asyncio
logging = _impl.logging
os = _impl.os
aiohttp = _impl.aiohttp
tempfile = _impl.tempfile
json = _impl.json

enable_metrics = _impl.enable_metrics
get_metrics = _impl.get_metrics

# Public logger instance used by the implementation.
logger = _impl.logger


def _make_range_db(src: str, start: int, end: int) -> str:
    """Return path to a temporary DB containing rows ``start``..``end``."""
    return _impl._make_range_db(src, start, end)


def _load_sync_state(path: str) -> int:
    """Return the last synced row id recorded in ``path``."""
    return _impl._load_sync_state(path)


def _save_sync_state(path: str, row_id: int) -> None:
    """Persist ``row_id`` to ``path``."""
    _impl._save_sync_state(path, row_id)


async def sync_database_to_server(
    db_path: str,
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    row_range: Tuple[int, int] | None = None,
) -> None:
    """Delegate to :func:`remote_sync.sync_database_to_server`."""
    await _impl.sync_database_to_server(
        db_path,
        url,
        timeout=timeout,
        retries=retries,
        row_range=row_range,
    )


async def sync_new_records(
    db_path: str,
    url: str,
    *,
    state_file: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> int:
    """Delegate to :func:`remote_sync.sync_new_records` using local wrapper."""
    if state_file is None:
        state_file = db_path + ".last"

    last_id = _load_sync_state(state_file)

    with sqlite3.connect(db_path) as db:
        cur = db.execute("SELECT MAX(rowid) FROM health_records")
        max_id = cur.fetchone()[0] or 0
    if max_id <= last_id:
        return 0

    await sync_database_to_server(
        db_path,
        url,
        timeout=timeout,
        retries=retries,
        row_range=(last_id + 1, max_id),
    )

    _save_sync_state(state_file, max_id)
    return max_id - last_id
