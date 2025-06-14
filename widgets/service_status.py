"""Widget showing whether services are running."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel
from localization import _

from .base import DashboardWidget
from utils import service_status


class ServiceStatusWidget(DashboardWidget):
    """Report whether key capture services are running."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        """Set up label widget and kick off the first refresh."""
        super().__init__(**kwargs)
        self.label = MDLabel(text=f"{_('services')}: {_('not_available')}")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        """Poll service status and update the label."""
        try:
            kis = service_status('kismet')
            btc = service_status('bettercap')
            self.label.text = (
                f"{_('kismet')}: { _('ok') if kis else _('down') } | "
                f"{_('bettercap')}: { _('ok') if btc else _('down') }"
            )
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("ServiceStatusWidget update failed: %s", exc)
