"""Simple FastAPI service for health records."""

from __future__ import annotations

import inspect
import logging
import os
import typing
from collections import defaultdict, deque
from dataclasses import asdict
from http import HTTPStatus
from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware

try:  # pragma: no cover - optional FastAPI dependency
    from fastapi import (
        Body,
        Depends,
        FastAPI,
        HTTPException,
        Request,
        WebSocket,
        WebSocketDisconnect,
    )
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.openapi.utils import get_openapi
    from fastapi.responses import Response  # noqa: E402
    from fastapi.responses import HTMLResponse, StreamingResponse
    from fastapi.security import (
        HTTPBasic,
        HTTPBasicCredentials,
        OAuth2PasswordBearer,
        OAuth2PasswordRequestForm,
    )
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
except Exception:
    FastAPI = type(
        "FastAPI",
        (),
        {
            "get": lambda *a, **k: (lambda f: f),
            "post": lambda *a, **k: (lambda f: f),
            "delete": lambda *a, **k: (lambda f: f),
            "websocket": lambda *a, **k: (lambda f: f),
            "add_middleware": lambda *a, **k: None,
        },
    )

    def _noop(*_a: typing.Any, **_k: typing.Any) -> None:
        return None

    Depends = _noop
    HTTPException = type(
        "HTTPException",
        (Exception,),
        {},
    )
    WebSocket = object
    WebSocketDisconnect = Exception
    Body = _noop
    Request = object
    HTMLResponse = StreamingResponse = Response = object
    Jinja2Templates = lambda *a, **k: None
    StaticFiles = object

    def get_openapi(*_a: typing.Any, **_k: typing.Any) -> dict[str, typing.Any]:
        return {}

    OAuth2PasswordBearer = type(
        "OAuth2PasswordBearer",
        (),
        {"__init__": lambda self, tokenUrl="/token", **k: None},
    )
    OAuth2PasswordRequestForm = type(
        "OAuth2PasswordRequestForm",
        (),
        {"__init__": lambda self, **k: None, "username": "", "password": ""},
    )
    OAuth2PasswordBearer = type(
        "OAuth2PasswordBearer",
        (),
        {"__init__": lambda self, **k: None},
    )
    OAuth2PasswordRequestForm = type(
        "OAuth2PasswordRequestForm",
        (),
        {"__init__": lambda self, **k: None},
    )
    CORSMiddleware = object

if TYPE_CHECKING:  # pragma: no cover - type hints only
    from fastapi import (
        Body,
        Depends,
        FastAPI,
        HTTPException,
        Request,
        WebSocket,
        WebSocketDisconnect,
    )
    from fastapi.responses import Response, StreamingResponse
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from fastapi.security import (
        HTTPBasic,
        HTTPBasicCredentials,
        OAuth2PasswordBearer,
        OAuth2PasswordRequestForm,
    )
    from fastapi.middleware.cors import CORSMiddleware

import asyncio
import functools
import importlib
import json
import secrets
import tempfile
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Tuple

from piwardrive.errors import GeofenceError
from piwardrive.logconfig import DEFAULT_LOG_PATH

try:  # allow tests to stub out ``database_service``
    from database_service import db_service
    from persistence import DashboardSettings, FingerprintInfo, User
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive.database_service import db_service
    from piwardrive.persistence import DashboardSettings, FingerprintInfo, User

from piwardrive.security import hash_secret, sanitize_path, verify_password

try:  # allow tests to provide a simplified utils module
    import utils as _utils
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive import utils as _utils

from typing import Awaitable, Callable

import config
import psutil
import vehicle_sensors

from piwardrive import export, graphql_api, orientation_sensors
from piwardrive.config import CONFIG_DIR
from piwardrive.gpsd_client import client as gps_client
from piwardrive.utils import MetricsResult
from sync import upload_data

try:  # allow tests to stub out lora_scanner
    import lora_scanner as _lora_scanner
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive import lora_scanner as _lora_scanner

try:  # allow tests to stub out analytics
    from analytics.baseline import analyze_health_baseline  # type: ignore
    from analytics.baseline import load_baseline_health
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive.analytics.baseline import (
        analyze_health_baseline,
        load_baseline_health,
    )


logger = logging.getLogger(__name__)

