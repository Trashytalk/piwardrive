from __future__ import annotations

import json
import logging.config
import os
from pathlib import Path
from typing import Dict, Any, Optional


class LoggingConfig:
    """Centralized logging configuration management."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> str:
        return str(Path.home() / ".config" / "piwardrive" / "logging.json")

    def _load_config(self) -> Dict[str, Any]:
        """Load logging configuration from file and environment."""
        base_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "structured": {"()": "piwardrive.logging.structured_logger.StructuredFormatter", "include_extra": True}
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "structured",
                    "level": "INFO",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "/var/log/piwardrive/app.log",
                    "formatter": "structured",
                    "maxBytes": 10_485_760,
                    "backupCount": 5,
                },
            },
            "loggers": {"piwardrive": {"level": "INFO", "handlers": ["console", "file"], "propagate": False}},
        }

        file_config: Dict[str, Any] = {}
        try:
            with open(self.config_path) as f:
                file_config = json.load(f)
        except FileNotFoundError:
            file_config = {}
        except Exception as exc:  # pragma: no cover - configuration may be invalid
            print(f"Failed to load logging config: {exc}")

        env_overrides = self._get_environment_overrides()
        return self._merge_configs(base_config, file_config, env_overrides)

    def _get_environment_overrides(self) -> Dict[str, Any]:
        env_level = os.getenv("PW_LOG_LEVEL")
        if env_level:
            return {"loggers": {"piwardrive": {"level": env_level}}}
        return {}

    def _merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        merged: Dict[str, Any] = {}
        for cfg in configs:
            for key, value in cfg.items():
                if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                    merged[key] = self._merge_configs(merged[key], value)
                else:
                    merged[key] = value
        return merged

    def apply(self) -> None:
        """Apply the loaded configuration using ``logging.config``."""
        logging.config.dictConfig(self.config)


__all__ = ["LoggingConfig"]

