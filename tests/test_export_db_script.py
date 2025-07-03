import json
import sys

import pytest


@pytest.mark.parametrize("fmt,check", [
    ("csv", lambda p: "ssid" in p.read_text()),
    ("json", lambda p: json.loads(p.read_text())[0]["ssid"] == "A"),
    ("gpx", lambda p: "<wpt" in p.read_text()),
    ("kml", lambda p: "<Placemark>" in p.read_text()),
])
def test_export_db_script(monkeypatch, tmp_path, fmt, check):
    records = [{"ssid": "A", "bssid": "AA", "lat": 1.0, "lon": 2.0}]

    async def fake_load_ap_cache():
        return records

    if "piwardrive.scripts.export_db" in sys.modules:
        del sys.modules["piwardrive.scripts.export_db"]
    import piwardrive.scripts.export_db as ed

    monkeypatch.setattr(ed.database.persistence, "load_ap_cache", fake_load_ap_cache)

    out = tmp_path / f"data.{fmt}"
    ed.main([str(out), "--format", fmt])
    assert check(out)
