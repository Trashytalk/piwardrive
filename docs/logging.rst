Logging
-------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

PiWardrive uses structured JSON logging configured by :func:`logconfig.setup_logging`.
The main log file is ``~/.config/piwardrive/app.log``. Set the ``PW_LOG_LEVEL``
environment variable to control verbosity or pass ``level`` to ``setup_logging``.
Common levels are ``DEBUG``, ``INFO``, ``WARNING`` and ``ERROR``.

Example::

    from piwardrive.logconfig import setup_logging
    import logging

    logger = setup_logging(
        "/tmp/piwardrive.log", level=logging.DEBUG, stdout=True
    )
    logger.info("PiWardrive initialized")

Logs from external tools are stored separately. ``kismet_logdir`` points to the
capture directory for Kismet (``/mnt/ssd/kismet_logs`` by default) while
BetterCAP writes to ``/var/log/bettercap.log``. Additional paths may be listed
in ``log_paths`` so the console screen and :doc:`status_service` ``/logs`` API
can display them.

Periodic cleanup compresses and rotates files under ``/var/log`` and any entries
from ``log_paths``. Adjust ``log_rotate_interval`` and ``log_rotate_archives`` in
``config.json`` or disable the behaviour entirely with ``cleanup_rotated_logs``.

Passing ``stdout=True`` to ``setup_logging`` duplicates output to the console,
which is useful during development or when running inside Docker.

Rotating Logs Manually
~~~~~~~~~~~~~~~~~~~~~~
Use ``scripts/rotate_logs.py`` to rotate the default log files without running PiWardrive::

    python scripts/rotate_logs.py

Specify paths as arguments or ``--max-files`` to choose how many archives to keep.
