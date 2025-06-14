Database Integration
--------------------

The :mod:`database` module uses SQLite to store historical access-point
and metrics data. Call :func:`database.init_db` on a connection from
:func:`database.get_connection` to create tables. Use
:func:`database.ingest_ap_data` and :func:`database.ingest_metrics`
to persist new records. Query recent entries with
:func:`database.query_recent_aps` and
:func:`database.query_recent_metrics`.
