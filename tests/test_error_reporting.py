"""Tests for :mod:`piwardrive.error_reporting`."""

import logging
from types import SimpleNamespace
from typing import Any

import piwardrive.error_reporting as er


def test_format_error_simple() -> None:
    """``format_error`` should zero-pad codes and prefix with ``E``."""

    assert er.format_error(404, "Not found") == "[E404] Not found"


def test_report_error_logs_and_alert(monkeypatch: Any) -> None:
    """``report_error`` should log the message and show an alert."""

    logged: list[str] = []
    monkeypatch.setattr(er.logging, "error", lambda msg: logged.append(msg))

    app = SimpleNamespace(alerts=[])  # type: ignore[var-annotated]

    def show_alert(title: str, message: str) -> None:
        app.alerts.append((title, message))

    app.show_alert = show_alert  # type: ignore[attr-defined]
    monkeypatch.setattr(er.App, "get_running_app", staticmethod(lambda: app))

    er.report_error("boom")

    assert logged == ["boom"]
    assert app.alerts == [("Error", "boom")]
