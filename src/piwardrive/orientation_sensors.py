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
import os
from typing import Any, Dict, Optional

try:  # pragma: no cover - optional DBus dependency
    import dbus
except Exception:  # pragma: no cover - missing dependency
    dbus = None

try:  # pragma: no cover - optional hardware dependency
    from mpu6050 import mpu6050
except Exception:  # pragma: no cover - missing dependency
    mpu6050 = None

logger = logging.getLogger(__name__)

# Default mapping between orientation strings and rotation angles.  The mapping
# is copied to ``_ORIENTATION_MAP`` so callers can freely modify the latter
# without losing the canonical defaults.
DEFAULT_ORIENTATION_MAP: Dict[str, float] = {
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

# Actual mapping used by :func:`orientation_to_angle`.  It can be customised via
# :func:`update_orientation_map` and restored using
# :func:`reset_orientation_map`.
_ORIENTATION_MAP: Dict[str, float] = DEFAULT_ORIENTATION_MAP.copy()


def orientation_to_angle(
    orientation: str, orientation_map: Optional[Dict[str, float]] = None
) -> Optional[float]:
    """Map orientation string to a rotation angle in degrees.

    The mapping can be customized by passing a dictionary via ``orientation_map``.
    """
    mapping = _ORIENTATION_MAP if orientation_map is None else orientation_map
    return mapping.get(orientation.lower())


def clone_orientation_map() -> Dict[str, float]:
    """Return a copy of the current orientation mapping."""
    return _ORIENTATION_MAP.copy()


def reset_orientation_map() -> None:
    """Restore :data:`_ORIENTATION_MAP` to the default values."""
    _ORIENTATION_MAP.clear()
    _ORIENTATION_MAP.update(DEFAULT_ORIENTATION_MAP)


def update_orientation_map(
    new_map: Dict[str, float],
    *,
    clear: bool = False,
    mapping: Optional[Dict[str, float]] = None,
) -> Dict[str, float]:
    """Update an orientation mapping.

    If ``mapping`` is ``None`` the global mapping is modified.  The updated
    mapping is returned so callers can work with a customized copy.
    """
    target = _ORIENTATION_MAP if mapping is None else mapping
    if clear:
        target.clear()
    target.update({k.lower(): v for k, v in new_map.items()})
    return target


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
    r"""Return raw accelerometer and gyroscope data from ``mpu6050`` sensor.

    The I\ :sup:`2`\ C address can be overridden via ``PW_MPU6050_ADDR``.
    """
    if mpu6050 is None:
        return None

    env_addr = os.getenv("PW_MPU6050_ADDR")
    if env_addr:
        try:
            address = int(env_addr, 0)
        except ValueError:
            logger.error("Invalid PW_MPU6050_ADDR: %s", env_addr)

    try:
        sensor = mpu6050(address)
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
