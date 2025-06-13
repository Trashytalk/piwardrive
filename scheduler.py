"""Simple polling scheduler built on ``kivy.clock.Clock``."""

from typing import Callable, Dict
from kivy.clock import Clock


class PollScheduler:
    """Manage named periodic callbacks via :class:`~kivy.clock.Clock`."""

    def __init__(self) -> None:
        self._events: Dict[str, Clock] = {}

    def schedule(self, name: str, callback: Callable, interval: float) -> None:
        """Register ``callback`` to run every ``interval`` seconds."""
        self.cancel(name)
        self._events[name] = Clock.schedule_interval(callback, interval)

    def cancel(self, name: str) -> None:
        """Cancel a scheduled callback by name."""
        ev = self._events.pop(name, None)
        if ev:
            Clock.unschedule(ev)

    def cancel_all(self) -> None:
        """Cancel all registered callbacks."""
        for name in list(self._events.keys()):
            self.cancel(name)
