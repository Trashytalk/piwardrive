import asyncio
import importlib


def _load(add_dummy_module):
    add_dummy_module("kivy.metrics", dp=lambda x: x)
    add_dummy_module(
        "kivy.clock", Clock=type("Clock", (), {"schedule_once": staticmethod(lambda cb, dt=0: cb(dt))})
    )
    add_dummy_module(
        "kivymd.uix.label",
        MDLabel=type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""}),
    )
    add_dummy_module(
        "kivymd.uix.card",
        MDCard=type("MDCard", (), {"__init__": lambda self, **kw: None, "add_widget": lambda self, w: None}),
    )
    add_dummy_module("kivy.uix.behaviors", DragBehavior=type("DragBehavior", (), {}))
    add_dummy_module("kivymd.uix.boxlayout", MDBoxLayout=type("MDBoxLayout", (), {}))

    gs = importlib.import_module("piwardrive.widgets.gps_status")
    ss = importlib.import_module("piwardrive.widgets.service_status")
    sig = importlib.import_module("piwardrive.widgets.signal_strength")
    stg = importlib.import_module("piwardrive.widgets.storage_usage")
    hs = importlib.import_module("piwardrive.widgets.handshake_counter")
    return gs, ss, sig, stg, hs


def test_gps_status_widget(monkeypatch, add_dummy_module):
    gs, _ss, _sig, _stg, _hs = _load(add_dummy_module)
    widget = object.__new__(gs.GPSStatusWidget)
    widget.label = gs.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(gs, "get_gps_fix_quality", lambda: "3D")
    gs.GPSStatusWidget.update(widget)
    assert "3D" in widget.label.text


def test_service_status_widget(monkeypatch, add_dummy_module):
    _gs, ss, _sig, _stg, _hs = _load(add_dummy_module)
    widget = object.__new__(ss.ServiceStatusWidget)
    widget.label = ss.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(ss, "service_status", lambda name: name == "kismet")
    ss.ServiceStatusWidget.update(widget)
    assert "ok" in widget.label.text and "down" in widget.label.text


def test_handshake_counter_widget(monkeypatch, add_dummy_module):
    _gs, _ss, _sig, _stg, hs = _load(add_dummy_module)
    widget = object.__new__(hs.HandshakeCounterWidget)
    widget.label = hs.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(hs, "count_bettercap_handshakes", lambda: 7)
    hs.HandshakeCounterWidget.update(widget)
    assert "7" in widget.label.text


def test_storage_usage_widget(monkeypatch, add_dummy_module):
    _gs, _ss, _sig, stg, _hs = _load(add_dummy_module)
    widget = object.__new__(stg.StorageUsageWidget)
    widget.label = stg.MDLabel()  # type: ignore[attr-defined]
    monkeypatch.setattr(stg, "get_disk_usage", lambda p: 55.0)
    stg.StorageUsageWidget.update(widget)
    assert "55" in widget.label.text


def test_signal_strength_widget(monkeypatch, add_dummy_module):
    _gs, _ss, sig, _stg, _hs = _load(add_dummy_module)
    widget = object.__new__(sig.SignalStrengthWidget)
    widget.label = sig.MDLabel()  # type: ignore[attr-defined]

    async def fake_fetch():
        return ([{}], [])

    def fake_run(coro, cb):
        cb(asyncio.run(coro))

    monkeypatch.setattr(sig, "fetch_kismet_devices_async", fake_fetch)
    monkeypatch.setattr(sig, "run_async_task", fake_run)
    monkeypatch.setattr(sig, "get_avg_rssi", lambda aps: -42.0)
    sig.SignalStrengthWidget.update(widget)
    assert "-42.0" in widget.label.text
