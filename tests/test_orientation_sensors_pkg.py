import types
from importlib import reload

import piwardrive.orientation_sensors as osens


def test_orientation_to_angle_pkg() -> None:
    assert osens.orientation_to_angle("normal") == 0.0
    assert osens.orientation_to_angle("left-up") == 270.0
    assert osens.orientation_to_angle("unknown") is None


def test_orientation_to_angle_custom_map_pkg() -> None:
    custom_map = {"flip": 45.0}
    assert osens.orientation_to_angle("flip", custom_map) == 45.0


def test_update_orientation_map_pkg() -> None:
    osens.update_orientation_map({"flip": 45.0})
    try:
        assert osens.orientation_to_angle("flip") == 45.0
    finally:
        reload(osens)


def test_get_orientation_dbus_missing_pkg(monkeypatch):
    monkeypatch.setattr(osens, "dbus", None)
    assert osens.get_orientation_dbus() is None


def test_get_orientation_dbus_success_pkg(monkeypatch):
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
        SystemBus=lambda: DummyBus(), Interface=interface
    )
    monkeypatch.setattr(osens, "dbus", dummy_dbus)
    assert osens.get_orientation_dbus() == "right-up"


def test_read_mpu6050_missing_pkg(monkeypatch):
    monkeypatch.setattr(osens, "mpu6050", None)
    assert osens.read_mpu6050() is None


def test_read_mpu6050_success_pkg(monkeypatch):
    class DummySensor:
        def __init__(self, address):
            self.address = address

        def get_accel_data(self):
            return {"x": 1}

        def get_gyro_data(self):
            return {"y": 2}

    monkeypatch.setattr(osens, "mpu6050", lambda addr: DummySensor(addr))
    data = osens.read_mpu6050()
    assert data == {"accelerometer": {"x": 1}, "gyroscope": {"y": 2}}
