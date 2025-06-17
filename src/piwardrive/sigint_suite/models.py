from __future__ import annotations

"""Typed record models used by scanner functions."""

from typing import Any, Optional


from pydantic import BaseModel, ConfigDict


class RecordBase(BaseModel):
    """Base model supporting dict-style access."""

    model_config = ConfigDict(extra="allow")

    def __getitem__(self, key: str) -> Any:  # pragma: no cover - simple proxy
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:  # pragma: no cover
        setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:  # pragma: no cover
        return getattr(self, key, default)


class WifiNetwork(RecordBase):
    """Information about a discovered Wi-Fi network."""

    cell: str
    ssid: Optional[str] = None
    bssid: Optional[str] = None
    frequency: Optional[str] = None
    channel: Optional[str] = None
    quality: Optional[str] = None
    encryption: Optional[str] = None
    vendor: Optional[str] = None
    heading: Optional[float] = None


class BandRecord(RecordBase):
    """Cellular band scan result."""

    band: str
    channel: str
    rssi: str


class ImsiRecord(RecordBase):
    """IMSI catcher scan result."""

    imsi: str
    mcc: str
    mnc: str
    rssi: str
    lat: Optional[float] = None
    lon: Optional[float] = None


class BluetoothDevice(RecordBase):
    """Bluetooth device information."""

    address: str
    name: str
    lat: Optional[float] = None
    lon: Optional[float] = None
