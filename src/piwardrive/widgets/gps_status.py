"""Widget showing GPS fix quality."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel
from ..localization import _

from .base import DashboardWidget
from ..utils import get_gps_fix_quality


class GPSStatusWidget(DashboardWidget):
    """Show quality of the current GPS fix."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        """Create label widget and request the first update."""
        super().__init__(**kwargs)
        self.label = MDLabel(text=f"{_('gps')}: {_('not_available')}")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        """Refresh with the latest GPS fix quality."""
        try:
            self.label.text = f"{_('gps')}: {get_gps_fix_quality()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("GPSStatusWidget update failed: %s", exc)
