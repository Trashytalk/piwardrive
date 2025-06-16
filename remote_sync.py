"""Remote data synchronization utilities."""

from __future__ import annotations

import logging
import os
import requests


logger = logging.getLogger(__name__)


def sync_database_to_server(db_path: str, url: str) -> None:
    """Upload the SQLite database at ``db_path`` to ``url`` via HTTP POST."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(db_path)
    try:
        with open(db_path, "rb") as fh:
            files = {"file": fh}
            resp = requests.post(url, files=files, timeout=30)
            resp.raise_for_status()
        logger.info("Database %s synced to %s", db_path, url)
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("Sync failed: %s", exc)
        raise
