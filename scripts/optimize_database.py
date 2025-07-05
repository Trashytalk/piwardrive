#!/usr/bin/env python3
"""
Advanced database optimization and performance enhancement script.
"""

import asyncio
import logging
import os
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseOptimizer:
    """Advanced database optimization and performance enhancement."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def create_advanced_indexes(self):
        """Create advanced performance indexes."""
        logger.info("Creating advanced performance indexes...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Advanced compound indexes for complex queries
        advanced_indexes = [
            # WiFi analysis indexes
            ("idx_wifi_bssid_time_compound", "wifi_detections", "bssid, detection_timestamp DESC"),
            ("idx_wifi_location_signal_compound", "wifi_detections", "latitude, longitude, signal_strength_dbm DESC"),
            ("idx_wifi_ssid_encryption_compound", "wifi_detections", "ssid, encryption_type"),
            ("idx_wifi_vendor_channel_compound", "wifi_detections", "vendor_name, channel"),
            ("idx_wifi_time_channel_compound", "wifi_detections", "detection_timestamp, channel"),
            
            # Bluetooth analysis indexes
            ("idx_bt_manufacturer_time_compound", "bluetooth_detections", "manufacturer_name, detection_timestamp DESC"),
            ("idx_bt_location_rssi_compound", "bluetooth_detections", "latitude, longitude, rssi_dbm DESC"),
            ("idx_bt_device_type_compound", "bluetooth_detections", "device_type, manufacturer_name"),
            
            # Cellular analysis indexes
            ("idx_cellular_network_time_compound", "cellular_detections", "network_name, detection_timestamp DESC"),
            ("idx_cellular_tech_signal_compound", "cellular_detections", "technology, signal_strength_dbm DESC"),
            ("idx_cellular_location_compound", "cellular_detections", "mcc, mnc, lac, cell_id"),
            
            # GPS and location indexes
            ("idx_gps_session_time_compound", "gps_tracks", "scan_session_id, timestamp"),
            ("idx_gps_location_accuracy_compound", "gps_tracks", "latitude, longitude, accuracy_meters"),
            
            # Analytics indexes
            ("idx_analytics_suspicious_date_compound", "network_analytics", "suspicious_score DESC, analysis_date"),
            ("idx_analytics_mobility_compound", "network_analytics", "mobility_score DESC, coverage_radius_meters DESC"),
            
            # Cross-table analysis indexes
            ("idx_suspicious_severity_time_compound", "suspicious_activities", "severity, detected_at DESC"),
            ("idx_suspicious_type_location_compound", "suspicious_activities", "activity_type, latitude, longitude"),
            
            # Materialized view indexes
            ("idx_daily_stats_date_compound", "daily_detection_stats", "detection_date DESC, total_detections DESC"),
            ("idx_coverage_grid_density_compound", "network_coverage_grid", "detection_count DESC, unique_networks DESC")
        ]
        
        created_count = 0
        for index_name, table_name, columns in advanced_indexes:
            try:
                # Check if table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                if not cursor.fetchone():
                    logger.warning(f"Table {table_name} does not exist, skipping index {index_name}")
                    continue
                
                # Check if index already exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index_name,))
                if cursor.fetchone():
                    logger.debug(f"Index {index_name} already exists")
                    continue
                
                # Create index
                create_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({columns})"
                cursor.execute(create_sql)
                created_count += 1
                logger.info(f"Created index: {index_name}")
                
            except Exception as e:
                logger.error(f"Failed to create index {index_name}: {e}")
        
        # Create partial indexes for filtered queries
        partial_indexes = [
            # Only index records with location data
            ("idx_wifi_with_location", "wifi_detections", "latitude, longitude", "latitude IS NOT NULL AND longitude IS NOT NULL"),
            # Only index strong signals
            ("idx_wifi_strong_signals", "wifi_detections", "signal_strength_dbm DESC", "signal_strength_dbm > -70"),
            # Only index open networks
            ("idx_wifi_open_networks", "wifi_detections", "ssid, bssid", "encryption_type = 'OPEN'"),
            # Only index recent detections (last 30 days)
            ("idx_wifi_recent", "wifi_detections", "detection_timestamp DESC", "detection_timestamp > datetime('now', '-30 days')"),
            # Only index high suspicious scores
            ("idx_suspicious_high_risk", "network_analytics", "bssid, suspicious_score", "suspicious_score > 0.7"),
        ]
        
        for index_name, table_name, columns, condition in partial_indexes:
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                if not cursor.fetchone():
                    continue
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (index_name,))
                if cursor.fetchone():
                    continue
                
                create_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({columns}) WHERE {condition}"
                cursor.execute(create_sql)
                created_count += 1
                logger.info(f"Created partial index: {index_name}")
                
            except Exception as e:
                logger.error(f"Failed to create partial index {index_name}: {e}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Created {created_count} advanced indexes")
        return created_count
    
    def optimize_database_settings(self):
        """Optimize database settings for performance."""
        logger.info("Optimizing database settings...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Performance optimizations
        optimizations = [
            ("PRAGMA journal_mode=WAL", "Enable Write-Ahead Logging"),
            ("PRAGMA synchronous=NORMAL", "Optimize synchronization"),
            ("PRAGMA cache_size=50000", "Increase cache size to ~200MB"),
            ("PRAGMA temp_store=MEMORY", "Store temporary tables in memory"),
            ("PRAGMA mmap_size=268435456", "Enable memory mapping (256MB)"),
            ("PRAGMA optimize", "Run optimization"),
        ]
        
        for pragma, description in optimizations:
            try:
                cursor.execute(pragma)
                logger.info(f"Applied: {description}")
            except Exception as e:
                logger.error(f"Failed to apply {pragma}: {e}")
        
        conn.commit()
        conn.close()
    
    def create_analysis_views(self):
        """Create analysis views for common queries."""
        logger.info("Creating analysis views...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Network summary view
        cursor.execute("DROP VIEW IF EXISTS network_summary")
        cursor.execute("""
            CREATE VIEW network_summary AS
            SELECT 
                w.bssid,
                w.ssid,
                w.vendor_name,
                COUNT(*) as total_detections,
                MIN(w.detection_timestamp) as first_seen,
                MAX(w.detection_timestamp) as last_seen,
                AVG(w.signal_strength_dbm) as avg_signal,
                MAX(w.signal_strength_dbm) as max_signal,
                COUNT(DISTINCT w.channel) as channel_count,
                COUNT(DISTINCT w.encryption_type) as encryption_types,
                COUNT(DISTINCT ROUND(w.latitude,4) || ',' || ROUND(w.longitude,4)) as unique_locations,
                COALESCE(nf.classification, 'unknown') as classification,
                COALESCE(na.suspicious_score, 0) as suspicious_score
            FROM wifi_detections w
            LEFT JOIN network_fingerprints nf ON w.bssid = nf.bssid
            LEFT JOIN network_analytics na ON w.bssid = na.bssid
            WHERE w.latitude IS NOT NULL AND w.longitude IS NOT NULL
            GROUP BY w.bssid, w.ssid, w.vendor_name
        """)
        
        # Suspicious activity summary view
        cursor.execute("DROP VIEW IF EXISTS suspicious_summary")
        cursor.execute("""
            CREATE VIEW suspicious_summary AS
            SELECT 
                activity_type,
                severity,
                COUNT(*) as incident_count,
                COUNT(DISTINCT scan_session_id) as affected_sessions,
                MIN(detected_at) as first_incident,
                MAX(detected_at) as latest_incident,
                COUNT(DISTINCT target_bssid) as unique_targets
            FROM suspicious_activities
            WHERE false_positive = 0
            GROUP BY activity_type, severity
            ORDER BY incident_count DESC
        """)
        
        # Location density view
        cursor.execute("DROP VIEW IF EXISTS location_density")
        cursor.execute("""
            CREATE VIEW location_density AS
            SELECT 
                ROUND(latitude, 3) as lat_rounded,
                ROUND(longitude, 3) as lon_rounded,
                COUNT(*) as total_detections,
                COUNT(DISTINCT bssid) as unique_networks,
                AVG(signal_strength_dbm) as avg_signal_strength,
                COUNT(DISTINCT scan_session_id) as scan_sessions
            FROM wifi_detections
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            GROUP BY ROUND(latitude, 3), ROUND(longitude, 3)
            HAVING COUNT(*) > 5
        """)
        
        # Temporal analysis view
        cursor.execute("DROP VIEW IF EXISTS temporal_analysis")
        cursor.execute("""
            CREATE VIEW temporal_analysis AS
            SELECT 
                strftime('%Y-%m-%d', detection_timestamp) as date,
                strftime('%H', detection_timestamp) as hour,
                strftime('%w', detection_timestamp) as day_of_week,
                COUNT(*) as detection_count,
                COUNT(DISTINCT bssid) as unique_networks,
                COUNT(DISTINCT scan_session_id) as scan_sessions,
                AVG(signal_strength_dbm) as avg_signal
            FROM wifi_detections
            GROUP BY strftime('%Y-%m-%d', detection_timestamp), 
                     strftime('%H', detection_timestamp),
                     strftime('%w', detection_timestamp)
        """)
        
        conn.commit()
        conn.close()
        
        logger.info("Created analysis views")
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze database performance."""
        logger.info("Analyzing database performance...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis = {}
        
        # Database size
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        analysis["database_size_mb"] = (page_count * page_size) / (1024 * 1024)
        
        # Table statistics
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        
        table_stats = {}
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = cursor.fetchone()[0]
                table_stats[table] = {"rows": row_count}
            except Exception as e:
                table_stats[table] = {"error": str(e)}
        
        analysis["table_stats"] = table_stats
        
        # Index statistics
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
        analysis["index_count"] = cursor.fetchone()[0]
        
        # Fragmentation
        cursor.execute("PRAGMA freelist_count")
        freelist_count = cursor.fetchone()[0]
        analysis["fragmentation_ratio"] = freelist_count / page_count if page_count > 0 else 0
        
        conn.close()
        
        return analysis
    
    def run_comprehensive_optimization(self) -> Dict[str, Any]:
        """Run comprehensive database optimization."""
        logger.info("Running comprehensive database optimization...")
        
        start_time = time.time()
        results = {
            "started_at": datetime.now().isoformat(),
            "operations": []
        }
        
        # Get baseline performance
        baseline = self.analyze_performance()
        results["baseline_performance"] = baseline
        
        # 1. Optimize database settings
        self.optimize_database_settings()
        results["operations"].append("database_settings_optimized")
        
        # 2. Create advanced indexes
        index_count = self.create_advanced_indexes()
        results["operations"].append(f"created_{index_count}_advanced_indexes")
        
        # 3. Create analysis views
        self.create_analysis_views()
        results["operations"].append("analysis_views_created")
        
        # 4. Run VACUUM and ANALYZE
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        logger.info("Running VACUUM...")
        cursor.execute("VACUUM")
        results["operations"].append("vacuum_completed")
        
        logger.info("Running ANALYZE...")
        cursor.execute("ANALYZE")
        results["operations"].append("analyze_completed")
        
        conn.close()
        
        # Get final performance
        final_performance = self.analyze_performance()
        results["final_performance"] = final_performance
        
        # Calculate improvements
        size_reduction = baseline["database_size_mb"] - final_performance["database_size_mb"]
        fragmentation_improvement = baseline["fragmentation_ratio"] - final_performance["fragmentation_ratio"]
        
        results["improvements"] = {
            "size_reduction_mb": size_reduction,
            "fragmentation_improvement": fragmentation_improvement,
            "new_indexes": index_count
        }
        
        results["completed_at"] = datetime.now().isoformat()
        results["duration_seconds"] = time.time() - start_time
        
        logger.info(f"Optimization completed in {results['duration_seconds']:.2f} seconds")
        
        return results


async def main():
    """Main optimization function."""
    print("=== PiWardrive Advanced Database Optimization ===\n")
    
    # Find database
    db_path = os.path.expanduser("~/.config/piwardrive/app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Please run the database initialization script first.")
        return
    
    print(f"Optimizing database: {db_path}")
    
    optimizer = DatabaseOptimizer(db_path)
    
    # Run comprehensive optimization
    results = optimizer.run_comprehensive_optimization()
    
    print("\n=== Optimization Results ===")
    print(f"Duration: {results['duration_seconds']:.2f} seconds")
    print(f"Operations completed: {len(results['operations'])}")
    
    baseline = results["baseline_performance"]
    final = results["final_performance"]
    improvements = results["improvements"]
    
    print(f"\nDatabase Size: {baseline['database_size_mb']:.2f} MB → {final['database_size_mb']:.2f} MB")
    if improvements["size_reduction_mb"] > 0:
        print(f"  ✅ Space saved: {improvements['size_reduction_mb']:.2f} MB")
    
    print(f"Fragmentation: {baseline['fragmentation_ratio']:.2%} → {final['fragmentation_ratio']:.2%}")
    if improvements["fragmentation_improvement"] > 0:
        print(f"  ✅ Fragmentation reduced by {improvements['fragmentation_improvement']:.2%}")
    
    print(f"Indexes: {baseline['index_count']} → {final['index_count']}")
    if improvements["new_indexes"] > 0:
        print(f"  ✅ Created {improvements['new_indexes']} new indexes")
    
    print(f"\nTable Statistics:")
    for table, stats in final["table_stats"].items():
        if "rows" in stats:
            print(f"  {table}: {stats['rows']:,} rows")
    
    print("\n✅ Database optimization completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
