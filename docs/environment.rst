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
``PW_DB_POOL_SIZE``
    Maximum number of connections in the SQLite pool (default ``10``).
``PW_DB_BUFFER_LIMIT``
    Number of health records buffered before a flush (default ``50``).
``PW_DB_FLUSH_INTERVAL``
    Seconds between automatic buffer flushes (default ``30``).
``PW_DB_SHARDS``
    Number of database shards for horizontal scaling.

``PW_HEALTH_FILE``
    JSON file returned by ``/api/status`` when present.

``PW_WEBUI_DIST``
    Path to the compiled web UI served by :mod:`piwardrive.web.webui_server`.

``PW_WEBUI_PORT``
    Override port for :mod:`piwardrive.web.webui_server` (default ``8000``).

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

``PW_MPU6050_ADDR``
    I\ :sup:`2`\ C address for :func:`orientation_sensors.read_mpu6050` (default ``0x68``).

``PW_ORIENTATION_MAP_FILE``
    Path to a JSON orientation map loaded at startup.

``PW_REMOTE_SYNC_URL``
    Upload endpoint for automatic database sync.

``PW_REMOTE_SYNC_TOKEN``
    Bearer token sent to ``PW_REMOTE_SYNC_URL`` if required.

``PW_REMOTE_SYNC_TIMEOUT``
    Timeout in seconds when uploading the database (default ``5``).

``PW_REMOTE_SYNC_RETRIES``
    Number of attempts made when uploads fail (default ``3``).

``PW_REMOTE_SYNC_INTERVAL``
    How often to upload the database in minutes. ``0`` disables scheduling.

``PW_UPDATE_INTERVAL``
    How often PiWardrive checks for updates in hours.

``PW_AGG_DIR``
    Directory used by ``aggregation_service`` to store data.

``PW_AGG_PORT``
    Listening port for ``aggregation_service`` (default ``9100``).

``PW_SERVICE_PORT``
    Port for the HTTP API when running ``service.py`` (default ``8000``).

``PW_API_USER``
    Username created with ``PW_API_PASSWORD_HASH`` (default ``admin``).

``PW_CORS_ORIGINS``
    Comma-separated origins allowed by CORS.

``PW_CONTENT_SECURITY_POLICY``
    Value for the ``Content-Security-Policy`` response header.

``PIWARDRIVE_RATE_LIMIT_REQUESTS``
    Requests allowed per ``PIWARDRIVE_RATE_LIMIT_WINDOW`` seconds.

``PIWARDRIVE_RATE_LIMIT_WINDOW``
    Time window in seconds for rate limiting.

``PW_DB_KEY``
    Passphrase for optional SQLCipher database encryption.

Remote Sync Variables
---------------------

The variables above control automatic uploads of the health database.  Their
defaults are summarised below.  See :doc:`remote_sync` for a full setup guide.

.. list-table:: ``PW_REMOTE_SYNC_*`` variables
   :header-rows: 1

   * - Variable
     - Purpose
     - Default
   * - ``PW_REMOTE_SYNC_URL``
     - Upload endpoint for automatic database sync
     - ``""``
   * - ``PW_REMOTE_SYNC_TOKEN``
     - Bearer token sent with uploads when defined
     - ``""``
   * - ``PW_REMOTE_SYNC_TIMEOUT``
     - Timeout in seconds for ``sync_database_to_server``
     - ``5``
   * - ``PW_REMOTE_SYNC_RETRIES``
     - Number of attempts made when uploads fail
     - ``3``
   * - ``PW_REMOTE_SYNC_INTERVAL``
     - How often to upload the database in minutes
     - ``60``

Remote Sync Overrides
---------------------

The variables above override keys in ``config.json`` when prefixed with
``PW_``. Set them in the environment to change the values returned by
:mod:`config.AppConfig.load` at runtime.

.. list-table:: ``PW_REMOTE_SYNC_*`` overrides
   :header-rows: 1

   * - Environment variable
     - Configuration key
   * - ``PW_REMOTE_SYNC_URL``
     - ``remote_sync_url``
   * - ``PW_REMOTE_SYNC_TOKEN``
     - ``remote_sync_token``
   * - ``PW_REMOTE_SYNC_TIMEOUT``
     - ``remote_sync_timeout``
   * - ``PW_REMOTE_SYNC_RETRIES``
     - ``remote_sync_retries``
   * - ``PW_REMOTE_SYNC_INTERVAL``
     - ``remote_sync_interval``

Configuration Overrides
-----------------------

The :mod:`config` module exposes many fields such as
``offline_tile_path``, ``kismet_logdir`` and ``bettercap_caplet``.
Prefix these keys with ``PW_`` to override their default paths at run time.
All available overrides are summarised below.

