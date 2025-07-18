from __future__ import annotations

"""Widget management API routes."""

import importlib
from typing import Any, Dict, List, TypedDict

from fastapi import APIRouter

from piwardrive.api.auth import AUTH_DEP
from piwardrive.database_service import db_service
from piwardrive.persistence import DashboardSettings


class WidgetsListResponse(TypedDict):
    widgets: List[str]


class WidgetMetrics(TypedDict):
    count: int
    active: int
    errors: int


class DashboardSettingsResponse(TypedDict):
    layout: List[Dict[str, Any]]
    widgets: List[str]


router = APIRouter()


async def _collect_widget_metrics() -> WidgetMetrics:
    # Import here to avoid circular imports
    from piwardrive.api.system import collect_widget_metrics

    return await collect_widget_metrics()


@router.get("/api/widgets")
async def list_widgets(_auth: Any = AUTH_DEP) -> WidgetsListResponse:
    widgets_mod = importlib.import_module("piwardrive.widgets")
    return {"widgets": list(getattr(widgets_mod, "__all__", []))}


@router.get("/widget-metrics")
async def get_widget_metrics(_auth: Any = AUTH_DEP) -> WidgetMetrics:
    return await _collect_widget_metrics()


@router.get("/plugins")
async def get_plugins(_auth: Any = AUTH_DEP) -> list[str]:
    from piwardrive import widgets

    return list(widgets.list_plugins())


@router.get("/dashboard-settings")
async def get_dashboard_settings_endpoint(
    _auth: Any = AUTH_DEP,
) -> DashboardSettingsResponse:
    settings = await db_service.load_dashboard_settings()
    return {"layout": settings.layout, "widgets": settings.widgets}


@router.post("/dashboard-settings")
async def update_dashboard_settings_endpoint(
    data: dict[str, Any], _auth: Any = AUTH_DEP
) -> DashboardSettingsResponse:
    layout = data.get("layout", [])
    widgets = data.get("widgets", [])
    await db_service.save_dashboard_settings(
        DashboardSettings(layout=layout, widgets=widgets)
    )
    return {"layout": layout, "widgets": widgets}
