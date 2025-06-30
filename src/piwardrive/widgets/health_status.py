"""Widget summarizing the results of the periodic health monitor."""

import logging
from typing import Any

from piwardrive.localization import _
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class HealthStatusWidget(DashboardWidget):
    """Display results from the global health monitor.

    A label widget is prepared on initialization and the first update is
    triggered immediately.
    """

    update_interval = 10.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('health')}: {_('not_available')}", halign="center"
        )
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:  # pragma: no cover - GUI update
        """Refresh the widget with the latest health metrics."""
        try:
            monitor = None
            try:
                from piwardrive import main

                monitor = getattr(main, "GLOBAL_HEALTH_MONITOR", None)
            except Exception:
                monitor = None
            data = monitor.data if monitor else None
            if not data:
                self.label.text = f"{_('health')}: {_('not_available')}"
                return
            disk = data["system"]["disk_percent"]
            net = _("ok") if data["network_ok"] else _("down")
            services = " ".join(
                f"{name}:{_('ok') if ok else _('down')}"
                for name, ok in data["services"].items()
            )
            self.label.text = f"{_('net')}:{net} {_('ssd')}:{disk:.0f}% {services}"
        except Exception as exc:
            logging.exception("HealthStatusWidget update failed: %s", exc)
