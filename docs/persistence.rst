Persistence
-----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Database Architecture
~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   graph TB
       A[PiWardrive Application] --> B[Persistence Module]
       B --> C[SQLite Database]
       C --> D[HealthRecord Table]
       C --> E[AppState Table]
       C --> F[Configuration Data]
       
       B --> G[Database Connection Pool]
       G --> H[WAL Mode]
       G --> I[Connection Caching]
       
       J[Optional Encryption] --> K[SQLCipher]
       K --> C
       
       L[Maintenance Tasks] --> M[Vacuum Operation]
       L --> N[Purge Old Records]
       L --> O[Database Optimization]
       
       style A fill:#e1f5fe
       style B fill:#e8f5e8
       style C fill:#fff3e0
       style D fill:#fce4ec
       style E fill:#f3e5f5
       style F fill:#ffebee

Data Flow
~~~~~~~~~

.. mermaid::

   sequenceDiagram
       participant App as Application
       participant Persist as Persistence Module
       participant DB as SQLite Database
       participant Health as Health Monitor
       
       App->>Persist: Initialize Database
       Persist->>DB: Create Schema
       DB-->>Persist: Schema Ready
       
       Health->>Persist: Store Health Metrics
       Persist->>DB: INSERT HealthRecord
       DB-->>Persist: Record Saved
       
       App->>Persist: Load Recent Health
       Persist->>DB: SELECT Health Records
       DB-->>Persist: Return Results
       Persist-->>App: Health Data
       
       App->>Persist: Save App State
       Persist->>DB: UPDATE AppState
       DB-->>Persist: State Saved
       
       Note over Persist,DB: WAL mode for better concurrency
       Note over DB: Optional SQLCipher encryption


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

Encryption
~~~~~~~~~~

Install ``pysqlcipher3`` and ``libsqlcipher-dev`` to enable optional
database encryption. Set ``PW_DB_KEY`` to a passphrase before running
``piwardrive-migrate`` or launching the application. When present the
database is opened with SQLCipher and the schema is created using the
provided key.

Inspect encrypted databases with ``sqlcipher`` instead of ``sqlite3``:

.. code-block:: bash

   PW_DB_KEY=secret sqlcipher ~/.config/piwardrive/app.db


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

Database Summary
----------------

Health monitor databases copied from remote devices can grow quickly. The
``db-summary`` command prints row counts for important tables so you can gauge
their size::

   db-summary ~/piwardrive/health.db

Pass ``--json`` to emit machine-readable output.
