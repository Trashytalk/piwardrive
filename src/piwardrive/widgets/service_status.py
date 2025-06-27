"""Widget showing whether services are running."""

import logging
from typing import Any

from piwardrive.localization import _
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp
from piwardrive.utils import service_status

from .base import DashboardWidget


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
