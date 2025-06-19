Status Service
==============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive exposes recent health metrics over HTTP using a small FastAPI
application. The ``/status`` endpoint is now asynchronous so heavy database
access occurs in a background thread. This allows multiple requests to run
concurrently and improves throughput on multi-core devices.

Run the server after activating your virtual environment::

   piwardrive-service

The API listens on ``0.0.0.0:8000`` by default. Request ``/status`` to retrieve
the last few records::

    curl http://localhost:8000/status

Use the ``limit`` query parameter to control how many entries are returned.


Autostart
---------

Copy ``examples/service_api.service`` into ``/etc/systemd/system/`` and enable it
with ``sudo systemctl enable --now service_api.service`` to run ``piwardrive-service`` on boot.


Additional Routes
-----------------

``/widget-metrics`` returns a summary used by the dashboard widgets::

   curl http://localhost:8000/widget-metrics

The JSON response includes CPU temperature, service status, handshake count,
average RSSI and network throughput (``rx_kbps``/``tx_kbps``). Battery level
and vehicle statistics (speed, RPM and engine load) are also returned when
available for use in external dashboards.

``/cpu`` reports the current CPU temperature and load percentage::

   curl http://localhost:8000/cpu

``/ram`` returns system memory usage::

   curl http://localhost:8000/ram

``/storage`` shows disk usage for ``/mnt/ssd`` by default (override with ``path``)::

   curl http://localhost:8000/storage

``/orientation`` reads sensors via ``orientation_sensors`` and returns the
current orientation string, rotation angle and raw accelerometer/gyroscope data::

   curl http://localhost:8000/orientation

``/gps`` exposes latitude, longitude, accuracy and fix quality from ``gpsd``::

   curl http://localhost:8000/gps
``/api/widgets`` lists all widget class names discovered by :mod:`piwardrive.widgets`::

   curl http://localhost:8000/api/widgets

This allows external dashboards to load widgets dynamically.


``/logs`` tails ``app.log`` (``lines`` query parameter controls length). The
file path is set by ``logconfig.DEFAULT_LOG_PATH`` and may be mirrored to
``stdout`` using ``setup_logging``. The endpoint validates that ``path`` is in
the ``log_paths`` whitelist defined in ``config.json``::

   curl "http://localhost:8000/logs?lines=50"

``/export/aps``
    Download saved Wi-Fi access points. Use the ``fmt`` query parameter to
    choose ``csv``, ``json``, ``geojson``, ``kml`` or ``gpx``.

``/export/bt``
    Return Bluetooth scan results in the requested format.

``/ws/status`` streams the same information over a WebSocket connection. Each
message combines the ``/status`` and ``/widget-metrics`` responses so clients can
stay up to date without polling::

   websocat ws://localhost:8000/ws/status

Each message includes ``seq`` and ``timestamp`` fields plus an ``errors`` counter
to help detect missed updates.

Set ``PW_API_PASSWORD_HASH`` to require HTTP basic auth for all routes.

Benchmark
---------

Run ``benchmarks/status_benchmark.py`` to estimate request throughput without
network overhead. The script uses ``httpx.AsyncClient`` to fire multiple
concurrent requests against the ASGI application::

    python benchmarks/status_benchmark.py

On a Raspberry Pi 5 the asynchronous implementation processes hundreds of
requests per second, roughly doubling the throughput compared to the original
synchronous handler.

