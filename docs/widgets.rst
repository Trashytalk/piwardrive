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
