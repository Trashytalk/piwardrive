import os
import sys
import types

import piwardrive.orientation_sensors as osens  # noqa: E402


def test_orientation_to_angle() -> None:
    assert osens.orientation_to_angle("normal") == 0.0
    assert osens.orientation_to_angle("left-up") == 270.0
    assert osens.orientation_to_angle("unknown") is None


def test_orientation_to_angle_custom_map() -> None:
    custom_map = {"flip": 45.0}
    assert osens.orientation_to_angle("flip", custom_map) == 45.0


def test_update_orientation_map() -> None:
    osens.update_orientation_map({"flip": 45.0})
    try:
        assert osens.orientation_to_angle("flip") == 45.0
    finally:
        osens.reset_orientation_map()


def test_update_orientation_map_clone() -> None:
    local_map = osens.clone_orientation_map()
    osens.update_orientation_map({"flip": 45.0}, mapping=local_map)
    assert osens.orientation_to_angle("flip", local_map) == 45.0
    # Global mapping should remain unchanged
    assert osens.orientation_to_angle("flip") is None


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

    dummy_dbus = types.SimpleNamespace(
        SystemBus=lambda: DummyBus(),
        Interface=interface,
    )
    monkeypatch.setattr(osens, "dbus", dummy_dbus)
    assert osens.get_orientation_dbus() == "right-up"


def test_get_heading(monkeypatch):
    monkeypatch.setattr(osens, "get_orientation_dbus", lambda: "right-up")
    monkeypatch.setattr(osens, "orientation_to_angle", lambda o, m=None: 90.0)
    assert osens.get_heading() == 90.0


def test_get_heading_none(monkeypatch):
    monkeypatch.setattr(osens, "get_orientation_dbus", lambda: None)
    assert osens.get_heading() is None
