Diagnostics
-----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Diagnostics Architecture
~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   graph TB
       A[Diagnostics Module] --> B[Health Monitor]
       A --> C[Self Test]
       A --> D[Service Status]
       A --> E[System Metrics]
       
       B --> F[Periodic Polling]
       B --> G[Health Records]
       B --> H[Export System]
       
       C --> I[CPU Temperature]
       C --> J[Network Connectivity]
       C --> K[Service States]
       C --> L[Disk SMART Health]
       
       D --> M[Service Management]
       D --> N[Restart Services]
       D --> O[Status Reporting]
       
       E --> P[CPU Usage]
       E --> Q[Memory Usage]
       E --> R[Disk Usage]
       E --> S[Network Stats]
       
       G --> T[Persistence Layer]
       H --> U[Health Export Files]
       
       style A fill:#e1f5fe
       style B fill:#e8f5e8
       style C fill:#fff3e0
       style D fill:#fce4ec
       style E fill:#f3e5f5

Health Monitoring Flow
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   sequenceDiagram
       participant HM as Health Monitor
       participant ST as Self Test
       participant Services as System Services
       participant DB as Database
       participant Export as Export System
       
       HM->>ST: Run Self Test (every 10s)
       ST->>Services: Check Service Status
       Services-->>ST: Service States
       ST->>ST: Collect System Metrics
       ST-->>HM: Health Results
       HM->>DB: Store Health Record
       
       Note over HM,DB: Configurable via health_poll_interval
       
       HM->>Export: Schedule Export (if enabled)
       Export->>DB: Query Health Records
       DB-->>Export: Health Data
       Export->>Export: Create Export File
       Export->>Export: Compress (if enabled)
       Export->>Export: Cleanup Old Files
       
       Note over Export: Retention policy applied


The :mod:`diagnostics` module exposes helpers for gathering system metrics and
rotating log files. Use ``diagnostics.self_test()`` to perform a quick health
check of network connectivity and running services. The ``HealthMonitor`` class
polls ``self_test`` periodically (default 10s, configurable via
``health_poll_interval``) and stores the latest results for widgets or other
components to display. ``self_test`` includes CPU temperature and usage
statistics, network reachability and service states. Disk SMART health is also
reported for ``/mnt/ssd`` and surfaced in the stats screen.

Health Monitoring
~~~~~~~~~~~~~~~~~

``health_poll_interval`` controls how often ``self_test`` runs. Override this in
``config.json`` or via ``PW_HEALTH_POLL_INTERVAL``. Setting a longer interval
reduces CPU usage while a shorter one yields more frequent updates.

Exports of :class:`persistence.HealthRecord` data are scheduled when
``health_export_interval`` is greater than zero. Files are written to
``health_export_dir`` and may be compressed with ``compress_health_exports``.
Old exports are deleted after ``health_export_retention`` days. The matching
environment variables ``PW_HEALTH_EXPORT_INTERVAL``, ``PW_HEALTH_EXPORT_DIR``,
``PW_COMPRESS_HEALTH_EXPORTS`` and ``PW_HEALTH_EXPORT_RETENTION`` mirror these
options.

``scripts/service_status.py`` provides a small command-line interface to
``diagnostics.get_service_statuses`` for quick checks outside the React dashboard. The same information is visible in the dashboard via the status service.

When a service check fails ``self_test`` calls
``utils.run_service_cmd(name, "restart")`` for any entry found in the
``restart_services`` list. Configure this behaviour in ``config.json`` or with
the ``PW_RESTART_SERVICES`` environment variable (a JSON array of service
names).

Use :func:`utils.report_error` to surface exceptions consistently. It logs the
message and displays a dialog via the running application if available.

The diagnostics module now integrates with the unified error handling system.
Failures raise subclasses of :class:`piwardrive.exceptions.PiWardriveError` and
are logged using the structured logger with a correlation identifier. This
enables easier debugging of background tasks such as log uploads or database
maintenance.

Profiling can be enabled by setting ``PW_PROFILE=1``. When active, a
``profile`` section is added to the system report and a summary is
logged on exit.  Set ``PW_PROFILE_CALLGRIND=/tmp/out.callgrind`` to
also export data in a format readable by KCachegrind.

Baseline Analysis
~~~~~~~~~~~~~~~~~

``baseline_history_days`` determines how far back the historical slice spans
when computing averages. ``baseline_threshold`` defines the minimum change that
triggers an anomaly in ``/baseline-analysis`` results. Adjust these values in
``config.json`` or via ``PW_BASELINE_HISTORY_DAYS`` and ``PW_BASELINE_THRESHOLD``.

Log Rotation
~~~~~~~~~~~~

``rotate_logs`` trims log files under ``/var/log`` and any additional paths
defined in the configuration. Each rotated file is compressed with ``gzip`` and
only a limited number of archives are kept to avoid filling the SSD on
unattended deployments. Set ``cleanup_rotated_logs`` to ``false`` in the
configuration to disable this periodic cleanup.
