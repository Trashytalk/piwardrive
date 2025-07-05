from __future__ import annotations

"""Central aggregation server for PiWardrive units."""

import asyncio
import logging
import os
import shutil
import tempfile
from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Iterable, List, Tuple

import aiosqlite
from fastapi import FastAPI, HTTPException, UploadFile

from . import analysis, heatmap
from .persistence import HealthRecord
from .security import validate_filename

DATA_DIR = os.path.expanduser(os.getenv("PW_AGG_DIR", "~/piwardrive-aggregation"))
DB_PATH = os.path.join(DATA_DIR, "aggregation.db")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
DEFAULT_PORT = 9100

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

_POOL: asyncio.Queue[aiosqlite.Connection] | None = None
_POOL_SIZE = int(os.getenv("PW_AGG_POOL_SIZE", "5"))


async def _init_pool() -> None:
    """Initialize the global connection pool if needed."""
    global _POOL
    if _POOL is not None:
        return
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    _POOL = asyncio.Queue(maxsize=_POOL_SIZE)
    for _ in range(_POOL_SIZE):
        conn = await aiosqlite.connect(DB_PATH)
        await conn.execute("PRAGMA journal_mode=WAL")
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS health_records (
                timestamp TEXT PRIMARY KEY,
                cpu_temp REAL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL
            )
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ap_points (
                lat REAL,
                lon REAL
            )
            """
        )
        await conn.commit()
        _POOL.put_nowait(conn)


@asynccontextmanager
async def _get_conn() -> AsyncIterator[aiosqlite.Connection]:
    """Yield a connection from the pool."""
    await _init_pool()
    if _POOL is None:
        raise RuntimeError("connection pool not initialized")
    conn = await _POOL.get()
    try:
        yield conn
    finally:
        await _POOL.put(conn)


async def _merge_records(
    records: Iterable[Tuple[str, float | None, float, float, float]],
) -> None:
    async with _get_conn() as conn:
        await conn.executemany(
            """INSERT OR IGNORE INTO health_records
            (timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent)
            VALUES (?, ?, ?, ?, ?)""",
            records,
        )
        await conn.commit()


async def _merge_points(points: Iterable[Tuple[float, float]]) -> None:
    async with _get_conn() as conn:
        await conn.executemany(
            "INSERT INTO ap_points (lat, lon) VALUES (?, ?)",
            points,
        )
        await conn.commit()


async def _process_upload(path: str) -> None:
    async with aiosqlite.connect(path) as db:
        cur = await db.execute(
            "SELECT timestamp, cpu_temp, cpu_percent, memory_percent, "
            "disk_percent FROM health_records"
        )
        recs = await cur.fetchall()
        await _merge_records([tuple(r) for r in recs])
        cur = await db.execute(
            "SELECT lat, lon FROM ap_cache WHERE lat IS NOT NULL AND lon IS NOT NULL"
        )
        pts = await cur.fetchall()
        await _merge_points([(float(r[0]), float(r[1])) for r in pts])


@app.post("/upload")
async def upload(file: UploadFile) -> Dict[str, str]:  # noqa: V103 - FastAPI route
    """Save ``file`` and merge its contents into the aggregation database."""
    # Called by FastAPI as a route handler.
    filename = file.filename or ""
    name = os.path.basename(filename)
    if name != filename:
        raise HTTPException(
            status_code=400, detail=f"Invalid filename: {file.filename}"
        )
    try:
        validate_filename(name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    dest = os.path.join(UPLOAD_DIR, name)
    fd, tmp_path = tempfile.mkstemp(dir=UPLOAD_DIR)
    os.close(fd)
    try:
        with open(tmp_path, "wb") as fh:
            shutil.copyfileobj(file.file, fh)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to save upload %s: %s", tmp_path, exc)
        raise
    await _process_upload(tmp_path)
    try:
        with open(tmp_path, "rb") as src, open(dest, "ab") as out:
            shutil.copyfileobj(src, out)
        os.remove(tmp_path)
    except OSError as exc:  # pragma: no cover - write errors
        logging.exception("Failed to finalize upload %s: %s", dest, exc)
        raise
    return {"saved": dest}


@app.get("/stats")
async def stats() -> Dict[str, float]:  # noqa: V103 - FastAPI route
    """Return averaged system metrics from all records."""
    # Called by FastAPI as a route handler.
    async with _get_conn() as conn:
        cur = await conn.execute(
            "SELECT timestamp, cpu_temp, cpu_percent, memory_percent, "
            "disk_percent FROM health_records"
        )
        rows = await cur.fetchall()
        records = [HealthRecord(*row) for row in rows]
    return analysis.compute_health_stats(records)


@app.get("/overlay")
async def overlay(bins: int = 100) -> Dict[str, List[Tuple[float, float, int]]]:
    # noqa: V103 - FastAPI route
    """Return heatmap points derived from all uploaded access points."""
    # Called by FastAPI as a route handler.
    async with _get_conn() as conn:
        cur = await conn.execute("SELECT lat, lon FROM ap_points")
        coords = [(float(r[0]), float(r[1])) for r in await cur.fetchall()]
    hist, lat_range, lon_range = heatmap.histogram(coords, bins=bins)
    points = heatmap.histogram_points(hist, lat_range, lon_range)
    return {"points": points}


async def main() -> None:
    import uvicorn

    await _init_pool()
    port = int(os.getenv("PW_AGG_PORT", str(DEFAULT_PORT)))
    config = uvicorn.Config(app, host="0.0.0.0", port=port)  # nosec B104
    server = uvicorn.Server(config)
    await server.serve()


__all__ = ["app", "main", "upload", "stats", "overlay"]

if __name__ == "__main__":
    asyncio.run(main())
