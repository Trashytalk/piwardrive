"""Widget displaying SQLite table counts and database size."""

import asyncio
import logging
import os
from typing import Any

from piwardrive.localization import _
from piwardrive.ui import Card
from piwardrive.ui import Label
from piwardrive.ui import dp

from .base import DashboardWidget

try:  # pragma: no cover - optional dependency
    from piwardrive.persistence import _db_path, get_table_counts
except Exception:  # pragma: no cover - fallbacks for tests without deps

    async def get_table_counts() -> dict[str, int]:
        """Return an empty table-count mapping when persistence is missing."""
        return {}

    def _db_path() -> str:
        return ""


try:  # pragma: no cover - optional dependency
    from piwardrive.utils import run_async_task
except Exception:  # pragma: no cover - simple fallback
    from concurrent.futures import Future
    from typing import Any, Callable, Coroutine, TypeVar

    T = TypeVar("T")

    def run_async_task(
        coro: Coroutine[Any, Any, T], callback: Callable[[T], None] | None = None
    ) -> Future[T]:
        """Synchronously execute ``coro`` and invoke ``callback`` if given."""
        fut: Future[T] = Future()

        try:
            result = asyncio.run(coro)
            fut.set_result(result)
            if callback is not None:
                callback(result)
        except Exception as exc:
            fut.set_exception(exc)
        return fut


class DBStatsWidget(DashboardWidget):
    """Show row counts for each table and the DB file size."""

    update_interval = 10.0

    def __init__(self, **kwargs: Any) -> None:
        """Create the widget and schedule the first update."""
        super().__init__(**kwargs)
        self.card = Card(orientation="vertical", padding=dp(8), radius=[8])
        self.label = Label(text=f"{_('db')}: {_('not_available')}", halign="center")
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
