"""Utilities for customizing MBTiles vector tile sets."""

from __future__ import annotations

import json
import os
import sqlite3


def apply_style(
    path: str,
    *,
    style_path: str | None = None,
    name: str | None = None,
    description: str | None = None,
) -> None:
    """
    Updates the metadata of an MBTiles file with optional style, name, and description fields.
    
    If a style JSON file is provided, its contents are validated and stored in the metadata. The function creates the metadata table if it does not exist and inserts or replaces the specified fields.
    
    Raises:
        FileNotFoundError: If the MBTiles file at the given path does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    style_json: str | None = None
    if style_path:
        with open(style_path, "r", encoding="utf-8") as fh:
            style_json = fh.read()
            json.loads(style_json)  # validate

    with sqlite3.connect(path) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS metadata (name TEXT, value TEXT)"
        )
        for key, value in (
            ("name", name),
            ("description", description),
            ("style", style_json),
        ):
            if value is not None:
                db.execute(
                    "INSERT OR REPLACE INTO metadata (name, value) VALUES (?, ?)",
                    (key, value),
                )
        db.commit()


def build_mbtiles(folder: str, output: str) -> None:
    """
    Create an MBTiles SQLite file at the specified output path by importing XYZ-format PBF tiles from a directory.
    
    Recursively scans the input folder for `.pbf` files organized in a three-level directory structure representing zoom, x, and y tile coordinates. Converts the y coordinate from XYZ to TMS format and inserts the tile data into the MBTiles database. Skips files that do not conform to the expected structure or have invalid coordinate values.
    
    Parameters:
        folder (str): Path to the root directory containing XYZ PBF tiles.
        output (str): Path where the resulting MBTiles file will be created.
    
    Raises:
        FileNotFoundError: If the input folder does not exist or is not a directory.
    """
    if not os.path.isdir(folder):
        raise FileNotFoundError(folder)

    with sqlite3.connect(output) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS tiles (
                zoom_level INTEGER,
                tile_column INTEGER,
                tile_row INTEGER,
                tile_data BLOB,
                UNIQUE (zoom_level, tile_column, tile_row)
            );
            CREATE TABLE IF NOT EXISTS metadata (name TEXT, value TEXT);
            """
        )
        for root, _, files in os.walk(folder):
            for f in files:
                if not f.endswith(".pbf"):
                    continue
                zxy = os.path.relpath(os.path.join(root, f), folder).split(os.sep)
                if len(zxy) != 3:
                    continue
                z, x, yext = zxy
                y, _ = os.path.splitext(yext)
                try:
                    z_i = int(z)
                    x_i = int(x)
                    y_i = int(y)
                except ValueError:
                    continue
                tile_row = (2 ** z_i - 1) - y_i  # TMS
                with open(os.path.join(root, f), "rb") as fh:
                    data = fh.read()
                db.execute(
                    (
                        "INSERT OR REPLACE INTO tiles (zoom_level, tile_column, "
                        "tile_row, tile_data)"
                    ),
                    (z_i, x_i, tile_row, data),
                )
        db.commit()
