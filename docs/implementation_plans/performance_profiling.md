# Performance Profiling Implementation Plan

## Overview

This plan outlines the implementation of systematic performance profiling for the PiWardrive application, focusing on identifying bottlenecks, monitoring resource usage, and optimizing critical paths.

## Phase 1: Performance Monitoring Setup

### Step 1: Create Performance Monitoring Middleware

```python
# src/piwardrive/middleware/performance_monitor.py

import time
import psutil
import threading
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data structure."""
    timestamp: datetime
    endpoint: str
    method: str
    duration: float
    cpu_usage: float
    memory_usage: float
    status_code: int
    error: str = None

class PerformanceMonitor:
    """Performance monitoring and profiling class."""
    
    def __init__(self, retention_hours: int = 24):
        self.metrics: List[PerformanceMetric] = []
        self.retention_hours = retention_hours
        self.lock = threading.Lock()
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_metrics, daemon=True)
        self.cleanup_thread.start()
    
    def record_metric(self, metric: PerformanceMetric):
        """Record a performance metric."""
        with self.lock:
            self.metrics.append(metric)
    
    def get_metrics(self, hours: int = 1) -> List[PerformanceMetric]:
        """Get metrics from the last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            return [m for m in self.metrics if m.timestamp >= cutoff]
    
    def get_endpoint_stats(self, endpoint: str, hours: int = 1) -> Dict[str, Any]:
        """Get statistics for a specific endpoint."""
        metrics = [m for m in self.get_metrics(hours) if m.endpoint == endpoint]
        
        if not metrics:
            return {}
        
        durations = [m.duration for m in metrics]
        cpu_usage = [m.cpu_usage for m in metrics]
        memory_usage = [m.memory_usage for m in metrics]
        
        return {
            "count": len(metrics),
            "avg_duration": sum(durations) / len(durations),
            "max_duration": max(durations),
            "min_duration": min(durations),
            "avg_cpu": sum(cpu_usage) / len(cpu_usage),
            "max_cpu": max(cpu_usage),
            "avg_memory": sum(memory_usage) / len(memory_usage),
            "max_memory": max(memory_usage),
            "error_rate": sum(1 for m in metrics if m.error) / len(metrics) * 100
        }
    
    def get_slowest_endpoints(self, hours: int = 1, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the slowest endpoints."""
        endpoint_stats = defaultdict(list)
        
        for metric in self.get_metrics(hours):
            endpoint_stats[metric.endpoint].append(metric.duration)
        
        # Calculate average duration for each endpoint
        endpoint_averages = {
            endpoint: sum(durations) / len(durations)
            for endpoint, durations in endpoint_stats.items()
        }
        
        # Sort by average duration (slowest first)
        sorted_endpoints = sorted(
            endpoint_averages.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "endpoint": endpoint,
                "avg_duration": duration,
                "call_count": len(endpoint_stats[endpoint])
            }
            for endpoint, duration in sorted_endpoints[:limit]
        ]
    
    def _cleanup_metrics(self):
        """Cleanup old metrics periodically."""
        while True:
            time.sleep(3600)  # Run every hour
            cutoff = datetime.now() - timedelta(hours=self.retention_hours)
            
            with self.lock:
                self.metrics = [m for m in self.metrics if m.timestamp >= cutoff]
                logger.info(f"Cleaned up old metrics. Current count: {len(self.metrics)}")

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# FastAPI middleware for performance monitoring
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
import asyncio

class PerformanceMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for performance monitoring."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Get initial resource usage
        process = psutil.Process()
        initial_cpu = process.cpu_percent()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process request
        response = await call_next(request)
        
        # Calculate metrics
        duration = time.time() - start_time
        final_cpu = process.cpu_percent()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Record metric
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            endpoint=request.url.path,
            method=request.method,
            duration=duration,
            cpu_usage=final_cpu,
            memory_usage=final_memory,
            status_code=response.status_code,
            error=None if response.status_code < 400 else f"HTTP {response.status_code}"
        )
        
        performance_monitor.record_metric(metric)
        
        # Add performance headers
        response.headers["X-Response-Time"] = str(duration)
        response.headers["X-CPU-Usage"] = str(final_cpu)
        response.headers["X-Memory-Usage"] = str(final_memory)
        
        return response
```

