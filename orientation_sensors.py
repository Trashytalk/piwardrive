from __future__ import annotations

"""Entry point for orientation_sensors module."""

from piwardrive.orientation_sensors import *  # noqa: F401,F403

"""Orientation sensor helpers for gyroscope and accelerometer.

The functions in this module try to read device orientation via different
approaches.  ``get_orientation_dbus`` uses the `dbus` package to query the
``iio-sensor-proxy`` service.  If either the Python bindings or the system
service are unavailable it returns ``None``.  ``read_mpu6050`` accesses an
external MPU‑6050 sensor using the optional ``mpu6050`` package.  Again,
``None`` is returned when the module or hardware is missing.  Callers should
check for ``None`` to gracefully handle setups without these sensors.
"""


import logging
from typing import Any, Dict, Optional

try:  # pragma: no cover - optional DBus dependency
    import dbus  # type: ignore
except Exception as exc:  # pragma: no cover - missing dependency
    dbus = None  # type: ignore
    logging.getLogger(__name__).warning(
        "dbus module not available: %s. Install 'dbus-python' to enable"
        " orientation via iio-sensor-proxy.",
        exc,
    )

try:  # pragma: no cover - optional hardware dependency
    from mpu6050 import mpu6050  # type: ignore
except Exception as exc:  # pragma: no cover - missing dependency
    mpu6050 = None  # type: ignore
    logging.getLogger(__name__).warning(
        "mpu6050 module not available: %s. Install 'mpu6050' to read sensor"
        " data.",
        exc,
    )

logger = logging.getLogger(__name__)

_ORIENTATION_MAP: Dict[str, float] = {
    "normal": 0.0,
    "bottom-up": 180.0,
    "right-up": 90.0,
    "left-up": 270.0,
    # additional common orientation aliases
    "portrait": 0.0,
    "portrait-upside-down": 180.0,
    "landscape-left": 90.0,
    "landscape-right": 270.0,
    "upside-down": 180.0,
}


def orientation_to_angle(
    orientation: str, orientation_map: Optional[Dict[str, float]] = None
) -> Optional[float]:
    """Map orientation string to a rotation angle in degrees.

    The mapping can be customized by passing a dictionary via ``orientation_map``.
    """
    mapping = _ORIENTATION_MAP if orientation_map is None else orientation_map
    return mapping.get(orientation.lower())


def update_orientation_map(new_map: Dict[str, float], *, clear: bool = False) -> None:
    """Update the global orientation mapping used by :func:`orientation_to_angle`."""
    if clear:
        _ORIENTATION_MAP.clear()
    _ORIENTATION_MAP.update({k.lower(): v for k, v in new_map.items()})


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


def get_heading(orientation_map: Optional[Dict[str, float]] = None) -> Optional[float]:
    """Return device heading in degrees if orientation sensors are available."""
    orient = get_orientation_dbus()
    if orient:
        return orientation_to_angle(orient, orientation_map)
    return None
