"""Pydantic models for PiWardrive API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WiFiScanRequest(BaseModel):
    """Parameters for initiating a Wi-Fi scan."""

    interface: str = Field(
        "wlan0",
        description="Wireless interface used for scanning",
        examples=["wlan0"],
    )
    timeout: int | None = Field(
        None,
        description="Optional timeout in seconds for the scan process",
        examples=[10],
    )

    model_config = ConfigDict(from_attributes=True)


class AccessPoint(BaseModel):
    """Information about a discovered Wi-Fi access point."""

    ssid: str | None = Field(None, description="Network SSID")
    bssid: str | None = Field(None, description="Access point MAC address")
    frequency: str | None = Field(None, description="Frequency in GHz")
    channel: str | None = Field(None, description="Wi-Fi channel")
    quality: str | None = Field(None, description="Signal quality")
    encryption: str | None = Field(None, description="Encryption protocol")
    vendor: str | None = Field(None, description="Vendor based on BSSID prefix")
    heading: float | None = Field(None, description="Heading in degrees at scan time")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "ssid": "ExampleNet",
                "bssid": "AA:BB:CC:DD:EE:FF",
                "frequency": "2.437",
                "channel": "6",
                "quality": "70/100",
                "encryption": "WPA2",
                "vendor": "RaspberryPi",
                "heading": 180.0,
            }
        },
    )


class WiFiScanResponse(BaseModel):
    """Wi-Fi scan result."""

    access_points: list[AccessPoint] = Field(
        default_factory=list,
        description="List of discovered access points",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "access_points": [
                    AccessPoint.model_config["json_schema_extra"]["example"]
                ]
            }
        },
    )


class BluetoothScanRequest(BaseModel):
    """Parameters for initiating a Bluetooth scan."""

    timeout: int | None = Field(
        None,
        description="Optional timeout in seconds for the scan process",
        examples=[10],
    )

    model_config = ConfigDict(from_attributes=True)


class BluetoothDevice(BaseModel):
    """Information about a discovered Bluetooth device."""

    address: str = Field(..., description="Device MAC address")
    name: str | None = Field(None, description="Reported device name")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"address": "AA:BB:CC:DD:EE:FF", "name": "Phone"}
        },
    )


class BluetoothScanResponse(BaseModel):
    """Bluetooth scan result."""

    devices: list[BluetoothDevice] = Field(
        default_factory=list,
        description="List of discovered Bluetooth devices",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "devices": [
                    BluetoothDevice.model_config["json_schema_extra"]["example"]
                ]
            }
        },
    )


class SystemStats(BaseModel):
    """System resource utilization metrics."""

    cpu_percent: float = Field(..., description="CPU usage percentage")
    memory_percent: float = Field(..., description="Memory usage percentage")
    disk_percent: float = Field(..., description="Disk usage percentage")
    temp_celsius: float | None = Field(
        None,
        description="Current CPU temperature in Celsius",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cpu_percent": 12.5,
                "memory_percent": 45.2,
                "disk_percent": 70.1,
                "temp_celsius": 52.3,
            }
        },
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    code: str = Field(..., description="Error code as string", examples=["404"])
    message: str = Field(..., description="Human readable error message")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"code": "404", "message": "Not found"}},
    )


class CellularScanRequest(BaseModel):
    """Parameters for initiating a cellular scan."""

    timeout: int | None = Field(
        None,
        description="Optional timeout in seconds for the scan process",
        examples=[10],
    )

    model_config = ConfigDict(from_attributes=True)


class CellTower(BaseModel):
    """Information about a discovered cellular tower."""

    tower_id: str = Field(..., description="Tower identifier")
    rssi: str | None = Field(None, description="Signal strength")
    lat: float | None = Field(None, description="Latitude")
    lon: float | None = Field(None, description="Longitude")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "tower_id": "12345",
                "rssi": "-60",
                "lat": 51.5,
                "lon": -0.1,
            }
        },
    )


class CellularScanResponse(BaseModel):
    """Cellular scan result."""

    towers: list[CellTower] = Field(
        default_factory=list,
        description="List of discovered cell towers",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "towers": [CellTower.model_config["json_schema_extra"]["example"]]
            }
        },
    )


class BluetoothDetection(BaseModel):
    """Row in ``bluetooth_detections`` table."""

    id: int | None = Field(None, description="Row ID")
    scan_session_id: str = Field(..., description="Scan session ID")
    detection_timestamp: str = Field(..., description="Timestamp ISO format")
    mac_address: str = Field(..., description="Device MAC address")
    device_name: str | None = Field(None, description="Bluetooth name")
    rssi_dbm: int | None = Field(None, description="Signal strength")
    latitude: float | None = Field(None, description="Latitude")
    longitude: float | None = Field(None, description="Longitude")

    model_config = ConfigDict(from_attributes=True)


class CellularDetection(BaseModel):
    """Row in ``cellular_detections`` table."""

    id: int | None = Field(None, description="Row ID")
    scan_session_id: str = Field(..., description="Scan session ID")
    detection_timestamp: str = Field(..., description="Timestamp ISO format")
    cell_id: int | None = Field(None, description="Cell ID")
    lac: int | None = Field(None, description="Location area code")
    mcc: int | None = Field(None, description="Mobile country code")
    mnc: int | None = Field(None, description="Mobile network code")
    signal_strength_dbm: int | None = Field(None, description="Signal strength")
    latitude: float | None = Field(None, description="Latitude")
    longitude: float | None = Field(None, description="Longitude")

    model_config = ConfigDict(from_attributes=True)


class NetworkFingerprint(BaseModel):
    """Fingerprint entry for a Wi-Fi network."""

    id: int | None = Field(None, description="Row ID")
    bssid: str = Field(..., description="BSSID")
    fingerprint_hash: str = Field(..., description="Fingerprint hash")
    classification: str | None = Field(None, description="Classification")
    risk_level: str | None = Field(None, description="Risk level")
    tags: str | None = Field(None, description="Tags JSON")
    created_at: str | None = Field(None, description="Creation time")

    model_config = ConfigDict(from_attributes=True)


class SuspiciousActivity(BaseModel):
    """Recorded suspicious network activity."""

    id: int | None = Field(None, description="Row ID")
    scan_session_id: str = Field(..., description="Scan session ID")
    activity_type: str = Field(..., description="Type of activity")
    severity: str = Field(..., description="Severity level")
    description: str | None = Field(None, description="Description")
    detected_at: str = Field(..., description="Timestamp ISO format")
    latitude: float | None = Field(None, description="Latitude")
    longitude: float | None = Field(None, description="Longitude")
    analyst_notes: str | None = Field(None, description="Analyst notes")

    model_config = ConfigDict(from_attributes=True)


class NetworkAnalyticsRecord(BaseModel):
    """Daily analytics metrics for a BSSID."""

    bssid: str = Field(..., description="BSSID")
    analysis_date: str = Field(..., description="Date")
    total_detections: int | None = Field(None, description="Number of detections")
    suspicious_score: float | None = Field(None, description="Suspicious score")

    model_config = ConfigDict(from_attributes=True)
