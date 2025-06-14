"""Widget summarizing the results of the periodic health monitor."""

import logging
from typing import Any

from kivy.app import App
from kivymd.uix.label import MDLabel
from localization import _

from .base import DashboardWidget


class HealthStatusWidget(DashboardWidget):
    """Display results from the global health monitor."""

    update_interval = 10.0

    def __init__(self, **kwargs: Any) -> None:
        """Create widget label and trigger the first update."""
        super().__init__(**kwargs)
        self.label = MDLabel(text=f"{_('health')}: {_('not_available')}")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:  # pragma: no cover - GUI update
        """Refresh the widget with the latest health metrics."""
        try:
            app = App.get_running_app()
            monitor = getattr(app, "health_monitor", None)
            data = monitor.data if monitor else None
            if not data:
                self.label.text = f"{_('health')}: {_('not_available')}"
                return
            disk = data["system"]["disk_percent"]
            net = _("ok") if data["network_ok"] else _("down")
            services = " ".join(
                f"{name}:{_('ok') if ok else _('down')}" for name, ok in data["services"].items()
            )
            self.label.text = (
                f"{_('net')}:{net} {_('ssd')}:{disk:.0f}% {services}"
            )
        except Exception as exc:
            logging.exception("HealthStatusWidget update failed: %s", exc)
