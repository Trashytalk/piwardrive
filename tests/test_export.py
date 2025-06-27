import importlib
import json
import os
import sys
import time
from types import ModuleType, SimpleNamespace

import pytest

import piwardrive.export as exp


def test_filter_records(monkeypatch: pytest.MonkeyPatch) -> None:
    records = [
        {
            "ssid": "A",
            "encryption": "WPA2",
            "bssid": "AA",
            "lat": 1.0,
            "lon": 2.0,
            "signal_dbm": -40,
            "last_time": 80,
        },
        {
            "ssid": "B",
            "encryption": "OPEN",
            "bssid": "BB",
            "lat": 3.0,
            "lon": 4.0,
            "signal_dbm": -80,
            "last_time": 20,
        },
    ]
    monkeypatch.setattr(time, "time", lambda: 100)
    assert exp.filter_records(records, encryption="OPEN") == [records[1]]
    assert exp.filter_records(records, oui="AA") == [records[0]]
    assert exp.filter_records(records, min_signal=-50) == [records[0]]
    assert exp.filter_records(records, max_age=30) == [records[0]]


def test_export_records_formats(tmp_path) -> None:
    recs = [{"ssid": "A", "bssid": "AA", "lat": 1.0, "lon": 2.0}]
    csv_path = tmp_path / "data.csv"
    exp.export_records(recs, str(csv_path), "csv")
    assert "ssid" in csv_path.read_text()

    json_path = tmp_path / "data.json"
    exp.export_records(recs, str(json_path), "json")
    assert json.load(open(json_path)) == recs

    gpx_path = tmp_path / "data.gpx"
    exp.export_records(recs, str(gpx_path), "gpx")
    assert "<wpt" in gpx_path.read_text()

    kml_path = tmp_path / "data.kml"
    exp.export_records(recs, str(kml_path), "kml")
    assert "<Placemark>" in kml_path.read_text()

    geo_path = tmp_path / "data.geojson"
    exp.export_records(recs, str(geo_path), "geojson")
    gj = json.load(open(geo_path))
    assert gj["features"][0]["geometry"]["coordinates"] == [2.0, 1.0]

    shp_path = tmp_path / "data.shp"
    exp.export_records(recs, str(shp_path), "shp")
    import shapefile
    r = shapefile.Reader(str(shp_path))
    assert r.numRecords == 1
    assert r.shapes()[0].points[0] == [2.0, 1.0]






def test_estimate_location_from_rssi() -> None:
    obs = [
        {"lat": 1.0, "lon": 1.0, "rssi": -30},
        {"lat": 2.0, "lon": 2.0, "rssi": -60},
    ]
    lat, lon = exp.estimate_location_from_rssi(obs)
    w1 = 1 / 30
    w2 = 1 / 60
    exp_lat = (1.0 * w1 + 2.0 * w2) / (w1 + w2)
    assert pytest.approx(lat) == exp_lat
    assert pytest.approx(lon) == exp_lat


def test_export_map_kml(tmp_path) -> None:
    track = [(1.0, 2.0), (3.0, 4.0)]
    aps = [{"ssid": "A", "lat": 1.0, "lon": 2.0}]
    bts = [{"name": "bt", "lat": 5.0, "lon": 6.0}]
    kml = tmp_path / "map.kml"
    exp.export_map_kml(track, aps, bts, str(kml))
    text = kml.read_text()
    assert "<LineString>" in text
    assert "2.0,1.0" in text
    assert "6.0,5.0" in text
    kmz = tmp_path / "map.kmz"
    exp.export_map_kml(track, aps, bts, str(kmz))
    import zipfile
    with zipfile.ZipFile(kmz) as zf:
        assert "doc.kml" in zf.namelist()
