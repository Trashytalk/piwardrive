"""Scheduling helpers for periodic callbacks."""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import os
import time
from datetime import datetime
from datetime import time as dt_time
from typing import Any, Awaitable, Callable, Dict, Mapping, Protocol, Sequence

from . import utils
from .core import config
from .gpsd_client import client as gps_client

ClockEvent = object


class Updatable(Protocol):
    """Protocol for widgets that can be scheduled."""

    update_interval: float

    def update(self) -> Awaitable[None] | None:
        """Update method to be implemented by schedulable widgets."""
        ...


class PollScheduler:
    """Manage named periodic callbacks using ``asyncio``."""

    def __init__(self) -> None:
        """Initialize the poll scheduler with empty task collections."""
        self._tasks: Dict[str, asyncio.Task] = {}
        self._next_runs: Dict[str, float] = {}
        self._durations: Dict[str, float] = {}
        self._rules: Dict[str, Mapping[str, Any]] = {}

    # ------------------------------------------------------------------
    # Scheduling rule helpers
    @staticmethod
    def _load_geofences() -> Dict[str, Sequence[tuple[float, float]]]:
        path = os.path.join(config.CONFIG_DIR, "geofences.json")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                _data = json.load(fh)
        except Exception:
            return {}
        result: Dict[str, Sequence[tuple[float, float]]] = {}
        for item in data if isinstance(data, list) else []:
            name = str(item.get("name", ""))
            points = [tuple(p) for p in item.get("points", []) if len(p) == 2]
            if name and points:
                result[name] = points
        return result

    @staticmethod
    def _match_time(ranges: Sequence[Sequence[str]] | None) -> bool:
        if not ranges:
            return True
        now = datetime.now().time()
        for start_s, end_s in ranges:
            try:
                start = dt_time.fromisoformat(start_s)
                end = dt_time.fromisoformat(end_s)
            except ValueError:
                continue
            if start <= end:
                if start <= now <= end:
                    return True
            else:
                if now >= start or now <= end:
                    return True
        return False

    @classmethod
    def check_rules(cls, rules: Mapping[str, Any]) -> bool:
        """Check if scheduling rules allow execution.
        
        Args:
            rules: Dictionary containing scheduling rules including
                time_ranges and geofences.
                
        Returns:
            True if all rules allow execution, False otherwise.
        """
        if not cls._match_time(rules.get("time_ranges")):
            return False
        geos = rules.get("geofences")
        if geos:
            pos = gps_client.get_position()
            if not pos:
                return False
            fences = cls._load_geofences()
            for name in geos:
                points = fences.get(name)
                if points and utils.point_in_polygon(pos, points):
                    return True
            return False
        return True

    def schedule(
        self,
        name: str,
        callback: Callable[[float], Awaitable[None] | None],
        interval: float,
        *,
        rules: Mapping[str, Any] | None = None,
    ) -> None:
        """Register ``callback`` to run every ``interval`` seconds."""
        if interval <= 0:
            raise ValueError("interval must be greater than 0")
        self.cancel(name)
        self._rules[name] = rules or {}

        async def _runner() -> None:
            last = time.time()
            next_run = last + interval
            while True:
                self._next_runs[name] = next_run
                start = time.perf_counter()
                try:
                    if self.check_rules(self._rules.get(name, {})):
                        dt = time.time() - last
                        last = time.time()
                        _result = callback(dt)
                        if inspect.isawaitable(result):
                            await result
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    logging.exception("Scheduled task %s failed: %s", name, exc)
                finally:
                    self._durations[name] = time.perf_counter() - start
                    next_run += interval
                    self._next_runs[name] = next_run
                await asyncio.sleep(max(0, next_run - time.time()))

        self._next_runs[name] = time.time() + interval
        self._durations[name] = float("nan")
        self._tasks[name] = asyncio.create_task(_runner())

    # ------------------------------------------------------------------
    # Widget helpers
    def register_widget(self, widget: Updatable, name: str | None = None) -> None:
        """Register a widget's ``update`` method based on ``update_interval``."""
        interval = getattr(widget, "update_interval", None)
        if interval is None:
            raise ValueError(f"Widget {widget} missing 'update_interval'")

        cb_name = name or f"{widget.__class__.__name__}-{id(widget)}"

        async def _call_update() -> None:
            try:
                _result = widget.update()
                if inspect.isawaitable(result):
                    await result
            except Exception as exc:  # pragma: no cover - UI update failures
                logging.exception("Widget %s update failed: %s", cb_name, exc)

        self.schedule(cb_name, lambda dt: _call_update(), interval)

    def cancel(self, name: str) -> None:
        """Cancel a scheduled callback by name."""
        task = self._tasks.pop(name, None)
        if task:
            task.cancel()
        self._rules.pop(name, None)

    def cancel_all(self) -> None:
        """Cancel all registered callbacks."""
        for name in list(self._tasks.keys()):
            self.cancel(name)

    def get_metrics(self) -> Dict[str, Dict[str, float]]:
        """Return metrics for each scheduled callback."""
        metrics: Dict[str, Dict[str, float]] = {}
        for name in self._tasks.keys():
            metrics[name] = {
                "next_run": self._next_runs.get(name, float("nan")),
                "last_duration": self._durations.get(name, float("nan")),
            }
        return metrics


class AsyncScheduler:
    """Manage periodic async callbacks using ``asyncio.create_task``."""

    def __init__(self) -> None:
        """Initialize the async scheduler with empty task collections."""
        self._tasks: Dict[str, asyncio.Task] = {}
        self._next_runs: Dict[str, float] = {}
        self._durations: Dict[str, float] = {}

    def schedule(
        self, name: str, callback: Callable[[], Awaitable[None] | None], interval: float
    ) -> None:
        """Run ``callback`` every ``interval`` seconds."""
        if interval <= 0:
            raise ValueError("interval must be greater than 0")
        self.cancel(name)

        async def _runner() -> None:
            next_run = time.time() + interval
            while True:
                self._next_runs[name] = next_run
                start = time.perf_counter()
                try:
                    _result = callback()
                    if inspect.isawaitable(result):
                        await result
                except asyncio.CancelledError:
                    raise
                except Exception as exc:  # pragma: no cover - background errors
                    logging.exception("AsyncScheduler task %s failed: %s", name, exc)
                finally:
                    self._durations[name] = time.perf_counter() - start
                    next_run += interval
                    self._next_runs[name] = next_run
                await asyncio.sleep(max(0, next_run - time.time()))

        self._next_runs[name] = time.time() + interval
        self._durations[name] = float("nan")
        self._tasks[name] = asyncio.create_task(_runner())

    def register_widget(self, widget: Updatable, name: str | None = None) -> None:
        """Register a widget's ``update`` coroutine based on ``update_interval``."""
        interval = getattr(widget, "update_interval", None)
        if interval is None:
            raise ValueError(f"Widget {widget} missing 'update_interval'")
        cb_name = name or f"{widget.__class__.__name__}-{id(widget)}"

        def _call_update() -> Awaitable[None] | None:
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
