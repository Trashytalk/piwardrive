import logging

"""
Comprehensive performance and load testing for PiWardrive.

This module contains performance tests, load tests, and benchmarks to ensure
the system performs well under various conditions.
"""

import asyncio
import json
import os
import shutil
import statistics
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch

import psutil
import pytest
import requests

from src.analysis import AnalysisEngine
from src.config import ConfigManager
from src.data.aggregation import AggregationService
from src.network.scanner import NetworkScanner
from src.persistence import PersistenceManager

# Import core components
from src.service import PiWardriveService
from src.webui.server import WebUIServer


@dataclass
class PerformanceMetrics:
    """Performance metrics container."""
    name: str
    duration: float
    memory_usage: int
    cpu_usage: float
    throughput: float
    latency: float
    success_rate: float
    error_count: int
    additional_metrics: Dict[str, Any]


class PerformanceTestFixture:
    """Fixture for performance tests."""

    def __init__(self, test_name: str):
        self.test_name = test_name
        self.test_dir = None
        self.config_path = None
        self.metrics = []
        self.start_time = None
        self.process = None

    def setup(self):
        """Set up performance test environment."""
        self.test_dir = tempfile.mkdtemp(prefix=f"piwardrive_perf_{self.test_name}_")
        self.config_path = os.path.join(self.test_dir, "config.json")

        # Performance-optimized configuration
        perf_config = {
            "database": {
                "path": os.path.join(self.test_dir, "perf_test.db"),"type": "sqlite","pool_size": 20,"connection_timeout": 30
            },"logging": {
                "level": "WARNING",  # Reduce logging overhead
                "file": os.path.join(self.test_dir, "perf_test.log")
            },"webui": {
                "port": 0,"host": "127.0.0.1","workers": 4
            },"network": {
                "scan_interval": 1,"batch_size": 100,"mock_data": True
            },"performance": {
                "enable_profiling": True,"memory_monitoring": True,"cpu_monitoring": True
            }
        }

        with open(self.config_path, 'w') as f:
            json.dump(perf_config, f)

        # Initialize process monitoring
        self.process = psutil.Process(os.getpid())

        return self

    def teardown(self):
        """Clean up performance test environment."""
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = time.time()

    def stop_monitoring(self,
        operation_name: str,operations_count: int = 1) -> PerformanceMetrics:
        """Stop monitoring and collect metrics."""
        end_time = time.time()
        duration = end_time - self.start_time

        # Collect system metrics
        memory_info = self.process.memory_info()
        cpu_percent = self.process.cpu_percent()

        metrics = PerformanceMetrics(
            name=operation_name,
            duration=duration,
            memory_usage=memory_info.rss,
            cpu_usage=cpu_percent,
            throughput=operations_count / duration if duration > 0 else 0,
            latency=duration / operations_count if operations_count > 0 else 0,
            success_rate=1.0,  # Will be updated by specific tests
            error_count=0,additional_metrics={}
        )

        self.metrics.append(metrics)
        return metrics

    @contextmanager
    def performance_context(self, operation_name: str, operations_count: int = 1):
        """Context manager for performance monitoring."""
        self.start_monitoring()
        try:
            yield
        finally:
            self.stop_monitoring(operation_name, operations_count)

@pytest.fixture
def perf_fixture(request):
    """Pytest fixture for performance tests."""
    fixture = PerformanceTestFixture(request.node.name)
    fixture.setup()
    yield fixture
    fixture.teardown()