### Step 2: Create Performance Profiling Decorator

```python
# src/piwardrive/utils/profiler.py

import functools
import time
import cProfile
import pstats
import io
import logging
from typing import Any, Dict, Optional, Callable
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

class FunctionProfiler:
    """Function-level performance profiler."""
    
    def __init__(self, profile_dir: str = "performance_profiles"):
        self.profile_dir = Path(profile_dir)
        self.profile_dir.mkdir(exist_ok=True)
        
        # Function call statistics
        self.call_stats: Dict[str, Dict[str, Any]] = {}
    
    def profile(self, func_name: Optional[str] = None, save_profile: bool = False):
        """Decorator for profiling function performance."""
        def decorator(func: Callable) -> Callable:
            name = func_name or f"{func.__module__}.{func.__name__}"
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                if save_profile:
                    # Use cProfile for detailed profiling
                    pr = cProfile.Profile()
                    pr.enable()
                    
                    result = func(*args, **kwargs)
                    
                    pr.disable()
                    
                    # Save profile data
                    profile_path = self.profile_dir / f"{name}_{int(time.time())}.prof"
                    pr.dump_stats(str(profile_path))
                    
                    # Generate stats report
                    s = io.StringIO()
                    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                    ps.print_stats()
                    
                    stats_path = self.profile_dir / f"{name}_{int(time.time())}.txt"
                    with open(stats_path, 'w') as f:
                        f.write(s.getvalue())
                    
                    logger.info(f"Profile saved: {profile_path}")
                else:
                    result = func(*args, **kwargs)
                
                duration = time.time() - start_time
                
                # Update call statistics
                if name not in self.call_stats:
                    self.call_stats[name] = {
                        "call_count": 0,
                        "total_time": 0.0,
                        "min_time": float('inf'),
                        "max_time": 0.0
                    }
                
                stats = self.call_stats[name]
                stats["call_count"] += 1
                stats["total_time"] += duration
                stats["min_time"] = min(stats["min_time"], duration)
                stats["max_time"] = max(stats["max_time"], duration)
                stats["avg_time"] = stats["total_time"] / stats["call_count"]
                
                # Log slow calls
                if duration > 1.0:  # Log calls taking more than 1 second
                    logger.warning(f"Slow function call: {name} took {duration:.2f}s")
                
                return result
            
            return wrapper
        return decorator
    
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get function call statistics."""
        return self.call_stats.copy()
    
    def reset_stats(self):
        """Reset function call statistics."""
        self.call_stats.clear()

# Global profiler instance
profiler = FunctionProfiler()

# Context manager for profiling code blocks
@contextmanager
def profile_block(name: str, save_profile: bool = False):
    """Context manager for profiling code blocks."""
    start_time = time.time()
    
    if save_profile:
        pr = cProfile.Profile()
        pr.enable()
    
    try:
        yield
    finally:
        if save_profile:
            pr.disable()
            
            profile_path = profiler.profile_dir / f"{name}_{int(time.time())}.prof"
            pr.dump_stats(str(profile_path))
            
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats()
            
            stats_path = profiler.profile_dir / f"{name}_{int(time.time())}.txt"
            with open(stats_path, 'w') as f:
                f.write(s.getvalue())
        
        duration = time.time() - start_time
        logger.info(f"Profile block '{name}' completed in {duration:.2f}s")

# Profiling decorator for async functions
def async_profile(func_name: Optional[str] = None, save_profile: bool = False):
    """Decorator for profiling async function performance."""
    def decorator(func: Callable) -> Callable:
        name = func_name or f"{func.__module__}.{func.__name__}"
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = await func(*args, **kwargs)
            
            duration = time.time() - start_time
            
            # Update call statistics
            if name not in profiler.call_stats:
                profiler.call_stats[name] = {
                    "call_count": 0,
                    "total_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0
                }
            
            stats = profiler.call_stats[name]
            stats["call_count"] += 1
            stats["total_time"] += duration
            stats["min_time"] = min(stats["min_time"], duration)
            stats["max_time"] = max(stats["max_time"], duration)
            stats["avg_time"] = stats["total_time"] / stats["call_count"]
            
            # Log slow calls
            if duration > 1.0:
                logger.warning(f"Slow async function call: {name} took {duration:.2f}s")
            
            return result
        
        return wrapper
    return decorator
```

