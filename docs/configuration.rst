Configuration
-------------

Configuration is stored in ``~/.config/piwardrive/config.json``. Most values can
be overridden using environment variables prefixed with ``PW_``. For example::

   PW_MAP_POLL_GPS=5 python main.py

To enable the optional battery widget set ``widget_battery_status`` to ``true``::

   PW_WIDGET_BATTERY_STATUS=1 python main.py

See :mod:`config` for defaults and helpers.
Backups are stored in ``backup_dir`` and run every ``backup_interval`` seconds.
