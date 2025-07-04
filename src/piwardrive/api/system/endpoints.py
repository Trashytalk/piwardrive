from __future__ import annotations

"""System information and configuration routes."""

import inspect
import json
import os
import tempfile
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from piwardrive import service
from piwardrive.database_service import db_service
from piwardrive.exceptions import ServiceError
from piwardrive.security import sanitize_path, verify_password

router = APIRouter()

ALLOWED_LOG_PATHS = service.ALLOWED_LOG_PATHS


@router.get("/cpu")
async def get_cpu(_auth: Any = service.AUTH_DEP) -> service.CPUInfo:
    return {
        "temp": service.get_cpu_temp(),
        "percent": await service.asyncio.to_thread(
            service.psutil.cpu_percent, interval=None
        ),
    }


@router.get("/ram")
async def get_ram(_auth: Any = service.AUTH_DEP) -> service.RAMInfo:
    return {"percent": service.get_mem_usage()}


@router.get("/storage")
async def get_storage(
    path: str = "/mnt/ssd", _auth: Any = service.AUTH_DEP
) -> service.StorageInfo:
    return {"percent": service.get_disk_usage(path)}


@router.get("/orientation")
async def get_orientation_endpoint(
    _auth: Any = service.AUTH_DEP,
) -> service.OrientationInfo:
    orient = await service.asyncio.to_thread(
        service.orientation_sensors.get_orientation_dbus
    )
    angle = None
    accel = gyro = None
    if orient:
        angle = service.orientation_sensors.orientation_to_angle(orient)
    else:
        data = await service.asyncio.to_thread(service.orientation_sensors.read_mpu6050)
        if data:
            accel = data.get("accelerometer")
            gyro = data.get("gyroscope")
    return {
        "orientation": orient,
        "angle": angle,
        "accelerometer": accel,
        "gyroscope": gyro,
    }


@router.get("/vehicle")
async def get_vehicle_endpoint(_auth: Any = service.AUTH_DEP) -> service.VehicleInfo:
    return {
        "speed": await service.asyncio.to_thread(
            service.vehicle_sensors.read_speed_obd
        ),
        "rpm": await service.asyncio.to_thread(service.vehicle_sensors.read_rpm_obd),
        "engine_load": await service.asyncio.to_thread(
            service.vehicle_sensors.read_engine_load_obd
        ),
    }


@router.get("/gps")
async def get_gps_endpoint(_auth: Any = service.AUTH_DEP) -> service.GPSInfo:
    try:
        pos = await service.asyncio.to_thread(service.gps_client.get_position)
    except Exception as exc:
        service.logging.exception("GPS read failed: %s", exc)
        pos = None
    lat = lon = None
    acc = service.get_gps_accuracy()
    fix = service.get_gps_fix_quality()
    if pos:
        lat, lon = pos
        await db_service.save_gps_tracks(
            [
                {
                    "scan_session_id": "adhoc",
                    "timestamp": datetime.utcnow().isoformat(),
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "altitude_meters": None,
                    "accuracy_meters": acc,
                    "heading_degrees": None,
                    "speed_kmh": None,
                    "satellite_count": None,
                    "hdop": None,
                    "vdop": None,
                    "pdop": None,
                    "fix_type": fix,
                }
            ]
        )
    return {"lat": lat, "lon": lon, "accuracy": acc, "fix": fix}


@router.get("/logs")
async def get_logs(
    lines: int = 200,
    path: str = service.DEFAULT_LOG_PATH,
    _auth: Any = service.AUTH_DEP,
) -> service.LogsResponse:
    safe = sanitize_path(path)
    if safe not in ALLOWED_LOG_PATHS:
        raise ServiceError("Invalid log path", status_code=400)
    data = service.async_tail_file(safe, lines)
    if inspect.isawaitable(data):
        lines_out = await data
    else:
        lines_out = data
    return {"path": safe, "lines": lines_out}


@router.get("/db-stats")
async def get_db_stats_endpoint(
    _auth: Any = service.AUTH_DEP,
) -> service.DBStatsResponse:
    counts = await db_service.get_table_counts()
    try:
        size_kb = os.path.getsize(db_service.db_path()) / 1024
    except OSError:
        size_kb = None
    return {"size_kb": size_kb, "tables": counts}


@router.get("/lora-scan")
async def lora_scan_endpoint(
    iface: str = "lora0", _auth: Any = service.AUTH_DEP
) -> service.LoraScanResponse:
    lines = await service.async_scan_lora(iface)
    return {"count": len(lines), "lines": lines}


@router.post("/service/{name}/{action}")
async def control_service_endpoint(
    name: str, action: str, _auth: Any = service.AUTH_DEP
) -> service.ServiceControlResponse:
    if action not in {"start", "stop", "restart"}:
        raise ServiceError("Invalid action", status_code=400)
    result = service.run_service_cmd(name, action) or (False, "", "")
    success, _out, err = result
    if not success:
        msg = err.strip() if isinstance(err, str) else str(err)
        raise ServiceError(msg or "command failed", status_code=500)
    return {"service": name, "action": action, "success": True}


