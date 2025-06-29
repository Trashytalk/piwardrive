CLI Tools
---------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Several helper scripts are installed alongside the React dashboard and optional touch interface. They can be invoked directly from the command line after installing the project:

``piwardrive-prefetch``
    Prefetch map tiles for an area without launching the interface::

        piwardrive-prefetch 37.7 -122.5 37.8 -122.4 --zoom 15

    The arguments define the bounding box (``lat1 lon1 lat2 lon2``) and optional zoom level.
    Provide ``--folder`` and ``--concurrency`` to control where tiles are saved
    and how many downloads run in parallel::

        piwardrive-prefetch 35.0 -120.2 35.1 -120.1 --folder ~/tiles --concurrency 8

``piwardrive-prefetch-batch``
    Prefetch multiple areas from a file::

        piwardrive-prefetch-batch boxes.txt --zoom 15

    Each line in ``boxes.txt`` should contain ``lat1 lon1 lat2 lon2``.
    You can also specify an output folder and concurrency level::

        piwardrive-prefetch-batch boxes.txt --folder ~/tiles --concurrency 4

``service-status``
    Show the active systemd services used by PiWardrive::

        service-status

    Returns ``active`` or ``inactive`` for ``gpsd``, ``kismet`` and ``bettercap``.
    Pass service names as arguments to check custom units::

        service-status nginx sshd

``piwardrive-service``
    Start the FastAPI status server described in :doc:`status_service`::

        piwardrive-service

    The server listens on ``0.0.0.0:8000`` by default.

``log-follow``
    Tail a log file and print new entries to the console::

        log-follow /var/log/syslog

    Control the number of initial lines and polling interval with ``--lines``
    and ``--interval``::

        log-follow /var/log/kismet.log --lines 20 --interval 0.5
        
``config-cli``
    View or modify configuration values. Operates on the local
    ``config.json`` by default or against the API when ``--url`` is
    provided::

        config-cli get theme
        config-cli set map_use_offline true

    Interact with a running server by supplying its base URL::

        config-cli --url http://localhost:8000 get theme

``piwardrive-maintain-tiles``
    Run cache cleanup from the command line. Combine ``--purge``,
    ``--limit`` and ``--vacuum`` to control which maintenance operations
    run::

        piwardrive-maintain-tiles --purge --limit --vacuum --offline offline.mbtiles

    For example, delete tiles older than a week without touching the
    MBTiles archive::

        piwardrive-maintain-tiles --purge --max-age-days 7

``export-shp``
    Write saved access points to a Shapefile::

        export-shp aps.shp

See ``--help`` on each command for additional options.
