Widgets
-------

The dashboard is composed of small widgets providing metrics such as CPU
temperature, handshake counts and service status. Every widget subclasses
:class:`widgets.base.DashboardWidget` which defines a polling method and render
hook.

Widgets can be arranged on the Dashboard screen via drag and drop. Their layout
is saved in ``config.json`` so the next launch restores the same ordering.
Polling intervals are configurable globally or per widget and can be adjusted
from the Settings screen. A built-in ``BatteryStatusWidget`` shows charge level
when the hardware exposes it.

Custom Widgets
~~~~~~~~~~~~~~

Additional widgets can be provided as plugins. Place Python modules in
``~/.config/piwardrive/plugins`` and they will be imported automatically on
startup. Each module may define one or more subclasses of
:class:`widgets.base.DashboardWidget`. Discovered classes are available from the
:mod:`widgets` package by name.

The plugin directory is scanned lazily and a timestamp is cached to avoid
repeated filesystem checks. Call :func:`widgets.clear_plugin_cache` after
installing new plugins so the next import or reload picks them up.

Example::

    from widgets.base import DashboardWidget

    class MyWidget(DashboardWidget):
        update_interval = 10.0

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # create UI elements here

        def update(self):
            pass

Compiled extensions written in PyO3 or Cython can also be used. Place the built
``.so``/``.pyd`` file or package inside ``~/.config/piwardrive/plugins``. The
extension must target the same Python version as PiWardrive and requires the
system headers and compiler tools (``build-essential``) to be installed.



Available Widgets
-----------------

The following sections describe each widget shipped with PiWardrive. All widgets share the
``update_interval`` attribute defined in :class:`widgets.base.DashboardWidget`. When creating a
custom dashboard layout this value can be overridden to change how often the widget refreshes.

BatteryStatusWidget
~~~~~~~~~~~~~~~~~~~
Displays the system battery percentage and charging state using :mod:`psutil`. It is disabled
by default and can be enabled via the ``widget_battery_status`` option in ``config.json`` or by
setting the ``PW_WIDGET_BATTERY_STATUS`` environment variable to ``1``.

CPUTempGraphWidget
~~~~~~~~~~~~~~~~~~
Plots CPU temperature over time. ``update_interval`` controls the sample rate in seconds and
``max_points`` limits how many samples are retained in the graph.

DiskUsageTrendWidget
~~~~~~~~~~~~~~~~~~~~
Graphs SSD usage percentage. The widget accepts ``update_interval`` and ``max_points`` parameters
similar to ``CPUTempGraphWidget``.

GPSStatusWidget
~~~~~~~~~~~~~~~
Shows the current GPS fix quality. Useful for quickly verifying that ``gpsd`` is providing data.

HandshakeCounterWidget
~~~~~~~~~~~~~~~~~~~~~~
Counts the number of captured Wi-Fi handshakes reported by BetterCAP.

ServiceStatusWidget
~~~~~~~~~~~~~~~~~~~
Reports whether the ``kismet`` and ``bettercap`` services are running.

StorageUsageWidget
~~~~~~~~~~~~~~~~~~
Displays disk usage for ``/mnt/ssd`` in percent.

NetworkThroughputWidget
~~~~~~~~~~~~~~~~~~~~~~~
Draws a real-time graph of bytes sent and received per second. ``update_interval`` controls the
polling frequency while ``max_points`` defines the graph width.

HealthStatusWidget
~~~~~~~~~~~~~~~~~~
Summarizes information from the background health monitor including network reachability and
disk statistics.


HealthAnalysisWidget
~~~~~~~~~~~~~~~~~~~~
Loads the last few :class:`persistence.HealthRecord` entries and computes averaged metrics.
A small temperature plot is rendered beneath the summary text.

LogViewer
~~~~~~~~~
Scrollable widget that tails a log file. ``log_path`` selects the file, ``max_lines`` determines
how many lines are shown and ``poll_interval`` sets how often the file is re-read. A helper
``jump_to_latest_error`` scrolls to the most recent line matching ``error_regex``.

.. note::
   Screenshots are not yet available for these widgets.
