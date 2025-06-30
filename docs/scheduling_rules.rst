Scheduling Rules
----------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

`PollScheduler.schedule` accepts an optional ``rules`` mapping controlling when a
callback runs. Rules may contain ``time_ranges`` and ``geofences`` entries. Time
ranges are ``["HH:MM", "HH:MM"]`` pairs in 24-hour notation. Geofences refer to
polygons saved in ``~/.config/piwardrive/geofences.json``.

Example configuration snippet::

    {
        "scan_rules": {
            "wifi": {
                "time_ranges": [["08:00", "18:00"]],
                "geofences": ["work"]
            }
        }
    }

Scans outside the defined windows or locations are skipped.