### Step 3: Create Performance API Endpoints

```python
# src/piwardrive/api/performance.py

from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import psutil
import gc

from piwardrive.api.auth import AUTH_DEP
from piwardrive.middleware.performance_monitor import performance_monitor
from piwardrive.utils.profiler import profiler

router = APIRouter(
    prefix="/performance",
    tags=["Performance"],
    dependencies=[Depends(AUTH_DEP)],
)

@router.get("/metrics")
async def get_performance_metrics(
    hours: int = Query(1, description="Number of hours to look back"),
    endpoint: Optional[str] = Query(None, description="Filter by endpoint")
):
    """Get performance metrics for the specified time period."""
    metrics = performance_monitor.get_metrics(hours)
    
    if endpoint:
        metrics = [m for m in metrics if m.endpoint == endpoint]
    
    # Convert to JSON-serializable format
    result = []
    for metric in metrics:
        result.append({
            "timestamp": metric.timestamp.isoformat(),
            "endpoint": metric.endpoint,
            "method": metric.method,
            "duration": metric.duration,
            "cpu_usage": metric.cpu_usage,
            "memory_usage": metric.memory_usage,
            "status_code": metric.status_code,
            "error": metric.error
        })
    
    return {
        "success": True,
        "data": {
            "metrics": result,
            "count": len(result),
            "time_range_hours": hours
        }
    }

@router.get("/stats")
async def get_performance_stats(
    hours: int = Query(1, description="Number of hours to look back")
):
    """Get aggregated performance statistics."""
    metrics = performance_monitor.get_metrics(hours)
    
    if not metrics:
        return {
            "success": True,
            "data": {
                "total_requests": 0,
                "avg_response_time": 0,
                "error_rate": 0
            }
        }
    
    # Calculate statistics
    total_requests = len(metrics)
    avg_response_time = sum(m.duration for m in metrics) / total_requests
    error_count = sum(1 for m in metrics if m.error)
    error_rate = (error_count / total_requests) * 100
    
    # Get endpoint statistics
    endpoint_stats = {}
    for metric in metrics:
        if metric.endpoint not in endpoint_stats:
            endpoint_stats[metric.endpoint] = performance_monitor.get_endpoint_stats(
                metric.endpoint, hours
            )
    
    return {
        "success": True,
        "data": {
            "total_requests": total_requests,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate,
            "slowest_endpoints": performance_monitor.get_slowest_endpoints(hours, 10),
            "endpoint_stats": endpoint_stats
        }
    }

@router.get("/system")
async def get_system_performance():
    """Get current system performance metrics."""
    # CPU information
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    
    # Memory information
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Disk information
    disk_usage = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    
    # Network information
    network_io = psutil.net_io_counters()
    
    # Process information
    process = psutil.Process()
    process_memory = process.memory_info()
    process_cpu = process.cpu_percent()
    
    return {
        "success": True,
        "data": {
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count,
                "frequency": {
                    "current": cpu_freq.current if cpu_freq else None,
                    "min": cpu_freq.min if cpu_freq else None,
                    "max": cpu_freq.max if cpu_freq else None
                }
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free,
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent
                }
            },
            "disk": {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": (disk_usage.used / disk_usage.total) * 100,
                "io": {
                    "read_bytes": disk_io.read_bytes if disk_io else None,
                    "write_bytes": disk_io.write_bytes if disk_io else None,
                    "read_count": disk_io.read_count if disk_io else None,
                    "write_count": disk_io.write_count if disk_io else None
                }
            },
            "network": {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv,
                "packets_sent": network_io.packets_sent,
                "packets_recv": network_io.packets_recv
            },
            "process": {
                "cpu_percent": process_cpu,
                "memory_rss": process_memory.rss,
                "memory_vms": process_memory.vms,
                "memory_percent": process.memory_percent()
            }
        }
    }

@router.get("/functions")
async def get_function_stats():
    """Get function call statistics."""
    stats = profiler.get_stats()
    
    return {
        "success": True,
        "data": {
            "functions": stats,
            "count": len(stats)
        }
    }

@router.post("/gc")
async def force_garbage_collection():
    """Force garbage collection and return memory stats."""
    # Get memory before GC
    process = psutil.Process()
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Force garbage collection
    collected = gc.collect()
    
    # Get memory after GC
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    memory_freed = memory_before - memory_after
    
    return {
        "success": True,
        "data": {
            "objects_collected": collected,
            "memory_before_mb": memory_before,
            "memory_after_mb": memory_after,
            "memory_freed_mb": memory_freed
        }
    }

@router.post("/reset-stats")
async def reset_performance_stats():
    """Reset function call statistics."""
    profiler.reset_stats()
    
    return {
        "success": True,
        "data": {
            "message": "Performance statistics reset"
        }
    }
```

