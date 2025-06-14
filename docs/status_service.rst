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
