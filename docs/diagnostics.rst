Diagnostics
-----------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


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
``diagnostics.get_service_statuses`` for quick checks outside the GUI.

Use :func:`utils.report_error` to surface exceptions consistently. It logs the
message and displays a dialog via the running application if available.

Profiling can be enabled by setting ``PW_PROFILE=1``. When active, a
``profile`` section is added to the system report and a summary is
logged on exit.  Set ``PW_PROFILE_CALLGRIND=/tmp/out.callgrind`` to
also export data in a format readable by KCachegrind.

Log Rotation
~~~~~~~~~~~~

``rotate_logs`` trims log files under ``/var/log`` and any additional paths
defined in the configuration. Each rotated file is compressed with ``gzip`` and
only a limited number of archives are kept to avoid filling the SSD on
unattended deployments. Set ``cleanup_rotated_logs`` to ``false`` in the
configuration to disable this periodic cleanup.
