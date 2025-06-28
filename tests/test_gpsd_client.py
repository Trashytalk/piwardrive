import importlib
import sys
import types

from piwardrive import gpsd_client


def _reload_with_dummy(monkeypatch, connect_ok=True, packet=None, raise_on_get=False):
    dummy = types.SimpleNamespace()

    def connect(host="127.0.0.1", port=2947):
        if not connect_ok:
            raise OSError("fail")

    def get_current():
        if raise_on_get:
            raise RuntimeError("boom")
        return packet

    dummy.connect = connect
    dummy.get_current = get_current
    monkeypatch.setitem(sys.modules, "gpsd", dummy)
    return importlib.reload(gpsd_client)


def test_get_position_none_on_failure(monkeypatch):
    mod = _reload_with_dummy(monkeypatch, connect_ok=False)
    assert mod.client.get_position() is None


def test_reconnect_after_error(monkeypatch):
    pkt = types.SimpleNamespace(mode=3, lat=1.0, lon=2.0, error={"x": 1.0, "y": 1.0})
    calls = [True, False]

    def get_current():
        if calls.pop(0):
            raise RuntimeError("fail")
        return pkt

    dummy = types.SimpleNamespace(
        connect=lambda host="127.0.0.1", port=2947: None, get_current=get_current
    )
    monkeypatch.setitem(sys.modules, "gpsd", dummy)
    mod = importlib.reload(gpsd_client)
    assert mod.client.get_position() is None
    assert mod.client.get_position() == (1.0, 2.0)


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("PW_GPSD_HOST", "1.2.3.4")
    monkeypatch.setenv("PW_GPSD_PORT", "1234")
    mod = _reload_with_dummy(monkeypatch)
    assert mod.client.host == "1.2.3.4"
    assert mod.client.port == 1234