.. list-table:: All ``PW_`` overrides
   :header-rows: 1

   * - Environment variable
     - Configuration key
   * - ``PW_ADMIN_PASSWORD_HASH``
     - ``admin_password_hash``
   * - ``PW_BETTERCAP_CAPLET``
     - ``bettercap_caplet``
   * - ``PW_BASELINE_HISTORY_DAYS``
     - ``baseline_history_days``
   * - ``PW_BASELINE_THRESHOLD``
     - ``baseline_threshold``
   * - ``PW_CLEANUP_ROTATED_LOGS``
     - ``cleanup_rotated_logs``
   * - ``PW_CLOUD_BUCKET``
     - ``cloud_bucket``
   * - ``PW_CLOUD_PREFIX``
     - ``cloud_prefix``
   * - ``PW_CLOUD_PROFILE``
     - ``cloud_profile``
   * - ``PW_COMPRESS_HEALTH_EXPORTS``
     - ``compress_health_exports``
   * - ``PW_COMPRESS_OFFLINE_TILES``
     - ``compress_offline_tiles``
   * - ``PW_DASHBOARD_LAYOUT``
     - ``dashboard_layout``
   * - ``PW_DEBUG_MODE``
     - ``debug_mode``
   * - ``PW_DISABLE_SCANNING``
     - ``disable_scanning``
   * - ``PW_GPS_MOVEMENT_THRESHOLD``
     - ``gps_movement_threshold``
   * - ``PW_HANDSHAKE_CACHE_SECONDS``
     - ``handshake_cache_seconds``
   * - ``PW_HEALTH_EXPORT_DIR``
     - ``health_export_dir``
   * - ``PW_HEALTH_EXPORT_INTERVAL``
     - ``health_export_interval``
   * - ``PW_HEALTH_EXPORT_RETENTION``
     - ``health_export_retention``
   * - ``PW_HEALTH_POLL_INTERVAL``
     - ``health_poll_interval``
   * - ``PW_KISMET_LOGDIR``
     - ``kismet_logdir``
   * - ``PW_LOG_PATHS``
     - ``log_paths``
   * - ``PW_LOG_ROTATE_ARCHIVES``
     - ``log_rotate_archives``
   * - ``PW_LOG_ROTATE_INTERVAL``
     - ``log_rotate_interval``
   * - ``PW_LOG_TAIL_CACHE_SECONDS``
     - ``log_tail_cache_seconds``
   * - ``PW_MAP_AUTO_PREFETCH``
     - ``map_auto_prefetch``
   * - ``PW_MAP_CLUSTER_APS``
     - ``map_cluster_aps``
   * - ``PW_MAP_CLUSTER_CAPACITY``
     - ``map_cluster_capacity``
   * - ``PW_MAP_FOLLOW_GPS``
     - ``map_follow_gps``
   * - ``PW_MAP_POLL_APS``
     - ``map_poll_aps``
   * - ``PW_MAP_POLL_BT``
     - ``map_poll_bt``
   * - ``PW_MAP_POLL_GPS``
     - ``map_poll_gps``
   * - ``PW_MAP_POLL_GPS_MAX``
     - ``map_poll_gps_max``
   * - ``PW_MAP_POLL_WIGLE``
     - ``map_poll_wigle``
   * - ``PW_MAP_SHOW_APS``
     - ``map_show_aps``
   * - ``PW_MAP_SHOW_BT``
     - ``map_show_bt``
   * - ``PW_MAP_SHOW_GPS``
     - ``map_show_gps``
   * - ``PW_MAP_SHOW_HEATMAP``
     - ``map_show_heatmap``
   * - ``PW_MAP_SHOW_WIGLE``
     - ``map_show_wigle``
   * - ``PW_MAP_USE_OFFLINE``
     - ``map_use_offline``
   * - ``PW_OFFLINE_TILE_PATH``
     - ``offline_tile_path``
   * - ``PW_REMOTE_SYNC_INTERVAL``
     - ``remote_sync_interval``
   * - ``PW_REMOTE_SYNC_RETRIES``
     - ``remote_sync_retries``
   * - ``PW_REMOTE_SYNC_TIMEOUT``
     - ``remote_sync_timeout``
   * - ``PW_REMOTE_SYNC_TOKEN``
     - ``remote_sync_token``
   * - ``PW_REMOTE_SYNC_URL``
     - ``remote_sync_url``
   * - ``PW_REPORTS_DIR``
     - ``reports_dir``
   * - ``PW_RESTART_SERVICES``
     - ``restart_services``
   * - ``PW_ROUTE_PREFETCH_INTERVAL``
     - ``route_prefetch_interval``
   * - ``PW_ROUTE_PREFETCH_LOOKAHEAD``
     - ``route_prefetch_lookahead``
   * - ``PW_THEME``
     - ``theme``
   * - ``PW_TILE_CACHE_LIMIT_MB``
     - ``tile_cache_limit_mb``
   * - ``PW_TILE_MAINTENANCE_INTERVAL``
     - ``tile_maintenance_interval``
   * - ``PW_TILE_MAX_AGE_DAYS``
     - ``tile_max_age_days``
   * - ``PW_UI_FONT_SIZE``
     - ``ui_font_size``
   * - ``PW_WIDGET_BATTERY_STATUS``
     - ``widget_battery_status``
   * - ``PW_WIGLE_API_KEY``
     - ``wigle_api_key``
   * - ``PW_WIGLE_API_NAME``
     - ``wigle_api_name``
   * - ``PW_INFLUX_URL``
     - ``influx_url``
   * - ``PW_INFLUX_TOKEN``
     - ``influx_token``
   * - ``PW_INFLUX_ORG``
     - ``influx_org``
   * - ``PW_INFLUX_BUCKET``
     - ``influx_bucket``
   * - ``PW_POSTGRES_DSN``
     - ``postgres_dsn``

