Centralized Aggregation Service
===============================

.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

PiWardrive units can upload their local databases to a single aggregation server.
The service merges uploaded health and Wi-Fi observations and exposes combined
statistics along with heatmap data for map overlays.

Run the server with::

    python -m piwardrive.aggregation_service

``docker-compose.aggregation.yml`` launches the aggregation service together
with a simple sync receiver. Start both with::

    docker compose -f docker-compose.aggregation.yml up

By default data is stored under ``~/piwardrive-aggregation``.  Set the
``PW_AGG_DIR`` environment variable to change the location. Set
``PW_AGG_PORT`` to change the listening port (defaults to ``9100``).

Installation
------------

Run ``scripts/install_aggregation_service.sh`` from the repository root on the
target server.  The helper creates an ``agg-env`` virtual environment,
installs the required Python packages and writes
``/etc/systemd/system/piwardrive-aggregation.service``.
Enable the unit with::

    sudo systemctl enable --now piwardrive-aggregation.service

The unit installed by the script matches ``examples/piwardrive-aggregation.service``
which you can also copy manually into ``/etc/systemd/system/``.

Endpoints
---------

``/upload``
    Accepts POST uploads created by :func:`remote_sync.sync_database_to_server`.

``/stats``
    Returns averaged system metrics across all uploaded records.

``/overlay``
    Returns heatmap points derived from all reported access point locations.

Container Image
---------------

``Dockerfile.aggregation`` builds a lightweight image running
``piwardrive.aggregation_service``.  Build it with::

   docker build -f Dockerfile.aggregation -t piwardrive-aggregation .

Run the container exposing port 9100 and mounting a data directory::

   docker run --rm -p 9100:9100 -v ~/agg-data:/data \
      -e PW_AGG_DIR=/data -e PW_AGG_PORT=9100 piwardrive-aggregation
