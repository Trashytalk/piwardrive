Environment Variables
=====================
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive and the companion SIGINT suite can be customised using several
environment variables. Any option in :mod:`config` may be overridden by
setting ``PW_<KEY>``. Common examples are shown in the README. Additional
variables are grouped by module below.

General
-------

``PW_ADMIN_PASSWORD``
    Plain text admin password used for privileged actions.

``PW_API_PASSWORD_HASH``
    Hash required for HTTP basic auth on API routes.

``PW_DB_PATH``
    Path to the SQLite database storing health metrics.

``PW_PROFILE_NAME``
    Name of the configuration profile to load at startup.

``PW_PROFILE``
    Set to ``1`` to enable cProfile logging.

``PW_PROFILE_CALLGRIND``
    File path for callgrind data when profiling is active.

``PW_LANG``
    Two-letter code selecting a translation under ``locales/``.

``PW_GPSD_HOST``
    Hostname or IP address of the running ``gpsd`` instance.

``PW_GPSD_PORT``
    Port used to connect to ``gpsd`` (default ``2947``).

``PW_GPS_MOVEMENT_THRESHOLD``
    Minimum speed in m/s before fast GPS polling is used.

Configuration Overrides
-----------------------

The :mod:`config` module exposes many fields such as
``offline_tile_path``, ``kismet_logdir`` and ``bettercap_caplet``.
Prefix these keys with ``PW_`` to override their default paths at run time.
Call :func:`config.list_env_overrides` to see the full mapping of
environment variables to configuration keys.

.. list-table:: Common overrides
   :header-rows: 1

   * - Environment variable
     - Configuration key
   * - ``PW_THEME``
     - ``theme``
   * - ``PW_MAP_POLL_GPS``
     - ``map_poll_gps``
   * - ``PW_OFFLINE_TILE_PATH``
     - ``offline_tile_path``

SIGINT Suite
------------

``IWLIST_CMD``
    Wi-Fi scanning executable used by :mod:`sigint_suite.wifi.scanner`.

``IW_PRIV_CMD``
    Privilege helper for Wi-Fi scans (default ``sudo``).

``IMSI_CATCH_CMD``
    Command executed by :mod:`sigint_suite.cellular.imsi_catcher.scanner`.

``BAND_SCAN_CMD``
    Command used by :mod:`sigint_suite.cellular.band_scanner.scanner`.

``TOWER_SCAN_CMD``
    Executable for :mod:`sigint_suite.cellular.tower_scanner.scanner`.

``TOWER_SCAN_TIMEOUT``
    Timeout in seconds for ``TOWER_SCAN_CMD`` (default ``10``).

``EXPORT_DIR``
    Output directory for scripts under ``sigint_suite/scripts``.

``SIGINT_EXPORT_DIR``
    Directory searched by :func:`sigint_integration.load_sigint_data`.

``SIGINT_DEBUG``
    Set to ``1`` to enable debug logging for SIGINT scanners.


