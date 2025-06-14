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

Example::

    from widgets.base import DashboardWidget

    class MyWidget(DashboardWidget):
        update_interval = 10.0

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # create UI elements here

        def update(self):
            pass
