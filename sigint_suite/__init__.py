"""Common initialization for sigint_suite."""
import logging
import os

_DEBUG_FLAG = "SIGINT_DEBUG"


def _setup_logging() -> None:
    """Configure basic logging based on ``SIGINT_DEBUG``."""
    level = logging.DEBUG if os.getenv(_DEBUG_FLAG) else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


_setup_logging()

