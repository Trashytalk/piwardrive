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

Packaging for pip
-----------------

Plugins can also be distributed as a standard Python package and installed with
``pip``.  Define an entry point under ``piwardrive.widgets`` so the loader can
discover your widget class without copying files manually.

Example project layout::

    mywidget/
    ├── pyproject.toml
    └── mywidget
        ├── __init__.py
        └── plugin.py

The ``pyproject.toml`` should declare the entry point group::

    [project.entry-points."piwardrive.widgets"]
    speed = "mywidget.plugin:SpeedWidget"

Installing the package with ``pip install .`` registers ``SpeedWidget`` and it
becomes available from :mod:`widgets` just like plugins placed in the local
directory.
