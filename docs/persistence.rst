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
are restored so the React dashboard picks up where it left off.

Database connections are
cached so repeated calls do not reinitialise the schema, reducing disk I/O.
The connection is placed into write-ahead logging mode using
``PRAGMA journal_mode=WAL`` to improve read/write concurrency.

Inspect the database using ``sqlite3 ~/.config/piwardrive/app.db``. The schema
is intentionally small and deleting the file only clears history—configuration
is kept separately in ``config.json``.

Maintenance
-----------

Run ``persistence.vacuum`` to reclaim free space after deleting rows. A
convenient ``piwardrive-vacuum`` command is installed which simply calls this
function::

   piwardrive-vacuum

Delete old health monitor rows with ``persistence.purge_old_health``. The
``prune-db`` command wraps this helper and accepts the retention period in
days::

   prune-db 30

Schema Migrations
-----------------

As new versions of PiWardrive add tables or columns, the database schema is
automatically migrated. The :mod:`persistence` module tracks a schema version
and applies migrations when a connection is opened. To manually run migrations
use the ``piwardrive-migrate`` command::

   piwardrive-migrate

Deleting ``app.db`` will recreate it with the latest schema, but the migration
command is useful when upgrading an existing installation.
