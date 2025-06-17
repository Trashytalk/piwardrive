Configuration
-------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


Configuration is stored in ``~/.config/piwardrive/config.json``. Most values can
be overridden using environment variables prefixed with ``PW_``. Changes to the
file are detected at runtime and applied automatically. For example::

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

Several sample profiles live in ``examples/``. ``default_profile.json`` mirrors the built-in defaults. ``desktop_kismet.json`` and ``desktop_no_kismet.json`` demonstrate common desktop setups with and without Kismet logging. ``mobile_kismet.json`` and ``mobile_no_kismet.json`` tweak the polling intervals and tile cache for phones or tablets. Copy any of these files to ``~/.config/piwardrive/profiles`` and select them via ``PW_PROFILE_NAME`` or ``active_profile``.

All values are validated on load. Invalid entries or environment overrides
raise ``ValueError`` with details about the offending fields.

You can modify these options from the application's **Settings** screen.
Each field is exposed via a text input or toggle and saved back to
``config.json`` for the next launch.
