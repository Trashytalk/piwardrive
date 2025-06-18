CLI Tools
---------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Several helper scripts are installed alongside the GUI. They can be invoked directly from the command line after installing the project:

``piwardrive-prefetch``
    Prefetch map tiles for an area without launching the interface::

        piwardrive-prefetch 37.7 -122.5 37.8 -122.4 --zoom 15

    The arguments define the bounding box (``lat1 lon1 lat2 lon2``) and optional zoom level.

``service-status``
    Show the active systemd services used by PiWardrive::

        service-status

    Returns ``active`` or ``inactive`` for ``gpsd``, ``kismet`` and ``bettercap``.

``piwardrive-service``
    Start the FastAPI status server described in :doc:`status_service`::

        piwardrive-service

``log-follow``
    Tail a log file and print new entries to the console::

        log-follow /var/log/syslog

See ``--help`` on each command for additional options.
