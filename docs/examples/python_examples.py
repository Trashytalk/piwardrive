"""Example Python client for the PiWardrive API."""

from __future__ import annotations

import requests

BASE_URL = "http://127.0.0.1:8000"


def scan_wifi(token: str | None = None) -> None:
    """Run a Wi-Fi scan and print access points."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.post(
        f"{BASE_URL}/wifi/scan",
        json={"interface": "wlan0"},
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    for ap in data.get("access_points", []):
        print(ap.get("ssid"), ap.get("bssid"))


if __name__ == "__main__":  # pragma: no cover - manual execution
    scan_wifi()
