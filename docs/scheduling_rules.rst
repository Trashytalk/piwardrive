Scheduling Rules
----------------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Scheduling Rules Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   graph TB
       A[PollScheduler] --> B[Schedule Rules]
       B --> C[Time Ranges]
       B --> D[Geofences]
       
       C --> E[Start Time]
       C --> F[End Time]
       C --> G[24-hour Format]
       
       D --> H[Geofence Polygons]
       D --> I[Location Matching]
       D --> J[GPS Coordinates]
       
       A --> K[Callback Execution]
       K --> L{Rule Check}
       L -->|Pass| M[Execute Callback]
       L -->|Fail| N[Skip Execution]
       
       H --> O[geofences.json]
       J --> P[Current Location]
       
       style A fill:#e1f5fe
       style B fill:#e8f5e8
       style C fill:#fff3e0
       style D fill:#fce4ec
       style K fill:#f3e5f5

Rule Evaluation Flow
~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   flowchart TD
       A[Scheduled Task] --> B{Time Range Check}
       B -->|Outside Range| C[Skip Task]
       B -->|Within Range| D{Geofence Check}
       D -->|Outside Geofence| C
       D -->|Within Geofence| E[Execute Task]
       D -->|No Geofence Rules| E
       
       style A fill:#e1f5fe
       style B fill:#fff3e0
       style C fill:#ffebee
       style D fill:#fce4ec
       style E fill:#e8f5e8

`PollScheduler.schedule` accepts an optional ``rules`` mapping controlling when a
callback runs. Rules may contain ``time_ranges`` and ``geofences`` entries. Time
ranges are ``["HH:MM", "HH:MM"]`` pairs in 24-hour notation. Geofences refer to
polygons saved in ``~/.config/piwardrive/geofences.json``.

Example configuration snippet::

    {
        "scan_rules": {
            "wifi": {
                "time_ranges": [["08:00", "18:00"]],
                "geofences": ["work"]
            }
        }
    }

Scans outside the defined windows or locations are skipped.
