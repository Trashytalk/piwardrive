import asyncio
import sqlite3
from pathlib import Path

from piwardrive.advanced_localization import load_kismet_data


def create_kismet_db(path: Path) -> None:
    """Create a minimal kismet-like database with sample rows."""
    with sqlite3.connect(path) as conn:
        conn.execute(
            "CREATE TABLE devices (devicekey INTEGER PRIMARY KEY, macaddr TEXT,"
            " ssid TEXT, type TEXT)"
        )
        conn.execute(
            "CREATE TABLE packets (devicekey INTEGER, lat REAL, lon REAL, signal "
            "INTEGER, gpstime INTEGER)"
        )
        conn.execute(
            "INSERT INTO devices VALUES (1, 'aa:bb:cc', 'test', 'infrastructure')"
        )
        conn.execute("INSERT INTO devices VALUES (2, 'dd:ee:ff', 'skip', 'client')")
        conn.execute("INSERT INTO packets VALUES (1, 10.0, 20.0, -30, 1000)")
        conn.execute("INSERT INTO packets VALUES (2, 1.0, 2.0, -40, 2000)")
        conn.commit()


def test_load_kismet_data_filters_and_returns_dataframe(tmp_path: Path) -> None:
    db = tmp_path / "kismet.db"
    create_kismet_db(db)

    df = asyncio.run(load_kismet_data(db))

    assert list(df.columns) == [
        "macaddr",
        "ssid",
        "lat",
        "lon",
        "rssi",
        "gpstime",
    ]
    assert len(df) == 1

    row = df.iloc[0]
    assert row["macaddr"] == "aa:bb:cc"
    assert row["ssid"] == "test"
    assert row["lat"] == 10.0
    assert row["lon"] == 20.0
    assert row["rssi"] == -30
    assert row["gpstime"] == 1000