## Phase 2: Database Performance Monitoring

### Step 1: Create Database Performance Monitor

```python
# src/piwardrive/db/performance_monitor.py

import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from contextlib import contextmanager
import sqlite3

logger = logging.getLogger(__name__)

@dataclass
class QueryMetric:
    """Database query performance metric."""
    timestamp: datetime
    query: str
    duration: float
    rows_affected: int
    connection_id: str
    error: Optional[str] = None

class DatabasePerformanceMonitor:
    """Database performance monitoring."""
    
    def __init__(self):
        self.query_metrics: List[QueryMetric] = []
        self.slow_query_threshold = 1.0  # seconds
    
    @contextmanager
    def monitor_query(self, query: str, connection_id: str = "default"):
        """Context manager for monitoring database queries."""
        start_time = time.time()
        rows_affected = 0
        error = None
        
        try:
            yield
        except Exception as e:
            error = str(e)
            raise
        finally:
            duration = time.time() - start_time
            
            metric = QueryMetric(
                timestamp=datetime.now(),
                query=query[:200] + "..." if len(query) > 200 else query,
                duration=duration,
                rows_affected=rows_affected,
                connection_id=connection_id,
                error=error
            )
            
            self.query_metrics.append(metric)
            
            # Log slow queries
            if duration > self.slow_query_threshold:
                logger.warning(f"Slow query detected: {duration:.2f}s - {query[:100]}...")
    
    def get_slow_queries(self, threshold: float = None) -> List[QueryMetric]:
        """Get queries that exceeded the threshold."""
        threshold = threshold or self.slow_query_threshold
        return [m for m in self.query_metrics if m.duration > threshold]
    
    def get_query_stats(self) -> Dict[str, Any]:
        """Get query statistics."""
        if not self.query_metrics:
            return {}
        
        durations = [m.duration for m in self.query_metrics]
        
        return {
            "total_queries": len(self.query_metrics),
            "avg_duration": sum(durations) / len(durations),
            "max_duration": max(durations),
            "min_duration": min(durations),
            "slow_queries": len(self.get_slow_queries()),
            "error_count": sum(1 for m in self.query_metrics if m.error)
        }

# Global database performance monitor
db_performance_monitor = DatabasePerformanceMonitor()

# SQLite connection wrapper with performance monitoring
class MonitoredSQLiteConnection:
    """SQLite connection wrapper with performance monitoring."""
    
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection_id = id(self.connection)
    
    def execute(self, query: str, parameters=None):
        """Execute a query with performance monitoring."""
        with db_performance_monitor.monitor_query(query, str(self.connection_id)):
            if parameters:
                return self.connection.execute(query, parameters)
            else:
                return self.connection.execute(query)
    
    def executemany(self, query: str, parameters):
        """Execute multiple queries with performance monitoring."""
        with db_performance_monitor.monitor_query(f"BULK: {query}", str(self.connection_id)):
            return self.connection.executemany(query, parameters)
    
    def __getattr__(self, name):
        """Delegate other attributes to the wrapped connection."""
        return getattr(self.connection, name)
```

## Phase 3: Memory Profiling

### Step 1: Create Memory Profiler

