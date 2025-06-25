from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from piwardrive.service import app as api_app


DEF_BUILD_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, "webui", "dist"
)


def create_app() -> FastAPI:
    """
    Create and configure a FastAPI application that serves API endpoints under '/api' and static web UI files from a build directory.
    
    Returns:
        FastAPI: The configured FastAPI application instance.
    
    Raises:
        RuntimeError: If the static web UI build directory does not exist.
    """
    app = FastAPI()
    app.mount("/api", api_app)

    dist_dir = os.getenv("PW_WEBUI_DIST", DEF_BUILD_DIR)
    if os.path.isdir(dist_dir):
        app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static")
    else:
        raise RuntimeError(
            "webui build not found; run 'npm run build' inside the webui directory"
        )
    return app


def main() -> None:
    """
    Start the FastAPI web server using Uvicorn on all network interfaces at port 8000.
    """
    import uvicorn

    uvicorn.run(create_app(), host="0.0.0.0", port=8000)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
