Status Service
==============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


PiWardrive exposes recent health metrics over HTTP using a small FastAPI
application. The ``/status`` endpoint is now asynchronous so heavy database
access occurs in a background thread. This allows multiple requests to run
concurrently and improves throughput on multi-core devices.

Run the server after activating your virtual environment::

    python -m service

The API listens on ``0.0.0.0:8000`` by default. Request ``/status`` to retrieve
the last few records::

    curl http://localhost:8000/status

Use the ``limit`` query parameter to control how many entries are returned.


Autostart
---------

Copy ``examples/service_api.service`` into ``/etc/systemd/system/`` and enable it
with ``sudo systemctl enable --now service_api.service`` to run ``python -m
service`` on boot.


Additional Routes
-----------------

``/widget-metrics`` returns a summary used by the dashboard widgets::

   curl http://localhost:8000/widget-metrics

The JSON response includes CPU temperature, service status, handshake count,
average RSSI and network throughput (``rx_kbps``/``tx_kbps``). Battery level
and vehicle statistics (speed, RPM and engine load) are also returned when
available for use in external dashboards.

``/logs`` tails ``app.log`` (``lines`` query parameter controls length). The
file path is set by ``logconfig.DEFAULT_LOG_PATH`` and may be mirrored to
``stdout`` using ``setup_logging``. The endpoint validates that ``path`` is in
the ``log_paths`` whitelist defined in ``config.json``::

   curl "http://localhost:8000/logs?lines=50"

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

