#!/usr/bin/env python3
"""
Simple test script to validate database improvements.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

print("=== Database Improvements Test ===")

# Test 1: Check if database exists
config_dir = Path.home() / ".config" / "piwardrive"
config_dir.mkdir(parents=True, exist_ok=True)
db_path = config_dir / "app.db"

print(f"Database path: {db_path}")
print(f"Database exists: {db_path.exists()}")

# Test 2: Create basic database schema
try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create basic tables
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wifi_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_session_id TEXT,
            detection_timestamp TIMESTAMP NOT NULL,
            bssid TEXT NOT NULL,
            ssid TEXT,
            channel INTEGER,
            signal_strength_dbm INTEGER,
            encryption_type TEXT,
            latitude REAL,
            longitude REAL,
            vendor_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS suspicious_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_session_id TEXT,
            activity_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            target_bssid TEXT,
            target_ssid TEXT,
            evidence TEXT,
            description TEXT,
            detected_at TIMESTAMP NOT NULL,
            latitude REAL,
            longitude REAL,
            false_positive BOOLEAN DEFAULT FALSE,
            analyst_notes TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS network_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bssid TEXT NOT NULL,
            analysis_date DATE NOT NULL,
            total_detections INTEGER,
            unique_locations INTEGER,
            avg_signal_strength REAL,
            max_signal_strength REAL,
            min_signal_strength REAL,
            signal_variance REAL,
            coverage_radius_meters REAL,
            mobility_score REAL,
            encryption_changes INTEGER,
            ssid_changes INTEGER,
            channel_changes INTEGER,
            suspicious_score REAL,
            last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (bssid, analysis_date)
        )
    """
    )

    conn.commit()
    print("✓ Basic database schema created")

    # Test 3: Create indexes
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_wifi_bssid ON wifi_detections(bssid)",
        "CREATE INDEX IF NOT EXISTS idx_wifi_timestamp ON wifi_detections(detection_timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_wifi_signal ON wifi_detections(signal_strength_dbm)",
        "CREATE INDEX IF NOT EXISTS idx_suspicious_type ON suspicious_activities(activity_type)",
        "CREATE INDEX IF NOT EXISTS idx_analytics_bssid ON network_analytics(bssid)",
        "CREATE INDEX IF NOT EXISTS idx_analytics_date ON network_analytics(analysis_date)",
    ]

    for index_sql in indexes:
        cursor.execute(index_sql)

    conn.commit()
    print("✓ Indexes created")

    # Test 4: Insert sample data
    cursor.execute(
        """
        INSERT OR REPLACE INTO wifi_detections
        (scan_session_id,
            detection_timestamp,
            bssid,
            ssid,
            channel,
            signal_strength_dbm,
            encryption_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "test_session",
            datetime.now().isoformat(),
            "00:11:22:33:44:55",
            "TestNetwork",
            6,
            -45,
            "WPA2",
        ),
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO network_analytics
        (bssid, analysis_date, total_detections, suspicious_score)
        VALUES (?, ?, ?, ?)
    """,
        ("00:11:22:33:44:55", datetime.now().date().isoformat(), 1, 0.1),
    )

    conn.commit()
    print("✓ Sample data inserted")

    # Test 5: Query data
    cursor.execute("SELECT COUNT(*) FROM wifi_detections")
    wifi_count = cursor.fetchone()[0]
    print(f"✓ WiFi detections count: {wifi_count}")

    cursor.execute("SELECT COUNT(*) FROM network_analytics")
    analytics_count = cursor.fetchone()[0]
    print(f"✓ Network analytics count: {analytics_count}")

    cursor.execute("SELECT COUNT(*) FROM suspicious_activities")
    suspicious_count = cursor.fetchone()[0]
    print(f"✓ Suspicious activities count: {suspicious_count}")

    # Test 6: Advanced queries
    cursor.execute(
        """
        SELECT
            DATE(detection_timestamp) as date,
            COUNT(*) as detections,
            COUNT(DISTINCT bssid) as unique_networks
        FROM wifi_detections
        GROUP BY DATE(detection_timestamp)
        ORDER BY date DESC
        LIMIT 5
    """
    )

    daily_stats = cursor.fetchall()
    print(f"✓ Daily statistics query returned {len(daily_stats)} rows")

    conn.close()
    print("✓ Database connection closed")

except Exception as e:
    print(f"✗ Database test failed: {e}")
    sys.exit(1)

print("=== All Database Tests Passed! ===")
