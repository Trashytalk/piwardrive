import importlib
import os
import sys
from types import ModuleType, SimpleNamespace
import pytest
import piwardrive.export as exp


def load_map_screen(monkeypatch):
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

    class DummyLabel:
        def __init__(self, *a, **k):
            pass
    modules["kivy.uix.label"].Label = DummyLabel
    modules["kivy.uix.screenmanager"].Screen = object
    modules["kivymd.uix.dialog"].MDDialog = object
    modules["kivymd.uix.menu"].MDDropdownMenu = object
    modules["kivymd.uix.textfield"].MDTextField = object

    class DummySnackbar:
        def __init__(self, *a, **k):
            pass
        def open(self):
            pass
    modules["kivymd.uix.snackbar"].Snackbar = DummySnackbar

    mapview = ModuleType("kivy_garden.mapview")
    class DummyMarker:
        def __init__(self, lat=0.0, lon=0.0, **_):
            self.lat = lat
            self.lon = lon
        def add_widget(self, *a, **k):
            pass
    mapview.MapMarker = DummyMarker
    mapview.MapMarkerPopup = DummyMarker
    mapview.MBTilesMapSource = object
    mapview.LineMapLayer = object
    modules["kivy_garden.mapview"] = mapview

    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)

    if "piwardrive.screens.map_screen" in sys.modules:
        monkeypatch.delitem(
            sys.modules, "piwardrive.screens.map_screen", raising=False
        )

    return importlib.import_module("piwardrive.screens.map_screen")


def test_plot_aps_estimates_location(monkeypatch):
    mod = load_map_screen(monkeypatch)
    class DummyApp:
        map_show_aps = True
        map_cluster_aps = False

    monkeypatch.setattr(mod.App, "get_running_app", staticmethod(lambda: DummyApp()))
    screen = mod.MapScreen()
    markers = []
    screen.ids = SimpleNamespace(
        mapview=SimpleNamespace(
            add_widget=lambda m: markers.append(m),
            remove_widget=lambda m: None,
            bind=lambda *a, **k: None,
            zoom=1,
        )
    )

    obs = [
        {"lat": 1.0, "lon": 2.0, "rssi": -30},
        {"lat": 2.0, "lon": 3.0, "rssi": -60},
    ]
    data = {"devices": [{"bssid": "AA", "ssid": "A", "encryption": "WPA2", "observations": obs}]}

    class FakeResp:
        def raise_for_status(self):
            pass
        def json(self):
            return data

    monkeypatch.setattr(screen._http, "get", lambda *a, **k: FakeResp())

    screen.plot_aps()

    assert len(markers) == 1
    lat_exp, lon_exp = exp.estimate_location_from_rssi(obs)
    m = markers[0]
    assert pytest.approx(m.lat) == lat_exp
    assert pytest.approx(m.lon) == lon_exp