```python
# src/piwardrive/utils/memory_profiler.py

import tracemalloc
import gc
import psutil
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@dataclass
class MemorySnapshot:
    """Memory usage snapshot."""
    timestamp: datetime
    rss_mb: float
    vms_mb: float
    percent: float
    available_mb: float
    tracemalloc_mb: Optional[float] = None
    top_traces: Optional[List[Dict[str, Any]]] = None

class MemoryProfiler:
    """Memory profiling and monitoring."""
    
    def __init__(self, enable_tracemalloc: bool = True):
        self.snapshots: List[MemorySnapshot] = []
        self.enable_tracemalloc = enable_tracemalloc
        
        if enable_tracemalloc:
            tracemalloc.start()
    
    def take_snapshot(self) -> MemorySnapshot:
        """Take a memory usage snapshot."""
        process = psutil.Process()
        memory_info = process.memory_info()
        system_memory = psutil.virtual_memory()
        
        snapshot = MemorySnapshot(
            timestamp=datetime.now(),
            rss_mb=memory_info.rss / 1024 / 1024,
            vms_mb=memory_info.vms / 1024 / 1024,
            percent=process.memory_percent(),
            available_mb=system_memory.available / 1024 / 1024
        )
        
        if self.enable_tracemalloc and tracemalloc.is_tracing():
            current_trace = tracemalloc.take_snapshot()
            snapshot.tracemalloc_mb = sum(stat.size for stat in current_trace.statistics('lineno')) / 1024 / 1024
            
            # Get top memory consuming code locations
            top_stats = current_trace.statistics('lineno')[:10]
            snapshot.top_traces = []
            
            for stat in top_stats:
                snapshot.top_traces.append({
                    "filename": stat.traceback.format()[-1],
                    "size_mb": stat.size / 1024 / 1024,
                    "count": stat.count
                })
        
        self.snapshots.append(snapshot)
        return snapshot
    
    def get_memory_trend(self, hours: int = 1) -> List[MemorySnapshot]:
        """Get memory usage trend over time."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=hours)
        return [s for s in self.snapshots if s.timestamp >= cutoff]
    
    def detect_memory_leaks(self) -> Dict[str, Any]:
        """Detect potential memory leaks."""
        if len(self.snapshots) < 2:
            return {"warning": "Not enough snapshots to detect leaks"}
        
        # Compare first and last snapshots
        first = self.snapshots[0]
        last = self.snapshots[-1]
        
        rss_growth = last.rss_mb - first.rss_mb
        vms_growth = last.vms_mb - first.vms_mb
        
        # Calculate growth rate
        time_diff = (last.timestamp - first.timestamp).total_seconds() / 3600  # hours
        rss_growth_rate = rss_growth / time_diff if time_diff > 0 else 0
        
        return {
            "rss_growth_mb": rss_growth,
            "vms_growth_mb": vms_growth,
            "rss_growth_rate_mb_per_hour": rss_growth_rate,
            "time_period_hours": time_diff,
            "potential_leak": rss_growth_rate > 10  # Growing more than 10MB/hour
        }
    
    @contextmanager
    def profile_block(self, name: str):
        """Context manager for profiling memory usage in a code block."""
        snapshot_before = self.take_snapshot()
        
        try:
            yield
        finally:
            snapshot_after = self.take_snapshot()
            
            memory_diff = snapshot_after.rss_mb - snapshot_before.rss_mb
            
            if memory_diff > 1:  # Log if more than 1MB difference
                logger.info(f"Memory usage in '{name}': {memory_diff:.2f}MB")
            
            return {
                "name": name,
                "memory_before_mb": snapshot_before.rss_mb,
                "memory_after_mb": snapshot_after.rss_mb,
                "memory_diff_mb": memory_diff
            }

# Global memory profiler
memory_profiler = MemoryProfiler()

# Memory profiling decorator
def profile_memory(func_name: Optional[str] = None):
    """Decorator for memory profiling."""
    def decorator(func):
        import functools
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func_name or f"{func.__module__}.{func.__name__}"
            
            with memory_profiler.profile_block(name):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

## Phase 4: Load Testing Framework

### Step 1: Create Load Testing Script

```python
# tools/performance/load_test.py

import asyncio
import aiohttp
import time
import json
import argparse
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import statistics

@dataclass
class LoadTestResult:
    """Load test result data."""
    endpoint: str
    method: str
    response_time: float
    status_code: int
    error: str = None

