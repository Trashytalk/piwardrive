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
        """
        Initialize an MBTiles reader for the specified file path.
        
        Raises:
            FileNotFoundError: If the provided path does not exist.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.path = path

    def tiles(self, z: int, x: int, y: int) -> bytes | None:
        """
        Retrieve the raw vector tile data for the specified zoom level, column, and row.
        
        Parameters:
        	z (int): Zoom level of the tile.
        	x (int): Tile column.
        	y (int): Tile row.
        
        Returns:
        	bytes | None: The raw tile data as bytes if found; otherwise, None.
        """
        try:
            with sqlite3.connect(self.path) as db:
                cur = db.execute(
                    (
                        "SELECT tile_data FROM tiles WHERE zoom_level=? "
                        "AND tile_column=? AND tile_row=?"
                    ),
                    (z, x, y),
                )
                row = cur.fetchone()
                return row[0] if row else None
        except Exception as exc:  # pragma: no cover - database errors
            logger.error("Tile read failed: %s", exc)
            return None


def available_tiles(path: str) -> Iterable[Tuple[int, int, int]]:
    """
    Yield (z, x, y) tuples for all tiles stored in the MBTiles file at the specified path.
    
    Parameters:
        path (str): Path to the MBTiles SQLite database file.
    
    Yields:
        Tuple[int, int, int]: Tuples representing the zoom level, column, and row of each available tile.
    """
    with sqlite3.connect(path) as db:
        cur = db.execute("SELECT zoom_level, tile_column, tile_row FROM tiles")
        yield from cur.fetchall()
