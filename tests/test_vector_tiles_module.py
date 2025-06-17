import sqlite3
import pytest

import piwardrive.vector_tiles as vt


def create_db(path):
    with sqlite3.connect(path) as db:
        db.execute(
            "CREATE TABLE tiles (zoom_level INTEGER, tile_column INTEGER, tile_row INTEGER, tile_data BLOB)"
        )
        db.execute("INSERT INTO tiles VALUES (1, 2, 3, ?)", (b'data',))
        db.execute("INSERT INTO tiles VALUES (2, 0, 0, ?)", (b'foo',))


def test_mbtile_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        vt.MBTiles(str(tmp_path / 'missing.mbtiles'))


def test_tiles_and_available(tmp_path):
    dbfile = tmp_path / 'tiles.mbtiles'
    create_db(dbfile)
    m = vt.MBTiles(str(dbfile))
    assert m.tiles(1, 2, 3) == b'data'
    assert m.tiles(9, 9, 9) is None
    tiles = set(vt.available_tiles(str(dbfile)))
    assert tiles == {(1, 2, 3), (2, 0, 0)}
