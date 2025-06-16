import os
import sys
import asyncio
from typing import Any
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def _load_widget(add_dummy_module):
    add_dummy_module("kivy.metrics", dp=lambda x: x)
    add_dummy_module(
        "kivymd.uix.label", MDLabel=type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""})
    )
    add_dummy_module(
        "kivymd.uix.card",
        MDCard=type("MDCard", (), {"__init__": lambda self, **kw: None, "add_widget": lambda self, w: None}),
    )
    add_dummy_module(
        "kivy.uix.behaviors", DragBehavior=type("DragBehavior", (), {})
    )
    add_dummy_module(
        "kivymd.uix.boxlayout", MDBoxLayout=type("MDBoxLayout", (), {})
    )
    return importlib.import_module("widgets.db_stats")


def test_widget_update(monkeypatch: Any, add_dummy_module) -> None:
    ds = _load_widget(add_dummy_module)
    widget = object.__new__(ds.DBStatsWidget)
    widget.label = ds.MDLabel()  # type: ignore[attr-defined]

    monkeypatch.setattr(ds, "_db_path", lambda: "x.db")
    monkeypatch.setattr(ds.os.path, "getsize", lambda p: 2048)
    monkeypatch.setattr(
        ds,
        "run_async_task",
        lambda coro, cb: (asyncio.run(coro), cb({"ap_cache": 2})),
    )
    ds.DBStatsWidget.update(widget)
    assert "2.0" in widget.label.text
