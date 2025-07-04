from __future__ import annotations

"""FastAPI application exposing PiWardrive APIs."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from piwardrive.api.analysis_queries import router as analysis_queries_router
from piwardrive.api.analytics import router as analytics_router
from piwardrive.api.analytics_jobs import router as jobs_router
from piwardrive.api.auth import AUTH_DEP, AuthMiddleware
from piwardrive.api.auth import router as auth_router
from piwardrive.api.common import (
    async_scan_lora,
    async_tail_file,
    fetch_metrics_async,
    get_avg_rssi,
    get_cpu_temp,
    get_disk_usage,
    get_gps_accuracy,
    get_gps_fix_quality,
    get_mem_usage,
    get_network_throughput,
    run_service_cmd,
    service_status_async,
)
from piwardrive.api.health import router as health_router
from piwardrive.api.system import collect_widget_metrics as _collect_widget_metrics
from piwardrive.api.system import router as system_router
from piwardrive.api.websockets import router as ws_router
from piwardrive.api.widgets import router as widgets_router
from piwardrive.error_middleware import add_error_middleware
from piwardrive.routes import analytics as analytics_routes
from piwardrive.routes import bluetooth as bluetooth_routes
from piwardrive.routes import cellular as cellular_routes
from piwardrive.routes import security as security_routes
from piwardrive.routes import websocket as websocket_routes
from piwardrive.routes import wifi as wifi_routes

app = FastAPI()

cors_origins = [
    o.strip() for o in os.getenv("PW_CORS_ORIGINS", "").split(",") if o.strip()
]
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(AuthMiddleware)
add_error_middleware(app)


app.include_router(wifi_routes.router)
app.include_router(bluetooth_routes.router)
app.include_router(cellular_routes.router)
app.include_router(analytics_routes.router)
app.include_router(jobs_router)
app.include_router(security_routes.router)
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(widgets_router)
app.include_router(system_router)
app.include_router(analytics_router)
app.include_router(analysis_queries_router)
app.include_router(ws_router)
app.include_router(websocket_routes.router)

__all__ = [
    "app",
    "AUTH_DEP",
    "async_scan_lora",
    "async_tail_file",
    "fetch_metrics_async",
    "get_avg_rssi",
    "get_cpu_temp",
    "get_mem_usage",
    "get_disk_usage",
    "get_network_throughput",
    "get_gps_fix_quality",
    "get_gps_accuracy",
    "service_status_async",
    "run_service_cmd",
    "_collect_widget_metrics",
]