# Common timing defaults
SUBPROCESS_TIMEOUT = 10
WEBSOCKET_SEND_TIMEOUT = 1
STREAM_SLEEP = 2
MIN_EVENT_INTERVAL = 0.01


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add common security headers."""

    def __init__(self, app: FastAPI, csp: str) -> None:
        super().__init__(app)
        self.csp = csp

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", self.csp)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Basic in-memory rate limiting per client IP."""

    def __init__(self, app: FastAPI, max_requests: int, window_seconds: int) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.records: defaultdict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        host = request.client.host if request.client else "anonymous"
        now = time.time()
        q = self.records[host]
        cutoff = now - self.window_seconds
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - q[0]))
            headers = {
                "X-RateLimit-Limit": str(self.max_requests),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(q[0] + self.window_seconds)),
                "X-RateLimit-Window": str(self.window_seconds),
                "Retry-After": str(retry_after),
            }
            return Response("rate limit exceeded", status_code=429, headers=headers)
        q.append(now)
        response = await call_next(request)
        remaining = self.max_requests - len(q)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(q[0] + self.window_seconds))
        response.headers["X-RateLimit-Window"] = str(self.window_seconds)
        return response


# TypedDict definitions for API responses
class TokenResponse(typing.TypedDict):
    """Bearer token response."""

    access_token: str
    token_type: str


class AuthLoginResponse(TokenResponse):
    """Auth token response that includes the user role."""

    role: str


class LogoutResponse(typing.TypedDict):
    """Logout operation result."""

    logout: bool


class HealthRecordDict(typing.TypedDict):
    """Serialized health record."""

    timestamp: str
    cpu_temp: float | None
    cpu_percent: float
    memory_percent: float
    disk_percent: float


class BaselineAnalysisResult(typing.TypedDict):
    """Result of comparing recent metrics to a baseline."""

    recent: dict[str, float]
    baseline: dict[str, float]
    delta: dict[str, float]
    anomalies: list[str]


class WidgetMetrics(typing.TypedDict):
    """Metrics used by dashboard widgets."""

    cpu_temp: float | None
    bssid_count: int
    handshake_count: int
    avg_rssi: float | None
    kismet_running: bool
    bettercap_running: bool
    gps_fix: str | None
    rx_kbps: float
    tx_kbps: float
    battery_percent: float | None
    battery_plugged: bool | None
    vehicle_speed: float | None
    vehicle_rpm: float | None
    engine_load: float | None


class WidgetsListResponse(typing.TypedDict):
    """Response containing available widget names."""

    widgets: list[str]


class CPUInfo(typing.TypedDict):
    """CPU temperature and utilization."""

    temp: float | None
    percent: float


class RAMInfo(typing.TypedDict):
    """Memory utilization."""

    percent: float | None


class StorageInfo(typing.TypedDict):
    """Disk usage percentage."""

    percent: float | None


class OrientationInfo(typing.TypedDict):
    """Orientation and raw sensor data."""

    orientation: str | None
    angle: float | None
    accelerometer: dict[str, float] | None
    gyroscope: dict[str, float] | None


class VehicleInfo(typing.TypedDict):
    """Vehicle sensor readings."""

    speed: float | None
    rpm: float | None
    engine_load: float | None


class GPSInfo(typing.TypedDict):
    """GPS information."""

    lat: float | None
    lon: float | None
    accuracy: float | None
    fix: str | None


class LogsResponse(typing.TypedDict):
    """Log tailing response."""

    path: str
    lines: list[str]


class DBStatsResponse(typing.TypedDict):
    """Database statistics."""

    size_kb: float | None
    tables: dict[str, int]


class LoraScanResponse(typing.TypedDict):
    """LoRa scan results."""

    count: int
    lines: list[str]


class CommandResponse(typing.TypedDict):
    """Result from running a shell command."""

    output: str


class ServiceControlResponse(typing.TypedDict):
    """Response from systemctl wrapper."""

    service: str
    action: str
    success: bool


class ServiceStatusResponse(typing.TypedDict):
    """Service active/inactive state."""

    service: str
    active: bool


class WebhooksResponse(typing.TypedDict):
    """Configured webhook URLs."""

    webhooks: list[str]


class DashboardSettingsResponse(typing.TypedDict):
    """Serialized dashboard layout settings."""

    layout: list[typing.Any]
    widgets: list[str]


class FingerprintInfoDict(typing.TypedDict):
    """Metadata about stored Wi-Fi fingerprints."""

    environment: str
    source: str
    record_count: int
    created_at: str | None


class Geofence(typing.TypedDict, total=False):
    """Polygon used to trigger entry/exit notifications."""

    name: str
    points: list[typing.Any]
    enter_message: str | None
    exit_message: str | None


class RemoveResponse(typing.TypedDict):
    """Result of a delete operation."""

    removed: bool


class SyncResponse(typing.TypedDict):
    """Count of uploaded records."""

    uploaded: int


