"""Widget displaying SQLite table counts and database size."""

import logging
import os
from typing import Any

from piwardrive.simpleui import dp, Label as MDLabel, Card as MDCard
from piwardrive.localization import _

from .base import DashboardWidget
from piwardrive.persistence import get_table_counts, _db_path
from piwardrive.utils import run_async_task


class DBStatsWidget(DashboardWidget):
    """Show row counts for each table and the DB file size."""

    update_interval = 10.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text=f"{_('db')}: {_('not_available')}", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Refresh table counts and DB file size."""

        def _apply(counts: dict[str, int]) -> None:
            try:
                size = os.path.getsize(_db_path()) / 1024
                parts = [f"{name}:{cnt}" for name, cnt in counts.items()]
                stats = " ".join(parts)
                self.label.text = f"{_('db')}: {size:.1f}KB {stats}"
            except Exception as exc:
                logging.exception("DBStatsWidget update failed: %s", exc)

        try:
            run_async_task(get_table_counts(), _apply)
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("DBStatsWidget schedule failed: %s", exc)
