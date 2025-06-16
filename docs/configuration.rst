Configuration
-------------

Configuration is stored in ``~/.config/piwardrive/config.json``. Most values can
be overridden using environment variables prefixed with ``PW_``. For example::

   PW_MAP_POLL_GPS=5 python main.py

To enable the optional battery widget set ``widget_battery_status`` to ``true``::

   PW_WIDGET_BATTERY_STATUS=1 python main.py

Disable all network scanning when operating offline with::

   PW_DISABLE_SCANNING=1 python main.py

Set ``PW_ADMIN_PASSWORD`` to allow privileged service actions without being
prompted for a password::

  PW_ADMIN_PASSWORD=secret python main.py

Log paths shown in the console screen can be customised via the ``log_paths``
list.  Provide a JSON array in ``config.json`` or set ``PW_LOG_PATHS`` to a
JSON encoded list to override the defaults.

See :mod:`config` for defaults and helpers.

Environment variables are parsed on startup. Any option in ``Config`` can be
specified as ``PW_<OPTION>``. Boolean variables accept ``1`` or ``0`` while
strings and integers are used verbatim. Invalid values trigger an early
``ValueError`` so configuration mistakes are detected before the GUI launches.

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

An example profile named ``default_profile.json`` is included under ``examples/`` with recommended settings. Copy this file to ``~/.config/piwardrive/profiles`` to bootstrap your own configuration.

All values are validated on load. Invalid entries or environment overrides
raise ``ValueError`` with details about the offending fields.

You can modify these options from the application's **Settings** screen.
Each field is exposed via a text input or toggle and saved back to
``config.json`` for the next launch.
