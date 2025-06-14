Diagnostics
----------

The :mod:`diagnostics` module exposes helpers for gathering system metrics and
rotating log files. Use ``diagnostics.self_test()`` to perform a quick health
check of network connectivity and running services. The ``HealthMonitor`` class
polls ``self_test`` periodically and stores the latest results for widgets or
other components to display.
