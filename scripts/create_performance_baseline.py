#!/usr/bin/env python3
"""
Performance Baseline Creation Script

This script creates performance baseline measurements for regression testing.
"""

import asyncio
import json
import time
import psutil
import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from piwardrive.performance import DatabaseOptimizer, AsyncOptimizer, RealtimeOptimizer


class PerformanceBaseline:
    """Creates and manages performance baselines."""
    
    def __init__(self, baseline_file: str = "performance_baseline.json"):
        self.baseline_file = Path(baseline_file)
        self.results = {}
        
    async def run_database_benchmarks(self) -> Dict[str, Any]:
        """Run database performance benchmarks."""
        print("Running database benchmarks...")
        
        db_optimizer = DatabaseOptimizer(":memory:")
        
        # Create test data
        await self._create_test_data(db_optimizer)
        
        # Run benchmarks
        query_times = []
        insert_times = []
        update_times = []
        
        # Query benchmark
        for _ in range(100):
            start_time = time.perf_counter()
            stats = db_optimizer.get_stats()
            end_time = time.perf_counter()
            query_times.append(end_time - start_time)
        
        # Insert benchmark
        for i in range(100):
            start_time = time.perf_counter()
            # Simulate insert operation
            await asyncio.sleep(0.001)  # Simulate DB operation
            end_time = time.perf_counter()
            insert_times.append(end_time - start_time)
        
        # Update benchmark
        for i in range(100):
            start_time = time.perf_counter()
            # Simulate update operation
            await asyncio.sleep(0.001)  # Simulate DB operation
            end_time = time.perf_counter()
            update_times.append(end_time - start_time)
        
        return {
            "query_performance": {
                "mean": statistics.mean(query_times),
                "median": statistics.median(query_times),
                "p95": statistics.quantiles(query_times, n=20)[18],  # 95th percentile
                "p99": statistics.quantiles(query_times, n=100)[98],  # 99th percentile
                "min": min(query_times),
                "max": max(query_times),
                "std_dev": statistics.stdev(query_times)
            },
            "insert_performance": {
                "mean": statistics.mean(insert_times),
                "median": statistics.median(insert_times),
                "p95": statistics.quantiles(insert_times, n=20)[18],
                "p99": statistics.quantiles(insert_times, n=100)[98],
                "min": min(insert_times),
                "max": max(insert_times),
                "std_dev": statistics.stdev(insert_times)
            },
            "update_performance": {
                "mean": statistics.mean(update_times),
                "median": statistics.median(update_times),
                "p95": statistics.quantiles(update_times, n=20)[18],
                "p99": statistics.quantiles(update_times, n=100)[98],
                "min": min(update_times),
                "max": max(update_times),
                "std_dev": statistics.stdev(update_times)
            }
        }
    
    async def _create_test_data(self, db_optimizer):
        """Create test data for benchmarks."""
        # This would create test data in the database
        pass
    
    async def run_async_benchmarks(self) -> Dict[str, Any]:
        """Run async performance benchmarks."""
        print("Running async benchmarks...")
        
        async_optimizer = AsyncOptimizer()
        
        # Task completion times
        task_times = []
        
        for _ in range(100):
            start_time = time.perf_counter()
            
            async with async_optimizer.monitor_operation("benchmark_task") as monitor:
                await asyncio.sleep(0.01)  # Simulate async work
                monitor.success()
            
            end_time = time.perf_counter()
            task_times.append(end_time - start_time)
        
        # Batch processing benchmark
        batch_times = []
        batch_sizes = [10, 50, 100, 200]
        
        for batch_size in batch_sizes:
            items = list(range(batch_size))
            start_time = time.perf_counter()
            
            # Simulate batch processing
            await asyncio.gather(*[asyncio.sleep(0.001) for _ in items])
            
            end_time = time.perf_counter()
            batch_times.append({
                "batch_size": batch_size,
                "total_time": end_time - start_time,
                "time_per_item": (end_time - start_time) / batch_size
            })
        
        return {
            "task_performance": {
                "mean": statistics.mean(task_times),
                "median": statistics.median(task_times),
                "p95": statistics.quantiles(task_times, n=20)[18],
                "p99": statistics.quantiles(task_times, n=100)[98],
                "min": min(task_times),
                "max": max(task_times),
                "std_dev": statistics.stdev(task_times)
            },
            "batch_performance": batch_times
        }
    
    async def run_realtime_benchmarks(self) -> Dict[str, Any]:
        """Run real-time performance benchmarks."""
        print("Running real-time benchmarks...")
        
        rt_optimizer = RealtimeOptimizer()
        
        # Message processing times
        message_times = []
        
        for _ in range(100):
            start_time = time.perf_counter()
            
            # Simulate message processing
            await asyncio.sleep(0.005)  # Simulate message handling
            
            end_time = time.perf_counter()
            message_times.append(end_time - start_time)
        
        # Connection handling benchmark
        connection_times = []
        
        for _ in range(50):
            start_time = time.perf_counter()
            
            # Simulate connection handling
            await asyncio.sleep(0.002)  # Simulate connection setup
            
            end_time = time.perf_counter()
            connection_times.append(end_time - start_time)
        
        return {
            "message_performance": {
                "mean": statistics.mean(message_times),
                "median": statistics.median(message_times),
                "p95": statistics.quantiles(message_times, n=20)[18],
                "p99": statistics.quantiles(message_times, n=100)[98],
                "min": min(message_times),
                "max": max(message_times),
                "std_dev": statistics.stdev(message_times)
            },
            "connection_performance": {
                "mean": statistics.mean(connection_times),
                "median": statistics.median(connection_times),
                "p95": statistics.quantiles(connection_times, n=20)[18],
                "p99": statistics.quantiles(connection_times, n=100)[98],
                "min": min(connection_times),
                "max": max(connection_times),
                "std_dev": statistics.stdev(connection_times)
            }
        }
    
    async def run_memory_benchmarks(self) -> Dict[str, Any]:
        """Run memory usage benchmarks."""
        print("Running memory benchmarks...")
        
        process = psutil.Process()
        
        # Initial memory usage
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Memory usage during operations
        memory_readings = []
        
        for _ in range(100):
            # Simulate memory-intensive operation
            data = [i for i in range(1000)]
            memory_readings.append(process.memory_info().rss / 1024 / 1024)
            del data
        
        # Final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_growth_mb": final_memory - initial_memory,
            "peak_memory_mb": max(memory_readings),
            "average_memory_mb": statistics.mean(memory_readings),
            "memory_variance": statistics.variance(memory_readings)
        }
    
    async def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all performance benchmarks."""
        print("Creating performance baseline...")
        
        start_time = time.perf_counter()
        
        # System information
        system_info = {
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": psutil.virtual_memory().total / 1024 / 1024 / 1024,
            "platform": sys.platform,
            "python_version": sys.version,
            "timestamp": datetime.now().isoformat()
        }
        
        # Run benchmarks
        benchmarks = {}
        
        try:
            benchmarks["database"] = await self.run_database_benchmarks()
        except Exception as e:
            print(f"Database benchmark failed: {e}")
            benchmarks["database"] = {"error": str(e)}
        
        try:
            benchmarks["async"] = await self.run_async_benchmarks()
        except Exception as e:
            print(f"Async benchmark failed: {e}")
            benchmarks["async"] = {"error": str(e)}
        
        try:
            benchmarks["realtime"] = await self.run_realtime_benchmarks()
        except Exception as e:
            print(f"Realtime benchmark failed: {e}")
            benchmarks["realtime"] = {"error": str(e)}
        
        try:
            benchmarks["memory"] = await self.run_memory_benchmarks()
        except Exception as e:
            print(f"Memory benchmark failed: {e}")
            benchmarks["memory"] = {"error": str(e)}
        
        end_time = time.perf_counter()
        
        return {
            "system_info": system_info,
            "benchmarks": benchmarks,
            "total_benchmark_time": end_time - start_time,
            "baseline_version": "1.0.0",
            "created_at": datetime.now().isoformat()
        }
    
    async def create_baseline(self):
        """Create and save performance baseline."""
        results = await self.run_all_benchmarks()
        
        # Save to file
        with open(self.baseline_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Performance baseline created: {self.baseline_file}")
        print(f"Total benchmark time: {results['total_benchmark_time']:.2f}s")
        
        return results
    
    def load_baseline(self) -> Optional[Dict[str, Any]]:
        """Load existing baseline."""
        if not self.baseline_file.exists():
            return None
        
        with open(self.baseline_file, 'r') as f:
            return json.load(f)
    
    def compare_with_baseline(self, current_results: Dict[str, Any], baseline: Dict[str, Any]) -> Dict[str, Any]:
        """Compare current results with baseline."""
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "regression_detected": False,
            "regressions": [],
            "improvements": [],
            "status": "unchanged"
        }
        
        # Compare database performance
        if "database" in current_results["benchmarks"] and "database" in baseline["benchmarks"]:
            db_comparison = self._compare_database_performance(
                current_results["benchmarks"]["database"],
                baseline["benchmarks"]["database"]
            )
            comparison["database"] = db_comparison
            
            if db_comparison.get("regression_detected"):
                comparison["regression_detected"] = True
                comparison["regressions"].extend(db_comparison["regressions"])
        
        # Compare async performance
        if "async" in current_results["benchmarks"] and "async" in baseline["benchmarks"]:
            async_comparison = self._compare_async_performance(
                current_results["benchmarks"]["async"],
                baseline["benchmarks"]["async"]
            )
            comparison["async"] = async_comparison
            
            if async_comparison.get("regression_detected"):
                comparison["regression_detected"] = True
                comparison["regressions"].extend(async_comparison["regressions"])
        
        # Compare memory performance
        if "memory" in current_results["benchmarks"] and "memory" in baseline["benchmarks"]:
            memory_comparison = self._compare_memory_performance(
                current_results["benchmarks"]["memory"],
                baseline["benchmarks"]["memory"]
            )
            comparison["memory"] = memory_comparison
            
            if memory_comparison.get("regression_detected"):
                comparison["regression_detected"] = True
                comparison["regressions"].extend(memory_comparison["regressions"])
        
        # Set overall status
        if comparison["regression_detected"]:
            comparison["status"] = "regression"
        elif comparison["improvements"]:
            comparison["status"] = "improvement"
        
        return comparison
    
    def _compare_database_performance(self, current: Dict[str, Any], baseline: Dict[str, Any]) -> Dict[str, Any]:
        """Compare database performance metrics."""
        comparison = {
            "regression_detected": False,
            "regressions": [],
            "improvements": []
        }
        
        # Compare query performance
        if "query_performance" in current and "query_performance" in baseline:
            current_p95 = current["query_performance"]["p95"]
            baseline_p95 = baseline["query_performance"]["p95"]
            
            # Consider 20% increase as regression
            if current_p95 > baseline_p95 * 1.2:
                comparison["regression_detected"] = True
                comparison["regressions"].append(
                    f"Query P95 regression: {current_p95:.4f}s vs {baseline_p95:.4f}s baseline"
                )
            elif current_p95 < baseline_p95 * 0.8:
                comparison["improvements"].append(
                    f"Query P95 improvement: {current_p95:.4f}s vs {baseline_p95:.4f}s baseline"
                )
        
        return comparison
    
    def _compare_async_performance(self, current: Dict[str, Any], baseline: Dict[str, Any]) -> Dict[str, Any]:
        """Compare async performance metrics."""
        comparison = {
            "regression_detected": False,
            "regressions": [],
            "improvements": []
        }
        
        # Compare task performance
        if "task_performance" in current and "task_performance" in baseline:
            current_mean = current["task_performance"]["mean"]
            baseline_mean = baseline["task_performance"]["mean"]
            
            # Consider 20% increase as regression
            if current_mean > baseline_mean * 1.2:
                comparison["regression_detected"] = True
                comparison["regressions"].append(
                    f"Async task regression: {current_mean:.4f}s vs {baseline_mean:.4f}s baseline"
                )
            elif current_mean < baseline_mean * 0.8:
                comparison["improvements"].append(
                    f"Async task improvement: {current_mean:.4f}s vs {baseline_mean:.4f}s baseline"
                )
        
        return comparison
    
    def _compare_memory_performance(self, current: Dict[str, Any], baseline: Dict[str, Any]) -> Dict[str, Any]:
        """Compare memory performance metrics."""
        comparison = {
            "regression_detected": False,
            "regressions": [],
            "improvements": []
        }
        
        # Compare memory growth
        if "memory_growth_mb" in current and "memory_growth_mb" in baseline:
            current_growth = current["memory_growth_mb"]
            baseline_growth = baseline["memory_growth_mb"]
            
            # Consider 50% increase as regression
            if current_growth > baseline_growth * 1.5:
                comparison["regression_detected"] = True
                comparison["regressions"].append(
                    f"Memory growth regression: {current_growth:.2f}MB vs {baseline_growth:.2f}MB baseline"
                )
            elif current_growth < baseline_growth * 0.5:
                comparison["improvements"].append(
                    f"Memory growth improvement: {current_growth:.2f}MB vs {baseline_growth:.2f}MB baseline"
                )
        
        return comparison


async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create performance baseline')
    parser.add_argument('--output', default='performance_baseline.json', help='Output file for baseline')
    parser.add_argument('--compare', help='Compare with existing baseline file')
    parser.add_argument('--threshold', type=float, default=20.0, help='Regression threshold percentage')
    
    args = parser.parse_args()
    
    baseline_creator = PerformanceBaseline(args.output)
    
    if args.compare:
        # Load comparison baseline
        comparison_baseline = baseline_creator.load_baseline()
        if not comparison_baseline:
            print(f"Baseline file not found: {args.compare}")
            return 1
        
        # Run current benchmarks
        current_results = await baseline_creator.run_all_benchmarks()
        
        # Compare results
        comparison = baseline_creator.compare_with_baseline(current_results, comparison_baseline)
        
        # Output results
        print(json.dumps(comparison, indent=2))
        
        # Exit with error if regression detected
        if comparison["regression_detected"]:
            print("❌ Performance regression detected!")
            return 1
        else:
            print("✅ No performance regression detected")
            return 0
    else:
        # Create new baseline
        results = await baseline_creator.create_baseline()
        print("✅ Performance baseline created successfully")
        return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
