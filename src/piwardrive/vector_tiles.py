"""Offline vector tile helpers."""

from __future__ import annotations

import logging
import os
import sqlite3
from typing import Iterable, Tuple

logger = logging.getLogger(__name__)


class MBTiles:
    """Simple reader for MBTiles formatted vector tiles."""

    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.path = path

    def tiles(self, z: int, x: int, y: int) -> bytes | None:
        try:
            with sqlite3.connect(self.path) as db:
                cur = db.execute(
                    "SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
                    (z, x, y),
                )
                row = cur.fetchone()
                return row[0] if row else None
        except Exception as exc:  # pragma: no cover - database errors
            logger.error("Tile read failed: %s", exc)
            return None


def available_tiles(path: str) -> Iterable[Tuple[int, int, int]]:
    """Yield ``(z, x, y)`` for tiles stored in ``path``."""
    with sqlite3.connect(path) as db:
        cur = db.execute("SELECT zoom_level, tile_column, tile_row FROM tiles")
        yield from cur.fetchall()
