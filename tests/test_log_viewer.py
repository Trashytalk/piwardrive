"""Tests for the log viewer widget."""

import os
import sys
import pytest

pytest.skip("GUI tests skipped in headless CI", allow_module_level=True)

os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_WINDOW", "mock")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from widgets.log_viewer import LogViewer


def test_log_viewer_filter_regex(tmp_path):
    log = tmp_path / "log.txt"
    log.write_text("INFO ok\nERROR bad\nDEBUG meh\n")
    lv = LogViewer(log_path=str(log), max_lines=10, filter_regex="ERROR")
    lv._refresh(0)
    assert lv.label.text.strip() == "ERROR bad"


def test_log_viewer_no_filter(tmp_path):
    log = tmp_path / "log.txt"
    log.write_text("A\nB\n")
    lv = LogViewer(log_path=str(log), max_lines=10)
    lv._refresh(0)
    assert lv.label.text.strip() == "A\nB"
