#!/usr/bin/env python3
"""
Performance Monitor for PiWardrive

This script provides continuous performance monitoring with alerting capabilities.
"""

import asyncio
import json
import logging
import os
import smtplib
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime
from email.mime.multipart import MimeMultipart
from email.mime.text import MimeText
from typing import Any, Dict, List, Optional

import aiohttp
import psutil
import requests


@dataclass
class PerformanceMetric:
    """Performance metric data structure."""

    name: str
    value: float
    unit: str
    timestamp: float
    threshold: Optional[float] = None
    category: str = "general"
    tags: Dict[str, str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}


@dataclass
class AlertConfig:
    """Alert configuration."""

    metric_name: str
    threshold: float
    operator: str  # '>', '<', '>=', '<=', '==', '!='
    severity: str  # 'info', 'warning', 'critical'
    cooldown_minutes: int = 5
    enabled: bool = True


class PerformanceMonitor:
    """Main performance monitoring class."""

    def __init__(self, config_file: str = "performance_config.json"):
        self.config = self._load_config(config_file)
        self.database_path = self.config.get("database_path", "performance_metrics.db")
        self.logger = self._setup_logger()
        self.alert_history: Dict[str, float] = {}
        self.running = False
        self._init_database()

    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        default_config = {
            "monitoring_interval": 60,  # seconds
            "database_path": "performance_metrics.db",
            "api_endpoints": [
                {"url": "http://localhost:8080/health", "name": "health_check"},
                {"url": "http://localhost:8080/api/status", "name": "status_api"},
            ],
            "performance_thresholds": {
                "api_response_time": 2.0,
                "database_query_time": 0.1,
                "memory_usage_percent": 80.0,
                "cpu_usage_percent": 80.0,
                "disk_usage_percent": 85.0,
            },
            "alerts": {
                "slack_webhook": "",
                "email_smtp_server": "",
                "email_smtp_port": 587,
                "email_username": "",
                "email_password": "",
                "email_recipients": [],
            },
            "monitoring_webhook": "",
            "monitoring_api_key": "",
        }

        try:
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
        except Exception as e:
            logging.error(f"Error loading config file: {e}")

        return default_config

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for performance monitoring."""
        logger = logging.getLogger("performance_monitor")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

            # File handler
            file_handler = logging.FileHandler("performance_monitor.log")
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)

        return logger

    def _init_database(self):
        """Initialize SQLite database for metrics storage."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    threshold REAL,
                    category TEXT DEFAULT 'general',
                    tags TEXT DEFAULT '{}'
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    value REAL NOT NULL,
                    threshold REAL NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    resolved BOOLEAN DEFAULT FALSE
                )
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_metrics_name ON performance_metrics(name)
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON performance_metrics(timestamp)
            """
            )

    async def collect_system_metrics(self) -> List[PerformanceMetric]:
        """Collect system performance metrics."""
        metrics = []

        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics.append(
            PerformanceMetric(
                name="cpu_usage_percent",
                value=cpu_percent,
                unit="percent",
                timestamp=time.time(),
                threshold=self.config["performance_thresholds"]["cpu_usage_percent"],
                category="system",
                tags={"type": "cpu"},
            )
        )

        # Memory metrics
        memory = psutil.virtual_memory()
        metrics.append(
            PerformanceMetric(
                name="memory_usage_percent",
                value=memory.percent,
                unit="percent",
                timestamp=time.time(),
                threshold=self.config["performance_thresholds"]["memory_usage_percent"],
                category="system",
                tags={"type": "memory"},
            )
        )

        metrics.append(
            PerformanceMetric(
                name="memory_available_mb",
                value=memory.available / 1024 / 1024,
                unit="MB",
                timestamp=time.time(),
                category="system",
                tags={"type": "memory"},
            )
        )

        # Disk metrics
        disk = psutil.disk_usage("/")
        disk_percent = (disk.used / disk.total) * 100
        metrics.append(
            PerformanceMetric(
                name="disk_usage_percent",
                value=disk_percent,
                unit="percent",
                timestamp=time.time(),
                threshold=self.config["performance_thresholds"]["disk_usage_percent"],
                category="system",
                tags={"type": "disk"},
            )
        )

        # Network metrics
        network = psutil.net_io_counters()
        metrics.append(
            PerformanceMetric(
                name="network_bytes_sent",
                value=network.bytes_sent,
                unit="bytes",
                timestamp=time.time(),
                category="network",
                tags={"type": "network", "direction": "sent"},
            )
        )

        metrics.append(
            PerformanceMetric(
                name="network_bytes_recv",
                value=network.bytes_recv,
                unit="bytes",
                timestamp=time.time(),
                category="network",
                tags={"type": "network", "direction": "received"},
            )
        )

        return metrics

    async def collect_api_metrics(self) -> List[PerformanceMetric]:
        """Collect API performance metrics."""
        metrics = []

        async with aiohttp.ClientSession() as session:
            for endpoint in self.config["api_endpoints"]:
                url = endpoint["url"]
                name = endpoint["name"]

                try:
                    start_time = time.perf_counter()
                    async with session.get(url, timeout=10) as response:
                        end_time = time.perf_counter()
                        response_time = end_time - start_time

                        metrics.append(
                            PerformanceMetric(
                                name=f"api_response_time_{name}",
                                value=response_time,
                                unit="seconds",
                                timestamp=time.time(),
                                threshold=self.config["performance_thresholds"][
                                    "api_response_time"
                                ],
                                category="api",
                                tags={"endpoint": name, "status": str(response.status)},
                            )
                        )

                        metrics.append(
                            PerformanceMetric(
                                name=f"api_status_code_{name}",
                                value=response.status,
                                unit="status_code",
                                timestamp=time.time(),
                                category="api",
                                tags={"endpoint": name},
                            )
                        )

                except Exception as e:
                    self.logger.error(f"Error checking API endpoint {url}: {e}")
                    metrics.append(
                        PerformanceMetric(
                            name=f"api_error_{name}",
                            value=1,
                            unit="count",
                            timestamp=time.time(),
                            category="api",
                            tags={"endpoint": name, "error": str(e)},
                        )
                    )

        return metrics

    async def collect_database_metrics(self) -> List[PerformanceMetric]:
        """Collect database performance metrics."""
        metrics = []

        try:
            # Simple database query timing
            start_time = time.perf_counter()
            with sqlite3.connect(self.database_path) as conn:
                conn.execute("SELECT COUNT(*) FROM performance_metrics")
                conn.fetchone()
            end_time = time.perf_counter()

            query_time = end_time - start_time
            metrics.append(
                PerformanceMetric(
                    name="database_query_time",
                    value=query_time,
                    unit="seconds",
                    timestamp=time.time(),
                    threshold=self.config["performance_thresholds"][
                        "database_query_time"
                    ],
                    category="database",
                    tags={"query": "count"},
                )
            )

            # Database size
            db_size = os.path.getsize(self.database_path) / 1024 / 1024  # MB
            metrics.append(
                PerformanceMetric(
                    name="database_size_mb",
                    value=db_size,
                    unit="MB",
                    timestamp=time.time(),
                    category="database",
                    tags={"type": "size"},
                )
            )

        except Exception as e:
            self.logger.error(f"Error collecting database metrics: {e}")
            metrics.append(
                PerformanceMetric(
                    name="database_error",
                    value=1,
                    unit="count",
                    timestamp=time.time(),
                    category="database",
                    tags={"error": str(e)},
                )
            )

        return metrics

    async def collect_application_metrics(self) -> List[PerformanceMetric]:
        """Collect application-specific metrics."""
        metrics = []

        try:
            # Check if main application processes are running
            piwardrive_processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                try:
                    if "piwardrive" in proc.info["name"].lower():
                        piwardrive_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            metrics.append(
                PerformanceMetric(
                    name="piwardrive_process_count",
                    value=len(piwardrive_processes),
                    unit="count",
                    timestamp=time.time(),
                    category="application",
                    tags={"type": "process"},
                )
            )

            # Aggregate CPU and memory usage for PiWardrive processes
            total_cpu = sum(proc.info["cpu_percent"] for proc in piwardrive_processes)
            total_memory = sum(
                proc.info["memory_percent"] for proc in piwardrive_processes
            )

            metrics.append(
                PerformanceMetric(
                    name="piwardrive_cpu_usage",
                    value=total_cpu,
                    unit="percent",
                    timestamp=time.time(),
                    category="application",
                    tags={"type": "cpu"},
                )
            )

            metrics.append(
                PerformanceMetric(
                    name="piwardrive_memory_usage",
                    value=total_memory,
                    unit="percent",
                    timestamp=time.time(),
                    category="application",
                    tags={"type": "memory"},
                )
            )

        except Exception as e:
            self.logger.error(f"Error collecting application metrics: {e}")

        return metrics

    def save_metrics(self, metrics: List[PerformanceMetric]):
        """Save metrics to database."""
        with sqlite3.connect(self.database_path) as conn:
            for metric in metrics:
                conn.execute(
                    """
                    INSERT INTO performance_metrics (
                        name, value, unit, timestamp, threshold, category, tags
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        metric.name,
                        metric.value,
                        metric.unit,
                        metric.timestamp,
                        metric.threshold,
                        metric.category,
                        json.dumps(metric.tags),
                    ),
                )
            conn.commit()

    def check_alerts(self, metrics: List[PerformanceMetric]):
        """Check metrics against thresholds and generate alerts."""
        current_time = time.time()

        for metric in metrics:
            if metric.threshold is None:
                continue

            # Check if metric exceeds threshold
            alert_triggered = False
            if metric.value > metric.threshold:
                alert_triggered = True

            if alert_triggered:
                # Check cooldown period
                last_alert = self.alert_history.get(metric.name, 0)
                if current_time - last_alert > (5 * 60):  # 5 minutes cooldown
                    self.send_alert(metric)
                    self.alert_history[metric.name] = current_time

    def send_alert(self, metric: PerformanceMetric):
        """Send alert for metric threshold breach."""
        severity = "warning" if metric.value < metric.threshold * 1.5 else "critical"

        message = (
            f"Performance Alert: {metric.name} = {metric.value:.2f} {metric.unit} "
            f"(threshold: {metric.threshold:.2f})"
        )

        self.logger.warning(message)

        # Save alert to database
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(
                """
                INSERT INTO alerts (
                    metric_name, value, threshold, severity, message, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    metric.name,
                    metric.value,
                    metric.threshold,
                    severity,
                    message,
                    time.time(),
                ),
            )
            conn.commit()

        # Send to external systems
        self.send_slack_alert(message, severity)
        self.send_email_alert(message, severity)
        self.send_to_monitoring_system(metric, severity)

    def send_slack_alert(self, message: str, severity: str):
        """Send alert to Slack."""
        webhook_url = self.config["alerts"]["slack_webhook"]
        if not webhook_url:
            return

        color = {"info": "good", "warning": "warning", "critical": "danger"}[severity]

        payload = {
            "attachments": [
                {
                    "color": color,
                    "title": f"PiWardrive Performance Alert ({severity.upper()})",
                    "text": message,
                    "timestamp": int(time.time()),
                }
            ]
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            self.logger.info("Slack alert sent successfully")
        except Exception as e:
            self.logger.error(f"Failed to send Slack alert: {e}")

    def send_email_alert(self, message: str, severity: str):
        """Send alert via email."""
        smtp_config = self.config["alerts"]
        if not smtp_config["email_smtp_server"] or not smtp_config["email_recipients"]:
            return

        try:
            msg = MimeMultipart()
            msg["From"] = smtp_config["email_username"]
            msg["To"] = ", ".join(smtp_config["email_recipients"])
            msg["Subject"] = f"PiWardrive Performance Alert ({severity.upper()})"

            body = f"""
            PiWardrive Performance Alert

            Severity: {severity.upper()}
            Message: {message}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            Please investigate and take appropriate action.
            """

            msg.attach(MimeText(body, "plain"))

            server = smtplib.SMTP(
                smtp_config["email_smtp_server"], smtp_config["email_smtp_port"]
            )
            server.starttls()
            server.login(smtp_config["email_username"], smtp_config["email_password"])
            server.send_message(msg)
            server.quit()

            self.logger.info("Email alert sent successfully")
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")

    def send_to_monitoring_system(self, metric: PerformanceMetric, severity: str):
        """Send metric to external monitoring system."""
        webhook_url = self.config["monitoring_webhook"]
        if not webhook_url:
            return

        payload = {
            "timestamp": metric.timestamp,
            "metric_name": metric.name,
            "value": metric.value,
            "unit": metric.unit,
            "threshold": metric.threshold,
            "category": metric.category,
            "tags": metric.tags,
            "alert_severity": severity,
        }

        headers = {"Content-Type": "application/json"}
        api_key = self.config["monitoring_api_key"]
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = requests.post(
                webhook_url, json=payload, headers=headers, timeout=10
            )
            response.raise_for_status()
            self.logger.info("Metrics sent to monitoring system")
        except Exception as e:
            self.logger.error(f"Failed to send metrics to monitoring system: {e}")

    async def run_monitoring_cycle(self):
        """Run one complete monitoring cycle."""
        self.logger.info("Starting monitoring cycle")

        # Collect all metrics
        all_metrics = []
        all_metrics.extend(await self.collect_system_metrics())
        all_metrics.extend(await self.collect_api_metrics())
        all_metrics.extend(await self.collect_database_metrics())
        all_metrics.extend(await self.collect_application_metrics())

        # Save metrics
        self.save_metrics(all_metrics)

        # Check for alerts
        self.check_alerts(all_metrics)

        self.logger.info(
            f"Monitoring cycle completed - collected {len(all_metrics)} metrics"
        )

    async def run(self):
        """Run the performance monitor continuously."""
        self.logger.info("Starting performance monitor")
        self.running = True

        while self.running:
            try:
                await self.run_monitoring_cycle()
                await asyncio.sleep(self.config["monitoring_interval"])
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring cycle: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    def stop(self):
        """Stop the performance monitor."""
        self.running = False
        self.logger.info("Performance monitor stopped")

    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for the last N hours."""
        since_timestamp = time.time() - (hours * 3600)

        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute(
                """
                SELECT name, AVG(value) as avg_value, MIN(value) as min_value,
                       MAX(value) as max_value, COUNT(*) as count
                FROM performance_metrics
                WHERE timestamp > ?
                GROUP BY name
                ORDER BY name
            """,
                (since_timestamp,),
            )

            metrics_summary = {}
            for row in cursor.fetchall():
                metrics_summary[row[0]] = {
                    "avg": row[1],
                    "min": row[2],
                    "max": row[3],
                    "count": row[4],
                }

            # Get recent alerts
            cursor = conn.execute(
                """
                SELECT metric_name, severity, COUNT(*) as alert_count
                FROM alerts
                WHERE timestamp > ?
                GROUP BY metric_name, severity
                ORDER BY alert_count DESC
            """,
                (since_timestamp,),
            )

            alerts_summary = {}
            for row in cursor.fetchall():
                if row[0] not in alerts_summary:
                    alerts_summary[row[0]] = {}
                alerts_summary[row[0]][row[1]] = row[2]

        return {
            "metrics": metrics_summary,
            "alerts": alerts_summary,
            "period_hours": hours,
        }


async def main():
    """Main function for running the performance monitor."""
    monitor = PerformanceMonitor()

    try:
        await monitor.run()
    except KeyboardInterrupt:
        monitor.stop()
    except Exception as e:
        logging.error(f"Error running performance monitor: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