class ConfigResponse(typing.TypedDict, total=False):
    """Application configuration values."""

    theme: str
    dashboard_layout: list[typing.Any]
    notification_webhooks: list[str]
    remote_sync_url: str | None


def error_json(code: int, message: str | None = None) -> dict[str, str]:
    """Return standardized error dictionary."""
    if message is None:
        try:
            message = HTTPStatus(code).phrase
        except Exception:
            message = str(code)
    return {"code": str(int(code)), "message": message}


async def _default_fetch_metrics_async(*_a: Any, **_k: Any) -> "MetricsResult":
    return _utils.MetricsResult([], [], 0)  # type: ignore[attr-defined]


fetch_metrics_async: Callable[..., Awaitable["MetricsResult"]] = getattr(
    _utils, "fetch_metrics_async", _default_fetch_metrics_async
)
get_avg_rssi = getattr(_utils, "get_avg_rssi", lambda *_a, **_k: None)
get_cpu_temp = getattr(_utils, "get_cpu_temp", lambda *_a, **_k: None)
get_mem_usage = getattr(_utils, "get_mem_usage", lambda *_a, **_k: None)
get_disk_usage = getattr(_utils, "get_disk_usage", lambda *_a, **_k: None)
get_network_throughput = getattr(
    _utils,
    "get_network_throughput",
    lambda *_a, **_k: (0, 0),
)
get_gps_fix_quality = getattr(_utils, "get_gps_fix_quality", lambda *_a, **_k: None)
get_gps_accuracy = getattr(_utils, "get_gps_accuracy", lambda *_a, **_k: None)


async def _default_async_scan_lora(*_a: Any, **_k: Any) -> list[str]:
    return []


async_scan_lora: Callable[[str], Awaitable[list[str]]] = getattr(
    _lora_scanner, "async_scan_lora", _default_async_scan_lora
)


async def _default_service_status_async(*_a: Any, **_k: Any) -> bool:
    return False


service_status_async: Callable[[str], Awaitable[bool]] = getattr(
    _utils, "service_status_async", _default_service_status_async
)

run_service_cmd: Callable[[str, str], Tuple[bool, str, str] | None] = getattr(
    _utils, "run_service_cmd", lambda *_a, **_k: None
)


async def _default_async_tail_file(*_a: Any, **_k: Any) -> list[str]:
    return []


async_tail_file: Callable[[str, int], Awaitable[list[str]]] = getattr(
    _utils, "async_tail_file", _default_async_tail_file
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECURITY_DEP = Depends(oauth2_scheme)
BODY = Body(...)
app = FastAPI()
if config.AppConfig.load().enable_graphql:
    graphql_api.add_graphql_route(app)
cors_origins_env = os.getenv("PW_CORS_ORIGINS", "")
cors_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

csp_header = os.getenv("PW_CONTENT_SECURITY_POLICY", "default-src 'self'")
app.add_middleware(SecurityHeadersMiddleware, csp=csp_header)

rl_requests = int(os.getenv("PIWARDRIVE_RATE_LIMIT_REQUESTS", "100"))
rl_window = int(os.getenv("PIWARDRIVE_RATE_LIMIT_WINDOW", "60"))
if rl_requests > 0:
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=rl_requests,
        window_seconds=rl_window,
    )

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "..", "templates")
)
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_docs(request: Request) -> HTMLResponse:
    """Serve custom Swagger UI."""
    return templates.TemplateResponse("api-docs.html", {"request": request})


