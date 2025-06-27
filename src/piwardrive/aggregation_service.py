from __future__ import annotations

"""Central aggregation server for PiWardrive units."""

import asyncio
import logging
import os
import shutil
import tempfile
from typing import Dict, Iterable, List, Tuple

import aiosqlite
from fastapi import FastAPI, UploadFile

from . import analysis, heatmap
from .persistence import HealthRecord

DATA_DIR = os.path.expanduser(os.getenv("PW_AGG_DIR", "~/piwardrive-aggregation"))
DB_PATH = os.path.join(DATA_DIR, "aggregation.db")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

_DB_CONN: aiosqlite.Connection | None = None


async def _get_conn() -> aiosqlite.Connection:
    """Return cached connection to the aggregation database."""
    global _DB_CONN
    if _DB_CONN is None:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        _DB_CONN = await aiosqlite.connect(DB_PATH)
        await _DB_CONN.execute("PRAGMA journal_mode=WAL")
        await _DB_CONN.execute(
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
        await _DB_CONN.execute(
            """
            CREATE TABLE IF NOT EXISTS ap_points (
                lat REAL,
                lon REAL
            )
            """
        )
        await _DB_CONN.commit()
    return _DB_CONN


async def _merge_records(
    records: Iterable[Tuple[str, float | None, float, float, float]],
) -> None:
    conn = await _get_conn()
    await conn.executemany(
        """INSERT OR IGNORE INTO health_records
            (timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent)
            VALUES (?, ?, ?, ?, ?)""",
        records,
    )
    await conn.commit()


async def _merge_points(points: Iterable[Tuple[float, float]]) -> None:
    conn = await _get_conn()
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
        await _merge_records(recs)
        cur = await db.execute(
            "SELECT lat, lon FROM ap_cache WHERE lat IS NOT NULL AND lon IS NOT NULL"
        )
        pts = await cur.fetchall()
        await _merge_points([(float(r[0]), float(r[1])) for r in pts])


@app.post("/upload")
async def upload(file: UploadFile) -> Dict[str, str]:  # noqa: V103 - FastAPI route
    """Save ``file`` and merge its contents into the aggregation database."""
    # Called by FastAPI as a route handler.
    dest = os.path.join(UPLOAD_DIR, file.filename)
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
    conn = await _get_conn()
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
    conn = await _get_conn()
    cur = await conn.execute("SELECT lat, lon FROM ap_points")
    coords = [(float(r[0]), float(r[1])) for r in await cur.fetchall()]
    hist, lat_range, lon_range = heatmap.histogram(coords, bins=bins)
    points = heatmap.histogram_points(hist, lat_range, lon_range)
    return {"points": points}


async def main() -> None:
    import uvicorn

    await _get_conn()
    config = uvicorn.Config(app, host="0.0.0.0", port=9100)  # nosec B104
    server = uvicorn.Server(config)
    await server.serve()


__all__ = ["app", "main", "upload", "stats", "overlay"]


if __name__ == "__main__":
    asyncio.run(main())
