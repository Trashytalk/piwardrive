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

Setup
~~~~~
To read orientation via DBus install ``iio-sensor-proxy`` and the Python
bindings::

   sudo apt install iio-sensor-proxy python3-dbus

``iio-sensor-proxy`` must be running. On most systems the service starts
automatically after installation.

For an external MPU-6050 sensor connect the module to the I\ :sup:`2`\ C bus
and install the helper library::

   sudo apt install python3-smbus
   pip install mpu6050

Orientation Map
~~~~~~~~~~~~~~~
Orientation strings returned by the helpers are mapped to rotation angles using
``orientation_sensors._ORIENTATION_MAP``. The default values are::

   normal: 0.0
   bottom-up: 180.0
   right-up: 90.0
   left-up: 270.0
   portrait: 0.0
   portrait-upside-down: 180.0
   landscape-left: 90.0
   landscape-right: 270.0
   upside-down: 180.0

Use :func:`orientation_sensors.update_orientation_map` to add or override
entries. :func:`orientation_sensors.orientation_to_angle` converts an orientation
string into a numeric angle using this mapping.

``calibrate-orientation`` guides you through positioning the device at
0°, 90°, 180° and 270°.  The resulting mapping is written to
``orientation_map.json`` and can be applied with
:func:`orientation_sensors.update_orientation_map`.

Refer to :func:`orientation_sensors.get_orientation_dbus` and
:func:`orientation_sensors.read_mpu6050` for reading the sensor values.
