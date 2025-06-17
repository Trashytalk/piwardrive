Orientation Sensors
-------------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

The :mod:`orientation_sensors` helpers try multiple methods to determine the
current device orientation. ``get_orientation_dbus`` queries the
``iio-sensor-proxy`` service via the optional ``dbus`` package. If the service or
Python bindings are missing, ``None`` is returned. ``read_mpu6050`` reads raw
accelerometer and gyroscope values from an external MPU-6050 attached over
I\ :sup:`2`\ C using the optional ``mpu6050`` package. Callers should check the
return value and gracefully handle ``None`` when neither dependency is present.

``get_heading`` combines these helpers to return an orientation angle in degrees
when available. Wi-Fi scans use this value to attach the current antenna
direction to RSSI measurements.
