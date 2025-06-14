Workflows
=========

The following diagrams illustrate common PiWardrive tasks.

Scanning and Logging
--------------------

.. mermaid::

   flowchart TD
       A[Boot Device] --> B[Load Configuration]
       B --> C[Start Kismet / BetterCAP]
       C --> D[Begin GPS Polling]
       D --> E[Record Access Points]
       E --> F[Write Logs / DB]

System Diagnostics
------------------

.. mermaid::

   sequenceDiagram
       participant User
       participant App
       participant Diagnostics
       participant Persistence

       User->>App: open Diagnostics screen
       App->>Diagnostics: self_test()
       Diagnostics->>Persistence: store HealthRecord
       Diagnostics-->>App: results
       App-->>User: show status