class LoadTester:
    """Load testing framework."""
    
    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.results: List[LoadTestResult] = []
    
    async def make_request(self, session: aiohttp.ClientSession, endpoint: str, method: str = "GET") -> LoadTestResult:
        """Make a single HTTP request."""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        start_time = time.time()
        
        try:
            async with session.request(method, url, headers=headers) as response:
                await response.text()  # Read response body
                
                return LoadTestResult(
                    endpoint=endpoint,
                    method=method,
                    response_time=time.time() - start_time,
                    status_code=response.status
                )
        except Exception as e:
            return LoadTestResult(
                endpoint=endpoint,
                method=method,
                response_time=time.time() - start_time,
                status_code=0,
                error=str(e)
            )
    
    async def run_load_test(self, endpoint: str, concurrent_users: int, requests_per_user: int, method: str = "GET"):
        """Run load test for a single endpoint."""
        print(f"Starting load test: {concurrent_users} users, {requests_per_user} requests each")
        
        async with aiohttp.ClientSession() as session:
            # Create tasks for all requests
            tasks = []
            
            for user in range(concurrent_users):
                for request in range(requests_per_user):
                    task = self.make_request(session, endpoint, method)
                    tasks.append(task)
            
            # Execute all requests
            results = await asyncio.gather(*tasks)
            self.results.extend(results)
    
    def analyze_results(self) -> Dict[str, Any]:
        """Analyze load test results."""
        if not self.results:
            return {}
        
        response_times = [r.response_time for r in self.results]
        status_codes = [r.status_code for r in self.results]
        errors = [r for r in self.results if r.error]
        
        return {
            "total_requests": len(self.results),
            "successful_requests": len([r for r in self.results if r.status_code == 200]),
            "failed_requests": len([r for r in self.results if r.status_code != 200]),
            "error_count": len(errors),
            "error_rate": len(errors) / len(self.results) * 100,
            "response_times": {
                "min": min(response_times),
                "max": max(response_times),
                "avg": statistics.mean(response_times),
                "median": statistics.median(response_times),
                "p95": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else max(response_times),
                "p99": statistics.quantiles(response_times, n=100)[98] if len(response_times) >= 100 else max(response_times)
            },
            "status_codes": {
                code: status_codes.count(code) for code in set(status_codes)
            }
        }
    
    def generate_report(self) -> str:
        """Generate a performance report."""
        analysis = self.analyze_results()
        
        if not analysis:
            return "No results to report"
        
        report = f"""
Load Test Report
================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
- Total Requests: {analysis['total_requests']}
- Successful: {analysis['successful_requests']}
- Failed: {analysis['failed_requests']}
- Error Rate: {analysis['error_rate']:.2f}%

Response Times:
- Min: {analysis['response_times']['min']:.3f}s
- Max: {analysis['response_times']['max']:.3f}s
- Average: {analysis['response_times']['avg']:.3f}s
- Median: {analysis['response_times']['median']:.3f}s
- 95th Percentile: {analysis['response_times']['p95']:.3f}s
- 99th Percentile: {analysis['response_times']['p99']:.3f}s

Status Codes:
"""
        
        for code, count in analysis['status_codes'].items():
            report += f"- {code}: {count} requests\n"
        
        return report

