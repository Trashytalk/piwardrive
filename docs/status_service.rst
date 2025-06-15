Status Service
==============

PiWardrive can expose recent health metrics over HTTP using a small FastAPI
application. The service reads the same ``HealthRecord`` data used by the GUI
and returns it as JSON.

Run the server after activating your virtual environment::

    python -m service

The API listens on ``0.0.0.0:8000`` by default. Request ``/status`` to retrieve
the last few records::

    curl http://localhost:8000/status

Use the ``limit`` query parameter to control how many entries are returned.

Additional Routes
-----------------

``/widget-metrics`` returns a summary used by the dashboard widgets::

   curl http://localhost:8000/widget-metrics

``/logs`` tails ``app.log`` (``lines`` query parameter controls length)::

   curl "http://localhost:8000/logs?lines=50"

Set ``PW_API_PASSWORD_HASH`` to require HTTP basic auth for all routes.
