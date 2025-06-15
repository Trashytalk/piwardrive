import os
import sys
from types import ModuleType
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

aiohttp_mod = ModuleType("aiohttp")
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules["aiohttp"] = aiohttp_mod

# provide dummy kivy modules
modules = {
    "kivy.app": ModuleType("kivy.app"),
    "kivy.metrics": ModuleType("kivy.metrics"),
    "kivymd.uix.label": ModuleType("kivymd.uix.label"),
    "kivy.uix.behaviors": ModuleType("kivy.uix.behaviors"),
    "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
    "kivymd.uix.card": ModuleType("kivymd.uix.card"),
}
modules["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
modules["kivy.metrics"].dp = lambda x: x
modules["kivy.metrics"].sp = lambda x: x
modules["kivy.uix.behaviors"].DragBehavior = type("DragBehavior", (), {})
modules["kivymd.uix.label"].MDLabel = type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""})
modules["kivymd.uix.boxlayout"].MDBoxLayout = type("MDBoxLayout", (), {})
modules["kivymd.uix.card"].MDCard = type("MDCard", (), {})
for name, mod in modules.items():
    sys.modules[name] = mod

import widgets.battery_status as bs

class DummyBattery:
    def __init__(self, percent: float, plugged: bool) -> None:
        self.percent = percent
        self.power_plugged = plugged

def test_widget_updates(monkeypatch: Any) -> None:
    widget = object.__new__(bs.BatteryStatusWidget)
    widget.label = modules["kivymd.uix.label"].MDLabel()
    monkeypatch.setattr(bs.psutil, "sensors_battery", lambda: DummyBattery(50, False))
    bs.BatteryStatusWidget.update(widget)
    assert "50" in widget.label.text
