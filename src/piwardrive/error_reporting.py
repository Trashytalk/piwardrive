import logging

ERROR_PREFIX = "E"


def format_error(code: int, message: str) -> str:
    """Return standardized error string like ``[E001] message``."""
    return f"[{ERROR_PREFIX}{int(code):03d}] {message}"


def report_error(message: str) -> None:
    """Log the error."""
    logging.error(message)


__all__ = ["ERROR_PREFIX", "format_error", "report_error"]
