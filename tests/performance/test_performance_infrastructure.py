#!/usr/bin/env python3
"""
Performance Test Infrastructure for PiWardrive

This module provides comprehensive performance testing capabilities
including load testing, stress testing, and performance benchmarking.
"""

import asyncio
import json
import os
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import aiohttp
import psutil
import pytest
import requests


@dataclass
class PerformanceTestResult:
    """Result of a performance test."""
    test_name: str
    duration: float
    throughput: float
    latency_avg: float
    latency_p95: float
    latency_p99: float
    success_rate: float
    error_count: int
    memory_peak: float
    cpu_peak: float
    timestamp: float

@dataclass
class LoadTestConfig:
    """Configuration for load testing."""
    url: str
    method: str = "GET"
    payload: Optional[Dict] = None
    headers: Optional[Dict] = None
    concurrent_users: int = 10
    duration_seconds: int = 60
    ramp_up_seconds: int = 10
    timeout: int = 30


class PerformanceTestRunner:
    """Main class for running performance tests."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.results: List[PerformanceTestResult] = []
        self.baseline_file = Path("performance_baseline.json")

    def run_api_load_test(self, config: LoadTestConfig) -> PerformanceTestResult:
        """Run API load test with specified configuration."""
        start_time = time.perf_counter()
        responses = []
        errors = []

        def make_request():
            try:
                response = requests.request(
                    config.method,
                    config.url,
                    json=config.payload,
                    headers=config.headers,
                    timeout=config.timeout
                )
                return {
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'success': 200 <= response.status_code < 300
                }
            except Exception as e:
                return {
                    'status_code': 0,
                    'response_time': config.timeout,
                    'success': False,
                    'error': str(e)
                }

        # Monitor system resources
        process = psutil.Process()
        memory_usage = []
        cpu_usage = []

        # Ramp up phase
        with ThreadPoolExecutor(max_workers=config.concurrent_users) as executor:
            futures = []

            # Submit requests over the duration
            end_time = time.perf_counter() + config.duration_seconds
            while time.perf_counter() < end_time:
                # Monitor resources
                memory_usage.append(process.memory_info().rss / 1024 / 1024)  # MB
                cpu_usage.append(process.cpu_percent())

                # Submit request
                future = executor.submit(make_request)
                futures.append(future)

                # Control rate
                time.sleep(1.0 / config.concurrent_users)

            # Collect results
            for future in futures:
                try:
                    result = future.result(timeout=config.timeout + 10)
                    responses.append(result)
                    if not result['success']:
                        errors.append(result.get('error', 'Unknown error'))
                except Exception as e:
                    errors.append(str(e))

        end_time = time.perf_counter()
        total_duration = end_time - start_time

        # Calculate metrics
        successful_responses = [r for r in responses if r['success']]
        response_times = [r['response_time'] for r in responses]

        if not response_times:
            response_times = [0]

        result = PerformanceTestResult(
            test_name=f"load_test_{config.method}_{config.url.split('/')[-1]}",
            duration=total_duration,
            throughput=len(successful_responses) / total_duration,
            latency_avg=statistics.mean(response_times),
            latency_p95=statistics.quantiles(response_times,
                n=20)[18] if len(response_times) > 1 else response_times[0],
                
            latency_p99=statistics.quantiles(response_times,
                n=100)[98] if len(response_times) > 1 else response_times[0],
                
            success_rate=len(successful_responses) / len(responses) if responses else 0,
            error_count=len(errors),
            memory_peak=max(memory_usage) if memory_usage else 0,
            cpu_peak=max(cpu_usage) if cpu_usage else 0,
            timestamp=time.time()
        )

        self.results.append(result)
        return result

    async def run_async_load_test(self,
        config: LoadTestConfig) -> PerformanceTestResult:
        """Run async load test for better performance."""
        start_time = time.perf_counter()
        responses = []
        errors = []

        async def make_async_request(session):
            try:
                request_start = time.perf_counter()
                async with session.request(
                    config.method,
                    config.url,
                    json=config.payload,
                    headers=config.headers,
                    timeout=aiohttp.ClientTimeout(total=config.timeout)
                ) as response:
                    request_end = time.perf_counter()
                    return {
                        'status_code': response.status,
                        'response_time': request_end - request_start,
                        'success': 200 <= response.status < 300
                    }
            except Exception as e:
                return {
                    'status_code': 0,
                    'response_time': config.timeout,
                    'success': False,
                    'error': str(e)
                }

        # Monitor system resources
        process = psutil.Process()
        memory_usage = []
        cpu_usage = []

        async with aiohttp.ClientSession() as session:
            tasks = []

            # Create tasks for the duration
            end_time = time.perf_counter() + config.duration_seconds
            while time.perf_counter() < end_time:
                # Monitor resources
                memory_usage.append(process.memory_info().rss / 1024 / 1024)  # MB
                cpu_usage.append(process.cpu_percent())

                # Create concurrent tasks
                for _ in range(config.concurrent_users):
                    task = asyncio.create_task(make_async_request(session))
                    tasks.append(task)

                await asyncio.sleep(1.0)

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    errors.append(str(result))
                else:
                    responses.append(result)
                    if not result['success']:
                        errors.append(result.get('error', 'Request failed'))

        end_time = time.perf_counter()
        total_duration = end_time - start_time

        # Calculate metrics
        successful_responses = [r for r in responses if r['success']]
        response_times = [r['response_time'] for r in responses]

        if not response_times:
            response_times = [0]

        result = PerformanceTestResult(
            test_name=f"async_load_test_{config.method}_{config.url.split('/')[-1]}",
            duration=total_duration,
            throughput=len(successful_responses) / total_duration,
            latency_avg=statistics.mean(response_times),
            latency_p95=statistics.quantiles(response_times,
                n=20)[18] if len(response_times) > 1 else response_times[0],
                
            latency_p99=statistics.quantiles(response_times,
                n=100)[98] if len(response_times) > 1 else response_times[0],
                
            success_rate=len(successful_responses) / len(responses) if responses else 0,
            error_count=len(errors),
            memory_peak=max(memory_usage) if memory_usage else 0,
            cpu_peak=max(cpu_usage) if cpu_usage else 0,
            timestamp=time.time()
        )

        self.results.append(result)
        return result

    def run_database_performance_test(self) -> PerformanceTestResult:
        """Run database performance tests."""
        start_time = time.perf_counter()

        # Test various database operations
        operations = [
            ('SELECT COUNT(*) FROM wifi_networks', 'count_wifi'),
            ('SELECT COUNT(*) FROM bluetooth_devices', 'count_bluetooth'),
            ('SELECT * FROM wifi_networks LIMIT 100', 'select_wifi_100'),
            ('SELECT * FROM bluetooth_devices LIMIT 100', 'select_bluetooth_100'),
        ]

        response_times = []
        errors = []

        for query, operation_name in operations:
            try:
                # This would connect to the actual database
                # For now, we'll simulate with API calls
                operation_start = time.perf_counter()

                # Simulate database operation via API
                response = requests.get(
                    f"{self.base_url}/api/database/query",
                    params={'query': query},
                    timeout=30
                )

                operation_end = time.perf_counter()
                operation_time = operation_end - operation_start

                response_times.append(operation_time)

                if response.status_code != 200:
                    errors.append(f"{operation_name}: HTTP {response.status_code}")

            except Exception as e:
                errors.append(f"{operation_name}: {str(e)}")
                response_times.append(30.0)  # Timeout value

        end_time = time.perf_counter()
        total_duration = end_time - start_time

        result = PerformanceTestResult(
            test_name="database_performance_test",
            duration=total_duration,
            throughput=len(operations) / total_duration,
            latency_avg=statistics.mean(response_times),
            latency_p95=statistics.quantiles(response_times,
                n=20)[18] if len(response_times) > 1 else response_times[0],
                
            latency_p99=statistics.quantiles(response_times,
                n=100)[98] if len(response_times) > 1 else response_times[0],
                
            success_rate=(len(operations) - len(errors)) / len(operations),
            error_count=len(errors),
            memory_peak=psutil.Process().memory_info().rss / 1024 / 1024,
            cpu_peak=psutil.Process().cpu_percent(),
            timestamp=time.time()
        )

        self.results.append(result)
        return result

    def run_stress_test(self) -> PerformanceTestResult:
        """Run stress test to find breaking points."""
        start_time = time.perf_counter()

        # Gradually increase load until system breaks
        max_concurrent = 1
        breaking_point = 0
        response_times = []
        errors = []

        while max_concurrent <= 200:  # Maximum reasonable concurrent users
            config = LoadTestConfig(
                url=f"{self.base_url}/api/status",
                concurrent_users=max_concurrent,
                duration_seconds=10,
                timeout=30
            )

            result = self.run_api_load_test(config)

            # Check if system is still performing well
            if result.success_rate < 0.95 or result.latency_avg > 5.0:
                breaking_point = max_concurrent
                break

            response_times.extend([result.latency_avg])
            max_concurrent *= 2

        end_time = time.perf_counter()
        total_duration = end_time - start_time

        result = PerformanceTestResult(
            test_name="stress_test",
            duration=total_duration,
            throughput=breaking_point,  # Users at breaking point
            latency_avg=statistics.mean(response_times) if response_times else 0,
            latency_p95=statistics.quantiles(response_times,
                n=20)[18] if len(response_times) > 1 else (response_times[0] if response_times else 0),
                
            latency_p99=statistics.quantiles(response_times,
                n=100)[98] if len(response_times) > 1 else (response_times[0] if response_times else 0),
                
            success_rate=1.0 if breaking_point == 0 else 0.95,
            error_count=len(errors),
            memory_peak=psutil.Process().memory_info().rss / 1024 / 1024,
            cpu_peak=psutil.Process().cpu_percent(),
            timestamp=time.time()
        )

        self.results.append(result)
        return result

    def save_results(self, filename: str = "performance_results.json"):
        """Save performance test results to JSON file."""
        results_data = {
            'timestamp': time.time(),
            'results': [asdict(result) for result in self.results],
            'summary': self.get_summary()
        }

        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of performance test results."""
        if not self.results:
            return {}

        return {
            'total_tests': len(self.results),
            'avg_throughput': statistics.mean([r.throughput for r in self.results]),
            'avg_latency': statistics.mean([r.latency_avg for r in self.results]),
            'overall_success_rate': statistics.mean([r.success_rate for r in self.results]),
                
            'total_errors': sum([r.error_count for r in self.results]),
            'peak_memory': max([r.memory_peak for r in self.results]),
            'peak_cpu': max([r.cpu_peak for r in self.results])
        }

    def compare_with_baseline(self,
        baseline_file: str = "performance_baseline.json") -> Dict[str,
        Any]:
        """Compare current results with baseline."""
        if not os.path.exists(baseline_file):
            return {'error': 'Baseline file not found'}

        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)

        current_summary = self.get_summary()
        baseline_summary = baseline_data.get('summary', {})

        comparison = {}

        for metric in ['avg_throughput', 'avg_latency', 'overall_success_rate']:
            if metric in current_summary and metric in baseline_summary:
                current_value = current_summary[metric]
                baseline_value = baseline_summary[metric]

                if baseline_value != 0:
                    percentage_change = ((current_value - baseline_value) / baseline_value) * 100
                    comparison[metric] = {
                        'current': current_value,
                        'baseline': baseline_value,
                        'change_percent': percentage_change,
                        'regression': percentage_change < -10  # 10% degradation threshold
                    }

        return comparison

