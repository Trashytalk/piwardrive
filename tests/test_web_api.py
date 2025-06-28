import json
import os
import sqlite3
import subprocess
import urllib.request
from pathlib import Path

SERVER_FILE = Path("In development") / "web_api.js"


def start_server(tmp_path):
    env = os.environ.copy()
    env["PW_GPS_DB"] = str(tmp_path / "db.sqlite")
    env["PW_APS_FILE"] = str(tmp_path / "aps.geojson")
    env["PW_BT_FILE"] = str(tmp_path / "bt.geojson")
    env["PW_RUN_LOG"] = str(tmp_path / "run.log")
    env["PORT"] = "0"
    proc = subprocess.Popen(
        ["node", str(SERVER_FILE)], stdout=subprocess.PIPE, text=True, env=env
    )
    line = proc.stdout.readline()
    if not line.startswith("Listening on "):
        proc.kill()
        raise RuntimeError("server failed to start")
    port = int(line.strip().split()[-1])
    return proc, port, Path(env["PW_RUN_LOG"])


def request_json(port, path, method="GET"):
    req = urllib.request.Request(f"http://127.0.0.1:{port}{path}", method=method)
    with urllib.request.urlopen(req) as resp:  # nosec B310
        return json.loads(resp.read())


def test_get_gps(tmp_path):
    db = tmp_path / "db.sqlite"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE gps_tracks (lat REAL, lon REAL, time TEXT)")
        conn.execute("INSERT INTO gps_tracks VALUES (1.2, 3.4, 't')")
        conn.commit()

    proc, port, _ = start_server(tmp_path)
    try:
        data = request_json(port, "/api/gps")
        assert data == {"lat": 1.2, "lon": 3.4, "time": "t"}
    finally:
        proc.terminate()
        proc.wait()


def test_get_aps(tmp_path):
    aps = tmp_path / "aps.geojson"
    aps.write_text('{"features": [1]}')

    proc, port, _ = start_server(tmp_path)
    try:
        data = request_json(port, "/api/aps")
        assert data["features"] == [1]
    finally:
        proc.terminate()
        proc.wait()


def test_get_bt(tmp_path):
    bt = tmp_path / "bt.geojson"
    bt.write_text('{"features": [2]}')

    proc, port, _ = start_server(tmp_path)
    try:
        data = request_json(port, "/api/bt")
        assert data["features"] == [2]
    finally:
        proc.terminate()
        proc.wait()


def test_toggle_kismet(tmp_path):
    proc, port, log = start_server(tmp_path)
    try:
        request_json(port, "/api/kismet/toggle?state=start", method="POST")
        request_json(port, "/api/kismet/toggle?state=stop", method="POST")
    finally:
        proc.terminate()
        proc.wait()

    lines = [json.loads(l) for l in log.read_text().splitlines()]
    assert lines == [
        ["sudo", "systemctl", "start", "kismet"],
        ["sudo", "systemctl", "stop", "kismet"],
    ]
