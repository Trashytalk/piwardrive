"""Utilities for customizing MBTiles vector tile sets."""

from __future__ import annotations

import json
import logging
import os
import sqlite3


def apply_style(
    path: str,
    *,
    style_path: str | None = None,
    name: str | None = None,
    description: str | None = None,
) -> None:
    """Update ``path`` metadata with the given style and fields."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    style_json: str | None = None
    if style_path:
        try:
            with open(style_path, "r", encoding="utf-8") as fh:
                style_json = fh.read()
                json.loads(style_json)  # validate
        except OSError as exc:
            raise FileNotFoundError(style_path) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid style JSON in {style_path}: {exc}") from exc

    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS metadata (name TEXT, value TEXT)")
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
    """Create an MBTiles file from ``folder`` of XYZ PBF tiles."""
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
                if not f.endswith(".pb"):
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
                tile_row = (2**z_i - 1) - y_i  # TMS
                try:
                    with open(os.path.join(root, f), "rb") as fh:
                        data = fh.read()
                except OSError as exc:
                    logging.exception("Failed to read tile %s: %s", f, exc)
                    continue
                db.execute(
                    (
                        "INSERT OR REPLACE INTO tiles ",
                        "(zoom_level, tile_column, tile_row, tile_data) ",
                        "VALUES (?, ?, ?, ?)",
                    ),
                    (z_i, x_i, tile_row, data),
                )
        db.commit()
