Widgets
-------
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.


The dashboard is composed of small widgets providing metrics such as CPU
temperature, handshake counts and service status. Every widget subclasses
:class:`widgets.base.DashboardWidget` which defines a polling method and render
hook.

Widgets can be arranged on the Dashboard screen via drag and drop. Their layout
is saved in ``config.json`` so the next launch restores the same ordering. The
browser UI reads the same configuration, allowing widgets to be viewed remotely.
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

Step-by-step example
~~~~~~~~~~~~~~~~~~~~

1. Ensure the plugin directory exists::

      mkdir -p ~/.config/piwardrive/plugins

2. Add your widget implementation. Save the following as
   ``~/.config/piwardrive/plugins/my_widget.py``::

      from widgets.base import DashboardWidget

      class MyWidget(DashboardWidget):
          update_interval = 10.0

          def __init__(self, **kwargs):
              super().__init__(**kwargs)
              # create UI elements here

          def update(self):
              pass

3. Refresh the cache so PiWardrive notices the new file::

      python -c "import widgets; widgets.clear_plugin_cache()"

4. Launch PiWardrive and open the Dashboard screen. Drag *MyWidget* onto
   the layout or add ``{"cls": "MyWidget"}`` to ``dashboard_layout`` in
   ``config.json``.

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

HeatmapWidget
~~~~~~~~~~~~~
Shows a heatmap of discovered access point locations. The widget loads
coordinates from the local database and renders a small image using
``heatmap.save_png``. The number of grid cells can be adjusted via the
``bins`` parameter when instantiating the widget.

OrientationWidget
~~~~~~~~~~~~~~~~~
Displays the current device orientation using :func:`orientation_sensors.get_orientation_dbus`.
This requires the ``dbus`` Python package and the ``iio-sensor-proxy`` service
to be running on the system.  When those are missing the helper falls back to
raw accelerometer data via :func:`orientation_sensors.read_mpu6050`, which uses
an external MPU‑6050 connected over I\ :sup:`2`\ C.  If neither option is
available the widget simply reports ``not_available``.

VehicleSpeedWidget
~~~~~~~~~~~~~~~~~~
Shows the vehicle speed reported by :func:`vehicle_sensors.read_speed_obd`.

LoRaScanWidget
~~~~~~~~~~~~~~
Runs :func:`lora_scanner.scan_lora` and reports how many devices were found.

LogViewer
~~~~~~~~~
Scrollable widget that tails a log file. ``log_path`` selects the file, ``max_lines`` determines
how many lines are shown and ``poll_interval`` sets how often the file is re-read.  A drop-down
menu exposes the ``log_paths`` list from configuration so different logs can be selected on the
fly.  A helper
``jump_to_latest_error`` scrolls to the most recent line matching ``error_regex``.

.. note::
   Screenshots are not yet available for these widgets.
