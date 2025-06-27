"""Backward compatibility wrapper for ``remote_sync`` package."""

from __future__ import annotations

import sqlite3

import remote_sync as _impl

asyncio = _impl.asyncio
logging = _impl.logging
os = _impl.os
aiohttp = _impl.aiohttp
tempfile = _impl.tempfile
json = _impl.json
logger = _impl.logger

_make_range_db = _impl._make_range_db
_load_sync_state = _impl._load_sync_state
_save_sync_state = _impl._save_sync_state


async def sync_database_to_server(*args, **kwargs):
    """Delegate to :func:`remote_sync.sync_database_to_server`."""
    return await _impl.sync_database_to_server(*args, **kwargs)


async def sync_new_records(
    db_path: str,
    url: str,
    *,
    state_file: str | None = None,
    timeout: int = 30,
    retries: int = 3,
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
