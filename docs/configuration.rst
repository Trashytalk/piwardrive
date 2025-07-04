Configuration
-------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


Configuration is stored in ``~/.config/piwardrive/config.json``. Most values can
be overridden using environment variables prefixed with ``PW_``. A filesystem
watcher monitors the file so changes are detected and applied automatically.
For example::

   PW_MAP_POLL_GPS=5 python -m piwardrive.main

To enable the optional battery widget set ``widget_battery_status`` to ``true``::

   PW_WIDGET_BATTERY_STATUS=1 python -m piwardrive.main

Disable all network scanning when operating offline with::

   PW_DISABLE_SCANNING=1 python -m piwardrive.main

Set ``PW_ADMIN_PASSWORD`` to allow privileged service actions without being
prompted for a password::

  PW_ADMIN_PASSWORD=secret python -m piwardrive.main

Log paths shown in the console screen can be customised via the ``log_paths``
list.  Provide a JSON array in ``config.json`` or set ``PW_LOG_PATHS`` to a
JSON encoded list to override the defaults.

See :mod:`config` for defaults and helpers. A machine-readable schema of all
fields lives in :download:`config_schema.json <config_schema.json>`.

Environment variables are parsed on startup. Any option in ``Config`` can be
specified as ``PW_<OPTION>``. Boolean variables accept ``1`` or ``0`` while
strings and integers are used verbatim. Invalid values trigger an early
``ValueError`` so configuration mistakes are detected before the React dashboard launches.

Configuration Profiles
----------------------

Multiple profiles can be stored under ``~/.config/piwardrive/profiles``.  The
file ``~/.config/piwardrive/active_profile`` stores the active profile name.
``load_config()`` loads this profile automatically unless the
``PW_PROFILE_NAME`` environment variable overrides it.

Use :func:`config.save_config` with ``profile="myprofile"`` to create or update
a profile. Switch via :func:`config.switch_profile` or by editing
``active_profile``. Profiles can be exported and imported using
:func:`config.export_profile` and :func:`config.import_profile`.

Several sample profiles live in ``examples/``. ``default_profile.json`` mirrors the built-in defaults. ``desktop_kismet.json`` and ``desktop_no_kismet.json`` demonstrate common desktop setups with and without Kismet logging. ``mobile_kismet.json`` and ``mobile_no_kismet.json`` tweak the polling intervals and tile cache for phones or tablets. Copy any of these files to ``~/.config/piwardrive/profiles`` and select them via ``PW_PROFILE_NAME`` or ``active_profile``.

All values are validated on load. Invalid entries or environment overrides
raise ``ValueError`` with details about the offending fields.

You can modify these options from the application's **Settings** screen.
Each field is exposed via a text input or toggle and saved back to
``config.json`` for the next launch.

Remote Sync
-----------

Automatic uploads to a remote server are controlled by several options:

``remote_sync_url``
    HTTP endpoint receiving the uploaded SQLite database.

``remote_sync_token``
    Bearer token added to the request when provided.

``remote_sync_timeout``
    Timeout in seconds before the upload is aborted.

``remote_sync_retries``
    Number of attempts made when a transfer fails.

``remote_sync_interval``
    How often to sync the database in minutes. Set to ``0`` to disable
    the scheduler.

Tile Prefetch and Maintenance
-----------------------------

``tile_maintenance_interval``
    How often the cache cleanup routine runs in seconds.

``route_prefetch_interval``
    Interval in seconds between automatic route tile prefetch attempts.

``route_prefetch_lookahead``
    Number of extrapolated GPS points used when predicting future tiles.

These options appear in the Settings form and can also be set via
``PW_TILE_MAINTENANCE_INTERVAL`` and ``PW_ROUTE_PREFETCH_INTERVAL``
environment variables.

Cache Tuning
------------

``handshake_cache_seconds``
    How long to cache BetterCAP handshake counts before re-scanning.

``log_tail_cache_seconds``
    Duration to cache tailed log lines before checking for updates.

Data Sink Integrations
----------------------

``influx_url``
    Base URL for an InfluxDB server.

``influx_token``
    Access token used for writes.

``influx_org``
    Organisation name associated with ``influx_token``.

``influx_bucket``
    Bucket receiving uploaded points.

``postgres_dsn``
    Connection string for a Postgres database.