@pytest.mark.performance
class TestPerformance:
    """Performance test suite using pytest."""

    @pytest.fixture(scope="class")
    def perf_runner(self):
        """Create performance test runner."""
        base_url = os.getenv('TEST_BASE_URL', 'http://localhost:8080')
        return PerformanceTestRunner(base_url)

    @pytest.fixture(scope="class")
    def load_test_config(self):
        """Create load test configuration."""
        return LoadTestConfig(
            url=f"{os.getenv('TEST_BASE_URL', 'http://localhost:8080')}/api/status",
            concurrent_users=10,
            duration_seconds=30
        )

    def test_api_response_time(self, perf_runner):
        """Test API response time requirements."""
        config = LoadTestConfig(
            url=f"{perf_runner.base_url}/api/status",
            concurrent_users=5,
            duration_seconds=10
        )

        result = perf_runner.run_api_load_test(config)

        # Assert performance requirements
        assert result.latency_avg < 2.0, \
            f"Average latency too high: {result.latency_avg}s"
        assert result.latency_p95 < 3.0, \
            f"95th percentile latency too high: {result.latency_p95}s"
        assert result.success_rate > 0.95, \
            f"Success rate too low: {result.success_rate:.2%}"

    def test_concurrent_user_handling(self, perf_runner):
        """Test concurrent user handling capability."""
        config = LoadTestConfig(
            url=f"{perf_runner.base_url}/api/status",
            concurrent_users=50,
            duration_seconds=30
        )

        result = perf_runner.run_api_load_test(config)

        assert result.throughput > 10, f"Throughput too low: {result.throughput} req/s"
        assert result.success_rate > 0.90, \
            f"Success rate too low under load: {result.success_rate:.2%}"

    def test_database_performance(self, perf_runner):
        """Test database performance requirements."""
        result = perf_runner.run_database_performance_test()

        assert result.latency_avg < 1.0, \
            f"Database operations too slow: {result.latency_avg}s"
        assert result.success_rate > 0.95, \
            f"Database success rate too low: {result.success_rate:.2%}"

    def test_memory_usage(self, perf_runner):
        """Test memory usage during load."""
        config = LoadTestConfig(
            url=f"{perf_runner.base_url}/api/status",
            concurrent_users=20,
            duration_seconds=60
        )

        result = perf_runner.run_api_load_test(config)

        # Memory should not exceed 500MB during normal operation
        assert result.memory_peak < 500, \
            f"Memory usage too high: {result.memory_peak}MB"

    @pytest.mark.slow
    def test_long_running_stability(self, perf_runner):
        """Test long-running stability."""
        config = LoadTestConfig(
            url=f"{perf_runner.base_url}/api/status",
            concurrent_users=10,
            duration_seconds=300  # 5 minutes
        )

        result = perf_runner.run_api_load_test(config)

        assert result.success_rate > 0.95, \
            f"Long-running stability issue: {result.success_rate:.2%}"
        assert result.latency_avg < 2.0, \
            f"Performance degradation over time: {result.latency_avg}s"

    @pytest.mark.stress
    def test_stress_breaking_point(self, perf_runner):
        """Test system breaking point."""
        result = perf_runner.run_stress_test()

        # System should handle at least 50 concurrent users
        assert result.throughput >= 50, \
            f"System breaking point too low: {result.throughput} users"

    def test_performance_regression(self, perf_runner):
        """Test for performance regression against baseline."""
        config = LoadTestConfig(
            url=f"{perf_runner.base_url}/api/status",
            concurrent_users=10,
            duration_seconds=30
        )

        perf_runner.run_api_load_test(config)
        comparison = perf_runner.compare_with_baseline()

        if 'error' not in comparison:
            for metric, data in comparison.items():
                assert not data['regression'], \
                    f"Performance regression detected in {metric}: {data['change_percent']:.1f}%"

if __name__ == "__main__":
    # Run performance tests
    runner = PerformanceTestRunner()

    # Run all performance tests
    print("Running API load test...")
    api_config = LoadTestConfig(
        url=f"{runner.base_url}/api/status",
        concurrent_users=20,
        duration_seconds=60
    )
    runner.run_api_load_test(api_config)

    print("Running database performance test...")
    runner.run_database_performance_test()

    print("Running stress test...")
    runner.run_stress_test()

    # Save results
    runner.save_results()

    # Print summary
    summary = runner.get_summary()
    print("\nPerformance Test Summary:")
    print(json.dumps(summary, indent=2))
