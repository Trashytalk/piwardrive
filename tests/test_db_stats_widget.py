import asyncio
import importlib
from typing import Any


def _load_widget():
    return importlib.import_module("piwardrive.widgets.db_stats")


def test_widget_update(monkeypatch: Any) -> None:
    ds = _load_widget()
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
