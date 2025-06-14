import os
import sys
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import database


def test_init_db_creates_tables(tmp_path: Any) -> None:
    db_path = tmp_path / "test.db"
    conn = database.get_connection(str(db_path))
    database.init_db(conn)
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    names = {row[0] for row in rows}
    assert {"ap_data", "metrics"}.issubset(names)


def test_ingest_and_query(tmp_path: Any) -> None:
    db_path = tmp_path / "test.db"
    conn = database.get_connection(str(db_path))
    database.init_db(conn)

    aps = [
        {"bssid": "AA:BB", "ssid": "Test", "gps-info": (1.0, 2.0), "signal": -50}
    ]
    database.ingest_ap_data(conn, aps)
    ap_rows = database.query_recent_aps(conn)
    assert len(ap_rows) == 1
    assert ap_rows[0]["bssid"] == "AA:BB"

    metrics = {
        "cpu_temp": 42.0,
        "mem_pct": 12.0,
        "disk_pct": 33.0,
        "handshake_count": 2,
        "lat": 1.0,
        "lon": 2.0,
    }
    database.ingest_metrics(conn, metrics)
    metric_rows = database.query_recent_metrics(conn)
    assert len(metric_rows) == 1
    assert metric_rows[0]["cpu_temp"] == 42.0
