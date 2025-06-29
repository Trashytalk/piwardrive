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
