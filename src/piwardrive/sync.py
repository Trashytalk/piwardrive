"""Module sync."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Sequence, Any

import aiohttp

from piwardrive import config


async def upload_data(records: Sequence[dict[str, Any]]) -> bool:
    """Upload ``records`` to the configured ``remote_sync_url``."""
    cfg = config.AppConfig.load()
    url = cfg.remote_sync_url
    if not url:
        return False

    timeout = aiohttp.ClientTimeout(total=cfg.remote_sync_timeout)
    headers = {}
    if cfg.remote_sync_token:
        headers["Authorization"] = f"Bearer {cfg.remote_sync_token}"

    payload = json.dumps(list(records))
    for attempt in range(1, cfg.remote_sync_retries + 1):
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, data=payload, headers=headers) as resp:
                    if resp.status == 200:
                        return True
                    raise RuntimeError(f"Status {resp.status}")
        except Exception as exc:  # pragma: no cover - network errors
            if attempt >= cfg.remote_sync_retries:
                logging.exception("upload_data failed: %s", exc)
                return False
            await asyncio.sleep(1)
    return False