async def main():
    parser = argparse.ArgumentParser(description="PiWardrive Load Testing")
    parser.add_argument("--url", default="http://localhost:8080", help="Base URL")
    parser.add_argument("--endpoint", default="/api/wifi/access-points", help="Endpoint to test")
    parser.add_argument("--users", type=int, default=10, help="Concurrent users")
    parser.add_argument("--requests", type=int, default=10, help="Requests per user")
    parser.add_argument("--method", default="GET", help="HTTP method")
    parser.add_argument("--token", help="Authentication token")
    
    args = parser.parse_args()
    
    tester = LoadTester(args.url, args.token)
    
    print(f"Testing {args.endpoint} with {args.users} concurrent users")
    
    start_time = time.time()
    await tester.run_load_test(args.endpoint, args.users, args.requests, args.method)
    total_time = time.time() - start_time
    
    print(f"\nLoad test completed in {total_time:.2f} seconds")
    print(f"Throughput: {len(tester.results) / total_time:.2f} requests/second")
    
    report = tester.generate_report()
    print(report)
    
    # Save detailed results
    with open(f"load_test_results_{int(time.time())}.json", "w") as f:
        json.dump([
            {
                "endpoint": r.endpoint,
                "method": r.method,
                "response_time": r.response_time,
                "status_code": r.status_code,
                "error": r.error
            }
            for r in tester.results
        ], f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
```

## Phase 5: Integration with Existing Codebase

### Step 1: Update Service Layer

```python
# src/piwardrive/service.py - Add performance monitoring

from piwardrive.middleware.performance_monitor import PerformanceMiddleware
from piwardrive.utils.profiler import profiler, async_profile
from piwardrive.utils.memory_profiler import memory_profiler, profile_memory

# Add middleware to FastAPI app
app.add_middleware(PerformanceMiddleware)

# Add profiling to critical functions
@app.get("/api/wifi/access-points")
@async_profile("get_access_points")
async def get_access_points():
    # Implementation with profiling
    pass

# Include performance router
from piwardrive.api.performance import router as performance_router
app.include_router(performance_router)
```

### Step 2: Create Performance Dashboard Component

```jsx
// webui/src/components/PerformanceDashboard.jsx

import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';

const PerformanceDashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [systemInfo, setSystemInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPerformanceData();
    
    // Set up periodic refresh
    const interval = setInterval(fetchPerformanceData, 30000); // 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchPerformanceData = async () => {
    try {
      const [metricsResponse, systemResponse] = await Promise.all([
        fetch('/api/performance/stats'),
        fetch('/api/performance/system')
      ]);
      
      const metricsData = await metricsResponse.json();
      const systemData = await systemResponse.json();
      
      if (metricsData.success) {
        setMetrics(metricsData.data);
      }
      
      if (systemData.success) {
        setSystemInfo(systemData.data);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching performance data:', error);
      setLoading(false);
    }
  };

  const forceGarbageCollection = async () => {
    try {
      const response = await fetch('/api/performance/gc', { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        alert(`Garbage collection completed. Freed ${data.data.memory_freed_mb.toFixed(2)} MB`);
        fetchPerformanceData(); // Refresh data
      }
    } catch (error) {
      console.error('Error forcing garbage collection:', error);
    }
  };

  if (loading) {
    return <div>Loading performance data...</div>;
  }

  return (
    <div className="performance-dashboard">
      <h2>Performance Dashboard</h2>
      
      {/* System Overview */}
      <div className="row">
        <div className="col-md-3">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">CPU Usage</h5>
              <h3 className="text-primary">{systemInfo?.cpu.percent.toFixed(1)}%</h3>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Memory Usage</h5>
              <h3 className="text-info">{systemInfo?.memory.percent.toFixed(1)}%</h3>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Disk Usage</h5>
              <h3 className="text-warning">{systemInfo?.disk.percent.toFixed(1)}%</h3>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Avg Response Time</h5>
              <h3 className="text-success">{metrics?.avg_response_time.toFixed(3)}s</h3>
            </div>
          </div>
        </div>
      </div>

      {/* API Performance */}
      <div className="row mt-4">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5>Slowest Endpoints</h5>
            </div>
            <div className="card-body">
              <table className="table">
                <thead>
                  <tr>
                    <th>Endpoint</th>
                    <th>Avg Duration</th>
                    <th>Calls</th>
                  </tr>
                </thead>
                <tbody>
                  {metrics?.slowest_endpoints.map((endpoint, index) => (
                    <tr key={index}>
                      <td>{endpoint.endpoint}</td>
                      <td>{endpoint.avg_duration.toFixed(3)}s</td>
                      <td>{endpoint.call_count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h5>System Actions</h5>
            </div>
            <div className="card-body">
              <button className="btn btn-warning" onClick={forceGarbageCollection}>
                Force Garbage Collection
              </button>
              <button className="btn btn-info ms-2" onClick={fetchPerformanceData}>
                Refresh Data
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceDashboard;
```

This implementation provides:

1. **Real-time Performance Monitoring**: Middleware that tracks all API requests
2. **Function-level Profiling**: Decorators for profiling specific functions
3. **Memory Profiling**: Tools to track memory usage and detect leaks
4. **Load Testing**: Framework for testing system performance under load
5. **Database Monitoring**: Performance tracking for database queries
6. **Performance Dashboard**: React component for visualizing performance metrics
7. **System Resource Monitoring**: CPU, memory, disk, and network usage tracking

The system provides comprehensive performance insights that can help identify bottlenecks and optimize the application.
