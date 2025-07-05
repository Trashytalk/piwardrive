from __future__ import annotations

from typing import Any

import pytest

from piwardrive import scan_report


@pytest.mark.asyncio
async def test_generate_scan_report() -> None:
    async def fake_load() -> list[dict[str, Any]]:
        return [
            {
                "ssid": "A",
                "encryption": "",
            },
            {"ssid": "B", "encryption": "WPA2"},
            {"ssid": "A", "encryption": None},
        ]

    orig = scan_report.load_ap_cache
    scan_report.load_ap_cache = lambda: fake_load()  # type: ignore
    try:
        report = await scan_report.generate_scan_report()
    finally:
        scan_report.load_ap_cache = orig

    assert report["total_networks"] == 3
    assert report["unique_ssids"] == 2
    assert report["open_networks"] == 2
