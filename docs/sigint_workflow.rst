SIGINT Workflow
---------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

The command-line tools packaged with :mod:`sigint_suite` allow quick collection
of wireless metadata. Results can be post-processed by plugins and hooks before
they are written to JSON files or saved in a SQLite database. The database can
then be uploaded to a remote host or consumed by the aggregation service.

.. mermaid::

   flowchart TD
       subgraph CLI Tools
           A[wifi-scan]
           B[bluetooth-scan]
           C[imsi-scan]
           D[band-scan]
           E[scan-all]
       end
       CLI Tools --> F[Scanner modules]
       F --> G{Plugins / hooks?}
       G -->|yes| H[Custom logic]
       G -->|no| I[Records]
       H --> I
       I --> J{Export}
       J --> K[JSON/CSV/YAML]
       J --> L[SQLite DB]
       L --> M[remote_sync.sync_database_to_server]
       M --> N[Aggregation service]
