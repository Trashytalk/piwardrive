from __future__ import annotations

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .dependencies import check_auth


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing authentication on protected routes."""

    def __init__(self, app: FastAPI, exempt: set[str] | None = None) -> None:
        super().__init__(app)
        self.exempt = exempt or {"/token", "/auth/login", "/auth/logout"}

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.exempt:
            header = request.headers.get("Authorization", "")
            token = header.removeprefix("Bearer ")
            try:
                await check_auth(token)
            except Exception:
                return Response(status_code=401)
        return await call_next(request)
