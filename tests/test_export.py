import json
import importlib
import os
import sys
from types import ModuleType, SimpleNamespace

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import export as exp


def test_filter_records() -> None:
    records = [
        {"ssid": "A", "encryption": "WPA2", "bssid": "AA", "lat": 1.0, "lon": 2.0},
        {"ssid": "B", "encryption": "OPEN", "bssid": "BB", "lat": 3.0, "lon": 4.0},
    ]
    assert exp.filter_records(records, encryption="OPEN") == [records[1]]
    assert exp.filter_records(records, oui="AA") == [records[0]]


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


def load_map_screen(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    modules = {
        "kivy.app": ModuleType("kivy.app"),
        "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
        "kivy.metrics": ModuleType("kivy.metrics"),
        "kivy.clock": ModuleType("kivy.clock"),
        "kivy.uix.label": ModuleType("kivy.uix.label"),
        "kivymd.uix.dialog": ModuleType("kivymd.uix.dialog"),
        "kivymd.uix.menu": ModuleType("kivymd.uix.menu"),
        "kivymd.uix.snackbar": ModuleType("kivymd.uix.snackbar"),
        "kivymd.uix.textfield": ModuleType("kivymd.uix.textfield"),
    }
    modules["kivy.app"].App = type(
        "App",
        (),
        {"get_running_app": staticmethod(lambda: None)},
    )
    modules["kivy.clock"].Clock = SimpleNamespace(create_trigger=lambda *a, **k: lambda *a2, **k2: None)
    modules["kivy.clock"].mainthread = lambda f: f
    modules["kivy.metrics"].dp = lambda x: x
    modules["kivy.uix.label"].Label = object
    modules["kivy.uix.screenmanager"].Screen = object
    modules["kivymd.uix.dialog"].MDDialog = object
    modules["kivymd.uix.menu"].MDDropdownMenu = object
    modules["kivymd.uix.textfield"].MDTextField = object

    class DummySnackbar:
        def __init__(self, *args, **kwargs):
            pass

        def open(self) -> None:
            pass

    modules["kivymd.uix.snackbar"].Snackbar = DummySnackbar

    mapview = ModuleType("kivy_garden.mapview")
    mapview.MapMarker = object
    mapview.MapMarkerPopup = object
    mapview.MBTilesMapSource = object
    mapview.LineMapLayer = object
    modules["kivy_garden.mapview"] = mapview

    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)

    if "screens.map_screen" in sys.modules:
        monkeypatch.delitem(sys.modules, "screens.map_screen", raising=False)

    return importlib.import_module("screens.map_screen")


def test_screen_export_ap_data(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    mod = load_map_screen(monkeypatch)
    screen = mod.MapScreen()
    screen.ap_markers = [
        SimpleNamespace(lat=1.0, lon=2.0, ap_data={"ssid": "A", "bssid": "AA", "encryption": "WPA2"}),
        SimpleNamespace(lat=3.0, lon=4.0, ap_data={"ssid": "B", "bssid": "BB", "encryption": "OPEN"}),
    ]
    out = tmp_path / "out.json"
    records = [
        {**getattr(m, "ap_data", {}), "lat": m.lat, "lon": m.lon}
        for m in screen.ap_markers
    ]
    filtered = exp.filter_records(records, encryption="OPEN")
    exp.export_records(filtered, str(out), "json")
    data = json.load(open(out))
    assert len(data) == 1
    assert data[0]["ssid"] == "B"
