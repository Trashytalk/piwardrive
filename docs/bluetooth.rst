Bluetooth Scanning
------------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive can display nearby Bluetooth devices on the map. The optional
scanner uses the :mod:`bleak` library to discover devices and plots markers when
GPS coordinates are available.

The poll interval is configured via ``map_poll_bt`` and markers can be hidden
with ``map_show_bt``. Both options are saved in ``config.json`` and may be
overridden with environment variables ``PW_MAP_POLL_BT`` and
``PW_MAP_SHOW_BT``. The underlying scan timeout defaults to 10 seconds but can
be adjusted by setting the ``BLUETOOTH_SCAN_TIMEOUT`` environment variable.
