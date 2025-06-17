"""Module logconfig."""
import json
import logging
import os
import sys
from logging import Logger
from typing import Iterable, Optional
from config import CONFIG_DIR

DEFAULT_LOG_PATH = os.path.join(CONFIG_DIR, "app.log")


class JsonFormatter(logging.Formatter):
    """Format log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        """Return the JSON formatted string for ``record``."""
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging(
    log_file: str = DEFAULT_LOG_PATH,
    level: int = logging.INFO,
    *,
    handlers: Optional[Iterable[logging.Handler]] = None,
    stdout: bool = False,
) -> Logger:
    """Configure root logger with JSON output.

    ``PW_LOG_LEVEL`` may override ``level`` with a name like ``DEBUG`` or a
    numeric value. Invalid values are ignored.

    Parameters
    ----------
    log_file:
        Destination file for :class:`logging.FileHandler`.
    level:
        Logging level for the root logger.
    handlers:
        Extra handlers to attach in addition to the file handler.
        If a handler has no formatter, :class:`JsonFormatter` is used.
    stdout:
        When ``True`` also attach a :class:`logging.StreamHandler` writing to
        ``sys.stdout``.
    """
    env_level = os.getenv("PW_LOG_LEVEL")
    if env_level:
        if env_level.isdigit():
            level = int(env_level)
        else:
            level = getattr(logging, env_level.upper(), level)

    logger = logging.getLogger()
    logger.setLevel(level)
    for h in list(logger.handlers):
        logger.removeHandler(h)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JsonFormatter())

    all_handlers: list[logging.Handler] = [file_handler]
    if handlers:
        all_handlers.extend(list(handlers))
    if stdout:
        all_handlers.append(logging.StreamHandler(sys.stdout))

    for h in all_handlers:
        if h.formatter is None:
            h.setFormatter(JsonFormatter())
        logger.addHandler(h)

    return logger
