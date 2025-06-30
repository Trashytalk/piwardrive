import types
from typing import Any

import piwardrive.utils as utils


def test_robust_request_retries(monkeypatch):
    calls = []

    def fake_request(method: str, url: str, **kwargs: Any) -> str:
        calls.append((method, url, kwargs.get("headers"), kwargs.get("timeout")))
        if len(calls) < 3:
            raise utils.requests.RequestException("boom")
        return "ok"

    sleeps: list[float] = []

    def fake_sleep(d: float) -> None:
        sleeps.append(d)

    monkeypatch.setattr(utils.requests, "request", fake_request)
    monkeypatch.setattr(utils.time, "sleep", fake_sleep)
    resp = utils.robust_request(
        "http://example.com",
        method="POST",
        headers={"X-Test": "y"},
        timeout=10,
    )
    assert resp == "ok"
    assert calls == [
        ("POST", "http://example.com", {"X-Test": "y"}, 10),
        ("POST", "http://example.com", {"X-Test": "y"}, 10),
        ("POST", "http://example.com", {"X-Test": "y"}, 10),
    ]
    assert sleeps == [1, 2]


def test_orientation_widget_update(monkeypatch):
    from piwardrive.widgets import orientation_widget as ow

    widget = object.__new__(ow.OrientationWidget)
    widget.label = ow.MDLabel()

    monkeypatch.setattr(
        ow.orientation_sensors, "get_orientation_dbus", lambda: "right-up"
    )
    monkeypatch.setattr(ow.orientation_sensors, "orientation_to_angle", lambda _: 90.0)
    ow.OrientationWidget.update(widget)

    assert "right-up" in widget.label.text
    assert "90" in widget.label.text
