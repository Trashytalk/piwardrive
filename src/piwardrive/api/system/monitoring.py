from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

import psutil

from piwardrive import service, vehicle_sensors
from piwardrive.database_service import db_service
from piwardrive.utils import MetricsResult


async def collect_widget_metrics() -> service.WidgetMetrics:
    """Return basic metrics used by dashboard widgets."""
    metrics: MetricsResult = await service.fetch_metrics_async()
    aps = metrics.aps
    handshakes = metrics.handshake_count
    rx, tx = service.get_network_throughput()
    try:
        since = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        suspicious_count = await db_service.count_suspicious_activities(since)
    except Exception:  # pragma: no cover - database errors
        service.logging.debug("suspicious activity count failed", exc_info=True)
        suspicious_count = 0
    batt_percent = batt_plugged = None
    try:
        batt = await asyncio.to_thread(psutil.sensors_battery)
        if batt is not None:
            batt_percent = batt.percent
            batt_plugged = batt.power_plugged
    except Exception:  # pragma: no cover - optional dependency
        service.logging.debug("battery info unavailable", exc_info=True)

    detection_rate = handshakes / max(len(aps), 1)
    threat_level = (
        "high" if suspicious_count > 10 else "medium" if suspicious_count > 0 else "low"
    )
    network_density = len(aps)
    security_score = max(0.0, 100 - suspicious_count * 5)

    return {
        "cpu_temp": service.get_cpu_temp(),
        "bssid_count": len(aps),
        "handshake_count": handshakes,
        "avg_rssi": service.get_avg_rssi(aps),
        "kismet_running": await service.service_status_async("kismet"),
        "bettercap_running": await service.service_status_async("bettercap"),
        "gps_fix": service.get_gps_fix_quality(),
        "rx_kbps": rx,
        "tx_kbps": tx,
        "suspicious_activity_count": suspicious_count,
        "detection_rate": detection_rate,
        "threat_level": threat_level,
        "network_density": network_density,
        "security_score": security_score,
        "battery_percent": batt_percent,
        "battery_plugged": batt_plugged,
        "vehicle_speed": await asyncio.to_thread(vehicle_sensors.read_speed_obd),
        "vehicle_rpm": await asyncio.to_thread(vehicle_sensors.read_rpm_obd),
        "engine_load": await asyncio.to_thread(vehicle_sensors.read_engine_load_obd),
    }
