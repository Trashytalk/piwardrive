"""Remote data synchronization utilities."""

from __future__ import annotations

import asyncio
import logging
import os

import aiohttp


logger = logging.getLogger(__name__)


async def sync_database_to_server(
    db_path: str,
    url: str,
    *,
    timeout: int = 30,
    retries: int = 3,
) -> None:
    """Upload the SQLite database at ``db_path`` to ``url`` via HTTP POST.

    Retries the transfer with exponential backoff if ``aiohttp`` raises an
    exception or an HTTP error status is returned.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(db_path)

    delay = 1.0
    with open(db_path, "rb") as fh:
        for attempt in range(1, retries + 1):
            try:
                fh.seek(0)
                timeout_cfg = aiohttp.ClientTimeout(total=timeout)
                async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
                    form = aiohttp.FormData()
                    form.add_field("file", fh, filename=os.path.basename(db_path))
                    async with session.post(url, data=form) as resp:
                        resp.raise_for_status()
                logger.info("Database %s synced to %s", db_path, url)
                return
            except Exception as exc:  # pragma: no cover - network errors
                if attempt >= retries:
                    logger.error("Sync failed: %s", exc)
                    raise
                await asyncio.sleep(delay)
                delay *= 2
