"""Module di."""
from __future__ import annotations

"""Minimal dependency injection container."""

from typing import Any, Callable, Dict
from threading import Lock


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

        """Register a concrete instance for ``key``."""
        self._instances[key] = instance

    def register_factory(self, key: str, factory: Callable[[], Any]) -> None:
        """Register a factory callback for ``key``."""
        self._factories[key] = factory

    def resolve(self, key: str) -> Any:
        """Return an instance for ``key`` or raise ``KeyError``."""
        if key in self._instances:
            return self._instances[key]
        if key in self._factories:
            instance = self._factories[key]()
            self._instances[key] = instance
            return instance
        raise KeyError(f"No provider for {key}")

    def has(self, key: str) -> bool:
        """Return ``True`` if ``key`` has a provider or instance."""
        return key in self._instances or key in self._factories
