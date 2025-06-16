import os
import sys
from types import ModuleType
import asyncio
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

import widgets.db_stats as ds


def test_widget_update(monkeypatch: Any) -> None:
    widget = object.__new__(ds.DBStatsWidget)
    widget.label = modules["kivymd.uix.label"].MDLabel()

    monkeypatch.setattr(ds, "_db_path", lambda: "x.db")
    monkeypatch.setattr(ds.os.path, "getsize", lambda p: 2048)
    monkeypatch.setattr(ds, "run_async_task", lambda coro, cb: (asyncio.run(coro), cb({"ap_cache": 2})))
    ds.DBStatsWidget.update(widget)
    assert "2.0" in widget.label.text
