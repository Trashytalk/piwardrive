import types
from importlib import reload

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import orientation_sensors as osens


def test_orientation_to_angle() -> None:
    assert osens.orientation_to_angle("normal") == 0.0
    assert osens.orientation_to_angle("left-up") == 270.0
    assert osens.orientation_to_angle("unknown") is None


def test_get_orientation_dbus_missing(monkeypatch):
    monkeypatch.setattr(osens, "dbus", None)
    assert osens.get_orientation_dbus() is None


def test_get_orientation_dbus_success(monkeypatch):
    class DummyIface:
        def HasAccelerometer(self):
            return True

        def ClaimAccelerometer(self):
            pass

        def ReleaseAccelerometer(self):
            pass

        def GetAccelerometerOrientation(self):
            return "right-up"

    class DummyBus:
        def get_object(self, _service, _path):
            return object()

    def interface(_obj, _name):
        return DummyIface()

    dummy_dbus = types.SimpleNamespace(SystemBus=lambda: DummyBus(), Interface=interface)
    monkeypatch.setattr(osens, "dbus", dummy_dbus)
    assert osens.get_orientation_dbus() == "right-up"
