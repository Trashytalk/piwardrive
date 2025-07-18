#!/usr/bin/env python3
"""
Real-time database monitoring, health alerting, and automated maintenance service.
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from piwardrive.core.persistence import (_get_conn,
                                         analyze_database_performance,
                                         backup_database, cleanup_old_data,
                                         count_suspicious_activities,
                                         load_daily_detection_stats,
                                         vacuum_database,
                                         validate_detection_data)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseMonitoringService:
    """Real-time database monitoring and alerting service."""

    def __init__(self):
        self.alert_thresholds = {
            "database_size_mb": 5000,  # 5GB
            "detection_rate_drop": 0.5,  # 50% drop
            "suspicious_activity_spike": 10,  # 10 in 1 hour
            "query_performance_ms": 1000,  # 1 second
            "disk_usage_percent": 90,
            "validation_errors": 5,
            "backup_age_hours": 48,
        }

        self.maintenance_schedule = {
            "vacuum_hours": 24,
            "backup_hours": 12,
            "cleanup_days": 7,
            "validation_hours": 6,
        }

        self.last_maintenance = {}
        self.alert_history = []

    async def start_monitoring(self, interval_seconds: int = 300):
        """Start continuous monitoring with specified interval."""
        logger.info(
            f"Starting database monitoring with {interval_seconds}s interval..."
        )

        while True:
            try:
                # Run monitoring checks
                await self.run_monitoring_cycle()

                # Check if maintenance is needed
                await self.check_maintenance_schedule()

                # Wait for next cycle
                await asyncio.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Monitoring cycle failed: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

    async def run_monitoring_cycle(self):
        """Run a single monitoring cycle."""
        logger.info("Running monitoring cycle...")

        alerts = []

        try:
            # Database performance monitoring
            performance_alerts = await self.monitor_database_performance()
            alerts.extend(performance_alerts)

            # Data quality monitoring
            quality_alerts = await self.monitor_data_quality()
            alerts.extend(quality_alerts)

            # Activity monitoring
            activity_alerts = await self.monitor_activity_patterns()
            alerts.extend(activity_alerts)

            # Storage monitoring
            storage_alerts = await self.monitor_storage_usage()
            alerts.extend(storage_alerts)

            # Backup monitoring
            backup_alerts = await self.monitor_backup_status()
            alerts.extend(backup_alerts)

            # Process alerts
            if alerts:
                await self.process_alerts(alerts)
                logger.warning(f"Generated {len(alerts)} alerts")
            else:
                logger.info("No alerts generated - system healthy")

        except Exception as e:
            logger.error(f"Monitoring cycle error: {e}")
            alerts.append(
                {
                    "type": "monitoring_error",
                    "severity": "high",
                    "message": f"Monitoring system error: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )
            await self.process_alerts(alerts)

    async def monitor_database_performance(self) -> List[Dict[str, Any]]:
        """Monitor database performance metrics."""
        alerts = []

        try:
            # Get performance analysis
            performance = await analyze_database_performance()

            # Check database size
            size_mb = performance["total_size"] / (1024 * 1024)
            if size_mb > self.alert_thresholds["database_size_mb"]:
                alerts.append(
                    {
                        "type": "database_size",
                        "severity": "medium",
                        "message": f"Database size is {size_mb:.1f} MB (threshold: {self.alert_thresholds['database_size_mb']} MB)",
                        "metrics": {"size_mb": size_mb},
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            # Check for performance recommendations
            if performance["recommendations"]:
                alerts.append(
                    {
                        "type": "performance_recommendations",
                        "severity": "low",
                        "message": f"Performance recommendations available: {len(performance['recommendations'])}",
                        "recommendations": performance["recommendations"],
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            # Test query performance
            start_time = datetime.now()
            async with _get_conn() as conn:
                cursor = await conn.execute("SELECT COUNT(*) FROM wifi_detections")
                await cursor.fetchone()

            query_time_ms = (datetime.now() - start_time).total_seconds() * 1000

            if query_time_ms > self.alert_thresholds["query_performance_ms"]:
                alerts.append(
                    {
                        "type": "slow_query",
                        "severity": "medium",
                        "message": f"Query performance degraded: {query_time_ms:.1f}ms (threshold: {self.alert_thresholds['query_performance_ms']}ms)",
                        "metrics": {"query_time_ms": query_time_ms},
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        except Exception as e:
            alerts.append(
                {
                    "type": "performance_monitoring_error",
                    "severity": "high",
                    "message": f"Failed to monitor database performance: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    async def monitor_data_quality(self) -> List[Dict[str, Any]]:
        """Monitor data quality and integrity."""
        alerts = []

        try:
            # Run data validation
            validation = await validate_detection_data()

            if validation["status"] == "invalid":
                alerts.append(
                    {
                        "type": "data_integrity",
                        "severity": "high",
                        "message": f"Data integrity issues detected: {len(validation['errors'])} errors",
                        "errors": validation["errors"],
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            if validation["status"] == "warning":
                alerts.append(
                    {
                        "type": "data_quality",
                        "severity": "medium",
                        "message": f"Data quality warnings: {len(validation['warnings'])} warnings",
                        "warnings": validation["warnings"],
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            # Check for data validation errors
            error_count = len(validation.get("errors", []))
            if error_count > self.alert_thresholds["validation_errors"]:
                alerts.append(
                    {
                        "type": "validation_errors",
                        "severity": "high",
                        "message": f"Too many validation errors: {error_count} (threshold: {self.alert_thresholds['validation_errors']})",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        except Exception as e:
            alerts.append(
                {
                    "type": "data_quality_monitoring_error",
                    "severity": "high",
                    "message": f"Failed to monitor data quality: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    async def monitor_activity_patterns(self) -> List[Dict[str, Any]]:
        """Monitor activity patterns and detect anomalies."""
        alerts = []

        try:
            # Check detection rate
            current_hour_stats = await load_daily_detection_stats(
                start=(datetime.now() - timedelta(hours=1)).isoformat(), limit=1
            )

            previous_hour_stats = await load_daily_detection_stats(
                start=(datetime.now() - timedelta(hours=2)).isoformat(),
                end=(datetime.now() - timedelta(hours=1)).isoformat(),
                limit=1,
            )

            if current_hour_stats and previous_hour_stats:
                current_rate = current_hour_stats[0].get("total_detections", 0)
                previous_rate = previous_hour_stats[0].get("total_detections", 0)

                if previous_rate > 0:
                    rate_change = (current_rate - previous_rate) / previous_rate

                    if rate_change < -self.alert_thresholds["detection_rate_drop"]:
                        alerts.append(
                            {
                                "type": "detection_rate_drop",
                                "severity": "medium",
                                "message": f"Detection rate dropped by {abs(rate_change)*100:.1f}%",
                                "metrics": {
                                    "current_rate": current_rate,
                                    "previous_rate": previous_rate,
                                    "change_percent": rate_change * 100,
                                },
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

            # Check suspicious activity levels
            suspicious_count = await count_suspicious_activities(
                since=(datetime.now() - timedelta(hours=1)).isoformat()
            )

            if suspicious_count > self.alert_thresholds["suspicious_activity_spike"]:
                alerts.append(
                    {
                        "type": "suspicious_activity_spike",
                        "severity": "high",
                        "message": f"Suspicious activity spike: {suspicious_count} activities in 1 hour",
                        "metrics": {"suspicious_count": suspicious_count},
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        except Exception as e:
            alerts.append(
                {
                    "type": "activity_monitoring_error",
                    "severity": "high",
                    "message": f"Failed to monitor activity patterns: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    async def monitor_storage_usage(self) -> List[Dict[str, Any]]:
        """Monitor storage usage and disk space."""
        alerts = []

        try:
            import shutil

            # Check disk space
            db_path = Path.home() / ".config" / "piwardrive" / "app.db"
            if db_path.exists():
                disk_usage = shutil.disk_usage(db_path.parent)

                usage_percent = (disk_usage.used / disk_usage.total) * 100

                if usage_percent > self.alert_thresholds["disk_usage_percent"]:
                    alerts.append(
                        {
                            "type": "disk_space",
                            "severity": "high",
                            "message": f"Disk usage at {usage_percent:.1f}% (threshold: {self.alert_thresholds['disk_usage_percent']}%)",
                            "metrics": {
                                "usage_percent": usage_percent,
                                "free_gb": disk_usage.free / (1024**3),
                                "total_gb": disk_usage.total / (1024**3),
                            },
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

        except Exception as e:
            alerts.append(
                {
                    "type": "storage_monitoring_error",
                    "severity": "medium",
                    "message": f"Failed to monitor storage usage: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    async def monitor_backup_status(self) -> List[Dict[str, Any]]:
        """Monitor backup status and freshness."""
        alerts = []

        try:
            backup_dir = Path.home() / ".config" / "piwardrive" / "backups"

            if backup_dir.exists():
                backup_files = list(backup_dir.glob("*.db"))

                if not backup_files:
                    alerts.append(
                        {
                            "type": "no_backups",
                            "severity": "high",
                            "message": "No database backups found",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                else:
                    # Find most recent backup
                    latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
                    backup_age = datetime.now() - datetime.fromtimestamp(
                        latest_backup.stat().st_mtime
                    )

                    if (
                        backup_age.total_seconds()
                        > self.alert_thresholds["backup_age_hours"] * 3600
                    ):
                        alerts.append(
                            {
                                "type": "stale_backup",
                                "severity": "medium",
                                "message": f"Latest backup is {backup_age.total_seconds()/3600:.1f} hours old",
                                "metrics": {
                                    "backup_age_hours": backup_age.total_seconds()
                                    / 3600,
                                    "latest_backup": str(latest_backup),
                                },
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

        except Exception as e:
            alerts.append(
                {
                    "type": "backup_monitoring_error",
                    "severity": "medium",
                    "message": f"Failed to monitor backup status: {str(e)}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    async def check_maintenance_schedule(self):
        """Check if scheduled maintenance tasks need to be run."""
        current_time = datetime.now()

        # Check vacuum schedule
        if self._should_run_maintenance(
            "vacuum", self.maintenance_schedule["vacuum_hours"]
        ):
            logger.info("Running scheduled vacuum...")
            try:
                result = await vacuum_database()
                logger.info(
                    f"Vacuum completed: {result['space_reclaimed']} bytes reclaimed"
                )
                self.last_maintenance["vacuum"] = current_time
            except Exception as e:
                logger.error(f"Vacuum failed: {e}")

        # Check backup schedule
        if self._should_run_maintenance(
            "backup", self.maintenance_schedule["backup_hours"]
        ):
            logger.info("Running scheduled backup...")
            try:
                backup_path = (
                    Path.home()
                    / ".config"
                    / "piwardrive"
                    / "backups"
                    / f"backup_{current_time.strftime('%Y%m%d_%H%M%S')}.db"
                )
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                result = await backup_database(str(backup_path))
                if result["status"] == "success":
                    logger.info(f"Backup completed: {backup_path}")
                    self.last_maintenance["backup"] = current_time
                else:
                    logger.error(f"Backup failed: {result['message']}")
            except Exception as e:
                logger.error(f"Backup failed: {e}")

        # Check cleanup schedule
        if self._should_run_maintenance(
            "cleanup", self.maintenance_schedule["cleanup_days"] * 24
        ):
            logger.info("Running scheduled cleanup...")
            try:
                result = await cleanup_old_data(days_to_keep=90)
                total_cleaned = sum(result.values())
                logger.info(f"Cleanup completed: {total_cleaned} records removed")
                self.last_maintenance["cleanup"] = current_time
            except Exception as e:
                logger.error(f"Cleanup failed: {e}")

        # Check validation schedule
        if self._should_run_maintenance(
            "validation", self.maintenance_schedule["validation_hours"]
        ):
            logger.info("Running scheduled validation...")
            try:
                result = await validate_detection_data()
                logger.info(f"Validation completed: {result['status']}")
                self.last_maintenance["validation"] = current_time
            except Exception as e:
                logger.error(f"Validation failed: {e}")

    def _should_run_maintenance(self, task: str, interval_hours: int) -> bool:
        """Check if a maintenance task should be run."""
        if task not in self.last_maintenance:
            return True

        last_run = self.last_maintenance[task]
        hours_since_last = (datetime.now() - last_run).total_seconds() / 3600

        return hours_since_last >= interval_hours

    async def process_alerts(self, alerts: List[Dict[str, Any]]):
        """Process and handle alerts."""
        for alert in alerts:
            # Add to alert history
            self.alert_history.append(alert)

            # Log alert
            severity = alert.get("severity", "medium")
            message = alert.get("message", "Unknown alert")

            if severity == "high":
                logger.error(f"HIGH SEVERITY ALERT: {message}")
            elif severity == "medium":
                logger.warning(f"MEDIUM SEVERITY ALERT: {message}")
            else:
                logger.info(f"LOW SEVERITY ALERT: {message}")

            # Send notifications (implement as needed)
            await self.send_alert_notification(alert)

    async def send_alert_notification(self, alert: Dict[str, Any]):
        """Send alert notification (placeholder for email/webhook notifications)."""
        # This is a placeholder - implement actual notification logic
        logger.info(f"Alert notification: {alert['type']} - {alert['message']}")

    async def get_health_status(self) -> Dict[str, Any]:
        """Get current system health status."""
        try:
            # Get recent performance data
            performance = await analyze_database_performance()

            # Get validation status
            validation = await validate_detection_data()

            # Get recent alerts
            recent_alerts = [
                alert
                for alert in self.alert_history
                if datetime.fromisoformat(alert["timestamp"])
                > datetime.now() - timedelta(hours=24)
            ]

            # Calculate health score
            health_score = 100

            if validation["status"] == "invalid":
                health_score -= 30
            elif validation["status"] == "warning":
                health_score -= 10

            high_severity_alerts = [
                a for a in recent_alerts if a.get("severity") == "high"
            ]
            medium_severity_alerts = [
                a for a in recent_alerts if a.get("severity") == "medium"
            ]

            health_score -= len(high_severity_alerts) * 15
            health_score -= len(medium_severity_alerts) * 5

            health_score = max(0, min(100, health_score))

            return {
                "health_score": health_score,
                "status": (
                    "healthy"
                    if health_score > 80
                    else "warning" if health_score > 60 else "critical"
                ),
                "database_performance": performance,
                "data_validation": validation,
                "recent_alerts": recent_alerts,
                "alert_summary": {
                    "total_24h": len(recent_alerts),
                    "high_severity": len(high_severity_alerts),
                    "medium_severity": len(medium_severity_alerts),
                },
                "last_maintenance": self.last_maintenance,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "health_score": 0,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }


async def main():
    """Main entry point for monitoring service."""
    try:
        logger.info("=== Database Monitoring Service Starting ===")

        service = DatabaseMonitoringService()

        # Get initial health status
        health_status = await service.get_health_status()
        logger.info(f"Initial health score: {health_status['health_score']}")

        # Start monitoring (run a few cycles for demonstration)
        for cycle in range(3):
            logger.info(f"Running monitoring cycle {cycle + 1}...")
            await service.run_monitoring_cycle()
            await service.check_maintenance_schedule()
            await asyncio.sleep(10)  # Short interval for demo

        # Final health status
        final_health = await service.get_health_status()
        logger.info(f"Final health score: {final_health['health_score']}")
        logger.info(f"Status: {final_health['status']}")

        logger.info("=== Database Monitoring Service Completed ===")

    except Exception as e:
        logger.error(f"Monitoring service failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
