import importlib
import os
import sys
from typing import Any


class DummyBattery:
    def __init__(self, percent: float, plugged: bool) -> None:
        self.percent = percent
        self.power_plugged = plugged


def _load_widget():
    return importlib.import_module("piwardrive.widgets.battery_status")


def test_widget_updates(monkeypatch: Any) -> None:
    bs = _load_widget()
    widget = object.__new__(bs.BatteryStatusWidget)
    widget.label = bs.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(bs.psutil, "sensors_battery", lambda: DummyBattery(50, False))
    bs.BatteryStatusWidget.update(widget)
    assert "50" in widget.label.text
