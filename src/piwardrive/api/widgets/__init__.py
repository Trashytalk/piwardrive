from __future__ import annotations

"""Widget management API routes."""

import importlib
from typing import Any

from fastapi import APIRouter

from piwardrive import service
from piwardrive.database_service import db_service

router = APIRouter()


async def _collect_widget_metrics() -> service.WidgetMetrics:
    return await service._collect_widget_metrics()


@router.get("/api/widgets")
async def list_widgets(_auth: Any = service.AUTH_DEP) -> service.WidgetsListResponse:
    widgets_mod = importlib.import_module("piwardrive.widgets")
    return {"widgets": list(getattr(widgets_mod, "__all__", []))}


@router.get("/widget-metrics")
async def get_widget_metrics(_auth: Any = service.AUTH_DEP) -> service.WidgetMetrics:
    return await _collect_widget_metrics()


@router.get("/plugins")
async def get_plugins(_auth: Any = service.AUTH_DEP) -> list[str]:
    from piwardrive import widgets

    return list(widgets.list_plugins())


@router.get("/dashboard-settings")
async def get_dashboard_settings_endpoint(
    _auth: Any = service.AUTH_DEP,
) -> service.DashboardSettingsResponse:
    settings = await db_service.load_dashboard_settings()
    return {"layout": settings.layout, "widgets": settings.widgets}


@router.post("/dashboard-settings")
async def update_dashboard_settings_endpoint(
    data: dict[str, Any], _auth: Any = service.AUTH_DEP
) -> service.DashboardSettingsResponse:
    layout = data.get("layout", [])
    widgets = data.get("widgets", [])
    await db_service.save_dashboard_settings(
        service.DashboardSettings(layout=layout, widgets=widgets)
    )
    return {"layout": layout, "widgets": widgets}