class TestDatabasePerformance:
    """Test database performance under various conditions."""

    def test_bulk_insert_performance(self, perf_fixture):
        """Test bulk data insertion performance."""
        _config = ConfigManager(perf_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Test different batch sizes
        batch_sizes = [100, 500, 1000, 2000]

        for batch_size in batch_sizes:
            with perf_fixture.performance_context(f"bulk_insert_{batch_size}",
                batch_size):
                # Generate test data
                test_data = []
                for i in range(batch_size):
                    test_data.append({
                        'ssid': f'PerfTestNetwork{i}',
                        'bssid': f'00:11:22:33:{i//256:02d}:{i%256:02d}',
                        'signal_strength': -45 - (i % 40),
                        'frequency': 2412 + (i % 13),
                        'timestamp': int(time.time()) + i
                    })

                # Bulk insert
                persistence.bulk_insert_networks(test_data)

        # Verify performance requirements
        for metrics in perf_fixture.metrics:
            if 'bulk_insert' in metrics.name:
                # Should handle at least 100 inserts per second
                assert metrics.throughput >= 100,f"Throughput too low: {metrics.throughput}"

                # Memory usage should be reasonable
                assert metrics.memory_usage < 500 * 1024 * 1024,f"Memory usage too high: {metrics.memory_usage}"

    def test_query_performance(self, perf_fixture):
        """Test database query performance."""
        _config = ConfigManager(perf_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Create test data
        test_data = []
        for i in range(10000):
            test_data.append({
                'ssid': f'QueryTestNetwork{i}',
                'bssid': f'00:11:22:33:{i//256:02d}:{i%256:02d}',
                'signal_strength': -45 - (i % 40),
                'frequency': 2412 + (i % 13),'timestamp': int(time.time()) + i
            })

        persistence.bulk_insert_networks(test_data)

        # Test different query types
        query_tests = [
            ("get_all_networks", lambda: persistence.get_networks()),("get_networks_by_ssid",lambda: persistence.get_networks_by_ssid("QueryTestNetwork1000")),("get_recent_networks", lambda: persistence.get_recent_networks(1000)),("get_networks_by_signal",
                lambda: persistence.get_networks_by_signal_range(-50,-40))
        ]

        for query_name, query_func in query_tests:
            with perf_fixture.performance_context(query_name, 1):
                _result = query_func()

        # Verify query performance
        for metrics in perf_fixture.metrics:
            if 'get_' in metrics.name:
                # Queries should complete quickly
                assert metrics.latency < 1.0, f"Query too slow: {metrics.latency}s"

    def test_concurrent_database_access(self, perf_fixture):
        """Test concurrent database access performance."""
        _config = ConfigManager(perf_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        def worker_function(worker_id, operations_per_worker):
            """Worker function for concurrent access."""
            for i in range(operations_per_worker):
                # Mix of read and write operations
                if i % 2 == 0:
                    # Write operation
                    network_data = {
                        'ssid': f'ConcurrentNetwork{worker_id}_{i}',
                        'bssid': f'00:11:22:33:{worker_id:02d}:{i%256:02d}',
                        'signal_strength': -50 - i,
                        'frequency': 2412 + i,'timestamp': int(time.time())
                    }
                    persistence.store_network(network_data)
                else:
                    # Read operation
                    persistence.get_recent_networks(10)

        # Test with different concurrency levels
        concurrency_levels = [2, 4, 8]
        operations_per_worker = 100

        for concurrency in concurrency_levels:
            with perf_fixture.performance_context(f"concurrent_access_{concurrency}",
                                                concurrency * operations_per_worker):
                # Start concurrent workers
                with ThreadPoolExecutor(max_workers=concurrency) as executor:
                    futures = []
                    for worker_id in range(concurrency):
                        future = executor.submit(worker_function,
                            worker_id,
                            operations_per_worker)
                        futures.append(future)

                    # Wait for all workers to complete
                    for future in futures:
                        future.result()

        # Verify concurrent access performance
        for metrics in perf_fixture.metrics:
            if 'concurrent_access' in metrics.name:
                # Should maintain reasonable throughput under concurrency
                assert metrics.throughput >= 50,f"Concurrent throughput too low: {metrics.throughput}"


class TestNetworkScannerPerformance:
    """Test network scanner performance."""

    def test_scan_processing_performance(self, perf_fixture):
        """Test network scan processing performance."""
        _config = ConfigManager(perf_fixture.config_path)

        # Mock network scanner with high data volume
        class MockHighVolumeScanner(NetworkScanner):
            def __init__(self, config):
                super().__init__(config)
                self.scan_results = []

            def scan_networks(self):
                # Simulate high-volume scan results
                results = []
                for i in range(1000):
                    results.append({
                        'ssid': f'HighVolumeNetwork{i}',
                        'bssid': f'00:11:22:33:{i//256:02d}:{i%256:02d}',
                        'signal_strength': -45 - (i % 40),
                        'frequency': 2412 + (i % 13),'timestamp': int(time.time())
                    })
                return results

        scanner = MockHighVolumeScanner(config)

        with perf_fixture.performance_context("high_volume_scan", 1000):
            results = scanner.scan_networks()

        # Verify scan performance
        metrics = perf_fixture.metrics[-1]
        assert metrics.throughput >= 500,f"Scan throughput too low: {metrics.throughput}"
        assert len(results) == 1000, "Not all scan results processed"

    def test_continuous_scanning_performance(self, perf_fixture):
        """Test continuous network scanning performance."""
        _config = ConfigManager(perf_fixture.config_path)

        class MockContinuousScanner(NetworkScanner):
            def __init__(self, config):
                super().__init__(config)
                self.scan_count = 0

            def scan_networks(self):
                self.scan_count += 1
                results = []
                for i in range(50):  # Smaller batches for continuous scanning
                    results.append({
                        'ssid': f'ContinuousNetwork{i}',
                        'bssid': f'00:11:22:33:44:{i:02d}',
                        'signal_strength': -45 - (i % 40),
                        'frequency': 2412 + (i % 13),'timestamp': int(time.time())
                    })
                return results

        scanner = MockContinuousScanner(config)

        with perf_fixture.performance_context("continuous_scanning", 10):
            # Simulate continuous scanning
            for _ in range(10):
                scanner.scan_networks()
                time.sleep(0.1)  # Brief pause between scans

        # Verify continuous scanning performance
        metrics = perf_fixture.metrics[-1]
        assert scanner.scan_count == 10, "Not all scans completed"
        assert metrics.duration < 5.0,f"Continuous scanning too slow: {metrics.duration}s"


class TestWebUIPerformance:
    """Test WebUI performance under load."""

    def test_api_response_performance(self, perf_fixture):
        """Test API response performance."""
        _config = ConfigManager(perf_fixture.config_path)

        # Start WebUI server
        server = WebUIServer(config)
        server.start()
        port = server.get_port()

        try:
            # Test different API endpoints
            endpoints = [
                "/api/status","/api/networks","/api/networks/recent","/api/analysis/summary"
            ]

            for endpoint in endpoints:
                with perf_fixture.performance_context(f"api_response_{endpoint.replace('/','_')}",
                    1):
                    response = requests.get(f"http://127.0.0.1:{port}{endpoint}")
                    assert response.status_code == 200

            # Verify API performance
            for metrics in perf_fixture.metrics:
                if 'api_response' in metrics.name:
                    # API responses should be fast
                    assert metrics.latency < 0.5,f"API response too slow: {metrics.latency}s"

        finally:
            server.stop()

    def test_concurrent_user_load(self, perf_fixture):
        """Test WebUI performance under concurrent user load."""
        _config = ConfigManager(perf_fixture.config_path)

        # Start WebUI server
        server = WebUIServer(config)
        server.start()
        port = server.get_port()

        try:
            def simulate_user_session(user_id, requests_per_user):
                """Simulate a user session with multiple requests."""
                session = requests.Session()
                successful_requests = 0

                for i in range(requests_per_user):
                    try:
                        endpoints = ["/api/status","/api/networks","/","/api/analysis/summary"]
                        endpoint = endpoints[i % len(endpoints)]

                        response = session.get(f"http://127.0.0.1:{port}{endpoint}")
                        if response.status_code == 200:
                            successful_requests += 1
                    except Exception as e:
                        print(f"User {user_id} request {i} failed: {e}")

                return successful_requests

            # Test different load levels
            load_levels = [
                (5, 20),   # 5 users, 20 requests each
                (10, 15),  # 10 users, 15 requests each
                (20, 10)   # 20 users, 10 requests each
            ]

            for concurrent_users, requests_per_user in load_levels:
                total_requests = concurrent_users * requests_per_user

                with perf_fixture.performance_context(f"concurrent_load_{concurrent_users}_{requests_per_user}",
                    
                                                    total_requests):
                    # Start concurrent user simulations
                    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
                        futures = []
                        for user_id in range(concurrent_users):
                            future = executor.submit(simulate_user_session,
                                user_id,
                                requests_per_user)
                            futures.append(future)

                        # Collect results
                        total_successful = sum(future.result() for future in futures)

                # Update success rate
                metrics = perf_fixture.metrics[-1]
                metrics.success_rate = total_successful / total_requests
                metrics.error_count = total_requests - total_successful

            # Verify load performance
            for metrics in perf_fixture.metrics:
                if 'concurrent_load' in metrics.name:
                    # Should maintain high success rate
                    assert metrics.success_rate >= 0.95,f"Success rate too low: {metrics.success_rate}"

                    # Should maintain reasonable throughput
                    assert metrics.throughput >= 10,f"Throughput too low under load: {metrics.throughput}"

        finally:
            server.stop()


class TestAnalysisPerformance:
    """Test analysis engine performance."""

    def test_large_dataset_analysis(self, perf_fixture):
        """Test analysis performance with large datasets."""
        _config = ConfigManager(perf_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Create large test dataset
        large_dataset_size = 50000
        test_data = []

        for i in range(large_dataset_size):
            test_data.append({
                'ssid': f'AnalysisTestNetwork{i}',
                'bssid': f'00:11:22:33:{i//256:02d}:{i%256:02d}',
                'signal_strength': -45 - (i % 40),
                'frequency': 2412 + (i % 13),'timestamp': int(time.time()) + i
            })

        persistence.bulk_insert_networks(test_data)

        # Test analysis operations
        analysis_engine = AnalysisEngine(config)

        analysis_operations = [
            ("network_analysis", lambda: analysis_engine.analyze_networks()),("signal_analysis", lambda: analysis_engine.analyze_signal_strength()),("frequency_analysis",
                lambda: analysis_engine.analyze_frequency_distribution()),("temporal_analysis", lambda: analysis_engine.analyze_temporal_patterns())
        ]

        for operation_name, operation_func in analysis_operations:
            with perf_fixture.performance_context(operation_name, 1):
                _result = operation_func()

        # Verify analysis performance
        for metrics in perf_fixture.metrics:
            if 'analysis' in metrics.name:
                # Analysis should complete in reasonable time
                assert metrics.latency < 10.0, f"Analysis too slow: {metrics.latency}s"

    def test_real_time_analysis_performance(self, perf_fixture):
        """Test real-time analysis performance."""
        _config = ConfigManager(perf_fixture.config_path)

        analysis_engine = AnalysisEngine(config)

        # Simulate real-time data stream
        def data_stream():
            for i in range(1000):
                yield {
                    'ssid': f'RealTimeNetwork{i}',
                    'bssid': f'00:11:22:33:44:{i%256:02d}',
                    'signal_strength': -45 - (i % 40),
                    'frequency': 2412 + (i % 13),'timestamp': int(time.time())
                }

        with perf_fixture.performance_context("real_time_analysis", 1000):
            # Process data stream
            for data_point in data_stream():
                analysis_engine.process_real_time_data(data_point)

        # Verify real-time analysis performance
        metrics = perf_fixture.metrics[-1]
        assert metrics.throughput >= 100,f"Real-time analysis throughput too low: {metrics.throughput}"


class TestMemoryPerformance:
    """Test memory usage and performance."""

    def test_memory_usage_patterns(self, perf_fixture):
        """Test memory usage patterns under different loads."""
        _config = ConfigManager(perf_fixture.config_path)

        # Test different memory usage scenarios
        scenarios = [
            ("idle_memory", lambda: time.sleep(1)),("light_load", lambda: self._simulate_light_load(config)),("heavy_load", lambda: self._simulate_heavy_load(config)),("sustained_load", lambda: self._simulate_sustained_load(config))
        ]

        for scenario_name, scenario_func in scenarios:
            with perf_fixture.performance_context(scenario_name, 1):
                scenario_func()

        # Verify memory usage patterns
        for metrics in perf_fixture.metrics:
            if metrics.name in ["idle_memory", "light_load"]:
                # Should use reasonable memory for light loads
                assert metrics.memory_usage < 100 * 1024 * 1024,f"Memory usage too high: {metrics.memory_usage}"
            elif metrics.name in ["heavy_load", "sustained_load"]:
                # Should handle heavy loads without excessive memory
                assert metrics.memory_usage < 500 * 1024 * 1024,f"Memory usage too high: {metrics.memory_usage}"

    def _simulate_light_load(self, config):
        """Simulate light system load."""
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Light data processing
        for i in range(100):
            network_data = {
                'ssid': f'LightLoadNetwork{i}',
                'bssid': f'00:11:22:33:44:{i:02d}',
                'signal_strength': -50,
                'frequency': 2412,'timestamp': int(time.time())
            }
            persistence.store_network(network_data)

    def _simulate_heavy_load(self, config):
        """Simulate heavy system load."""
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Heavy data processing
        test_data = []
        for i in range(10000):
            test_data.append({
                'ssid': f'HeavyLoadNetwork{i}',
                'bssid': f'00:11:22:33:{i//256:02d}:{i%256:02d}',
                'signal_strength': -45 - (i % 40),
                'frequency': 2412 + (i % 13),'timestamp': int(time.time()) + i
            })

        persistence.bulk_insert_networks(test_data)

        # Heavy analysis
        analysis_engine = AnalysisEngine(config)
        analysis_engine.analyze_networks()

    def _simulate_sustained_load(self, config):
        """Simulate sustained system load."""
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Sustained load over time
        for batch in range(10):
            test_data = []
            for i in range(1000):
                test_data.append({
                    'ssid': f'SustainedLoadNetwork{batch}_{i}',
                    'bssid': f'00:11:22:33:{batch:02d}:{i%256:02d}',
                    'signal_strength': -45 - (i % 40),
                    'frequency': 2412 + (i % 13),'timestamp': int(time.time()) + i
                })

            persistence.bulk_insert_networks(test_data)
            time.sleep(0.1)  # Brief pause between batches


class TestAsyncPerformance:
    """Test asynchronous operation performance."""

    @pytest.mark.asyncio
    async def test_async_data_processing_performance(self, perf_fixture):
        """Test asynchronous data processing performance."""
        _config = ConfigManager(perf_fixture.config_path)

        async def async_data_processor(data_batch):
            """Process data asynchronously."""
            processed_data = []
            for data in data_batch:
                # Simulate async processing
                await asyncio.sleep(0.001)
                processed_data.append({
                    **data,
                    'processed': True,
                    'processed_at': time.time()
                })
            return processed_data

        # Generate test data
        test_batches = []
        for batch_id in range(10):
            batch = []
            for i in range(100):
                batch.append({
                    'id': f'{batch_id}_{i}',
                    'data': f'test_data_{batch_id}_{i}','timestamp': time.time()
                })
            test_batches.append(batch)

        with perf_fixture.performance_context("async_processing", 1000):
            # Process batches concurrently
            tasks = []
            for batch in test_batches:
                task = asyncio.create_task(async_data_processor(batch))
                tasks.append(task)

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks)

        # Verify async processing performance
        metrics = perf_fixture.metrics[-1]
        assert metrics.throughput >= 100,f"Async processing throughput too low: {metrics.throughput}"
        assert len(results) == 10, "Not all batches processed"

    @pytest.mark.asyncio
    async def test_async_concurrent_operations(self, perf_fixture):
        """Test concurrent async operations performance."""
        _config = ConfigManager(perf_fixture.config_path)

        async def async_operation(operation_id, duration=0.1):
            """Simulate async operation."""
            await asyncio.sleep(duration)
            return f"Operation {operation_id} completed"

        # Test different concurrency levels
        concurrency_levels = [10, 50, 100]

        for concurrency in concurrency_levels:
            with perf_fixture.performance_context(f"async_concurrent_{concurrency}",concurrency):
                # Start concurrent operations
                tasks = []
                for i in range(concurrency):
                    task = asyncio.create_task(async_operation(i, 0.01))
                    tasks.append(task)

                # Wait for completion
                results = await asyncio.gather(*tasks)

            # Verify concurrent performance
            metrics = perf_fixture.metrics[-1]
            assert len(results) == concurrency, "Not all operations completed"
            assert metrics.duration < 1.0,f"Concurrent operations too slow: {metrics.duration}s"


class TestStressTest:
    """Stress testing for system limits."""

    def test_maximum_concurrent_connections(self, perf_fixture):
        """Test maximum concurrent connections handling."""
        _config = ConfigManager(perf_fixture.config_path)

        # Start WebUI server
        server = WebUIServer(config)
        server.start()
        port = server.get_port()

        try:
            # Test increasing connection counts
            connection_counts = [50, 100, 200]

            for connection_count in connection_counts:
                successful_connections = 0

                with perf_fixture.performance_context(f"max_connections_{connection_count}",connection_count):
                    def make_connection(conn_id):
                        try:
                            response = requests.get(f"http://127.0.0.1:{port}/api/status",
                                timeout=10)
                            return response.status_code == 200
                        except Exception:
                            return False

                    # Start concurrent connections
                    with ThreadPoolExecutor(max_workers=connection_count) as executor:
                        futures = []
                        for i in range(connection_count):
                            future = executor.submit(make_connection, i)
                            futures.append(future)

                        # Count successful connections
                        successful_connections = sum(1 for future in futures if future.result())

                # Update metrics
                metrics = perf_fixture.metrics[-1]
                metrics.success_rate = successful_connections / connection_count
                metrics.error_count = connection_count - successful_connections

            # Verify stress test results
            for metrics in perf_fixture.metrics:
                if 'max_connections' in metrics.name:
                    # Should handle reasonable connection loads
                    if '50' in metrics.name or '100' in metrics.name:
                        assert metrics.success_rate >= 0.95,f"Connection success rate too low: {metrics.success_rate}"

        finally:
            server.stop()

    def test_memory_leak_detection(self, perf_fixture):
        """Test for memory leaks under sustained load."""
        _config = ConfigManager(perf_fixture.config_path)

        # Monitor memory usage over time
        memory_samples = []

        def collect_memory_sample():
            process = psutil.Process(os.getpid())
            return process.memory_info().rss

        # Initial memory baseline
        _initial_memory = collect_memory_sample()

        with perf_fixture.performance_context("memory_leak_test", 1000):
            # Sustained operations
            persistence = PersistenceManager(config)
            persistence.initialize()

            for cycle in range(10):
                # Simulate work cycle
                test_data = []
                for i in range(100):
                    test_data.append({
                        'ssid': f'MemoryLeakTest{cycle}_{i}',
                        'bssid': f'00:11:22:33:{cycle:02d}:{i%256:02d}',
                        'signal_strength': -50,
                        'frequency': 2412,
                        'timestamp': int(time.time())
                    })

                persistence.bulk_insert_networks(test_data)

                # Sample memory usage
                memory_samples.append(collect_memory_sample())

                # Brief pause
                time.sleep(0.1)

        # Analyze memory usage trend
        if len(memory_samples) > 1:
            memory_growth = (memory_samples[-1] - memory_samples[0]) / len(memory_samples)

            # Memory growth should be minimal
            assert memory_growth < 1024 * 1024,f"Potential memory leak detected: {memory_growth} bytes/cycle"


def generate_performance_report(metrics_list: List[PerformanceMetrics]) -> Dict[str,Any]:
    """Generate a comprehensive performance report."""
    report = {
        'summary': {
            'total_tests': len(metrics_list),
            'total_duration': sum(m.duration for m in metrics_list),
            'avg_throughput': statistics.mean([m.throughput for m in metrics_list if m.throughput > 0]),
                
            'avg_latency': statistics.mean([m.latency for m in metrics_list if m.latency > 0]),
                
            'overall_success_rate': statistics.mean([m.success_rate for m in metrics_list])
        },
        'detailed_results': []
    }

    for metrics in metrics_list:
        report['detailed_results'].append({
            'test_name': metrics.name,
            'duration': metrics.duration,
            'throughput': metrics.throughput,
            'latency': metrics.latency,
            'memory_usage_mb': metrics.memory_usage / (1024 * 1024),
            'cpu_usage_percent': metrics.cpu_usage,
            'success_rate': metrics.success_rate,
            'error_count': metrics.error_count
        })

    return report

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
