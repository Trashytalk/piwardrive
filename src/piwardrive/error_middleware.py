import logging

"""FastAPI middleware for unified error handling."""

from __future__ import annotations

from logging import Logger
from typing import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .exceptions import PiWardriveError
from .logging.structured_logger import get_logger


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware that converts :class:`PiWardriveError` to JSON responses."""

    def __init__(self, app: ASGIApp, logger: Logger | None = None) -> None:
        super().__init__(app)
        self.logger = logger or get_logger(__name__).logger

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[JSONResponse]]
    ):
        try:
            return await call_next(request)
        except PiWardriveError as exc:
            self.logger.error("PiWardrive error: %s", exc, exc_info=exc)
            return JSONResponse(
                status_code=exc.status_code, content={"detail": str(exc)}
            )
        except Exception:  # noqa: BLE001
            self.logger.exception("Unhandled application error")
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )


def add_error_middleware(app: FastAPI, logger: Logger | None = None) -> None:
    """Attach :class:`ErrorHandlingMiddleware` to ``app``."""
    app.add_middleware(ErrorHandlingMiddleware, logger=logger)


__all__ = ["ErrorHandlingMiddleware", "add_error_middleware"]
