"""Widget showing whether services are running."""

import logging
from typing import Any
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from piwardrive.localization import _

from .base import DashboardWidget
from piwardrive.utils import service_status


class ServiceStatusWidget(DashboardWidget):
    """Report whether key capture services are running."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        """Set up label widget and kick off the first refresh."""
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('services')}: {_('not_available')}", halign="center"
        )
        self.card.add_widget(self.label)
        self.add_widget(self.card)
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
