"""Wi-Fi scanning API routes."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends

from piwardrive import persistence, service
from piwardrive.models import (
    AccessPoint,
    ErrorResponse,
    WiFiScanRequest,
    WiFiScanResponse,
)
from piwardrive.services import network_fingerprinting, security_analyzer
from piwardrive.services.stream_processor import stream_processor
from piwardrive.sigint_suite.wifi.scanner import async_scan_wifi

router = APIRouter(prefix="/wifi", tags=["wifi"])


@router.get(
    "/scan",
    response_model=WiFiScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_wifi_get(
    interface: str = "wlan0",
    timeout: int | None = None,
    _auth: None = Depends(service._check_auth),
) -> WiFiScanResponse:
    """Perform a Wi-Fi scan and return discovered access points."""
    nets = await async_scan_wifi(interface=interface, timeout=timeout)
    aps = [AccessPoint.model_validate(n.model_dump()) for n in nets]
    timestamp = datetime.utcnow().isoformat()
    pos = service.gps_client.get_position()
    acc = service.get_gps_accuracy()
    fix = service.get_gps_fix_quality()
    lat = lon = None
    if pos:
        lat, lon = pos
        await persistence.save_gps_tracks(
            [
                {
                    "scan_session_id": "adhoc",
                    "timestamp": timestamp,
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
    records = [
        {
            "scan_session_id": "adhoc",
            "detection_timestamp": timestamp,
            "bssid": ap.bssid,
            "ssid": ap.ssid,
            "channel": int(ap.channel) if ap.channel else None,
            "frequency_mhz": int(float(ap.frequency) * 1000) if ap.frequency else None,
            "signal_strength_dbm": None,
            "noise_floor_dbm": None,
            "snr_db": None,
            "encryption_type": ap.encryption,
            "cipher_suite": None,
            "authentication_method": None,
            "wps_enabled": False,
            "vendor_oui": ap.bssid[:8].upper() if ap.bssid else None,
            "vendor_name": ap.vendor,
            "device_type": None,
            "latitude": lat,
            "longitude": lon,
            "altitude_meters": None,
            "accuracy_meters": None,
            "heading_degrees": ap.heading,
            "speed_kmh": None,
            "beacon_interval_ms": None,
            "dtim_period": None,
            "ht_capabilities": None,
            "vht_capabilities": None,
            "he_capabilities": None,
            "country_code": None,
            "regulatory_domain": None,
            "tx_power_dbm": None,
            "load_percentage": None,
            "station_count": None,
            "data_rates": None,
            "first_seen": timestamp,
            "last_seen": timestamp,
            "detection_count": 1,
        }
        for ap in aps
    ]
    await persistence.save_wifi_detections(records)
    await network_fingerprinting.fingerprint_wifi_records(records)
    await security_analyzer.analyze_wifi_records(records)
    stream_processor.publish_wifi(records)
    return WiFiScanResponse(access_points=aps)


@router.post(
    "/scan",
    response_model=WiFiScanResponse,
    responses={401: {"model": ErrorResponse}},
)
async def scan_wifi_post(
    req: WiFiScanRequest,
    _auth: None = Depends(service._check_auth),
) -> WiFiScanResponse:
    """Perform a Wi-Fi scan using parameters in the request body."""
    nets = await async_scan_wifi(interface=req.interface, timeout=req.timeout)
    aps = [AccessPoint.model_validate(n.model_dump()) for n in nets]
    timestamp = datetime.utcnow().isoformat()
    pos = service.gps_client.get_position()
    acc = service.get_gps_accuracy()
    fix = service.get_gps_fix_quality()
    lat = lon = None
    if pos:
        lat, lon = pos
        await persistence.save_gps_tracks(
            [
                {
                    "scan_session_id": "adhoc",
                    "timestamp": timestamp,
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
    records = [
        {
            "scan_session_id": "adhoc",
            "detection_timestamp": timestamp,
            "bssid": ap.bssid,
            "ssid": ap.ssid,
            "channel": int(ap.channel) if ap.channel else None,
            "frequency_mhz": int(float(ap.frequency) * 1000) if ap.frequency else None,
            "signal_strength_dbm": None,
            "noise_floor_dbm": None,
            "snr_db": None,
            "encryption_type": ap.encryption,
            "cipher_suite": None,
            "authentication_method": None,
            "wps_enabled": False,
            "vendor_oui": ap.bssid[:8].upper() if ap.bssid else None,
            "vendor_name": ap.vendor,
            "device_type": None,
            "latitude": lat,
            "longitude": lon,
            "altitude_meters": None,
            "accuracy_meters": None,
            "heading_degrees": ap.heading,
            "speed_kmh": None,
            "beacon_interval_ms": None,
            "dtim_period": None,
            "ht_capabilities": None,
            "vht_capabilities": None,
            "he_capabilities": None,
            "country_code": None,
            "regulatory_domain": None,
            "tx_power_dbm": None,
            "load_percentage": None,
            "station_count": None,
            "data_rates": None,
            "first_seen": timestamp,
            "last_seen": timestamp,
            "detection_count": 1,
        }
        for ap in aps
    ]
    await persistence.save_wifi_detections(records)
    await network_fingerprinting.fingerprint_wifi_records(records)
    await security_analyzer.analyze_wifi_records(records)
    stream_processor.publish_wifi(records)
    return WiFiScanResponse(access_points=aps)
