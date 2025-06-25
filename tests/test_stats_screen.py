import importlib
from types import ModuleType, SimpleNamespace

import sys


def _load_screen(monkeypatch):
    modules = {
        "kivy.app": ModuleType("kivy.app"),
        "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
    }
    modules["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
    modules["kivy.uix.screenmanager"].Screen = object
    for n, m in modules.items():
        monkeypatch.setitem(sys.modules, n, m)
    if "piwardrive.screens.stats_screen" in sys.modules:
        monkeypatch.delitem(sys.modules, "piwardrive.screens.stats_screen")
    return importlib.import_module("piwardrive.screens.stats_screen")


class DummyLabel:
    def __init__(self) -> None:
        self.text = ""

def test_update_stats_uses_monitor(monkeypatch):
    mod = _load_screen(monkeypatch)
    # patch translation to identity
    monkeypatch.setattr(mod, "_", lambda x: x)

    StatsScreen = mod.StatsScreen

    root = SimpleNamespace(ids={
        "cpu_label": DummyLabel(),
        "mem_label": DummyLabel(),
        "disk_label": DummyLabel(),
    })

    monitor = SimpleNamespace(data={
        "system": {
            "cpu_temp": 40.0,
            "memory_percent": 25.0,
            "disk_percent": 55.0,
            "ssd_smart": "OK",
        },
        "services": {"kismet": True, "bettercap": False},
    })

    app = SimpleNamespace(root=root, scheduler=SimpleNamespace(), health_monitor=monitor)
    sys.modules["kivy.app"].App.get_running_app = staticmethod(lambda: app)

    screen = object.__new__(StatsScreen)
    screen.ids = {
        "disk_health_label": DummyLabel(),
        "kismet_status_label": DummyLabel(),
        "bettercap_status_label": DummyLabel(),
    }

    StatsScreen.update_stats(screen, 0)

    assert "40" in root.ids["cpu_label"].text
    assert "25" in root.ids["mem_label"].text
    assert "55" in root.ids["disk_label"].text
    assert "OK" in screen.ids["disk_health_label"].text
    assert "OK" in screen.ids["kismet_status_label"].text
    assert "DOWN" in screen.ids["bettercap_status_label"].text
