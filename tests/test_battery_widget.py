import importlib
import os
import sys
from typing import Any


class DummyBattery:
    def __init__(self, percent: float, plugged: bool) -> None:
        self.percent = percent
        self.power_plugged = plugged


def _load_widget(add_dummy_module):
    add_dummy_module(
        "kivy.app",
        App=type("App", (), {"get_running_app": staticmethod(lambda: None)}),
    )
    add_dummy_module("kivy.metrics", dp=lambda x: x, sp=lambda x: x)
    add_dummy_module(
        "kivy.uix.behaviors",
        DragBehavior=type("DragBehavior", (), {}),
    )
    add_dummy_module(
        "kivymd.uix.label",
        MDLabel=type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""}),
    )
    add_dummy_module(
        "kivymd.uix.boxlayout",
        MDBoxLayout=type("MDBoxLayout", (), {}),
    )
    add_dummy_module(
        "kivymd.uix.card",
        MDCard=type("MDCard", (), {}),
    )
    return importlib.import_module("piwardrive.widgets.battery_status")


def test_widget_updates(add_dummy_module, monkeypatch: Any) -> None:
    bs = _load_widget(add_dummy_module)
    widget = object.__new__(bs.BatteryStatusWidget)
    widget.label = bs.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(bs.psutil, "sensors_battery", lambda: DummyBattery(50, False))
    bs.BatteryStatusWidget.update(widget)
    assert "50" in widget.label.text