Using a ``.env`` File
---------------------

Environment variables can be collected in ``~/.config/piwardrive/.env`` so they
do not need to be specified on the command line. Each line contains a
``KEY=value`` pair. Blank lines and ``#`` comments are ignored. Source the file
before launching PiWardrive or reference it via ``EnvironmentFile`` in a systemd
service.

Example ``.env``::

   PW_ADMIN_PASSWORD_HASH=$pbkdf2-sha256$...
   PW_DB_PATH=/mnt/ssd/piwardrive/app.db
   PW_OFFLINE_TILE_PATH=/mnt/ssd/tiles/offline.mbtiles
   PW_REMOTE_SYNC_URL=http://10.0.0.2:9000/
   PW_REMOTE_SYNC_TOKEN=secret
   PW_LOG_ROTATE_INTERVAL=86400
   PW_LOG_ROTATE_ARCHIVES=7

Typical Production Overrides
----------------------------

.. list-table:: Typical ``.env`` overrides
   :header-rows: 1

   * - Variable
     - Purpose
     - Example
   * - ``PW_DB_PATH``
     - Location of the SQLite database
     - ``/mnt/ssd/piwardrive/app.db``
   * - ``PW_OFFLINE_TILE_PATH``
     - Path to offline map tiles
     - ``/mnt/ssd/tiles/offline.mbtiles``
   * - ``PW_REMOTE_SYNC_URL``
     - Server receiving health uploads
     - ``http://10.0.0.2:9000/``
   * - ``PW_REMOTE_SYNC_TOKEN``
     - Bearer token for ``PW_REMOTE_SYNC_URL``
     - ``changeme``
   * - ``PW_LOG_ROTATE_INTERVAL``
     - Seconds between log rotations
     - ``86400``
   * - ``PW_LOG_ROTATE_ARCHIVES``
     - Number of rotated logs to keep
     - ``7``

SIGINT Suite
------------

``IWLIST_CMD``
    Wi-Fi scanning executable used by :mod:`piwardrive.sigint_suite.wifi.scanner`.

``IW_PRIV_CMD``
    Privilege helper for Wi-Fi scans (default ``sudo``).

``IMSI_CATCH_CMD``
    Command executed by :mod:`piwardrive.sigint_suite.cellular.imsi_catcher.scanner`.

``BAND_SCAN_CMD``
    Command used by :mod:`piwardrive.sigint_suite.cellular.band_scanner.scanner`.

``TOWER_SCAN_CMD``
    Executable for :mod:`piwardrive.sigint_suite.cellular.tower_scanner.scanner`.

``TOWER_SCAN_TIMEOUT``
    Timeout in seconds for ``TOWER_SCAN_CMD`` (default ``10``).

``EXPORT_DIR``
    Output directory for scripts under ``piwardrive/integrations/sigint_suite/scripts``.

``SIGINT_EXPORT_DIR``
    Directory searched by :func:`sigint_integration.load_sigint_data`.

``SIGINT_DEBUG``
    Set to ``1`` to enable debug logging for SIGINT scanners.

SIGINT Plugins
~~~~~~~~~~~~~~

Custom SIGINT scanners can be added as plugins. Place Python modules in
``~/.config/piwardrive/sigint_plugins`` and they will be imported automatically
whenever :mod:`piwardrive.sigint_suite` is loaded. Each plugin should provide a
``scan()`` function returning records such as ``WifiNetwork`` or
``BluetoothDevice``. After installing new plugins, call
``piwardrive.sigint_suite.plugins.clear_plugin_cache()`` so the next import
reloads the directory.