def custom_openapi() -> dict[str, typing.Any]:
    """Return customized OpenAPI schema with security settings."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PiWardrive API",
        version="1.0.0",
        description="REST API for Wi-Fi analysis and IoT monitoring",
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {})
    security = components.setdefault("securitySchemes", {})
    security["BearerAuth"] = {"type": "http", "scheme": "bearer"}
    for path in openapi_schema.get("paths", {}).values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

F = typing.TypeVar("F", bound=typing.Callable[..., typing.Any])


def _wrap_route(
    method: typing.Callable[..., typing.Any], *args: typing.Any, **kwargs: typing.Any
) -> typing.Callable[[F], F]:
    return typing.cast(typing.Callable[[F], F], method(*args, **kwargs))


def GET(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable[[F], F]:
    """Wrapper around :func:`FastAPI.get`."""
    return _wrap_route(app.get, *args, **kwargs)


def POST(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable[[F], F]:
    """Wrapper around :func:`FastAPI.post`."""
    return _wrap_route(app.post, *args, **kwargs)


def PUT(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable[[F], F]:
    """Wrapper around :func:`FastAPI.put`."""
    return _wrap_route(app.put, *args, **kwargs)


def DELETE(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable[[F], F]:
    """Wrapper around :func:`FastAPI.delete`."""
    return _wrap_route(app.delete, *args, **kwargs)


def WEBSOCKET(*args: typing.Any, **kwargs: typing.Any) -> typing.Callable[[F], F]:
    """Wrapper around :func:`FastAPI.websocket`."""
    return _wrap_route(app.websocket, *args, **kwargs)


# Include route modules
from piwardrive.routes import wifi as wifi_routes

app.include_router(wifi_routes.router)


# Allowed log file paths for the /logs endpoint
ALLOWED_LOG_PATHS = {
    sanitize_path(p) for p in config.DEFAULT_CONFIG.log_paths + [DEFAULT_LOG_PATH]
}

# In-memory token store mapping token string to username
TOKENS: dict[str, str] = {}

# Path storing polygon geofences
GEOFENCE_FILE = os.path.join(CONFIG_DIR, "geofences.json")


@functools.lru_cache(maxsize=1)
def _load_geofences() -> list[dict[str, Any]]:
    """Return list of saved geofence dictionaries."""
    try:
        with open(GEOFENCE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return data
    except FileNotFoundError:
        return []
    except Exception as exc:
        raise GeofenceError("Failed to load geofences") from exc
    return []


def _save_geofences(polys: list[dict[str, Any]]) -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(GEOFENCE_FILE, "w", encoding="utf-8") as fh:
            json.dump(polys, fh, indent=2)
    except OSError as exc:
        logging.exception("Failed to save geofences: %s", exc)
        raise GeofenceError("Failed to save geofences") from exc
    _load_geofences.cache_clear()


async def _ensure_default_user() -> None:
    """Create default user from environment variables if needed."""
    pw_hash = os.getenv("PW_API_PASSWORD_HASH")
    if not pw_hash:
        return
    username = os.getenv("PW_API_USER", "admin")
    if await db_service.get_user(username) is None:
        await db_service.save_user(User(username=username, password_hash=pw_hash))


async def _check_auth(token: str = SECURITY_DEP) -> None:
    """Validate bearer token."""
    await _ensure_default_user()
    if not token:
        raise HTTPException(status_code=401, detail=error_json(401, "Unauthorized"))
    user = await db_service.get_user_by_token(hash_secret(token))
    if user is None:
        raise HTTPException(status_code=401, detail=error_json(401, "Unauthorized"))


@POST("/token")
async def token_login(
    form: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
) -> TokenResponse:
    """Return bearer token for valid credentials."""
    await _ensure_default_user()
    user = await db_service.get_user(form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail=error_json(401, "Unauthorized"))
    token = secrets.token_urlsafe(32)
    await db_service.update_user_token(user.username, hash_secret(token))
    return {"access_token": token, "token_type": "bearer"}


AUTH_DEP = Depends(_check_auth)


@POST("/auth/login")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
) -> AuthLoginResponse:
    """Validate credentials and return a bearer token."""
    user = await db_service.get_user(form.username)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail=error_json(401, "Unauthorized"))
    token = secrets.token_urlsafe(32)
    TOKENS[token] = user.username
    return {"access_token": token, "token_type": "bearer", "role": user.role}


@POST("/auth/logout")
async def logout(token: str = SECURITY_DEP) -> LogoutResponse:
    """Invalidate the current token."""
    TOKENS.pop(token, None)
    return {"logout": True}


@GET("/status")
async def get_status(
    limit: int = 5, _auth: User | None = AUTH_DEP
) -> list[HealthRecordDict]:
    """Return ``limit`` most recent :class:`HealthRecord` entries."""
    records = db_service.load_recent_health(limit)
    if inspect.isawaitable(records):
        records = await records

    return [asdict(rec) for rec in records]


@GET("/baseline-analysis")
async def baseline_analysis_endpoint(
    limit: int = 10,
    days: int = 30,
    threshold: float = 5.0,
    _auth: None = AUTH_DEP,
) -> BaselineAnalysisResult:
    """Compare recent metrics to historical averages."""
    recent = db_service.load_recent_health(limit)
    if inspect.isawaitable(recent):
        recent = await recent
    baseline = load_baseline_health(days, limit)
    if inspect.isawaitable(baseline):
        baseline = await baseline
    return analyze_health_baseline(recent, baseline, threshold)


async def _collect_widget_metrics() -> WidgetMetrics:
    """Return basic metrics used by dashboard widgets."""
    metrics = await fetch_metrics_async()
    aps = metrics.aps
    handshakes = metrics.handshake_count
    rx, tx = get_network_throughput()
    batt_percent = batt_plugged = None
    try:
        batt = await asyncio.to_thread(psutil.sensors_battery)
        if batt is not None:
            batt_percent = batt.percent
            batt_plugged = batt.power_plugged
    except Exception:  # pragma: no cover - optional dependency
        logging.debug("battery info unavailable", exc_info=True)

    return {
        "cpu_temp": get_cpu_temp(),
        "bssid_count": len(aps),
        "handshake_count": handshakes,
        "avg_rssi": get_avg_rssi(aps),
        "kismet_running": await service_status_async("kismet"),
        "bettercap_running": await service_status_async("bettercap"),
        "gps_fix": get_gps_fix_quality(),
        "rx_kbps": rx,
        "tx_kbps": tx,
        "battery_percent": batt_percent,
        "battery_plugged": batt_plugged,
        "vehicle_speed": await asyncio.to_thread(vehicle_sensors.read_speed_obd),
        "vehicle_rpm": await asyncio.to_thread(vehicle_sensors.read_rpm_obd),
        "engine_load": await asyncio.to_thread(vehicle_sensors.read_engine_load_obd),
    }


@GET("/api/widgets")
async def list_widgets(_auth: User | None = AUTH_DEP) -> WidgetsListResponse:
    """Return available dashboard widget class names."""
    widgets_mod = importlib.import_module("piwardrive.widgets")
    return {"widgets": list(getattr(widgets_mod, "__all__", []))}


@GET("/widget-metrics")
async def get_widget_metrics(_auth: User | None = AUTH_DEP) -> WidgetMetrics:
    """Return basic metrics used by dashboard widgets."""
    return await _collect_widget_metrics()


@GET("/plugins")
async def get_plugins(_auth: User | None = AUTH_DEP) -> list[str]:
    """Return discovered plugin widget class names."""
    from piwardrive import widgets

    return typing.cast(list[str], widgets.list_plugins())


@GET("/cpu")
async def get_cpu(_auth: User | None = AUTH_DEP) -> CPUInfo:
    """Return CPU temperature and usage percentage."""
    return {
        "temp": get_cpu_temp(),
        "percent": await asyncio.to_thread(psutil.cpu_percent, interval=None),
    }


@GET("/ram")
async def get_ram(_auth: User | None = AUTH_DEP) -> RAMInfo:
    """Return system memory usage percentage."""
    return {"percent": get_mem_usage()}


@GET("/storage")
async def get_storage(
    path: str = "/mnt/ssd",
    _auth: User | None = AUTH_DEP,
) -> StorageInfo:
    """Return disk usage percentage for ``path``."""
    return {"percent": get_disk_usage(path)}


@GET("/orientation")
async def get_orientation_endpoint(
    _auth: User | None = AUTH_DEP,
) -> OrientationInfo:
    """Return device orientation and raw sensor data."""
    orient = await asyncio.to_thread(orientation_sensors.get_orientation_dbus)
    angle = None
    accel = gyro = None
    if orient:
        angle = orientation_sensors.orientation_to_angle(orient)
    else:
        data = await asyncio.to_thread(orientation_sensors.read_mpu6050)
        if data:
            accel = data.get("accelerometer")
            gyro = data.get("gyroscope")
    return {
        "orientation": orient,
        "angle": angle,
        "accelerometer": accel,
        "gyroscope": gyro,
    }


@GET("/vehicle")
async def get_vehicle_endpoint(_auth: User | None = AUTH_DEP) -> VehicleInfo:
    """Return vehicle metrics from OBD-II sensors."""
    return {
        "speed": await asyncio.to_thread(vehicle_sensors.read_speed_obd),
        "rpm": await asyncio.to_thread(vehicle_sensors.read_rpm_obd),
        "engine_load": await asyncio.to_thread(vehicle_sensors.read_engine_load_obd),
    }


@GET("/gps")
async def get_gps_endpoint(_auth: User | None = AUTH_DEP) -> GPSInfo:
    """Return current GPS position."""
    pos = await asyncio.to_thread(gps_client.get_position)
    lat = lon = None
    if pos:
        lat, lon = pos
    return {
        "lat": lat,
        "lon": lon,
        "accuracy": get_gps_accuracy(),
        "fix": get_gps_fix_quality(),
    }


@GET("/logs")
async def get_logs(
    lines: int = 200,
    path: str = DEFAULT_LOG_PATH,
    _auth: User | None = AUTH_DEP,
) -> LogsResponse:
    """Return last ``lines`` from ``path``."""
    safe = sanitize_path(path)
    if safe not in ALLOWED_LOG_PATHS:
        raise HTTPException(status_code=400, detail=error_json(400, "Invalid log path"))
    data = async_tail_file(safe, lines)
    if inspect.isawaitable(data):
        lines_out = await data
    else:
        lines_out = data
    return {"path": safe, "lines": lines_out}


@GET("/db-stats")
async def get_db_stats_endpoint(_auth: User | None = AUTH_DEP) -> DBStatsResponse:
    """Return SQLite table counts and database size."""
    counts = await db_service.get_table_counts()
    try:
        size_kb = os.path.getsize(db_service.db_path()) / 1024
    except OSError:
        size_kb = None
    return {"size_kb": size_kb, "tables": counts}


@GET("/lora-scan")
async def lora_scan_endpoint(
    iface: str = "lora0", _auth: User | None = AUTH_DEP
) -> LoraScanResponse:
    """Run ``lora-scan`` on ``iface`` and return output lines."""
    lines = await async_scan_lora(iface)
    return {"count": len(lines), "lines": lines}


@POST("/service/{name}/{action}")
async def control_service_endpoint(
    name: str,
    action: str,
    _auth: User | None = AUTH_DEP,
) -> ServiceControlResponse:
    """Start or stop a systemd service."""
    if action not in {"start", "stop", "restart"}:
        raise HTTPException(status_code=400, detail=error_json(400, "Invalid action"))
    result = run_service_cmd(name, action) or (False, "", "")
    success, _out, err = result
    if not success:
        msg = err.strip() if isinstance(err, str) else str(err)
        raise HTTPException(
            status_code=500, detail=error_json(500, msg or "command failed")
        )
    return {"service": name, "action": action, "success": True}


@GET("/service/{name}")
async def get_service_status_endpoint(
    name: str, _auth: User | None = AUTH_DEP
) -> ServiceStatusResponse:
    """Return whether a ``systemd`` service is active."""
    active = await service_status_async(name)
    return {"service": name, "active": active}


@GET("/config")
async def get_config_endpoint(_auth: User | None = AUTH_DEP) -> ConfigResponse:
    """Return the current configuration from ``config.json``."""
    return asdict(config.load_config())


@POST("/config")
async def update_config_endpoint(
    updates: dict[str, Any] = BODY,
    _auth: User | None = AUTH_DEP,
) -> ConfigResponse:
    """Update configuration values and persist them."""
    cfg = config.load_config()
    data = asdict(cfg)
    for key, value in updates.items():
        if key not in data:
            raise HTTPException(
                status_code=400, detail=error_json(400, f"Unknown field: {key}")
            )
        data[key] = value
    if data.get("remote_sync_url", "") == "":
        data["remote_sync_url"] = None
    try:
        config.validate_config_data(data)
    except Exception as exc:  # pragma: no cover - validation tested separately
        raise HTTPException(status_code=400, detail=error_json(400, str(exc)))
    config.save_config(config.Config(**data))
    return data


@GET("/webhooks")
async def get_webhooks_endpoint(_auth: None = AUTH_DEP) -> WebhooksResponse:
    """Return configured notification webhook URLs."""
    cfg = config.load_config()
    return {"webhooks": list(cfg.notification_webhooks)}


@POST("/webhooks")
async def update_webhooks_endpoint(
    urls: list[str] = BODY, _auth: None = AUTH_DEP
) -> WebhooksResponse:
    """Update notification webhook URL list."""
    cfg = config.load_config()
    cfg.notification_webhooks = list(urls)
    config.save_config(cfg)
    return {"webhooks": cfg.notification_webhooks}


@GET("/dashboard-settings")
async def get_dashboard_settings_endpoint(
    _auth: User | None = AUTH_DEP,
) -> DashboardSettingsResponse:
    """Return persisted dashboard layout and widget list."""
    settings = await db_service.load_dashboard_settings()
    return {"layout": settings.layout, "widgets": settings.widgets}


@POST("/dashboard-settings")
async def update_dashboard_settings_endpoint(
    data: dict[str, Any] = BODY,
    _auth: User | None = AUTH_DEP,
) -> DashboardSettingsResponse:
    """Persist dashboard layout and widget list."""
    layout = data.get("layout", [])
    widgets = data.get("widgets", [])
    await db_service.save_dashboard_settings(
        DashboardSettings(layout=layout, widgets=widgets)
    )
    return {"layout": layout, "widgets": widgets}


@GET("/fingerprints")
async def list_fingerprints_endpoint(
    _auth: None = AUTH_DEP,
) -> dict[str, list[FingerprintInfoDict]]:
    """Return stored fingerprint metadata."""
    items = await db_service.load_fingerprint_info()
    return {"fingerprints": [asdict(i) for i in items]}


@POST("/fingerprints")
async def add_fingerprint_endpoint(
    data: dict[str, Any] = BODY, _auth: None = AUTH_DEP
) -> FingerprintInfoDict:
    """Store fingerprint metadata in the database."""
    info = FingerprintInfo(
        environment=data.get("environment", ""),
        source=data.get("source", ""),
        record_count=int(data.get("record_count", 0)),
    )
    await db_service.save_fingerprint_info(info)
    return asdict(info)


@GET("/geofences")
async def list_geofences_endpoint(
    _auth: User | None = AUTH_DEP,
) -> list[Geofence]:
    """Return saved geofence polygons."""
    return _load_geofences()


@POST("/geofences")
async def add_geofence_endpoint(
    data: dict[str, Any] = BODY, _auth: User | None = AUTH_DEP
) -> list[Geofence]:
    """Add a new polygon to ``geofences.json``."""
    polys = _load_geofences()
    polys.append(
        {
            "name": data.get("name", "geofence"),
            "points": data.get("points", []),
            "enter_message": data.get("enter_message"),
            "exit_message": data.get("exit_message"),
        }
    )
    _save_geofences(polys)
    return polys


@PUT("/geofences/{name}")
async def update_geofence_endpoint(
    name: str,
    updates: dict[str, Any] = BODY,
    _auth: User | None = AUTH_DEP,
) -> Geofence:
    """Modify a saved polygon."""
    polys = _load_geofences()
    for poly in polys:
        if poly.get("name") == name:
            if "name" in updates:
                poly["name"] = updates["name"]
            if "points" in updates:
                poly["points"] = updates["points"]
            if "enter_message" in updates:
                poly["enter_message"] = updates["enter_message"]
            if "exit_message" in updates:
                poly["exit_message"] = updates["exit_message"]
            _save_geofences(polys)
            return poly
    raise HTTPException(status_code=404, detail=error_json(404, "Not found"))


@DELETE("/geofences/{name}")
async def remove_geofence_endpoint(
    name: str, _auth: User | None = AUTH_DEP
) -> RemoveResponse:
    """Delete ``name`` from ``geofences.json``."""
    polys = _load_geofences()
    for idx, poly in enumerate(polys):
        if poly.get("name") == name:
            polys.pop(idx)
            _save_geofences(polys)
            return {"removed": True}
    raise HTTPException(status_code=404, detail=error_json(404, "Not found"))


@POST("/sync")
async def sync_records(limit: int = 100, _auth: User | None = AUTH_DEP) -> SyncResponse:
    """Upload recent health records to the configured sync endpoint."""
    records = db_service.load_recent_health(limit)
    if inspect.isawaitable(records):
        records = await records
    success = await upload_data([asdict(r) for r in records])
    if not success:
        raise HTTPException(status_code=502, detail=error_json(502, "Upload failed"))
    return {"uploaded": len(records)}


EXPORT_CONTENT_TYPES = {
    "csv": "text/csv",
    "json": "application/json",
    "gpx": "application/gpx+xml",
    "kml": "application/vnd.google-earth.kml+xml",
    "geojson": "application/geo+json",
    "shp": "application/octet-stream",
}


def _make_export_response(data: bytes, fmt: str, name: str) -> Response:
    """Return ``Response`` serving ``data`` as ``name.fmt``."""
    return Response(
        content=data,
        media_type=EXPORT_CONTENT_TYPES.get(fmt, "application/octet-stream"),
        headers={"Content-Disposition": f"attachment; filename={name}.{fmt}"},
    )


async def _export_layer(
    records: Sequence[Mapping[str, Any]], fmt: str, name: str
) -> Response:
    """Convert ``records`` to ``fmt`` and return as HTTP response."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        export.export_records(records, tmp.name, fmt)
        tmp.flush()
        path = tmp.name
    data = Path(path).read_bytes()
    os.remove(path)
    return _make_export_response(data, fmt, name)


