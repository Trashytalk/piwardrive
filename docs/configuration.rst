Configuration
-------------

Configuration is stored in ``~/.config/piwardrive/config.json``. Most values can
be overridden using environment variables prefixed with ``PW_``. For example::

   PW_MAP_POLL_GPS=5 python main.py

To enable the optional battery widget set ``widget_battery_status`` to ``true``::

   PW_WIDGET_BATTERY_STATUS=1 python main.py

See :mod:`config` for defaults and helpers.

All values are validated on load. Invalid entries or environment overrides
raise ``ValueError`` with details about the offending fields.

You can modify these options from the application's **Settings** screen.
Each field is exposed via a text input or toggle and saved back to
``config.json`` for the next launch.
