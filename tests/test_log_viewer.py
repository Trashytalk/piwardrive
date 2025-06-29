import os
from types import SimpleNamespace
from typing import Any

from piwardrive.widgets.log_viewer import LogViewer


def test_log_viewer_filter_regex(tmp_path: Any) -> None:
    log = tmp_path / "log.txt"
    log.write_text("INFO ok\nERROR bad\nDEBUG meh\n")
    lv = LogViewer(log_path=str(log), max_lines=10, filter_regex="ERROR")
    lv._refresh(0)
    assert lv.label.text.strip() == "ERROR bad"


def test_log_viewer_no_filter(tmp_path: Any) -> None:
    log = tmp_path / "log.txt"
    log.write_text("A\nB\n")
    lv = LogViewer(log_path=str(log), max_lines=10)
    lv._refresh(0)
    assert lv.label.text.strip() == "A\nB"


def test_log_viewer_path_menu(monkeypatch: Any) -> None:
    app = SimpleNamespace(log_paths=["/a", "/b"])
    monkeypatch.setattr("piwardrive.widgets.log_viewer.App.get_running_app", lambda: app)
    lv = LogViewer()
    lv.show_path_menu(None)
    items = lv._menu.kwargs["items"]  # type: ignore[attr-defined]
    assert items[0]["text"] == "a"
    items[1]["on_release"]()
    assert lv.log_path == "/b"
