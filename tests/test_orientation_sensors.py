"""Tests for :mod:`piwardrive.orientation_sensors` using dummy modules."""

from __future__ import annotations

import importlib
import sys

import piwardrive.orientation_sensors as osens  # noqa: E402


def _reload() -> None:
    """Reload the orientation_sensors module with current ``sys.modules``."""
    importlib.reload(osens)


def test_orientation_to_angle() -> None:
    assert osens.orientation_to_angle("normal") == 0.0  # nosec B101
    assert osens.orientation_to_angle("left-up") == 270.0  # nosec B101
    assert osens.orientation_to_angle("unknown") is None  # nosec B101


def test_orientation_to_angle_custom_map() -> None:
    custom_map = {"flip": 45.0}
    assert osens.orientation_to_angle("flip", custom_map) == 45.0  # nosec B101


def test_update_orientation_map() -> None:
    osens.update_orientation_map({"flip": 45.0})
    try:
        assert osens.orientation_to_angle("flip") == 45.0  # nosec B101
    finally:
        osens.reset_orientation_map()


def test_update_orientation_map_clone() -> None:
    local_map = osens.clone_orientation_map()
    osens.update_orientation_map({"flip": 45.0}, mapping=local_map)
    assert osens.orientation_to_angle("flip", local_map) == 45.0  # nosec B101
    # Global mapping should remain unchanged
    assert osens.orientation_to_angle("flip") is None  # nosec B101


def test_get_orientation_dbus_missing(monkeypatch) -> None:
    monkeypatch.delitem(sys.modules, "dbus", raising=False)
    _reload()
    try:
        assert osens.get_orientation_dbus() is None  # nosec B101
    finally:
        _reload()


def test_get_orientation_dbus_success(add_dummy_module) -> None:
    class DummyIface:
        def HasAccelerometer(self) -> bool:
            return True

        def ClaimAccelerometer(self) -> None:
            pass

        def ReleaseAccelerometer(self) -> None:
            pass

        def GetAccelerometerOrientation(self) -> str:
            return "right-up"

    class DummyBus:
        def get_object(self, _service: str, _path: str) -> object:
            return object()

    def interface(_obj: object, _name: str) -> DummyIface:
        return DummyIface()

    add_dummy_module(
        "dbus",
        SystemBus=lambda: DummyBus(),
        Interface=interface,
    )
    _reload()
    try:
        assert osens.get_orientation_dbus() == "right-up"  # nosec B101
    finally:
        _reload()


def test_get_heading(monkeypatch):
    monkeypatch.setattr(osens, "get_orientation_dbus", lambda: "right-up")
    monkeypatch.setattr(osens, "orientation_to_angle", lambda o, m=None: 90.0)
    assert osens.get_heading() == 90.0  # nosec B101


def test_get_heading_none(monkeypatch):
    monkeypatch.setattr(osens, "get_orientation_dbus", lambda: None)
    assert osens.get_heading() is None  # nosec B101


def test_read_mpu6050_missing(monkeypatch) -> None:
    monkeypatch.delitem(sys.modules, "mpu6050", raising=False)
    _reload()
    try:
        assert osens.read_mpu6050() is None  # nosec B101
    finally:
        _reload()


def test_read_mpu6050_success(add_dummy_module) -> None:
    class DummySensor:
        def __init__(self, address: int) -> None:
            self.address = address

        def get_accel_data(self) -> dict:
            return {"x": 1}

        def get_gyro_data(self) -> dict:
            return {"y": 2}

    add_dummy_module("mpu6050", mpu6050=lambda addr: DummySensor(addr))
    _reload()
    try:
        assert osens.read_mpu6050() == {  # nosec B101
            "accelerometer": {"x": 1},
            "gyroscope": {"y": 2},
        }
    finally:
        _reload()


def test_read_mpu6050_env(monkeypatch, add_dummy_module) -> None:
    class DummySensor:
        def __init__(self, address: int) -> None:
            self.address = address

        def get_accel_data(self) -> dict:
            return {"addr": self.address}

        def get_gyro_data(self) -> dict:
            return {"addr": self.address}

    add_dummy_module("mpu6050", mpu6050=lambda addr: DummySensor(addr))
    monkeypatch.setenv("PW_MPU6050_ADDR", "0x69")
    _reload()
    try:
        assert osens.read_mpu6050() == {  # nosec B101
            "accelerometer": {"addr": 0x69},
            "gyroscope": {"addr": 0x69},
        }
    finally:
        monkeypatch.delenv("PW_MPU6050_ADDR", raising=False)
        _reload()
