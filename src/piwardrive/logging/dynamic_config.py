import json
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


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
        self._setup_file_watcher()
        self.reload_config()

    def _setup_file_watcher(self):
        """Setup file system watcher for configuration changes."""
        self.observer = Observer()
        self.observer.schedule(
            LogConfigWatcher(self), str(self.config_path.parent), recursive=False
        )
        self.observer.start()

    def reload_config(self):
        """Reload configuration from file."""
        try:
            with self.lock:
                with open(self.config_path, "r") as f:
                    new_config = json.load(f)

                if self._validate_config(new_config):
                    old_config = self.config.copy()
                    self.config = new_config
                    self._notify_observers(old_config, new_config)

        except Exception as e:
            # Log error but don't crash
            print(f"Error reloading log config: {e}")

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
            except Exception as e:
                print(f"Error notifying config observer: {e}")

    def get_level_config(self) -> Dict[str, Any]:
        """Get current level configuration."""
        with self.lock:
            return self.config.get("levels", {}).copy()

    def get_filter_config(self) -> Dict[str, Any]:
        """Get current filter configuration."""
        with self.lock:
            return self.config.get("filters", {}).copy()

    def update_component_level(self, component: str, level: str):
        """Update log level for component via API."""
        with self.lock:
            if "levels" not in self.config:
                self.config["levels"] = {}
            if "components" not in self.config["levels"]:
                self.config["levels"]["components"] = {}

            self.config["levels"]["components"][component] = level
            self._save_config()

    def _save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
