import types
from typing import Any

import piwardrive.utils as utils


def test_robust_request_retries(monkeypatch):
    calls = []

    def fake_get(url: str, *, timeout: int) -> str:
        calls.append(url)
        if len(calls) < 3:
            raise Exception("boom")
        return "ok"

    def fake_retry(func: Any, *, attempts: int = 1, delay: float = 0) -> Any:
        assert attempts == 3
        result = None
        for _ in range(attempts):
            try:
                result = func()
                break
            except Exception:
                continue
        return result

    monkeypatch.setattr(utils, "retry_call", fake_retry, raising=False)
    monkeypatch.setattr(utils.requests, "get", fake_get)
    resp = utils.robust_request("http://example.com")
    assert resp == "ok"
    assert len(calls) == 3


def test_orientation_widget_update(monkeypatch):
    from piwardrive.widgets import orientation_widget as ow

    widget = object.__new__(ow.OrientationWidget)
    widget.label = ow.MDLabel()

    monkeypatch.setattr(ow.orientation_sensors, "get_orientation_dbus", lambda: "right-up")
    monkeypatch.setattr(ow.orientation_sensors, "orientation_to_angle", lambda _: 90.0)
    ow.OrientationWidget.update(widget)

    assert "right-up" in widget.label.text
    assert "90" in widget.label.text
