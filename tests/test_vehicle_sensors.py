import os
import sys
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import piwardrive.vehicle_sensors as vs  # noqa: E402


def test_read_rpm_obd_missing(monkeypatch):
    monkeypatch.setattr(vs, "obd", None)
    assert vs.read_rpm_obd() is None


def test_read_engine_load_obd_success(monkeypatch):
    class DummyVal:
        def __init__(self, val):
            self.val = val

        def to(self, _unit):
            return self.val

    class DummyConn:
        def query(self, _cmd):
            return types.SimpleNamespace(value=DummyVal(50.0))

    dummy_obd = types.SimpleNamespace(
        OBD=lambda port=None: DummyConn(),
        commands=types.SimpleNamespace(ENGINE_LOAD="ENGINE_LOAD", RPM="RPM"),
    )
    monkeypatch.setattr(vs, "obd", dummy_obd)
    assert vs.read_engine_load_obd() == 50.0
    assert vs.read_rpm_obd() == 50.0
