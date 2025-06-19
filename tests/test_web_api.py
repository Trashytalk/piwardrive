import importlib.util
from pathlib import Path
import sqlite3

from fastapi.testclient import TestClient


def load_web_api():
    path = Path('In development') / 'web_api.py'
    spec = importlib.util.spec_from_file_location('web_api', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module


def test_get_gps(tmp_path, monkeypatch):
    mod = load_web_api()
    db = tmp_path / 'db.sqlite'
    with sqlite3.connect(db) as conn:
        conn.execute('CREATE TABLE gps_tracks (lat REAL, lon REAL, time TEXT)')
        conn.execute("INSERT INTO gps_tracks VALUES (1.2, 3.4, 't')")
        conn.commit()

    def fake_path(p):
        return db if p.endswith('db.sqlite') else Path(p)
    monkeypatch.setattr(mod, 'Path', fake_path)

    client = TestClient(mod.app)
    resp = client.get('/api/gps')
    assert resp.json() == {'lat': 1.2, 'lon': 3.4, 'time': 't'}


def test_get_aps(tmp_path, monkeypatch):
    mod = load_web_api()
    aps = tmp_path / 'aps.geojson'
    aps.write_text('{"features": [1]}')

    def fake_path(p):
        return aps if p.endswith('aps.geojson') else Path(p)
    monkeypatch.setattr(mod, 'Path', fake_path)

    client = TestClient(mod.app)
    resp = client.get('/api/aps')
    assert resp.json()['features'] == [1]


def test_get_bt(tmp_path, monkeypatch):
    mod = load_web_api()
    bt = tmp_path / 'bt.geojson'
    bt.write_text('{"features": [2]}')

    def fake_path(p):
        return bt if p.endswith('bt.geojson') else Path(p)
    monkeypatch.setattr(mod, 'Path', fake_path)

    client = TestClient(mod.app)
    resp = client.get('/api/bt')
    assert resp.json()['features'] == [2]


def test_toggle_kismet(monkeypatch):
    mod = load_web_api()
    calls = []
    monkeypatch.setattr(mod.subprocess, 'run', lambda cmd, check=False: calls.append(cmd))

    client = TestClient(mod.app)
    resp = client.post('/api/kismet/toggle', params={'state': 'start'})
    assert resp.status_code == 200
    resp = client.post('/api/kismet/toggle', params={'state': 'stop'})
    assert calls == [["sudo", "systemctl", "start", "kismet"], ["sudo", "systemctl", "stop", "kismet"]]
