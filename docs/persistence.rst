Persistence
-----------

The :mod:`persistence` module provides simple SQLite storage under
``~/.config/piwardrive/app.db``. Health monitor metrics are inserted as
:class:`HealthRecord` rows and can be retrieved with
``load_recent_health``. ``AppState`` tracks the last active screen and
startup time for restoration on the next launch.
