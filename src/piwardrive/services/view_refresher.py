"""Service for periodically refreshing materialized database views."""

from __future__ import annotations

from piwardrive import persistence
from piwardrive.scheduler import PollScheduler
from piwardrive.utils import run_async_task


class ViewRefresher:
    """Periodically refresh materialized view tables."""

    def __init__(self, scheduler: PollScheduler, interval: int = 3600) -> None:
        """Initialize the view refresher service.
        
        Args:
            scheduler: The poll scheduler to use for periodic refresh.
            interval: Refresh interval in seconds (default: 3600 = 1 hour).
        """
        self._scheduler = scheduler
        self._event = "view_refresher"
        scheduler.schedule(
            self._event, lambda _dt: run_async_task(self.run()), interval
        )
        run_async_task(self.run())

    async def run(self) -> None:
        """Execute the view refresh operation."""
        await persistence.refresh_daily_detection_stats()
        await persistence.refresh_network_coverage_grid()


__all__ = ["ViewRefresher"]
