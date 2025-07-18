#!/usr/bin/env python3
"""
Test Metrics Collection System for PiWardrive

This module provides comprehensive test metrics collection, analysis, and reporting
for the PiWardrive test suite.
"""

import json
import logging
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

import psutil


@dataclass
class TestMetric:
    """Test execution metric."""

    test_name: str
    duration: float
    status: str
    error: Optional[str] = None
    timestamp: float = 0
    memory_peak: float = 0
    cpu_usage: float = 0
    test_category: str = "unit"
    file_path: str = ""
    line_number: int = 0


@dataclass
class TestSuiteMetrics:
    """Test suite execution metrics."""

    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    total_duration: float
    timestamp: float
    coverage_percentage: float = 0.0
    test_metrics: List[TestMetric] = None

    def __post_init__(self):
        if self.test_metrics is None:
            self.test_metrics = []


class TestMetricsCollector:
    """Collects and manages test execution metrics."""

    def __init__(self, database_path: str = "test_metrics.db"):
        self.database_path = database_path
        self.metrics: Dict[str, TestMetric] = {}
        self.start_times: Dict[str, float] = {}
        self.resource_tracking: Dict[str, Dict[str, float]] = {}
        self.logger = self._setup_logger()
        self._init_database()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger for metrics collection."""
        logger = logging.getLogger("test_metrics")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _init_database(self):
        """Initialize SQLite database for metrics storage."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS test_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    duration REAL NOT NULL,
                    status TEXT NOT NULL,
                    error TEXT,
                    timestamp REAL NOT NULL,
                    memory_peak REAL DEFAULT 0.0,
                    cpu_usage REAL DEFAULT 0.0,
                    test_category TEXT DEFAULT 'unit',
                    file_path TEXT DEFAULT '',
                    line_number INTEGER DEFAULT 0
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS test_suite_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_tests INTEGER NOT NULL,
                    passed_tests INTEGER NOT NULL,
                    failed_tests INTEGER NOT NULL,
                    skipped_tests INTEGER NOT NULL,
                    total_duration REAL NOT NULL,
                    timestamp REAL NOT NULL,
                    coverage_percentage REAL DEFAULT 0.0,
                    git_commit TEXT DEFAULT '',
                    branch TEXT DEFAULT ''
                )
            """
            )
            conn.execute(
                """CREATE INDEX IF NOT EXISTS idx_test_name ON test_metrics(test_name)"""
            )
            conn.execute(
                """CREATE INDEX IF NOT EXISTS idx_timestamp ON test_metrics(timestamp)"""
            )

    def start_test(self, test_name: str):
        """Start tracking a test."""
        self.start_times[test_name] = time.perf_counter()
        self.resource_tracking[test_name] = {
            "memory_start": psutil.Process().memory_info().rss / 1024 / 1024,
            "cpu_start": psutil.Process().cpu_percent(),
        }
        self.logger.debug(f"Started tracking test: {test_name}")

    def end_test(
        self,
        test_name: str,
        status: str,
        error: Optional[str] = None,
        test_category: str = "unit",
        file_path: str = "",
        line_number: int = 0,
    ):
        """End tracking a test and record metrics."""
        if test_name not in self.start_times:
            self.logger.warning(f"Test {test_name} was not started")
            return

        duration = time.perf_counter() - self.start_times[test_name]
        memory_current = psutil.Process().memory_info().rss / 1024 / 1024
        memory_peak = max(
            memory_current, self.resource_tracking[test_name]["memory_start"]
        )
        cpu_usage = psutil.Process().cpu_percent()

        metric = TestMetric(
            test_name=test_name,
            duration=duration,
            status=status,
            error=error,
            timestamp=time.time(),
            memory_peak=memory_peak,
            cpu_usage=cpu_usage,
            test_category=test_category,
            file_path=file_path,
            line_number=line_number,
        )

        self.metrics[test_name] = metric
        self.logger.info(f"Test {test_name} completed: {status} in {duration:.3f}s")

        # Store in database
        self._store_metric(metric)

        # Cleanup
        del self.start_times[test_name]
        del self.resource_tracking[test_name]

    def _store_metric(self, metric: TestMetric):
        """Store metric in database."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute(
                """
                INSERT INTO test_metrics 
                (test_name, duration, status, error, timestamp, memory_peak, 
                 cpu_usage, test_category, file_path, line_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    metric.test_name,
                    metric.duration,
                    metric.status,
                    metric.error,
                    metric.timestamp,
                    metric.memory_peak,
                    metric.cpu_usage,
                    metric.test_category,
                    metric.file_path,
                    metric.line_number,
                ),
            )

    def get_metrics(self) -> Dict[str, TestMetric]:
        """Get all collected metrics."""
        return self.metrics.copy()

    def get_suite_summary(self) -> TestSuiteMetrics:
        """Get summary of test suite execution."""
        metrics_list = list(self.metrics.values())
        total_tests = len(metrics_list)
        passed_tests = sum(1 for m in metrics_list if m.status == "passed")
        failed_tests = sum(1 for m in metrics_list if m.status == "failed")
        skipped_tests = sum(1 for m in metrics_list if m.status == "skipped")
        total_duration = sum(m.duration for m in metrics_list)

        return TestSuiteMetrics(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            total_duration=total_duration,
            timestamp=time.time(),
            test_metrics=metrics_list,
        )

    def generate_report(self, format_type: str = "json") -> str:
        """Generate test metrics report."""
        summary = self.get_suite_summary()

        if format_type == "json":
            return json.dumps(asdict(summary), indent=2, default=str)
        elif format_type == "html":
            return self._generate_html_report(summary)
        else:
            return self._generate_text_report(summary)

    def _generate_html_report(self, summary: TestSuiteMetrics) -> str:
        """Generate HTML report."""
        html = f"""
        <html>
        <head><title>Test Metrics Report</title></head>
        <body>
        <h1>Test Suite Results</h1>
        <p>Total Tests: {summary.total_tests}</p>
        <p>Passed: {summary.passed_tests}</p>
        <p>Failed: {summary.failed_tests}</p>
        <p>Skipped: {summary.skipped_tests}</p>
        <p>Total Duration: {summary.total_duration:.2f}s</p>
        <h2>Individual Test Results</h2>
        <table border="1">
        <tr><th>Test</th><th>Status</th><th>Duration</th><th>Memory (MB)</th></tr>
        """

        for metric in summary.test_metrics:
            html += f"""
            <tr>
                <td>{metric.test_name}</td>
                <td>{metric.status}</td>
                <td>{metric.duration:.3f}s</td>
                <td>{metric.memory_peak:.1f}</td>
            </tr>
            """

        html += "</table></body></html>"
        return html

    def _generate_text_report(self, summary: TestSuiteMetrics) -> str:
        """Generate text report."""
        report = f"""
