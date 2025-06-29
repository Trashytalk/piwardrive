import sqlite3
from pathlib import Path

import piwardrive.vector_tile_customizer as vtc  # noqa: E402


def test_apply_style(tmp_path: Path) -> None:
    db_path = tmp_path / "tiles.mbtiles"
    with sqlite3.connect(db_path) as db:
        db.execute("CREATE TABLE metadata (name TEXT, value TEXT)")

    style_file = tmp_path / "style.json"
    style_file.write_text('{"version":8}')

    vtc.apply_style(str(db_path), style_path=str(style_file), name="N", description="D")

    with sqlite3.connect(db_path) as db:
        rows = {k: v for k, v in db.execute("SELECT name, value FROM metadata")}
    assert rows["style"] == style_file.read_text()
    assert rows["name"] == "N"
    assert rows["description"] == "D"


def test_build_mbtiles(tmp_path: Path) -> None:
    folder = tmp_path / "tiles"
    (folder / "1" / "2").mkdir(parents=True)
    tile = folder / "1" / "2" / "3.pbf"
    tile.write_bytes(b"data")

    out = tmp_path / "out.mbtiles"
    vtc.build_mbtiles(str(folder), str(out))

    with sqlite3.connect(out) as db:
        row = db.execute(
            "SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles"
        ).fetchone()
    assert row == (1, 2, (2**1 - 1) - 3, b"data")