@GET("/export/aps")
async def export_access_points(
    fmt: str = "geojson", _auth: User | None = AUTH_DEP
) -> Response:
    """Return saved Wi-Fi access points in the specified format."""
    records = db_service.load_ap_cache()
    if inspect.isawaitable(records):
        records = await records
    try:
        from sigint_integration import load_sigint_data

        records.extend(load_sigint_data("wifi"))
    except Exception:
        logging.debug("sigint integration failed", exc_info=True)
    return await _export_layer(records, fmt.lower(), "aps")


@GET("/export/bt")
async def export_bluetooth(
    fmt: str = "geojson", _auth: User | None = AUTH_DEP
) -> Response:
    """Return saved Bluetooth device data in the specified format."""
    try:
        from sigint_integration import load_sigint_data

        records = load_sigint_data("bluetooth")
    except Exception:
        records = []
    return await _export_layer(records, fmt.lower(), "bt")


@WEBSOCKET("/ws/aps")
async def ws_aps(websocket: WebSocket) -> None:
    """Stream new access points over WebSocket."""
    await websocket.accept()
    seq = 0
    last_time = 0.0
    error_count = 0
    try:
        while True:
            start = time.perf_counter()
            records = db_service.load_ap_cache(last_time)
            if inspect.isawaitable(records):
                records = await records
            load_time = time.perf_counter() - start
            new = records
            logger.debug("ws_aps: fetched %d aps in %.6fs", len(new), load_time)
            if new:
                last_time = max(r["last_time"] for r in new)
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "aps": new,
                "load_time": load_time,
                "errors": error_count,
            }
            try:
                await asyncio.wait_for(
                    websocket.send_json(data), timeout=WEBSOCKET_SEND_TIMEOUT
                )
            except (asyncio.TimeoutError, Exception):
                error_count += 1
                await websocket.close()
                break
            seq += 1
            await asyncio.sleep(STREAM_SLEEP)
    except WebSocketDisconnect:
        pass


