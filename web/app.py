import asyncio
import base64
import hmac
import os

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from piwardrive.error_middleware import add_error_middleware
from piwardrive.security import verify_password
from piwardrive.service import _collect_widget_metrics
from piwardrive.service import app as api_app
from piwardrive.service import list_widgets

DEF_BUILD_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "webui", "dist")


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """HTTP basic authentication using constant-time credential checks."""

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.user = os.getenv("PW_API_USER", "admin")
        self.pw_hash = os.getenv("PW_API_PASSWORD_HASH")

    async def dispatch(self, request: Request, call_next):
        if self.pw_hash and request.url.path.startswith("/api"):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Basic "):
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
            try:
                creds = base64.b64decode(header[6:]).decode()
                username, password = creds.split(":", 1)
            except Exception:
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
            valid_user = hmac.compare_digest(username, self.user)
            valid_pw = verify_password(password, self.pw_hash)
            if not (valid_user and valid_pw):
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
        return await call_next(request)


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(BasicAuthMiddleware)
    add_error_middleware(app)
    app.mount("/api", api_app)
    app.add_api_route("/api/widgets", list_widgets, methods=["GET"])

    @app.websocket("/ws/updates")
    async def ws_updates(ws: WebSocket) -> None:
        await ws.accept()
        try:
            while True:
                metrics = await _collect_widget_metrics()
                await ws.send_json(metrics)
                await asyncio.sleep(2)
        except WebSocketDisconnect:
            pass

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

    port = int(os.environ.get("PW_WEBUI_PORT", 8000))
    uvicorn.run(create_app(), host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
