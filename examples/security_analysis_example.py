"""Demonstrate running the new detection services."""

import asyncio
from piwardrive.services import security_analyzer, network_fingerprinting


async def main() -> None:
    records = [
        {
            "scan_session_id": "demo",
            "detection_timestamp": "2025-01-01T00:00:00Z",
            "bssid": "AA:BB:CC:DD:EE:FF",
            "ssid": "DemoNet",
            "signal_strength_dbm": -40,
        }
    ]
    await security_analyzer.analyze_wifi_records(records)
    await network_fingerprinting.fingerprint_wifi_records(records)
    print("Analysis complete")


if __name__ == "__main__":
    asyncio.run(main())
