import json
import logging
import os
from logging import Logger
from .config import CONFIG_DIR

DEFAULT_LOG_PATH = os.path.join(CONFIG_DIR, "app.log")


class JsonFormatter(logging.Formatter):
    """Format log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
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
) -> Logger:
    """Configure root logger with JSON output."""
    logger = logging.getLogger()
    logger.setLevel(level)
    for h in list(logger.handlers):
        logger.removeHandler(h)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    handler = logging.FileHandler(log_file)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    return logger