Test Suite Summary
==================
Total Tests: {summary.total_tests}
Passed: {summary.passed_tests}
Failed: {summary.failed_tests}
Skipped: {summary.skipped_tests}
Total Duration: {summary.total_duration:.2f}s
Success Rate: {(summary.passed_tests / summary.total_tests * 100):.1f}%

Individual Test Results:
"""
        for metric in summary.test_metrics:
            report += (
                f"  {metric.test_name}: {metric.status} ({metric.duration:.3f}s)\n"
            )
            if metric.error:
                report += f"    Error: {metric.error}\n"

        return report

    def export_to_ci(self, ci_system: str = "github") -> Dict[str, Any]:
        """Export metrics for CI system integration."""
        summary = self.get_suite_summary()

        if ci_system == "github":
            return {
                "summary": f"Tests: {summary.passed_tests}/{summary.total_tests} passed",
                "details": {
                    "total_tests": summary.total_tests,
                    "passed_tests": summary.passed_tests,
                    "failed_tests": summary.failed_tests,
                    "duration": summary.total_duration,
                },
            }

        return asdict(summary)

    @contextmanager
    def track_test(self, test_name: str, test_category: str = "unit"):
        """Context manager for tracking test execution."""
        self.start_test(test_name)
        try:
            yield
            self.end_test(test_name, "passed", test_category=test_category)
        except Exception as e:
            self.end_test(test_name, "failed", str(e), test_category=test_category)
            raise

    def clear_metrics(self):
        """Clear all collected metrics."""
        self.metrics.clear()
        self.start_times.clear()
        self.resource_tracking.clear()

    def get_historical_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical test metrics from database."""
        cutoff = time.time() - (days * 24 * 60 * 60)

        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.execute(
                """
                SELECT * FROM test_metrics 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """,
                (cutoff,),
            )

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze test performance trends."""
        historical_data = self.get_historical_data()

        if not historical_data:
            return {"error": "No historical data available"}

        # Group by test name
        test_trends = {}
        for record in historical_data:
            test_name = record["test_name"]
            if test_name not in test_trends:
                test_trends[test_name] = []
            test_trends[test_name].append(record)

        # Calculate trends
        trends = {}
        for test_name, records in test_trends.items():
            durations = [r["duration"] for r in records]
            avg_duration = sum(durations) / len(durations)

            # Recent vs historical comparison
            recent = durations[:10] if len(durations) > 10 else durations
            historical = durations[10:] if len(durations) > 10 else []

            trend = "stable"
            if historical:
                recent_avg = sum(recent) / len(recent)
                historical_avg = sum(historical) / len(historical)
                change = (recent_avg - historical_avg) / historical_avg * 100

                if change > 20:
                    trend = "slower"
                elif change < -20:
                    trend = "faster"

            trends[test_name] = {
                "average_duration": avg_duration,
                "trend": trend,
                "total_runs": len(records),
                "failure_rate": sum(1 for r in records if r["status"] == "failed")
                / len(records)
                * 100,
            }

        return trends


# Global metrics collector instance
_metrics_collector = None


def get_metrics_collector() -> TestMetricsCollector:
    """Get the global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = TestMetricsCollector()
    return _metrics_collector


def track_test_performance(test_name: str, test_category: str = "unit"):
    """Decorator for tracking test performance."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            collector = get_metrics_collector()
            with collector.track_test(test_name, test_category):
                return func(*args, **kwargs)

        return wrapper

    return decorator
