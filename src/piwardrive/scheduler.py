"""Scheduling helpers for periodic callbacks."""

from __future__ import annotations

import asyncio
import inspect
import logging
import time
from typing import Any, Awaitable, Callable, Dict
try:  # pragma: no cover - optional Kivy dependency
    from kivy.clock import Clock, ClockEvent
except Exception:  # pragma: no cover - fallback stubs for tests
    class _DummyEvent:
        def cancel(self) -> None:
            pass

    class _DummyClock:
        @staticmethod
        def schedule_interval(
            callback: Callable[[float], Any], interval: float
        ) -> _DummyEvent:
            """Return a dummy event for tests."""
            return _DummyEvent()

        @staticmethod
        def unschedule(event: _DummyEvent) -> None:
            """No-op unschedule used in tests."""
            pass

    Clock = _DummyClock()
    ClockEvent = _DummyEvent


import utils


class PollScheduler:
    """Manage named periodic callbacks via :class:`~kivy.clock.Clock`."""

    def __init__(self) -> None:
        self._events: Dict[str, ClockEvent] = {}
        self._next_runs: Dict[str, float] = {}
        self._durations: Dict[str, float] = {}

    def schedule(self, name: str, callback: Callable, interval: float) -> None:
        """Register ``callback`` to run every ``interval`` seconds."""
        self.cancel(name)

        def _wrapper(dt: float) -> None:
            start = time.perf_counter()
            try:
                result = callback(dt)
                if inspect.isawaitable(result):
                    utils.run_async_task(result)  # type: ignore[arg-type]
            except Exception as exc:  # pragma: no cover - scheduled errors
                logging.exception("Scheduled task %s failed: %s", name, exc)
            finally:
                self._durations[name] = time.perf_counter() - start
                self._next_runs[name] = time.time() + interval

        self._next_runs[name] = time.time() + interval
        self._durations[name] = float("nan")
        self._events[name] = Clock.schedule_interval(_wrapper, interval)

        # ------------------------------------------------------------------
    # Widget helpers
    def register_widget(self, widget: Any, name: str | None = None) -> None:
        """Register a widget's ``update`` method based on ``update_interval``."""
        interval = getattr(widget, "update_interval", None)
        if interval is None:
            raise ValueError(f"Widget {widget} missing 'update_interval'")

        cb_name = name or f"{widget.__class__.__name__}-{id(widget)}"

        def _call_update(_dt: float) -> None:
            try:
                result = widget.update()
                if inspect.isawaitable(result):
                    utils.run_async_task(result)  # type: ignore[arg-type]
            except Exception as exc:  # pragma: no cover - UI update failures
                logging.exception("Widget %s update failed: %s", cb_name, exc)

        self.schedule(cb_name, _call_update, interval)

    def cancel(self, name: str) -> None:
        """Cancel a scheduled callback by name."""
        ev = self._events.pop(name, None)
        if ev:
            Clock.unschedule(ev)

    def cancel_all(self) -> None:
        """Cancel all registered callbacks."""
        for name in list(self._events.keys()):
            self.cancel(name)

    def get_metrics(self) -> Dict[str, Dict[str, float]]:
        """Return metrics for each scheduled callback."""
        metrics: Dict[str, Dict[str, float]] = {}
        for name in self._events.keys():
            metrics[name] = {
                "next_run": self._next_runs.get(name, float("nan")),
                "last_duration": self._durations.get(name, float("nan")),
            }
        return metrics


class AsyncScheduler:
    """Manage periodic async callbacks using ``asyncio.create_task``."""

    def __init__(self) -> None:
        self._tasks: Dict[str, asyncio.Task] = {}
        self._next_runs: Dict[str, float] = {}
        self._durations: Dict[str, float] = {}

    def schedule(
        self, name: str, callback: Callable[[], Awaitable[Any] | Any], interval: float
    ) -> None:
        """Run ``callback`` every ``interval`` seconds."""
        self.cancel(name)

        async def _runner() -> None:
            next_run = time.time() + interval
            while True:
                self._next_runs[name] = next_run
                start = time.perf_counter()
                try:
                    result = callback()
                    if inspect.isawaitable(result):
                        await result
                except asyncio.CancelledError:
                    raise
                except Exception as exc:  # pragma: no cover - background errors
                    logging.exception("AsyncScheduler task %s failed: %s", name, exc)
                finally:
                    self._durations[name] = time.perf_counter() - start
                    next_run = time.time() + interval
                    self._next_runs[name] = next_run
                await asyncio.sleep(interval)

        self._next_runs[name] = time.time() + interval
        self._durations[name] = float("nan")
        self._tasks[name] = asyncio.create_task(_runner())

    def register_widget(self, widget: Any, name: str | None = None) -> None:
        """Register a widget's ``update`` coroutine based on ``update_interval``."""
        interval = getattr(widget, "update_interval", None)
        if interval is None:
            raise ValueError(f"Widget {widget} missing 'update_interval'")
        cb_name = name or f"{widget.__class__.__name__}-{id(widget)}"

        def _call_update() -> Awaitable[Any] | Any:
            return widget.update()

        self.schedule(cb_name, _call_update, interval)

    def cancel(self, name: str) -> None:
        """Cancel the task registered under ``name`` if it exists."""
        task = self._tasks.pop(name, None)
        if task:
            task.cancel()
        self._next_runs.pop(name, None)
        self._durations.pop(name, None)

    async def cancel_all(self) -> None:
        """Cancel all running tasks and wait for them to finish."""
        tasks = list(self._tasks.values())
        self._tasks.clear()
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self._next_runs.clear()
        self._durations.clear()

    def get_metrics(self) -> Dict[str, Dict[str, float]]:
        """Return metrics for each running task."""
        metrics: Dict[str, Dict[str, float]] = {}
        for name in self._tasks.keys():
            metrics[name] = {
                "next_run": self._next_runs.get(name, float("nan")),
                "last_duration": self._durations.get(name, float("nan")),
            }
        return metrics
