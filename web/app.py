import os
import base64
import asyncio
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from piwardrive.service import app as api_app
from piwardrive.service import list_widgets, _collect_widget_metrics
from piwardrive.security import verify_password

DEF_BUILD_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "webui", "dist")

class BasicAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        pw_hash = os.getenv("PW_API_PASSWORD_HASH")
        if pw_hash and request.url.path.startswith("/api"):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Basic "):
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
            try:
                creds = base64.b64decode(header[6:]).decode()
                password = creds.split(":", 1)[1]
            except Exception:
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
            if not verify_password(password, pw_hash):
                return Response(status_code=401, headers={"WWW-Authenticate": "Basic"})
        return await call_next(request)

def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(BasicAuthMiddleware)
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
