"""Structured logging system for PiWardrive.

Provides JSON-formatted logging with context tracking, distributed tracing
support, and configurable output handlers for the PiWardrive platform.

Features:
- Structured JSON log output
- Request-scoped context tracking
- Distributed tracing support
- Configurable handlers (console, file, queue)
- Fallback serialization for complex objects
- Exception formatting with traceback details
"""

import json
import logging
import os
import socket
import threading
from contextvars import ContextVar
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Dict, Optional

from ..fastjson import dumps


def _get_version() -> str:
    try:
        return version("piwardrive")
    except PackageNotFoundError:
        return "0"


@dataclass
class LogContext:
    """Standard log context structure."""

    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    component: Optional[str] = None
    operation: Optional[str] = None
    instance_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None


# Context variable for request-scoped logging
log_context: ContextVar[LogContext] = ContextVar("log_context", default=LogContext())


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def __init__(self, include_extra: bool = True):
        super().__init__()
        self.include_extra = include_extra
        self.hostname = socket.gethostname()
        self.version = _get_version()

    def _serialize(self, record_dict: Dict[str, Any]) -> str:
        """Serialize the record dictionary to JSON."""
        try:
            return dumps(record_dict)
        except Exception:
            # Fallback to builtin json on serialization failure
            try:
                return json.dumps(record_dict, default=str)
            except Exception:
                return "{}"

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        """Format log record as structured JSON."""
        ctx = log_context.get()
        context_data = asdict(ctx)
        log_data: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": {k: v for k, v in context_data.items() if v is not None},
            "metadata": {
                "hostname": self.hostname,
                "pid": os.getpid(),
                "thread_id": threading.get_ident(),
                "version": self.version,
            },
        }

        if (
            self.include_extra
            and hasattr(record, "extra")
            and isinstance(record.extra, dict)
            and "extra" in record.extra
            and record.extra["extra"]
        ):
            log_data["data"] = record.extra["extra"]

        if record.exc_info and record.exc_info is not True:
            exc_type = record.exc_info[0].__name__ if record.exc_info[0] else ""
            log_data["exception"] = {
                "type": exc_type,
                "message": str(record.exc_info[1]) if record.exc_info[1] else "",
                "traceback": self.formatException(record.exc_info),
            }

        return self._serialize(log_data)


class PiWardriveLogger:
    """Centralized logger for PiWardrive application."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup structured logger with configuration."""
        logger = logging.getLogger(self.name)
        if logger.handlers:
            return logger

        level = self.config.get("level", logging.INFO)
        logger.setLevel(level)

        handler: logging.Handler
        if self.config.get("queue", False):
            from logging.handlers import QueueHandler, QueueListener
            from queue import SimpleQueue

            queue: SimpleQueue[logging.LogRecord] = SimpleQueue()
            handler = QueueHandler(queue)
            listener = QueueListener(queue, *self._create_handlers())
            listener.start()
            logger.addHandler(handler)
        else:
            for h in self._create_handlers():
                logger.addHandler(h)

        logger.propagate = False
        return logger

    def _create_handlers(self) -> list[logging.Handler]:
        handlers: list[logging.Handler] = []
        streams = self.config.get("streams", True)
        log_file = self.config.get("file")
        formatter = StructuredFormatter()

        if streams:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            handlers.append(stream_handler)

        if log_file:
            import os
            from logging.handlers import RotatingFileHandler

            try:
                # Ensure the directory exists
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)

                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=self.config.get("max_bytes", 10_485_760),
                    backupCount=self.config.get("backup_count", 5),
                )
                file_handler.setFormatter(formatter)
                handlers.append(file_handler)
            except (
                OSError,
                PermissionError,
                FileNotFoundError,
                NotADirectoryError,
            ) as e:
                # If file handler creation fails, log a warning and continue with stream handler only
                import warnings

                warnings.warn(
                    f"Failed to create file handler for {log_file}: {e}", UserWarning
                )

        return handlers

    def _log(
        self,
        level: int,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        if not self.logger.isEnabledFor(level):
            return
        record_extra = {"extra": extra} if extra else {}
        self.logger.log(level, message, extra=record_extra, **kwargs)

    def info(
        self, message: str, extra: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None:
        """Log info message with structured data."""
        self._log(logging.INFO, message, extra, **kwargs)

    def error(
        self,
        message: str,
        exc_info: bool = True,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Log error message with exception details."""
        self._log(logging.ERROR, message, extra, exc_info=exc_info, **kwargs)

    def debug(
        self, message: str, extra: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None:
        """Log debug message with structured data."""
        self._log(logging.DEBUG, message, extra, **kwargs)

    def warning(
        self, message: str, extra: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> None:
        """Log warning message with structured data."""
        self._log(logging.WARNING, message, extra, **kwargs)


def set_log_context(**kwargs: Any) -> None:
    """Update the current log context with ``kwargs``."""
    ctx = log_context.get()
    updated = dataclass_replace(ctx, **kwargs)
    log_context.set(updated)


def dataclass_replace(obj: LogContext, **changes: Any) -> LogContext:
    _data = asdict(obj)
    _data.update({k: v for k, v in changes.items() if v is not None})
    return LogContext(**_data)


def get_logger(name: str, **config: Any) -> PiWardriveLogger:
    """Return a :class:`PiWardriveLogger` instance."""
    return PiWardriveLogger(name, config)


__all__ = [
    "LogContext",
    "StructuredFormatter",
    "PiWardriveLogger",
    "set_log_context",
    "get_logger",
]
