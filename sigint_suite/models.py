from __future__ import annotations

"""Typed record models used by scanner functions."""

from typing import Optional
from pydantic import BaseModel


class WifiNetwork(BaseModel):
    """Information about a discovered Wi-Fi network."""

    cell: str
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    frequency: Optional[str] = None
    channel: Optional[str] = None
    quality: Optional[str] = None
    encryption: Optional[str] = None
    vendor: Optional[str] = None


class BandRecord(BaseModel):
    """Cellular band scan result."""

    band: str
    channel: str
    rssi: str


class ImsiRecord(BaseModel):
    """IMSI catcher scan result."""

    imsi: str
    mcc: str
    mnc: str
    rssi: str
    lat: Optional[float] = None
    lon: Optional[float] = None


class BluetoothDevice(BaseModel):
    """Bluetooth device information."""

    address: str
    name: str
    lat: Optional[float] = None
    lon: Optional[float] = None
