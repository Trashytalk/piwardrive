import importlib
import os
import sys
from typing import Any


def _load_widgets(add_dummy_module):
    add_dummy_module("kivy.metrics", dp=lambda x: x)
    add_dummy_module(
        "kivymd.uix.label",
        MDLabel=type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""}),
    )
    add_dummy_module(
        "kivymd.uix.card",
        MDCard=type(
            "MDCard",
            (),
            {"__init__": lambda self, **kw: None, "add_widget": lambda self, w: None},
        ),
    )
    add_dummy_module("kivy.uix.behaviors", DragBehavior=type("DragBehavior", (), {}))
    add_dummy_module("kivymd.uix.boxlayout", MDBoxLayout=type("MDBoxLayout", (), {}))
    ow = importlib.import_module("piwardrive.widgets.orientation_widget")
    vs = importlib.import_module("piwardrive.widgets.vehicle_speed")
    lw = importlib.import_module("piwardrive.widgets.lora_scan_widget")
    return ow, vs, lw


def test_orientation_widget(monkeypatch: Any, add_dummy_module) -> None:
    ow, _vs, _lw = _load_widgets(add_dummy_module)
    widget = object.__new__(ow.OrientationWidget)
    widget.label = ow.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(
        ow.orientation_sensors, "get_orientation_dbus", lambda: "right-up"
    )
    monkeypatch.setattr(ow.orientation_sensors, "orientation_to_angle", lambda o: 90.0)
    ow.OrientationWidget.update(widget)
    assert "right-up" in widget.label.text


def test_vehicle_speed_widget(monkeypatch: Any, add_dummy_module) -> None:
    _ow, vs, _lw = _load_widgets(add_dummy_module)
    widget = object.__new__(vs.VehicleSpeedWidget)
    widget.label = vs.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(vs.vehicle_sensors, "read_speed_obd", lambda port=None: 42.5)
    vs.VehicleSpeedWidget.update(widget)
    assert "42.5" in widget.label.text


def test_lora_scan_widget(monkeypatch: Any, add_dummy_module) -> None:
    _ow, _vs, lw = _load_widgets(add_dummy_module)
    widget = object.__new__(lw.LoRaScanWidget)
    widget.label = lw.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(
        lw.lora_scanner, "scan_lora", lambda interface="lora0": ["a", "b", "c"]
    )
    lw.LoRaScanWidget.update(widget)
    assert "3" in widget.label.text
