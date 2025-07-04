from __future__ import annotations

import asyncio
import psutil

from piwardrive import vehicle_sensors
from piwardrive import service
from piwardrive.utils import MetricsResult


async def collect_widget_metrics() -> service.WidgetMetrics:
    """Return basic metrics used by dashboard widgets."""
    metrics: MetricsResult = await service.fetch_metrics_async()
    aps = metrics.aps
    handshakes = metrics.handshake_count
    rx, tx = service.get_network_throughput()
    batt_percent = batt_plugged = None
    try:
        batt = await asyncio.to_thread(psutil.sensors_battery)
        if batt is not None:
            batt_percent = batt.percent
            batt_plugged = batt.power_plugged
    except Exception:  # pragma: no cover - optional dependency
        service.logging.debug("battery info unavailable", exc_info=True)

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
        "battery_percent": batt_percent,
        "battery_plugged": batt_plugged,
        "vehicle_speed": await asyncio.to_thread(vehicle_sensors.read_speed_obd),
        "vehicle_rpm": await asyncio.to_thread(vehicle_sensors.read_rpm_obd),
        "engine_load": await asyncio.to_thread(vehicle_sensors.read_engine_load_obd),
    }
