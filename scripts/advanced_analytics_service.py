#!/usr/bin/env python3
"""
Advanced analytics service for automated suspicious activity detection,
network behavior analysis, and real-time intelligence.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import math

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from piwardrive.core.persistence import (
    _get_conn,
    save_suspicious_activities,
    load_network_analytics,
    compute_network_analytics,
    save_network_analytics
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedAnalyticsService:
    """Advanced analytics service for automated network intelligence."""
    
    def __init__(self):
        self.suspicious_thresholds = {
            "signal_variance": 40,  # dBm
            "mobility_score": 0.8,  # High mobility
            "encryption_changes": 3,  # Multiple encryption changes
            "ssid_changes": 2,  # Multiple SSID changes
            "channel_changes": 5,  # Excessive channel hopping
            "detection_frequency": 100,  # Too many detections in short time
            "location_distance": 1000,  # meters, impossible travel distance
            "time_window": 300  # seconds, time window for analysis
        }
    
    async def run_comprehensive_analysis(self):
        """Run comprehensive network analysis."""
        logger.info("Starting comprehensive network analysis...")
        
        try:
            # 1. Automated suspicious activity detection
            suspicious_count = await self.detect_suspicious_activities()
            logger.info(f"Detected {suspicious_count} suspicious activities")
            
            # 2. Network behavior pattern analysis
            behavior_analysis = await self.analyze_network_behavior_patterns()
            logger.info(f"Analyzed {len(behavior_analysis)} network behavior patterns")
            
            # 3. Geospatial clustering analysis
            clustering_results = await self.perform_geospatial_clustering()
            logger.info(f"Identified {len(clustering_results)} geospatial clusters")
            
            # 4. Time-series trend analysis
            trend_analysis = await self.analyze_time_series_trends()
            logger.info(f"Analyzed trends for {len(trend_analysis)} networks")
            
            # 5. Device fingerprinting automation
            fingerprint_results = await self.automated_device_fingerprinting()
            logger.info(f"Generated {len(fingerprint_results)} device fingerprints")
            
            # 6. Real-time anomaly detection
            anomaly_results = await self.detect_real_time_anomalies()
            logger.info(f"Detected {len(anomaly_results)} real-time anomalies")
            
            return {
                "suspicious_activities": suspicious_count,
                "behavior_patterns": len(behavior_analysis),
                "geospatial_clusters": len(clustering_results),
                "trend_analysis": len(trend_analysis),
                "device_fingerprints": len(fingerprint_results),
                "real_time_anomalies": len(anomaly_results),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            raise
    
    async def detect_suspicious_activities(self) -> int:
        """Automated suspicious activity detection."""
        logger.info("Running automated suspicious activity detection...")
        
        suspicious_activities = []
        
        async with _get_conn() as conn:
            # Detect rapid signal strength changes (possible spoofing)
            cursor = await conn.execute("""
                SELECT bssid, detection_timestamp, signal_strength_dbm, latitude, longitude
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-1 hour')
                AND signal_strength_dbm IS NOT NULL
                ORDER BY bssid, detection_timestamp
            """)
            
            detections = await cursor.fetchall()
            
            # Group by BSSID and analyze signal patterns
            bssid_detections = {}
            for detection in detections:
                bssid = detection[0]
                if bssid not in bssid_detections:
                    bssid_detections[bssid] = []
                bssid_detections[bssid].append(detection)
            
            for bssid, detections_list in bssid_detections.items():
                if len(detections_list) < 2:
                    continue
                
                # Check for rapid signal changes
                signals = [d[2] for d in detections_list]
                signal_variance = max(signals) - min(signals)
                
                if signal_variance > self.suspicious_thresholds["signal_variance"]:
                    suspicious_activities.append({
                        "scan_session_id": "automated_detection",
                        "activity_type": "signal_spoofing",
                        "severity": "high",
                        "target_bssid": bssid,
                        "evidence": json.dumps({
                            "signal_variance": signal_variance,
                            "detection_count": len(detections_list),
                            "time_span": "1 hour"
                        }),
                        "description": f"Rapid signal strength changes detected: {signal_variance:.1f} dBm variance",
                        "detected_at": datetime.now().isoformat(),
                        "latitude": detections_list[0][3],
                        "longitude": detections_list[0][4],
                        "false_positive": False,
                        "analyst_notes": "Automated detection - requires manual verification"
                    })
                
                # Check for impossible travel speeds
                for i in range(1, len(detections_list)):
                    prev_detection = detections_list[i-1]
                    curr_detection = detections_list[i]
                    
                    if prev_detection[3] and prev_detection[4] and curr_detection[3] and curr_detection[4]:
                        distance = self._calculate_distance(
                            prev_detection[3], prev_detection[4],
                            curr_detection[3], curr_detection[4]
                        )
                        
                        time_diff = (datetime.fromisoformat(curr_detection[1]) - 
                                   datetime.fromisoformat(prev_detection[1])).total_seconds()
                        
                        if time_diff > 0:
                            speed = distance / time_diff  # m/s
                            
                            if speed > 150:  # Impossible speed (>540 km/h)
                                suspicious_activities.append({
                                    "scan_session_id": "automated_detection",
                                    "activity_type": "impossible_mobility",
                                    "severity": "high",
                                    "target_bssid": bssid,
                                    "evidence": json.dumps({
                                        "speed_ms": speed,
                                        "distance_m": distance,
                                        "time_diff_s": time_diff
                                    }),
                                    "description": f"Impossible travel speed: {speed:.1f} m/s",
                                    "detected_at": datetime.now().isoformat(),
                                    "latitude": curr_detection[3],
                                    "longitude": curr_detection[4],
                                    "false_positive": False,
                                    "analyst_notes": "Possible location spoofing or device cloning"
                                })
            
            # Detect suspicious SSIDs
            cursor = await conn.execute("""
                SELECT DISTINCT bssid, ssid, encryption_type, COUNT(*) as freq
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-1 hour')
                AND ssid IS NOT NULL
                GROUP BY bssid, ssid, encryption_type
                HAVING freq > 10
            """)
            
            ssid_detections = await cursor.fetchall()
            
            for detection in ssid_detections:
                bssid, ssid, encryption, frequency = detection
                
                # Check for suspicious SSID patterns
                suspicious_patterns = [
                    "free", "wifi", "internet", "guest", "public", "open",
                    "test", "linksys", "default", "admin", "router", "ap"
                ]
                
                if any(pattern in ssid.lower() for pattern in suspicious_patterns):
                    if encryption == "open" or frequency > 50:
                        suspicious_activities.append({
                            "scan_session_id": "automated_detection",
                            "activity_type": "suspicious_ssid",
                            "severity": "medium",
                            "target_bssid": bssid,
                            "target_ssid": ssid,
                            "evidence": json.dumps({
                                "ssid_pattern": ssid,
                                "encryption": encryption,
                                "frequency": frequency
                            }),
                            "description": f"Suspicious SSID pattern: {ssid}",
                            "detected_at": datetime.now().isoformat(),
                            "false_positive": False,
                            "analyst_notes": "Potential evil twin or honeypot"
                        })
            
            # Detect rogue access points (non-standard vendor behavior)
            cursor = await conn.execute("""
                SELECT bssid, vendor_name, COUNT(DISTINCT channel) as channel_changes,
                       COUNT(DISTINCT encryption_type) as encryption_changes,
                       COUNT(*) as total_detections
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-1 hour')
                GROUP BY bssid, vendor_name
                HAVING channel_changes > 3 OR encryption_changes > 2
            """)
            
            rogue_detections = await cursor.fetchall()
            
            for detection in rogue_detections:
                bssid, vendor, channel_changes, encryption_changes, total = detection
                
                suspicious_activities.append({
                    "scan_session_id": "automated_detection",
                    "activity_type": "rogue_access_point",
                    "severity": "high",
                    "target_bssid": bssid,
                    "evidence": json.dumps({
                        "vendor": vendor,
                        "channel_changes": channel_changes,
                        "encryption_changes": encryption_changes,
                        "total_detections": total
                    }),
                    "description": f"Rogue AP behavior: {channel_changes} channel changes, {encryption_changes} encryption changes",
                    "detected_at": datetime.now().isoformat(),
                    "false_positive": False,
                    "analyst_notes": "Excessive configuration changes indicate potential rogue device"
                })
        
        # Save suspicious activities
        if suspicious_activities:
            await save_suspicious_activities(suspicious_activities)
            logger.info(f"Saved {len(suspicious_activities)} suspicious activities")
        
        return len(suspicious_activities)
    
    async def analyze_network_behavior_patterns(self) -> List[Dict[str, Any]]:
        """Analyze network behavior patterns for each BSSID."""
        logger.info("Analyzing network behavior patterns...")
        
        behavior_patterns = []
        
        async with _get_conn() as conn:
            # Get recent network activity
            cursor = await conn.execute("""
                SELECT bssid, 
                       COUNT(*) as total_detections,
                       COUNT(DISTINCT DATE(detection_timestamp)) as active_days,
                       COUNT(DISTINCT ssid) as ssid_count,
                       COUNT(DISTINCT encryption_type) as encryption_count,
                       COUNT(DISTINCT channel) as channel_count,
                       AVG(signal_strength_dbm) as avg_signal,
                       MIN(signal_strength_dbm) as min_signal,
                       MAX(signal_strength_dbm) as max_signal,
                       COUNT(DISTINCT latitude || ',' || longitude) as location_count
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-7 days')
                GROUP BY bssid
                HAVING total_detections > 5
                ORDER BY total_detections DESC
            """)
            
            networks = await cursor.fetchall()
            
            for network in networks:
                (bssid, total_detections, active_days, ssid_count, encryption_count,
                 channel_count, avg_signal, min_signal, max_signal, location_count) = network
                
                # Calculate behavior metrics
                detection_frequency = total_detections / max(active_days, 1)
                signal_variance = max_signal - min_signal if min_signal and max_signal else 0
                mobility_score = location_count / total_detections if total_detections > 0 else 0
                
                # Behavior classification
                behavior_type = "normal"
                risk_level = "low"
                
                if detection_frequency > 50:
                    behavior_type = "high_frequency"
                    risk_level = "medium"
                
                if ssid_count > 2:
                    behavior_type = "ssid_hopping"
                    risk_level = "high"
                
                if encryption_count > 2:
                    behavior_type = "encryption_changing"
                    risk_level = "high"
                
                if channel_count > 5:
                    behavior_type = "channel_hopping"
                    risk_level = "high"
                
                if mobility_score > 0.5:
                    behavior_type = "highly_mobile"
                    risk_level = "medium"
                
                pattern = {
                    "bssid": bssid,
                    "behavior_type": behavior_type,
                    "risk_level": risk_level,
                    "metrics": {
                        "total_detections": total_detections,
                        "active_days": active_days,
                        "detection_frequency": detection_frequency,
                        "ssid_count": ssid_count,
                        "encryption_count": encryption_count,
                        "channel_count": channel_count,
                        "signal_variance": signal_variance,
                        "mobility_score": mobility_score,
                        "location_count": location_count
                    },
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
                behavior_patterns.append(pattern)
        
        return behavior_patterns
    
    async def perform_geospatial_clustering(self) -> List[Dict[str, Any]]:
        """Perform geospatial clustering of network detections."""
        logger.info("Performing geospatial clustering analysis...")
        
        clusters = []
        
        async with _get_conn() as conn:
            # Get detections with location data
            cursor = await conn.execute("""
                SELECT bssid, latitude, longitude, signal_strength_dbm,
                       COUNT(*) as detection_count
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-24 hours')
                AND latitude IS NOT NULL AND longitude IS NOT NULL
                GROUP BY bssid, 
                         CAST(latitude * 1000 AS INT),
                         CAST(longitude * 1000 AS INT)
                ORDER BY detection_count DESC
            """)
            
            detections = await cursor.fetchall()
            
            # Simple clustering based on location proximity
            processed_detections = set()
            
            for i, detection in enumerate(detections):
                if i in processed_detections:
                    continue
                
                bssid, lat, lon, signal, count = detection
                
                # Find nearby detections
                cluster_detections = [detection]
                cluster_center_lat = lat
                cluster_center_lon = lon
                
                for j, other_detection in enumerate(detections[i+1:], i+1):
                    if j in processed_detections:
                        continue
                    
                    other_bssid, other_lat, other_lon, other_signal, other_count = other_detection
                    
                    # Calculate distance
                    distance = self._calculate_distance(lat, lon, other_lat, other_lon)
                    
                    if distance < 100:  # Within 100 meters
                        cluster_detections.append(other_detection)
                        processed_detections.add(j)
                
                processed_detections.add(i)
                
                # Create cluster if it has multiple networks
                if len(cluster_detections) > 1:
                    cluster = {
                        "cluster_id": f"cluster_{len(clusters) + 1}",
                        "center_latitude": cluster_center_lat,
                        "center_longitude": cluster_center_lon,
                        "network_count": len(cluster_detections),
                        "total_detections": sum(d[4] for d in cluster_detections),
                        "networks": [
                            {
                                "bssid": d[0],
                                "latitude": d[1],
                                "longitude": d[2],
                                "signal_strength": d[3],
                                "detection_count": d[4]
                            }
                            for d in cluster_detections
                        ],
                        "cluster_density": len(cluster_detections) / 0.01,  # networks per 100m²
                        "analysis_timestamp": datetime.now().isoformat()
                    }
                    
                    clusters.append(cluster)
        
        return clusters
    
    async def analyze_time_series_trends(self) -> List[Dict[str, Any]]:
        """Analyze time-series trends for network activity."""
        logger.info("Analyzing time-series trends...")
        
        trends = []
        
        async with _get_conn() as conn:
            # Get hourly detection counts for the last 7 days
            cursor = await conn.execute("""
                SELECT bssid,
                       strftime('%Y-%m-%d %H', detection_timestamp) as hour,
                       COUNT(*) as detection_count,
                       AVG(signal_strength_dbm) as avg_signal
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-7 days')
                GROUP BY bssid, hour
                ORDER BY bssid, hour
            """)
            
            hourly_data = await cursor.fetchall()
            
            # Group by BSSID
            bssid_trends = {}
            for row in hourly_data:
                bssid, hour, count, avg_signal = row
                if bssid not in bssid_trends:
                    bssid_trends[bssid] = []
                bssid_trends[bssid].append({
                    "hour": hour,
                    "detection_count": count,
                    "avg_signal": avg_signal
                })
            
            # Analyze trends for each BSSID
            for bssid, hourly_detections in bssid_trends.items():
                if len(hourly_detections) < 24:  # Need at least 24 hours of data
                    continue
                
                # Calculate trend metrics
                counts = [h["detection_count"] for h in hourly_detections]
                signals = [h["avg_signal"] for h in hourly_detections if h["avg_signal"]]
                
                # Simple trend analysis
                avg_count = sum(counts) / len(counts)
                max_count = max(counts)
                min_count = min(counts)
                
                # Detect patterns
                trend_type = "stable"
                if max_count > avg_count * 3:
                    trend_type = "bursty"
                elif max_count - min_count < avg_count * 0.5:
                    trend_type = "consistent"
                
                # Detect peak hours
                peak_hours = []
                for h in hourly_detections:
                    if h["detection_count"] > avg_count * 1.5:
                        peak_hours.append(h["hour"])
                
                trend = {
                    "bssid": bssid,
                    "trend_type": trend_type,
                    "metrics": {
                        "avg_detections_per_hour": avg_count,
                        "max_detections_per_hour": max_count,
                        "min_detections_per_hour": min_count,
                        "total_hours_analyzed": len(hourly_detections),
                        "peak_hours": peak_hours
                    },
                    "analysis_period": "7 days",
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
                trends.append(trend)
        
        return trends
    
    async def automated_device_fingerprinting(self) -> List[Dict[str, Any]]:
        """Automated device fingerprinting based on network characteristics."""
        logger.info("Performing automated device fingerprinting...")
        
        fingerprints = []
        
        async with _get_conn() as conn:
            # Get network characteristics for fingerprinting
            cursor = await conn.execute("""
                SELECT bssid, 
                       GROUP_CONCAT(DISTINCT ssid) as ssids,
                       GROUP_CONCAT(DISTINCT encryption_type) as encryptions,
                       GROUP_CONCAT(DISTINCT channel) as channels,
                       vendor_name,
                       AVG(signal_strength_dbm) as avg_signal,
                       COUNT(*) as detection_count,
                       MIN(detection_timestamp) as first_seen,
                       MAX(detection_timestamp) as last_seen
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-7 days')
                GROUP BY bssid, vendor_name
                HAVING detection_count > 10
            """)
            
            networks = await cursor.fetchall()
            
            for network in networks:
                (bssid, ssids, encryptions, channels, vendor, avg_signal,
                 detection_count, first_seen, last_seen) = network
                
                # Generate fingerprint characteristics
                characteristics = {
                    "ssid_patterns": ssids.split(',') if ssids else [],
                    "encryption_methods": encryptions.split(',') if encryptions else [],
                    "channel_usage": channels.split(',') if channels else [],
                    "vendor": vendor,
                    "signal_characteristics": {
                        "avg_signal_strength": avg_signal,
                        "detection_frequency": detection_count
                    }
                }
                
                # Device classification based on characteristics
                device_type = "unknown"
                confidence = 0.5
                
                if vendor:
                    if "cisco" in vendor.lower():
                        device_type = "enterprise_ap"
                        confidence = 0.8
                    elif "tp-link" in vendor.lower() or "netgear" in vendor.lower():
                        device_type = "consumer_router"
                        confidence = 0.7
                    elif "apple" in vendor.lower():
                        device_type = "mobile_device"
                        confidence = 0.6
                
                # Check for IoT device patterns
                if ssids and any("iot" in s.lower() or "smart" in s.lower() for s in ssids.split(',')):
                    device_type = "iot_device"
                    confidence = 0.7
                
                # Check for mobile hotspot patterns
                if ssids and any("iphone" in s.lower() or "android" in s.lower() for s in ssids.split(',')):
                    device_type = "mobile_hotspot"
                    confidence = 0.8
                
                fingerprint = {
                    "bssid": bssid,
                    "device_type": device_type,
                    "confidence": confidence,
                    "characteristics": characteristics,
                    "fingerprint_hash": hash(str(characteristics)),
                    "first_seen": first_seen,
                    "last_seen": last_seen,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
                fingerprints.append(fingerprint)
        
        return fingerprints
    
    async def detect_real_time_anomalies(self) -> List[Dict[str, Any]]:
        """Detect real-time anomalies in network behavior."""
        logger.info("Detecting real-time anomalies...")
        
        anomalies = []
        
        async with _get_conn() as conn:
            # Detect sudden spikes in network activity
            cursor = await conn.execute("""
                SELECT strftime('%Y-%m-%d %H:%M', detection_timestamp) as minute,
                       COUNT(*) as detection_count,
                       COUNT(DISTINCT bssid) as unique_networks
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-1 hour')
                GROUP BY minute
                ORDER BY minute
            """)
            
            minute_stats = await cursor.fetchall()
            
            if len(minute_stats) > 10:
                counts = [row[1] for row in minute_stats]
                avg_count = sum(counts) / len(counts)
                
                for minute, count, unique_networks in minute_stats:
                    if count > avg_count * 3:  # Spike detection
                        anomalies.append({
                            "anomaly_type": "detection_spike",
                            "severity": "medium",
                            "timestamp": minute,
                            "metrics": {
                                "detection_count": count,
                                "unique_networks": unique_networks,
                                "baseline_average": avg_count,
                                "spike_ratio": count / avg_count
                            },
                            "description": f"Detection spike: {count} detections vs {avg_count:.1f} average",
                            "detected_at": datetime.now().isoformat()
                        })
            
            # Detect new networks appearing suddenly
            cursor = await conn.execute("""
                SELECT bssid, ssid, MIN(detection_timestamp) as first_seen,
                       COUNT(*) as detection_count
                FROM wifi_detections
                WHERE detection_timestamp > datetime('now', '-1 hour')
                GROUP BY bssid
                HAVING first_seen > datetime('now', '-15 minutes')
                AND detection_count > 5
            """)
            
            new_networks = await cursor.fetchall()
            
            for bssid, ssid, first_seen, detection_count in new_networks:
                anomalies.append({
                    "anomaly_type": "new_network_burst",
                    "severity": "medium",
                    "target_bssid": bssid,
                    "target_ssid": ssid,
                    "metrics": {
                        "first_seen": first_seen,
                        "detection_count": detection_count,
                        "time_window": "15 minutes"
                    },
                    "description": f"New network with high activity: {detection_count} detections",
                    "detected_at": datetime.now().isoformat()
                })
        
        return anomalies
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in meters."""
        R = 6371000  # Earth's radius in meters
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon/2) * math.sin(delta_lon/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c


async def main():
    """Main entry point for advanced analytics service."""
    try:
        logger.info("=== Advanced Analytics Service Starting ===")
        
        service = AdvancedAnalyticsService()
        results = await service.run_comprehensive_analysis()
        
        logger.info("=== Advanced Analytics Results ===")
        logger.info(f"Suspicious Activities: {results['suspicious_activities']}")
        logger.info(f"Behavior Patterns: {results['behavior_patterns']}")
        logger.info(f"Geospatial Clusters: {results['geospatial_clusters']}")
        logger.info(f"Trend Analysis: {results['trend_analysis']}")
        logger.info(f"Device Fingerprints: {results['device_fingerprints']}")
        logger.info(f"Real-time Anomalies: {results['real_time_anomalies']}")
        
        logger.info("=== Advanced Analytics Service Completed ===")
        
    except Exception as e:
        logger.error(f"Advanced analytics service failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
