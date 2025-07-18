"""Helpers for uploading data to various storage backends."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Iterable, Mapping

from . import cloud_export

logger = logging.getLogger(__name__)


async def upload_to_s3(
    path: str, bucket: str, key: str, profile: str | None = None
) -> None:
    """Upload ``path`` to an S3 ``bucket`` using :mod:`cloud_export`."""
    await asyncio.to_thread(cloud_export.upload_to_s3, path, bucket, key, profile)


async def write_influxdb(
    url: str,
    token: str,
    org: str,
    bucket: str,
    records: Iterable[str],
) -> None:
    """POST line protocol ``records`` to InfluxDB."""
    try:
        from aiohttp import ClientSession
    except Exception as exc:  # pragma: no cover - optional dep
        raise RuntimeError("aiohttp required for InfluxDB uploads") from exc

    endpoint = f"{url.rstrip('/')}/api/v2/write"
    params = {"org": org, "bucket": bucket, "precision": "s"}
    headers = {"Authorization": f"Token {token}"}
    _data = "\n".join(records).encode()
    async with ClientSession() as session:
        async with session.post(
            endpoint, params=params, data=_data, headers=headers
        ) as resp:
            resp.raise_for_status()


async def write_postgres(
    dsn: str, table: str, rows: Iterable[Mapping[str, Any]]
) -> None:
    """Insert ``rows`` into ``table`` on the Postgres server ``dsn``."""
    try:
        import asyncpg
    except Exception as exc:  # pragma: no cover - optional dep
        raise RuntimeError("asyncpg required for Postgres uploads") from exc

    rows = list(rows)
    if not rows:
        return

    columns = list(rows[0].keys())
    values = [tuple(r[c] for c in columns) for r in rows]
    placeholders = ", ".join(f"${i}" for i in range(1, len(columns) + 1))
    query = f'INSERT INTO {table} ({", ".join(columns)}) VALUES ({placeholders})'

    conn = await asyncpg.connect(dsn)
    try:
        await conn.executemany(query, values)
    finally:
        await conn.close()
