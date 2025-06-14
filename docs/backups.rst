Backups
-------

The :mod:`backup` module provides helpers to snapshot configuration
and collected logs. Backups are written as ``.tar.gz`` archives in
``~/.config/piwardrive/backups`` by default. Each archive contains the
current ``config.json`` and the contents of the configured Kismet log
directory.

Use :func:`backup.create_backup` to create a snapshot and
:func:`backup.restore_backup` to revert the configuration and logs to a
previous state. :func:`backup.schedule_backups` registers a periodic
task with :class:`scheduler.PollScheduler` using the ``backup_interval``
setting from :class:`config.AppConfig`.
