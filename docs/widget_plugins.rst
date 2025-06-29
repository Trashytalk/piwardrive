Widget Plugin Directory
=======================
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

Custom widgets can be installed without modifying the PiWardrive source. The
loader scans ``~/.config/piwardrive/plugins`` when :mod:`widgets` is imported.

Layout
------

The directory may contain standalone ``.py`` files, packages or compiled
extensions. Each module is checked for subclasses of
:class:`widgets.base.DashboardWidget` which are registered by name.

Example structure::

    ~/.config/piwardrive/plugins
    ├── my_widget.py
    └── speed_widget
        └── __init__.py

The plugin directory timestamp is cached so repeated imports do not hit the
filesystem. Call :func:`widgets.clear_plugin_cache` after adding or removing
files to refresh the cache.

Environment Variable
--------------------

By default plugins are loaded from ``~/.config/piwardrive/plugins``. Set
``PIWARDIVE_PLUGIN_DIR`` to override this location before importing
:mod:`widgets`. The value must point to a directory containing your plugin
modules and takes precedence over the default path.

Examples
--------

A simple widget showing an API request lives in
``examples/plugins/weather_widget.py``. It queries the Open-Meteo service for
London's current temperature and displays the result.
