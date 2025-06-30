"""Remote data synchronization utilities."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sqlite3
import tempfile
import time

import aiohttp

logger = logging.getLogger(__name__)

# Default behavior tuning
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
INITIAL_RETRY_DELAY = 1.0

# Treat these environment variable values as "metrics disabled"
_DISABLED_METRIC_VALUES = {
    None,
    "",
    "0",
    "false",
    "False",
}
_METRIC_ENV = os.getenv("PW_REMOTE_SYNC_METRICS")
_METRICS_ENABLED = _METRIC_ENV not in _DISABLED_METRIC_VALUES
_SUCCESS_TOTAL = 0
_FAILURE_TOTAL = 0
_LAST_DURATION = float("nan")


def enable_metrics(enabled: bool = True) -> None:
    """Enable or disable runtime metrics."""
    global _METRICS_ENABLED
    _METRICS_ENABLED = enabled


def get_metrics() -> dict[str, float | int]:
    """Return sync metrics if enabled, otherwise an empty dict."""
    if not _METRICS_ENABLED:
        return {}
    return {
        "success_total": _SUCCESS_TOTAL,
        "failure_total": _FAILURE_TOTAL,
        "last_duration": _LAST_DURATION,
    }


def _make_range_db(src: str, start: int, end: int) -> str:
    """Return path to a temporary DB with rows ``start``..``end`` from ``src``."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        dest = tmp.name

    with sqlite3.connect(src) as src_db, sqlite3.connect(dest) as dst_db:
        dst_db.execute(
            """CREATE TABLE health_records (
                timestamp TEXT PRIMARY KEY,
                cpu_temp REAL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL
            )"""
        )
        dst_db.execute(
            """CREATE TABLE ap_cache (
                bssid TEXT,
                ssid TEXT,
                encryption TEXT,
                lat REAL,
                lon REAL,
                last_time INTEGER
            )"""
        )

        cur = src_db.execute(
            "SELECT timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent"
            " FROM health_records WHERE rowid BETWEEN ? AND ?",
            (start, end),
        )
        dst_db.executemany(
            "INSERT INTO health_records VALUES (?, ?, ?, ?, ?)",
            cur,
        )

        cur = src_db.execute(
            "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache "
            "WHERE rowid BETWEEN ? AND ?",
            (start, end),
        )
        dst_db.executemany("INSERT INTO ap_cache VALUES (?, ?, ?, ?, ?, ?)", cur)
        dst_db.commit()

    return dest


def _load_sync_state(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return int(json.load(fh))
    except Exception:
        return 0


def _save_sync_state(path: str, row_id: int) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(row_id, fh)
    except OSError as exc:  # pragma: no cover - write errors
        logger.exception("Failed to write %s: %s", path, exc)


async def sync_new_records(
    db_path: str,
    url: str,
    *,
    state_file: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> int:
    """Sync new ``health_records`` rows to ``url``.

    ``state_file`` stores the last synced rowid and defaults to ``db_path``
    suffixed with ``.last``.  Returns the number of records uploaded.
    """
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


async def sync_database_to_server(
    db_path: str,
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    row_range: tuple[int, int] | None = None,
) -> None:
    """Upload the SQLite database at ``db_path`` to ``url`` via HTTP POST.

    Retries the transfer with exponential backoff if ``aiohttp`` raises an
    exception or an HTTP error status is returned.
    """
    global _SUCCESS_TOTAL, _FAILURE_TOTAL, _LAST_DURATION

    if not os.path.exists(db_path):
        raise FileNotFoundError(db_path)

    delay = INITIAL_RETRY_DELAY
    temp_path = None
    if row_range is not None:
        start, end = row_range
        temp_path = _make_range_db(db_path, start, end)
        path = temp_path
    else:
        path = db_path

    start = time.perf_counter() if _METRICS_ENABLED else 0.0
    with open(path, "rb") as fh:
        for attempt in range(1, retries + 1):
            try:
                fh.seek(0)
                timeout_cfg = aiohttp.ClientTimeout(total=timeout)
                async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
                    form = aiohttp.FormData()
                    form.add_field("file", fh, filename=os.path.basename(db_path))
                    async with session.post(url, data=form) as resp:
                        resp.raise_for_status()
                logger.info("Database %s synced to %s", path, url)
                if temp_path is not None:
                    os.unlink(temp_path)
                if _METRICS_ENABLED:
                    _SUCCESS_TOTAL += 1
                    _LAST_DURATION = time.perf_counter() - start
                return
            except Exception as exc:  # pragma: no cover - network errors
                if attempt >= retries:
                    logger.error("Sync failed: %s", exc)
                    if temp_path is not None:
                        os.unlink(temp_path)
                    if _METRICS_ENABLED:
                        _FAILURE_TOTAL += 1
                        _LAST_DURATION = time.perf_counter() - start
                    raise
                await asyncio.sleep(delay)
                delay *= 2
