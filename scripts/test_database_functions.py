#!/usr/bin/env python3
"""
Test script to validate database functions and populate with sample data.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from piwardrive.core.persistence import (
        analyze_network_behavior,
        compute_network_analytics,
        count_suspicious_activities,
        get_table_counts,
        load_recent_suspicious,
        refresh_daily_detection_stats,
        refresh_network_coverage_grid,
        run_suspicious_activity_detection,
        save_bluetooth_detections,
        save_cellular_detections,
        save_gps_tracks,
        save_network_fingerprints,
        save_scan_session,
        save_suspicious_activities,
        save_wifi_detections,)
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_sample_data():
    """Create sample data to test database functions."""
    logger.info("Creating sample data...")

    # Sample scan session
    session_id = "test-session-001"
    session_data = {
        "id": session_id,"device_id": "test-device-001","scan_type": "wifi","started_at": datetime.now().isoformat(),"completed_at": (datetime.now() + timedelta(minutes=30)).isoformat(),"duration_seconds": 1800,"location_start_lat": 40.7128,"location_start_lon": -74.0060,"location_end_lat": 40.7138,"location_end_lon": -74.0050,"interface_used": "wlan0","scan_parameters": json.dumps({"channels": [1, 6, 11], "scan_time": 30}),"total_detections": 0
    }

    await save_scan_session(session_data)
    logger.info(f"Created scan session: {session_id}")

    # Sample WiFi detections
    wifi_detections = []
    base_time = datetime.now()

    # Regular networks
    for i in range(5):
        wifi_detections.append({
            "scan_session_id": session_id,"detection_timestamp": (base_time + timedelta(minutes=i)).isoformat(),"bssid": f"aa:bb:cc:dd:ee:{i:02x}","ssid": f"TestNetwork{i}","channel": 6 + (i % 3) * 5,"frequency_mhz": 2437 + (i % 3) * 25,"signal_strength_dbm": -50 - (i * 5),"noise_floor_dbm": -95,"snr_db": 45 - (i * 5),"encryption_type": "WPA2-PSK","vendor_oui": "aa:bb:cc","vendor_name": "Test Vendor","latitude": 40.7128 + (i * 0.001),"longitude": -74.0060 + (i * 0.001),"first_seen": (base_time + timedelta(minutes=i)).isoformat(),"last_seen": (base_time + timedelta(minutes=i+10)).isoformat(),"detection_count": 1
        })

    # Evil twin candidate (same SSID, different BSSID)
    wifi_detections.append({
        "scan_session_id": session_id,"detection_timestamp": (base_time + timedelta(minutes=10)).isoformat(),"bssid": "ff:ee:dd:cc:bb:aa","ssid": "TestNetwork0",  # Same as first network
        "channel": 11,"frequency_mhz": 2462,"signal_strength_dbm": -60,"encryption_type": "OPEN",  # Different encryption
        "latitude": 40.7130,"longitude": -74.0058,"first_seen": (base_time + timedelta(minutes=10)).isoformat(),"last_seen": (base_time + timedelta(minutes=20)).isoformat(),"detection_count": 1
    })

    # Hidden SSID
    wifi_detections.append({
        "scan_session_id": session_id,"detection_timestamp": (base_time + timedelta(minutes=15)).isoformat(),"bssid": "12:34:56:78:9a:bc","ssid": "",  # Hidden SSID
        "channel": 1,"frequency_mhz": 2412,"signal_strength_dbm": -70,"encryption_type": "WPA2-PSK","latitude": 40.7125,"longitude": -74.0065,"first_seen": (base_time + timedelta(minutes=15)).isoformat(),"last_seen": (base_time + timedelta(minutes=25)).isoformat(),"detection_count": 1
    })

    await save_wifi_detections(wifi_detections)
    logger.info(f"Created {len(wifi_detections)} WiFi detections")

    # Sample Bluetooth detections
    bluetooth_detections = [
        {
            "scan_session_id": session_id,"detection_timestamp": (base_time + timedelta(minutes=5)).isoformat(),"mac_address": "11:22:33:44:55:66","device_name": "TestPhone","device_type": "smartphone","manufacturer_name": "Test Manufacturer","rssi_dbm": -45,"latitude": 40.7130,"longitude": -74.0055,"first_seen": (base_time + timedelta(minutes=5)).isoformat(),"last_seen": (base_time + timedelta(minutes=15)).isoformat(),"detection_count": 1
        }
    ]

    await save_bluetooth_detections(bluetooth_detections)
    logger.info(f"Created {len(bluetooth_detections)} Bluetooth detections")

    # Sample GPS tracks
    gps_tracks = []
    for i in range(10):
        gps_tracks.append({
            "scan_session_id": session_id,"timestamp": (base_time + timedelta(minutes=i*3)).isoformat(),"latitude": 40.7128 + (i * 0.0001),"longitude": -74.0060 + (i * 0.0001),"altitude_meters": 10.0 + i,"accuracy_meters": 3.0,"speed_kmh": 5.0,"satellite_count": 8
        })

    await save_gps_tracks(gps_tracks)
    logger.info(f"Created {len(gps_tracks)} GPS tracks")

    # Sample network fingerprints
    fingerprints = [
        {
            "bssid": "aa:bb:cc:dd:ee:00","ssid": "TestNetwork0","fingerprint_hash": "abc123def456","confidence_score": 0.9,"device_model": "Test Router Model","classification": "home","risk_level": "low"
        }
    ]

    await save_network_fingerprints(fingerprints)
    logger.info(f"Created {len(fingerprints)} network fingerprints")

    return session_id

async def test_analytics_functions(session_id: str):
    """Test analytics and detection functions."""
    logger.info("Testing analytics functions...")

    # Test suspicious activity detection
    suspicious_count = await run_suspicious_activity_detection(session_id)
    logger.info(f"Detected {suspicious_count} suspicious activities")

    # Test network analytics computation
    await compute_network_analytics()
    logger.info("Computed network analytics")

    # Test materialized view refresh
    await refresh_daily_detection_stats()
    logger.info("Refreshed daily detection stats")

    await refresh_network_coverage_grid()
    logger.info("Refreshed network coverage grid")

    # Test network behavior analysis
    behavior = await analyze_network_behavior("aa:bb:cc:dd:ee:00")
    logger.info(f"Network behavior analysis: mobility={behavior['mobility_score']:.2f},suspicion={behavior['suspicion_score']:.2f}")

    return suspicious_count

async def test_query_functions():
    """Test query functions."""
    logger.info("Testing query functions...")

    # Test table counts
    counts = await get_table_counts()
    logger.info(f"Table counts: {counts}")

    # Test suspicious activity queries
    total_suspicious = await count_suspicious_activities()
    recent_suspicious = await load_recent_suspicious(5)

    logger.info(f"Total suspicious activities: {total_suspicious}")
    logger.info(f"Recent suspicious activities: {len(recent_suspicious)}")

    return counts

async def main():
    """Main test function."""
    print("=== PiWardrive Database Function Tests ===\n")

    try:
        # Create sample data
        session_id = await create_sample_data()

        # Test analytics functions
        suspicious_count = await test_analytics_functions(session_id)

        # Test query functions
        counts = await test_query_functions()

        print("\n=== Test Results ===")
        print(f"✅ Sample data created successfully")
        print(f"✅ Detected {suspicious_count} suspicious activities")
        print(f"✅ Analytics computed successfully")
        print(f"✅ Table counts: {sum(counts.values())} total records")

        # Show some detailed results
        if suspicious_count > 0:
            recent = await load_recent_suspicious(3)
            print(f"\nRecent suspicious activities:")
            for activity in recent:
                print(f"  - {activity['activity_type']}: {activity['description']}")

        print("\n✅ All database functions tested successfully!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
