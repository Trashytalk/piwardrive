import importlib
import os
import sqlite3
import sys

from fastapi.testclient import TestClient


def _create_src_db(path: str) -> None:
    with sqlite3.connect(path) as db:
        db.execute(
            """CREATE TABLE health_records (
                timestamp TEXT PRIMARY KEY,
                cpu_temp REAL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL
            )"""
        )
        db.execute(
            """CREATE TABLE ap_cache (
                bssid TEXT,
                ssid TEXT,
                encryption TEXT,
                lat REAL,
                lon REAL,
                last_time INTEGER
            )"""
        )
        db.execute("INSERT INTO health_records VALUES ('t1', 40.0, 10.0, 50.0, 20.0)")
        db.execute("INSERT INTO health_records VALUES ('t2', 50.0, 20.0, 40.0, 30.0)")
        db.execute("INSERT INTO ap_cache VALUES ('b', 's', 'wpa', 1.0, 2.0, 0)")
        db.execute("INSERT INTO ap_cache VALUES ('c', 's', 'wpa', 1.1, 2.1, 0)")
        db.commit()


def test_upload_and_stats(tmp_path):
    os.environ["PW_AGG_DIR"] = str(tmp_path)
    module = importlib.import_module("piwardrive.aggregation_service")
    importlib.reload(module)
    db_path = tmp_path / "upload.db"
    _create_src_db(str(db_path))

    client = TestClient(module.app)
    with open(db_path, "rb") as fh:
        resp = client.post("/upload", files={"file": ("db", fh)})
    assert resp.status_code == 200

    resp = client.get("/stats")
    data = resp.json()
    assert round(data["temp_avg"], 1) == 45.0
    assert data["cpu_avg"] == 15.0

    resp = client.get("/overlay?bins=1")
    pts = resp.json()["points"]
    assert pts and pts[0][2] == 2


def test_upload_appends(tmp_path):
    os.environ["PW_AGG_DIR"] = str(tmp_path)
    module = importlib.import_module("piwardrive.aggregation_service")
    importlib.reload(module)
    db_path = tmp_path / "upload.db"
    _create_src_db(str(db_path))

    dest = tmp_path / "uploads" / "db"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("x")

    client = TestClient(module.app)
    with open(db_path, "rb") as fh:
        resp = client.post("/upload", files={"file": ("db", fh)})
    assert resp.status_code == 200
    assert dest.stat().st_size > 1


def test_upload_rejects_traversal(tmp_path):
    os.environ["PW_AGG_DIR"] = str(tmp_path)
    module = importlib.import_module("piwardrive.aggregation_service")
    importlib.reload(module)
    db_path = tmp_path / "upload.db"
    _create_src_db(str(db_path))

    client = TestClient(module.app)
    with open(db_path, "rb") as fh:
        resp = client.post("/upload", files={"file": ("../db", fh)})
    assert resp.status_code == 400


def test_upload_rejects_nested_traversal(tmp_path):
    os.environ["PW_AGG_DIR"] = str(tmp_path)
    module = importlib.import_module("piwardrive.aggregation_service")
    importlib.reload(module)
    db_path = tmp_path / "upload.db"
    _create_src_db(str(db_path))

    client = TestClient(module.app)
    with open(db_path, "rb") as fh:
        resp = client.post("/upload", files={"file": ("../../etc/passwd", fh)})
    assert resp.status_code == 400
