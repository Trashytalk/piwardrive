import logging

"""Dynamic logging configuration reloader."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, Callable, Dict, List

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from ..exceptions import ConfigurationError, ServiceError
from ..logging.structured_logger import get_logger


class LogConfigWatcher(FileSystemEventHandler):
    """Watches for log configuration file changes."""

    def __init__(self, config_manager: "DynamicLogConfig"):
        self.config_manager = config_manager

    def on_modified(self, event):
        """Handle configuration file modifications."""
        if event.is_directory:
            return

        if event.src_path == str(self.config_manager.config_path):
            self.config_manager.reload_config()


class DynamicLogConfig:
    """Dynamic log configuration management."""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.observers: List[Callable] = []
        self.lock = threading.RLock()
        self.logger = get_logger(__name__).logger
        self._setup_file_watcher()
        self.reload_config()

    def _setup_file_watcher(self):
        """Setup file system watcher for configuration changes."""
        self.observer = Observer()
        self.observer.schedule(
            LogConfigWatcher(self), str(self.config_path.parent), recursive=False
        )
        self.observer.start()

    def reload_config(self) -> None:
        """Reload configuration from file."""
        try:
            with self.lock:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    _newconfig = json.load(f)

                if self._validate_config(new_config):
                    old_config = self.config.copy()
                    self.config = new_config
                    self._notify_observers(old_config, new_config)
        except FileNotFoundError as exc:
            raise ConfigurationError(
                f"Config file not found: {self.config_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ConfigurationError("Invalid JSON in log configuration") from exc
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Error reloading log config: %s", exc, exc_info=exc)

    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration before applying."""
        required_fields = ["levels", "filters", "handlers"]
        return all(field in config for field in required_fields)

    def add_observer(self, callback: Callable):
        """Add configuration change observer."""
        self.observers.append(callback)

    def _notify_observers(self, old_config: Dict, new_config: Dict):
        """Notify observers of configuration changes."""
        for observer in self.observers:
            try:
                observer(old_config, new_config)
            except Exception as exc:  # noqa: BLE001
                self.logger.error(
                    "Error notifying config observer: %s", exc, exc_info=exc
                )

    def get_level_config(self) -> Dict[str, Any]:
        """Get current level configuration."""
        with self.lock:
            return self.config.get("levels", {}).copy()

    def get_filter_config(self) -> Dict[str, Any]:
        """Get current filter configuration."""
        with self.lock:
            return self.config.get("filters", {}).copy()

    def update_component_level(self, component: str, level: str) -> None:
        """Update log level for ``component`` via API."""
        with self.lock:
            if "levels" not in self.config:
                self.config["levels"] = {}
            if "components" not in self.config["levels"]:
                self.config["levels"]["components"] = {}

            self.config["levels"]["components"][component] = level
            self._save_config()

    def _save_config(self) -> None:
        """Persist configuration to disk."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except OSError as exc:
            raise ServiceError("Unable to write log configuration") from exc
        except Exception as exc:  # noqa: BLE001
            self.logger.error("Error saving config: %s", exc, exc_info=exc)
