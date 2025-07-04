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

Packaging a Plugin as a Module
------------------------------

To publish a widget on PyPI or share it with others, structure your code like a
standard Python package and include an entry point under
``piwardrive.widgets``.  The loader imports any classes referenced here when the
package is installed.

Example layout::

    myplugin/
    ├── pyproject.toml
    └── myplugin
        ├── __init__.py
        └── dashboard.py

``pyproject.toml`` should map a name to your widget class::

    [project.entry-points."piwardrive.widgets"]
    dashboard = "myplugin.dashboard:DashboardWidget"

Running ``pip install .`` installs the package and registers
``DashboardWidget`` automatically.

Widget Marketplace
------------------
The widget marketplace provides a curated list of third party widgets that can
be installed with a single click.  The API endpoint ``/widget-marketplace``
returns available entries while ``POST /widget-marketplace/install`` installs a
selected plugin.  Uploaded widgets are shared through the same interface so
others can discover them easily.
