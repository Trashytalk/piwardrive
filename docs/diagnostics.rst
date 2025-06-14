Diagnostics
----------

The :mod:`diagnostics` module exposes helpers for gathering system metrics and
rotating log files. Use ``diagnostics.self_test()`` to perform a quick health
check of network connectivity and running services. The ``HealthMonitor`` class
polls ``self_test`` periodically (default 10s, configurable via
``health_poll_interval``) and stores the latest results for widgets or other
components to display. ``self_test`` includes CPU temperature and
usage statistics, network reachability and service states.

Use :func:`utils.report_error` to surface exceptions consistently. It logs the
message and displays a dialog via the running application if available.
