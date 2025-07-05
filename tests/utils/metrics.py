#!/usr/bin/env python3
"""
Test Metrics Collection System for PiWardrive

This module provides comprehensive test metrics collection, analysis, and reporting
for the PiWardrive test suite.
"""

import json
import time
import sqlite3
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import pytest
import psutil
import requests
from contextlib import contextmanager


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
        self.system_metrics: Dict[str, Any] = {}
        self.logger = self._setup_logger()
        self._init_database()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for metrics collection."""
        logger = logging.getLogger("test_metrics")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _init_database(self):
        """Initialize SQLite database for metrics storage."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS test_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_name TEXT NOT NULL,
                    duration REAL NOT NULL,
                    status TEXT NOT NULL,
                    error TEXT,
                    timestamp REAL NOT NULL,
                    memory_peak REAL DEFAULT 0,
                    cpu_usage REAL DEFAULT 0,
                    test_category TEXT DEFAULT 'unit',
                    file_path TEXT DEFAULT '',
                    line_number INTEGER DEFAULT 0
                )
            """)
            
            conn.execute("""
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
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_test_name ON test_metrics(test_name)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON test_metrics(timestamp)
            """)
    
    def start_test(self, test_name: str):
        """Start tracking a test."""
        self.start_times[test_name] = time.perf_counter()
        self.system_metrics[test_name] = {
            'memory_start': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            'cpu_start': psutil.Process().cpu_percent()
        }
        self.logger.debug(f"Started tracking test: {test_name}")
    
    def end_test(self, test_name: str, status: str, error: Optional[str] = None,
                test_category: str = "unit", file_path: str = "", line_number: int = 0):
        """End tracking a test and record metrics."""
        if test_name not in self.start_times:
            self.logger.warning(f"Test {test_name} was not started")
            return
        
        duration = time.perf_counter() - self.start_times[test_name]
        
        # Calculate system metrics
        memory_peak = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        cpu_usage = psutil.Process().cpu_percent()
        
        # Create test metric
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
            line_number=line_number
        )
        
        self.metrics[test_name] = metric
        self.logger.info(f"Test {test_name} completed: {status} in {duration:.3f}s")
        
        # Clean up
        del self.start_times[test_name]
        if test_name in self.system_metrics:
            del self.system_metrics[test_name]
    
    def save_metrics(self, file_path: Optional[str] = None):
        """Save metrics to JSON file."""
        if file_path is None:
            file_path = f"test_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        metrics_data = {
            'timestamp': time.time(),
            'metrics': {name: asdict(metric) for name, metric in self.metrics.items()}
        }
        
        with open(file_path, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        self.logger.info(f"Metrics saved to {file_path}")
    
    def save_to_database(self, suite_metrics: Optional[TestSuiteMetrics] = None):
        """Save metrics to SQLite database."""
        with sqlite3.connect(self.database_path) as conn:
            # Save individual test metrics
            for metric in self.metrics.values():
                conn.execute("""
                    INSERT INTO test_metrics (
                        test_name, duration, status, error, timestamp,
                        memory_peak, cpu_usage, test_category, file_path, line_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metric.test_name, metric.duration, metric.status, metric.error,
                    metric.timestamp, metric.memory_peak, metric.cpu_usage,
                    metric.test_category, metric.file_path, metric.line_number
                ))
            
            # Save suite metrics if provided
            if suite_metrics:
                git_commit = self._get_git_commit()
                git_branch = self._get_git_branch()
                
                conn.execute("""
                    INSERT INTO test_suite_metrics (
                        total_tests, passed_tests, failed_tests, skipped_tests,
                        total_duration, timestamp, coverage_percentage,
                        git_commit, branch
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    suite_metrics.total_tests, suite_metrics.passed_tests,
                    suite_metrics.failed_tests, suite_metrics.skipped_tests,
                    suite_metrics.total_duration, suite_metrics.timestamp,
                    suite_metrics.coverage_percentage, git_commit, git_branch
                ))
            
            conn.commit()
        
        self.logger.info("Metrics saved to database")
    
    def _get_git_commit(self) -> str:
        """Get current git commit hash."""
        try:
            import subprocess
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else ''
        except:
            return ''
    
    def _get_git_branch(self) -> str:
        """Get current git branch."""
        try:
            import subprocess
            result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else ''
        except:
            return ''
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics."""
        if not self.metrics:
            return {}
        
        total_tests = len(self.metrics)
        passed_tests = sum(1 for m in self.metrics.values() if m.status == 'passed')
        failed_tests = sum(1 for m in self.metrics.values() if m.status == 'failed')
        skipped_tests = sum(1 for m in self.metrics.values() if m.status == 'skipped')
        
        total_duration = sum(m.duration for m in self.metrics.values())
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'skipped_tests': skipped_tests,
            'total_duration': total_duration,
            'average_duration': avg_duration,
            'pass_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'slowest_tests': self._get_slowest_tests(5),
            'failed_tests_details': self._get_failed_tests()
        }
    
    def _get_slowest_tests(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the slowest tests."""
        sorted_metrics = sorted(self.metrics.values(), key=lambda m: m.duration, reverse=True)
        return [
            {
                'test_name': m.test_name,
                'duration': m.duration,
                'category': m.test_category
            }
            for m in sorted_metrics[:limit]
        ]
    
    def _get_failed_tests(self) -> List[Dict[str, Any]]:
        """Get details of failed tests."""
        failed_tests = [m for m in self.metrics.values() if m.status == 'failed']
        return [
            {
                'test_name': m.test_name,
                'error': m.error,
                'duration': m.duration,
                'file_path': m.file_path,
                'line_number': m.line_number
            }
            for m in failed_tests
        ]
    
    def generate_report(self, output_file: str = "test_report.html"):
        """Generate HTML test report."""
        summary = self.get_metrics_summary()
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PiWardrive Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; }
                .metric { margin: 10px 0; }
                .passed { color: green; }
                .failed { color: red; }
                .skipped { color: orange; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>PiWardrive Test Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <div class="metric">Total Tests: {total_tests}</div>
                <div class="metric passed">Passed: {passed_tests}</div>
                <div class="metric failed">Failed: {failed_tests}</div>
                <div class="metric skipped">Skipped: {skipped_tests}</div>
                <div class="metric">Total Duration: {total_duration:.2f}s</div>
                <div class="metric">Average Duration: {average_duration:.3f}s</div>
                <div class="metric">Pass Rate: {pass_rate:.1%}</div>
            </div>
            
            <h2>Slowest Tests</h2>
            <table>
                <tr><th>Test Name</th><th>Duration (s)</th><th>Category</th></tr>
                {slowest_tests_rows}
            </table>
            
            <h2>Failed Tests</h2>
            <table>
                <tr><th>Test Name</th><th>Error</th><th>Duration (s)</th><th>File</th></tr>
                {failed_tests_rows}
            </table>
            
            <p><em>Report generated at {timestamp}</em></p>
        </body>
        </html>
        """
        
        # Generate table rows
        slowest_tests_rows = ""
        for test in summary.get('slowest_tests', []):
            slowest_tests_rows += f"<tr><td>{test['test_name']}</td><td>{test['duration']:.3f}</td><td>{test['category']}</td></tr>"
        
        failed_tests_rows = ""
        for test in summary.get('failed_tests_details', []):
            error = test['error'][:100] + "..." if test['error'] and len(test['error']) > 100 else test['error']
            failed_tests_rows += f"<tr><td>{test['test_name']}</td><td>{error}</td><td>{test['duration']:.3f}</td><td>{test['file_path']}</td></tr>"
        
        # Fill template
        html_content = html_template.format(
            **summary,
            slowest_tests_rows=slowest_tests_rows,
            failed_tests_rows=failed_tests_rows,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML report generated: {output_file}")
    
    def send_metrics_to_monitoring(self, monitoring_url: str, api_key: str = ""):
        """Send metrics to external monitoring system."""
        summary = self.get_metrics_summary()
        
        payload = {
            'timestamp': time.time(),
            'metrics': {
                'test_total': summary['total_tests'],
                'test_passed': summary['passed_tests'],
                'test_failed': summary['failed_tests'],
                'test_skipped': summary['skipped_tests'],
                'test_duration': summary['total_duration'],
                'test_pass_rate': summary['pass_rate']
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        try:
            response = requests.post(monitoring_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            self.logger.info(f"Metrics sent to monitoring system: {monitoring_url}")
        except requests.RequestException as e:
            self.logger.error(f"Failed to send metrics to monitoring system: {e}")


# Global instance for pytest plugin
_metrics_collector = None


def get_metrics_collector() -> TestMetricsCollector:
    """Get global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = TestMetricsCollector()
    return _metrics_collector


@contextmanager
def test_metrics_context(test_name: str, category: str = "unit"):
    """Context manager for test metrics collection."""
    collector = get_metrics_collector()
    collector.start_test(test_name)
    
    try:
        yield collector
        collector.end_test(test_name, "passed", test_category=category)
    except Exception as e:
        collector.end_test(test_name, "failed", str(e), test_category=category)
        raise


# Pytest plugin hooks
def pytest_runtest_setup(item):
    """Called before each test is run."""
    collector = get_metrics_collector()
    test_name = item.nodeid
    collector.start_test(test_name)


def pytest_runtest_teardown(item, nextitem):
    """Called after each test is run."""
    collector = get_metrics_collector()
    test_name = item.nodeid
    
    # Determine test status
    if hasattr(item, 'rep_call'):
        if item.rep_call.failed:
            status = "failed"
            error = str(item.rep_call.longrepr) if item.rep_call.longrepr else None
        elif item.rep_call.skipped:
            status = "skipped"
            error = None
        else:
            status = "passed"
            error = None
    else:
        status = "unknown"
        error = None
    
    # Determine test category
    category = "unit"
    if "integration" in test_name:
        category = "integration"
    elif "performance" in test_name:
        category = "performance"
    elif "e2e" in test_name or "end_to_end" in test_name:
        category = "e2e"
    
    collector.end_test(test_name, status, error, category)


def pytest_sessionfinish(session, exitstatus):
    """Called after the entire test session finishes."""
    collector = get_metrics_collector()
    
    # Create suite metrics
    summary = collector.get_metrics_summary()
    suite_metrics = TestSuiteMetrics(
        total_tests=summary.get('total_tests', 0),
        passed_tests=summary.get('passed_tests', 0),
        failed_tests=summary.get('failed_tests', 0),
        skipped_tests=summary.get('skipped_tests', 0),
        total_duration=summary.get('total_duration', 0),
        timestamp=time.time()
    )
    
    # Save metrics
    collector.save_metrics()
    collector.save_to_database(suite_metrics)
    collector.generate_report()
    
    # Send to monitoring if configured
    monitoring_url = os.getenv('MONITORING_URL')
    if monitoring_url:
        api_key = os.getenv('MONITORING_API_KEY', '')
        collector.send_metrics_to_monitoring(monitoring_url, api_key)


if __name__ == "__main__":
    # Example usage
    collector = TestMetricsCollector()
    
    # Simulate some test metrics
    collector.start_test("test_example_1")
    time.sleep(0.1)  # Simulate test execution
    collector.end_test("test_example_1", "passed")
    
    collector.start_test("test_example_2")
    time.sleep(0.05)
    collector.end_test("test_example_2", "failed", "AssertionError: Expected 1 but got 2")
    
    # Generate report
    collector.generate_report()
    print("Test metrics collection demo completed")
