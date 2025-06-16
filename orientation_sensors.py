"""Orientation sensor helpers for gyroscope and accelerometer.

The functions in this module try to read device orientation via different
approaches.  ``get_orientation_dbus`` uses the `dbus` package to query the
``iio-sensor-proxy`` service.  If either the Python bindings or the system
service are unavailable it returns ``None``.  ``read_mpu6050`` accesses an
external MPU‑6050 sensor using the optional ``mpu6050`` package.  Again,
``None`` is returned when the module or hardware is missing.  Callers should
check for ``None`` to gracefully handle setups without these sensors.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

try:  # pragma: no cover - optional DBus dependency
    import dbus  # type: ignore
except Exception:  # pragma: no cover - missing dependency
    dbus = None  # type: ignore

try:  # pragma: no cover - optional hardware dependency
    from mpu6050 import mpu6050  # type: ignore
except Exception:  # pragma: no cover - missing dependency
    mpu6050 = None  # type: ignore

logger = logging.getLogger(__name__)

_ORIENTATION_MAP: Dict[str, float] = {
    "normal": 0.0,
    "bottom-up": 180.0,
    "right-up": 90.0,
    "left-up": 270.0,
}


def orientation_to_angle(orientation: str) -> Optional[float]:
    """Map orientation string to a rotation angle in degrees."""
    return _ORIENTATION_MAP.get(orientation.lower())


def get_orientation_dbus() -> Optional[str]:
    """Return device orientation via ``iio-sensor-proxy`` if available."""
    if dbus is None:
        return None
    try:
        bus = dbus.SystemBus()
        proxy = bus.get_object("net.hadess.SensorProxy", "/net/hadess/SensorProxy")
        iface = dbus.Interface(proxy, "net.hadess.SensorProxy")
        if not iface.HasAccelerometer():
            return None
        iface.ClaimAccelerometer()
        try:
            orientation = str(iface.GetAccelerometerOrientation())
        finally:
            iface.ReleaseAccelerometer()
        return orientation
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("DBus orientation read failed: %s", exc)
        return None


def read_mpu6050(address: int = 0x68) -> Optional[Dict[str, Any]]:
    """Return raw accelerometer and gyroscope data from ``mpu6050`` sensor."""
    if mpu6050 is None:
        return None
    try:
        sensor = mpu6050(address)  # type: ignore
        return {
            "accelerometer": sensor.get_accel_data(),
            "gyroscope": sensor.get_gyro_data(),
        }
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("MPU6050 read failed: %s", exc)
        return None
