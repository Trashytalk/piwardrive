"""Run the FastAPI service with a bundled web frontend.

This script mounts the compiled React app from ``webui/dist`` and exposes the
API under ``/api``.  It is meant for development and is not part of the main
application entry point.
"""

from __future__ import annotations

import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from piwardrive.service import app as api_app


def create_app() -> FastAPI:
    """Return a FastAPI instance serving both API and static files."""
    app = FastAPI()
    app.mount("/api", api_app)

    dist_dir = os.path.join(
        os.path.dirname(__file__), os.pardir, os.pardir, "webui", "dist"
    )
    if os.path.isdir(dist_dir):
        app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static")
    else:
        raise RuntimeError(
            "webui build not found; run 'npm run build' inside the webui directory"
        )
    return app


def main() -> None:
    uvicorn.run(create_app(), host="0.0.0.0", port=8000)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
