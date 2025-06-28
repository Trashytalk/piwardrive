"""Helpers for capturing uncaught exceptions.

This module provides a simple ``install`` function that configures basic
logging for uncaught exceptions.  When used with FastAPI, the handler can be
attached to an application instance to log and return a generic HTTP 500
response.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any

try:  # pragma: no cover - FastAPI is an optional dependency
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except Exception:  # pragma: no cover - allow running without FastAPI
    FastAPI = None  # type: ignore[misc, assignment]
    Request = None  # type: ignore[misc, assignment]
    JSONResponse = None  # type: ignore[misc, assignment]

_installed = False


def _log_exception(exc_type: type[BaseException], exc: BaseException, tb: Any) -> None:
    """Log an uncaught exception."""
    logging.exception("Unhandled exception", exc_info=(exc_type, exc, tb))


def _async_exception_handler(
    loop: asyncio.AbstractEventLoop, context: dict[str, Any]
) -> None:
    """Log unhandled exceptions from asyncio event loops."""
    exc = context.get("exception")
    if exc:
        logging.exception("Unhandled asyncio exception", exc_info=exc)
    else:
        logging.error("Unhandled asyncio exception: %s", context.get("message"))


def install(app: FastAPI | None = None) -> None:
    """Install handlers for uncaught exceptions.

    If ``app`` is provided and FastAPI is available, an exception handler is
    registered that logs the error and responds with ``HTTP 500``.
    """

    global _installed
    if _installed:
        return

    sys.excepthook = _log_exception

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # pragma: no cover - no running loop
        loop = None

    if loop is not None:
        loop.set_exception_handler(_async_exception_handler)

    if app is not None and FastAPI is not None:

        @app.exception_handler(Exception)  # type: ignore[arg-type]
        async def _fastapi_handler(request: Request, exc: Exception):
            logging.exception("Unhandled FastAPI exception", exc_info=exc)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

    _installed = True


__all__ = ["install"]
