import importlib
import sys
import types

import gps_handler


def _reload_with_dummy(monkeypatch, gps_cls):
    dummy_mod = types.SimpleNamespace(gps=gps_cls, WATCH_ENABLE=1, WATCH_NEWSTYLE=2)
    monkeypatch.setitem(sys.modules, "gps", dummy_mod)
    return importlib.reload(gps_handler)


class _DummyBase:
    def __init__(self, *args, **kwargs):
        pass

    def stream(self, flags):
        pass

    def close(self):
        pass


def test_position_none_on_connect_failure(monkeypatch):
    class Dummy(_DummyBase):
        def __init__(self, *args, **kwargs):
            raise OSError("fail")

    mod = _reload_with_dummy(monkeypatch, Dummy)
    assert mod.handler.get_position() is None


def test_timeout_returns_none(monkeypatch):
    class Dummy(_DummyBase):
        def waiting(self, timeout=0):
            return False

        def next(self):  # pragma: no cover - not called
            return {}

    mod = _reload_with_dummy(monkeypatch, Dummy)
    assert mod.handler.get_position(timeout=0.1) is None


def test_reconnect_after_error(monkeypatch):
    packet = types.SimpleNamespace(
        class_="TPV", lat=1.0, lon=2.0, epx=1.0, epy=1.0, mode=3
    )
    calls = [True, False]

    class Dummy(_DummyBase):
        def waiting(self, timeout=0):
            return True

        def next(self):
            if calls.pop(0):
                raise RuntimeError("boom")
            return packet

    mod = _reload_with_dummy(monkeypatch, Dummy)
    assert mod.handler.get_position() is None
    assert mod.handler.get_position() == (1.0, 2.0)
