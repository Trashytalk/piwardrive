Centralized Aggregation Service
===============================

.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

PiWardrive units can upload their local databases to a single aggregation server.
The service merges uploaded health and Wi-Fi observations and exposes combined
statistics along with heatmap data for map overlays.

Run the server with::

    python -m piwardrive.aggregation_service

By default data is stored under ``~/piwardrive-aggregation``.  Set the
``PW_AGG_DIR`` environment variable to change the location.

Installation
------------

Run ``scripts/install_aggregation_service.sh`` from the repository root on the
target server.  The helper creates an ``agg-env`` virtual environment,
installs the required Python packages and writes
``/etc/systemd/system/piwardrive-aggregation.service``.
Enable the unit with::

    sudo systemctl enable --now piwardrive-aggregation.service

Endpoints
---------

``/upload``
    Accepts POST uploads created by :func:`remote_sync.sync_database_to_server`.

``/stats``
    Returns averaged system metrics across all uploaded records.

``/overlay``
    Returns heatmap points derived from all reported access point locations.