@router.get("/service/{name}")
async def get_service_status_endpoint(
    name: str, _auth: Any = service.AUTH_DEP
) -> service.ServiceStatusResponse:
    active = await service.service_status_async(name)
    return {"service": name, "active": active}


@router.get("/config")
async def get_config_endpoint(_auth: Any = service.AUTH_DEP) -> service.ConfigResponse:
    return asdict(service.config.load_config())


@router.post("/config")
async def update_config_endpoint(
    updates: dict[str, Any], _auth: Any = service.AUTH_DEP
) -> service.ConfigResponse:
    cfg = service.config.load_config()
    data = asdict(cfg)
    for key, value in updates.items():
        if key not in data:
            raise ServiceError(f"Unknown field: {key}", status_code=400)
        data[key] = value
    if data.get("remote_sync_url", "") == "":
        data["remote_sync_url"] = None
    try:
        service.config.validate_config_data(data)
    except Exception as exc:
        raise ServiceError(str(exc), status_code=400)
    service.config.save_config(service.config.Config(**data))
    return data


@router.get("/webhooks")
async def get_webhooks_endpoint(
    _auth: Any = service.AUTH_DEP,
) -> service.WebhooksResponse:
    cfg = service.config.load_config()
    return {"webhooks": list(cfg.notification_webhooks)}


@router.post("/webhooks")
async def update_webhooks_endpoint(
    urls: list[str], _auth: Any = service.AUTH_DEP
) -> service.WebhooksResponse:
    cfg = service.config.load_config()
    cfg.notification_webhooks = list(urls)
    service.config.save_config(cfg)
    return {"webhooks": cfg.notification_webhooks}


@router.get("/fingerprints")
async def list_fingerprints_endpoint(
    _auth: Any = service.AUTH_DEP,
) -> dict[str, list[service.FingerprintInfoDict]]:
    items = await db_service.load_fingerprint_info()
    return {"fingerprints": [asdict(i) for i in items]}


@router.post("/fingerprints")
async def add_fingerprint_endpoint(
    data: dict[str, Any], _auth: Any = service.AUTH_DEP
) -> service.FingerprintInfoDict:
    info = service.FingerprintInfo(
        environment=data.get("environment", ""),
        source=data.get("source", ""),
        record_count=int(data.get("record_count", 0)),
    )
    await db_service.save_fingerprint_info(info)
    return asdict(info)


@router.get("/geofences")
async def list_geofences_endpoint(
    _auth: Any = service.AUTH_DEP,
) -> list[service.Geofence]:
    return service._load_geofences()


@router.post("/geofences")
async def add_geofence_endpoint(
    data: dict[str, Any], _auth: Any = service.AUTH_DEP
) -> list[service.Geofence]:
    polys = service._load_geofences()
    polys.append(
        {
            "name": data.get("name", "geofence"),
            "points": data.get("points", []),
            "enter_message": data.get("enter_message"),
            "exit_message": data.get("exit_message"),
        }
    )
    service._save_geofences(polys)
    return polys


@router.put("/geofences/{name}")
async def update_geofence_endpoint(
    name: str, updates: dict[str, Any], _auth: Any = service.AUTH_DEP
) -> service.Geofence:
    polys = service._load_geofences()
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
            service._save_geofences(polys)
            return poly
    raise ServiceError("Not found", status_code=404)


@router.delete("/geofences/{name}")
async def remove_geofence_endpoint(
    name: str, _auth: Any = service.AUTH_DEP
) -> service.RemoveResponse:
    polys = service._load_geofences()
    for idx, poly in enumerate(polys):
        if poly.get("name") == name:
            polys.pop(idx)
            service._save_geofences(polys)
            return {"removed": True}
    raise ServiceError("Not found", status_code=404)


EXPORT_CONTENT_TYPES = service.EXPORT_CONTENT_TYPES
_make_export_response = service._make_export_response
_export_layer = service._export_layer


@router.get("/export/aps")
async def export_access_points(
    fmt: str = "geojson", _auth: Any = service.AUTH_DEP
) -> Response:
    records = db_service.load_ap_cache()
    if inspect.isawaitable(records):
        records = await records
    try:
        from sigint_integration import load_sigint_data

        records.extend(load_sigint_data("wifi"))
    except Exception:
        service.logging.debug("sigint integration failed", exc_info=True)
    return await _export_layer(records, fmt.lower(), "aps")


@router.get("/export/bt")
async def export_bluetooth(
    fmt: str = "geojson", _auth: Any = service.AUTH_DEP
) -> Response:
    try:
        from sigint_integration import load_sigint_data

        records = load_sigint_data("bluetooth")
    except Exception:
        records = []
    return await _export_layer(records, fmt.lower(), "bt")
