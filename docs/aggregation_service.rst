Centralized Aggregation Service
===============================

PiWardrive units can upload their local databases to a single aggregation server.
The service merges uploaded health and Wi-Fi observations and exposes combined
statistics along with heatmap data for map overlays.

Run the server with::

    python -m piwardrive.aggregation_service

By default data is stored under ``~/piwardrive-aggregation``.  Set the
``PW_AGG_DIR`` environment variable to change the location.

Endpoints
---------

``/upload``
    Accepts POST uploads created by :func:`remote_sync.sync_database_to_server`.

``/stats``
    Returns averaged system metrics across all uploaded records.

``/overlay``
    Returns heatmap points derived from all reported access point locations.
