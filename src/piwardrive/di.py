"""Minimal dependency injection container."""

from __future__ import annotations

from threading import Lock
from typing import Any, Callable, Dict


class Container:
    """Very small service container."""

    def __init__(self) -> None:
        self._instances: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._lock = Lock()

    def register_instance(self, key: str, instance: Any) -> None:
        with self._lock:
            self._instances[key] = instance

    def register_factory(self, key: str, factory: Callable[[], Any]) -> None:
        with self._lock:
            self._factories[key] = factory

    def resolve(self, key: str) -> Any:
        with self._lock:
            if key in self._instances:
                return self._instances[key]
            if key in self._factories:
                instance = self._factories[key]()
                self._instances[key] = instance
                return instance
            raise KeyError(f"No provider for {key}")

    def has(self, key: str) -> bool:
        with self._lock:
            return key in self._instances or key in self._factories