@GET("/sse/aps")
async def sse_aps(request: Request) -> StreamingResponse:
    """Stream new access points via Server-Sent Events."""

    async def _event_gen() -> typing.AsyncGenerator[str, None]:
        seq = 0
        last_time = 0.0
        error_count = 0
        while True:
            if await request.is_disconnected():
                break
            start = time.perf_counter()
            records = db_service.load_ap_cache(last_time)
            if inspect.isawaitable(records):
                records = await records
            load_time = time.perf_counter() - start
            new = records
            logger.debug("sse_aps: fetched %d aps in %.6fs", len(new), load_time)
            if new:
                last_time = max(r["last_time"] for r in new)
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "aps": new,
                "load_time": load_time,
                "errors": error_count,
            }
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await asyncio.sleep(STREAM_SLEEP)

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )


@WEBSOCKET("/ws/status")
async def ws_status(websocket: WebSocket) -> None:
    """Stream status and widget metrics periodically over WebSocket."""
    await websocket.accept()
    seq = 0
    error_count = 0
    try:
        while True:
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "status": await get_status(),
                "metrics": await _collect_widget_metrics(),
                "errors": error_count,
            }
            try:
                await asyncio.wait_for(
                    websocket.send_json(data), timeout=WEBSOCKET_SEND_TIMEOUT
                )
            except (asyncio.TimeoutError, Exception):
                error_count += 1
                await websocket.close()
                break
            seq += 1
            await asyncio.sleep(STREAM_SLEEP)
    except WebSocketDisconnect:
        pass


