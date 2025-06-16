import os
import sys
from types import ModuleType
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# provide dummy kivy modules
modules = {
    "kivy.metrics": ModuleType("kivy.metrics"),
    "kivymd.uix.label": ModuleType("kivymd.uix.label"),
    "kivymd.uix.card": ModuleType("kivymd.uix.card"),
    "kivy.uix.behaviors": ModuleType("kivy.uix.behaviors"),
    "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
}
modules["kivy.metrics"].dp = lambda x: x
modules["kivymd.uix.label"].MDLabel = type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""})
modules["kivymd.uix.card"].MDCard = type("MDCard", (), {"__init__": lambda self, **kw: None, "add_widget": lambda self, w: None})
modules["kivy.uix.behaviors"].DragBehavior = type("DragBehavior", (), {})
modules["kivymd.uix.boxlayout"].MDBoxLayout = type("MDBoxLayout", (), {})
for n, m in modules.items():
    sys.modules[n] = m

import widgets.orientation_widget as ow
import widgets.vehicle_speed as vs
import widgets.lora_scan_widget as lw


def test_orientation_widget(monkeypatch: Any) -> None:
    widget = object.__new__(ow.OrientationWidget)
    widget.label = modules["kivymd.uix.label"].MDLabel()
    monkeypatch.setattr(ow.orientation_sensors, "get_orientation_dbus", lambda: "right-up")
    monkeypatch.setattr(ow.orientation_sensors, "orientation_to_angle", lambda o: 90.0)
    ow.OrientationWidget.update(widget)
    assert "right-up" in widget.label.text


def test_vehicle_speed_widget(monkeypatch: Any) -> None:
    widget = object.__new__(vs.VehicleSpeedWidget)
    widget.label = modules["kivymd.uix.label"].MDLabel()
    monkeypatch.setattr(vs.vehicle_sensors, "read_speed_obd", lambda port=None: 42.5)
    vs.VehicleSpeedWidget.update(widget)
    assert "42.5" in widget.label.text


def test_lora_scan_widget(monkeypatch: Any) -> None:
    widget = object.__new__(lw.LoRaScanWidget)
    widget.label = modules["kivymd.uix.label"].MDLabel()
    monkeypatch.setattr(lw.lora_scanner, "scan_lora", lambda interface="lora0": ["a", "b", "c"])
    lw.LoRaScanWidget.update(widget)
    assert "3" in widget.label.text

