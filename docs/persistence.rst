Persistence
-----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


The :mod:`persistence` module provides a lightweight SQLite database at
``~/.config/piwardrive/app.db`` by default. Set ``PW_DB_PATH`` to override
this location. Health monitor metrics are stored as
:class:`HealthRecord` rows and can be queried with ``load_recent_health``.
The same file stores ``AppState`` which remembers the last active screen and
the start time of the previous session. When PiWardrive launches these values
are restored so the GUI picks up where it left off. Database connections are
cached so repeated calls do not reinitialise the schema, reducing disk I/O.
The connection is placed into write-ahead logging mode using
``PRAGMA journal_mode=WAL`` to improve read/write concurrency.

Inspect the database using ``sqlite3 ~/.config/piwardrive/app.db``. The schema
is intentionally small and deleting the file only clears history—configuration
is kept separately in ``config.json``.