@GET("/sse/status")
async def sse_status(request: Request) -> StreamingResponse:
    """Stream status and widget metrics via Server-Sent Events."""

    async def _event_gen() -> typing.AsyncGenerator[str, None]:
        seq = 0
        error_count = 0
        while True:
            if await request.is_disconnected():
                break
            data = {
                "seq": seq,
                "timestamp": time.time(),
                "status": await get_status(),
                "metrics": await _collect_widget_metrics(),
                "errors": error_count,
            }
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await asyncio.sleep(STREAM_SLEEP)

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )


@GET("/sse/history")
async def sse_history(
    request: Request, limit: int = 100, interval: float = 1.0
) -> StreamingResponse:
    """Stream historical health records for playback."""
    records = await db_service.load_health_history()
    if limit:
        records = records[-limit:]

    async def _event_gen() -> typing.AsyncGenerator[str, None]:
        seq = 0
        for rec in records:
            if await request.is_disconnected():
                break
            data = {"seq": seq, "record": asdict(rec)}
            yield f"data: {json.dumps(data)}\n\n"
            seq += 1
            await asyncio.sleep(max(interval, MIN_EVENT_INTERVAL))

    headers = {
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    }
    return StreamingResponse(
        _event_gen(), media_type="text/event-stream", headers=headers
    )


async def main() -> None:
    """Run the FastAPI app using ``uvicorn``."""
    import uvicorn

    port_str = os.getenv("PW_SERVICE_PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        logger.warning("invalid PW_SERVICE_PORT=%r, defaulting to 8000", port_str)
        port = 8000
    config = uvicorn.Config(app, host="127.0.0.1", port=port)
    server = uvicorn.Server(config)
    await server.serve()
    vehicle_sensors.close_obd()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        from utils import shutdown_async_loop

        vehicle_sensors.close_obd()
        shutdown_async_loop()
