from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from piwardrive.service import app as api_app
from piwardrive.service import list_widgets

DEF_BUILD_DIR = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, "webui", "dist"
)


def create_app() -> FastAPI:
    """Return a FastAPI instance serving API routes and static files."""
    app = FastAPI()
    app.mount("/api", api_app)
    # Expose widget listing without double prefix when mounted
    app.add_api_route("/api/widgets", list_widgets, methods=["GET"])

    dist_dir = os.getenv("PW_WEBUI_DIST", DEF_BUILD_DIR)
    if os.path.isdir(dist_dir):
        app.mount("/", StaticFiles(directory=dist_dir, html=True), name="static")
    else:
        raise RuntimeError(
            "webui build not found; run 'npm run build' inside the webui directory"
        )
    return app


def main() -> None:
    import uvicorn

    # Allow overriding the listening port via the PW_WEBUI_PORT environment
    # variable.  Default to 8000 when not set.
    port = int(os.environ.get("PW_WEBUI_PORT", 8000))

    uvicorn.run(create_app(), host="127.0.0.1", port=port)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
