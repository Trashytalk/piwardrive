import logging

from .config import LoggingConfig
from .structured_logger import (
    LogContext,
    PiWardriveLogger,
    StructuredFormatter,
    get_logger,
    set_log_context,
)


def init_logging(config_path: str | None = None) -> None:
    """Apply logging configuration from ``config_path`` if provided."""
    LoggingConfig(config_path).apply()


__all__ = [
    "LogContext",
    "StructuredFormatter",
    "PiWardriveLogger",
    "LoggingConfig",
    "init_logging",
    "set_log_context",
    "get_logger",
]
