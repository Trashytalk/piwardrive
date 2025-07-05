# Performance Tuning Guide

This guide covers performance optimization strategies for PiWardrive, including database optimization, application tuning, and load testing methodologies.

## Overview

PiWardrive performance optimization focuses on several key areas:
- **Database performance**: Query optimization, indexing, and connection management
- **Application performance**: Async operations, caching, and resource management
- **Hardware optimization**: CPU, memory, and storage optimization
- **Network performance**: Bandwidth optimization and connection pooling

## Database Performance Tuning

### SQLite Optimization

#### Journal Mode Configuration
```python
# Configure SQLite for optimal performance
async def configure_database_performance():
    async with aiosqlite.connect(db_path) as conn:
        # Use WAL mode for better concurrency
        await conn.execute("PRAGMA journal_mode=WAL")
        
        # Increase cache size (in KB)
        await conn.execute("PRAGMA cache_size=10000")
        
        # Optimize synchronous mode
        await conn.execute("PRAGMA synchronous=NORMAL")
        
        # Enable memory-mapped I/O
        await conn.execute("PRAGMA mmap_size=268435456")  # 256MB
        
        # Optimize temp storage
        await conn.execute("PRAGMA temp_store=MEMORY")
        
        # Set busy timeout
        await conn.execute("PRAGMA busy_timeout=30000")
```

#### Query Optimization

**Efficient Queries**
```python
# Good: Using indexes effectively
async def get_recent_networks(limit: int = 100):
    async with aiosqlite.connect(db_path) as conn:
        cursor = await conn.execute("""
            SELECT bssid, ssid, signal_strength, last_seen
            FROM wifi_networks 
            WHERE last_seen > datetime('now', '-1 hour')
            ORDER BY last_seen DESC 
            LIMIT ?
        """, (limit,))
        return await cursor.fetchall()

# Bad: Full table scan
async def get_recent_networks_bad():
    async with aiosqlite.connect(db_path) as conn:
        cursor = await conn.execute("""
            SELECT * FROM wifi_networks 
            ORDER BY datetime(last_seen) DESC
        """)
        return await cursor.fetchall()
```

**Batch Operations**
```python
async def batch_insert_networks(networks: List[Dict]):
    """Efficiently insert multiple networks using batch operations."""
    async with aiosqlite.connect(db_path) as conn:
        await conn.execute("BEGIN TRANSACTION")
        try:
            await conn.executemany("""
                INSERT OR REPLACE INTO wifi_networks 
                (bssid, ssid, frequency, signal_strength, encryption, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (n['bssid'], n['ssid'], n['frequency'], 
                 n['signal_strength'], n['encryption'], n['last_seen'])
                for n in networks
            ])
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
```

#### Index Strategy

**Composite Indexes**
```sql
-- Optimize location-based queries
CREATE INDEX idx_wifi_location_time ON wifi_networks(gps_lat, gps_lon, last_seen);

-- Optimize filtering and sorting
CREATE INDEX idx_wifi_signal_time ON wifi_networks(signal_strength, last_seen);

-- Optimize text searches
CREATE INDEX idx_wifi_ssid_lower ON wifi_networks(lower(ssid));
```

**Partial Indexes**
```sql
-- Index only active networks
CREATE INDEX idx_wifi_active ON wifi_networks(last_seen) 
WHERE last_seen > datetime('now', '-24 hours');

-- Index only named networks
CREATE INDEX idx_wifi_named ON wifi_networks(ssid, signal_strength) 
WHERE ssid IS NOT NULL AND ssid != '';
```

### Connection Management

**Connection Pooling**
```python
import asyncio
from contextlib import asynccontextmanager

class DatabasePool:
    def __init__(self, db_path: str, max_connections: int = 10):
        self.db_path = db_path
        self.pool = asyncio.Queue(maxsize=max_connections)
        self.initialized = False
    
    async def init_pool(self):
        """Initialize connection pool."""
        if self.initialized:
            return
        
        for _ in range(self.pool.maxsize):
            conn = await aiosqlite.connect(self.db_path)
            await self.configure_connection(conn)
            await self.pool.put(conn)
        
        self.initialized = True
    
    async def configure_connection(self, conn):
        """Configure connection for optimal performance."""
        await conn.execute("PRAGMA journal_mode=WAL")
        await conn.execute("PRAGMA cache_size=5000")
        await conn.execute("PRAGMA synchronous=NORMAL")
        await conn.execute("PRAGMA temp_store=MEMORY")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get connection from pool."""
        conn = await self.pool.get()
        try:
            yield conn
        finally:
            await self.pool.put(conn)
```

## Application Performance Tuning

### Async Operations

**Concurrent Processing**
```python
async def process_scan_results_concurrent(scan_results: List[Dict]):
    """Process scan results concurrently."""
    semaphore = asyncio.Semaphore(10)  # Limit concurrent operations
    
    async def process_single_result(result):
        async with semaphore:
            # Process individual result
            enriched = await enrich_network_data(result)
            await save_network_data(enriched)
    
    tasks = [process_single_result(result) for result in scan_results]
    await asyncio.gather(*tasks, return_exceptions=True)
```

**Efficient Data Streaming**
```python
async def stream_large_dataset(query: str, batch_size: int = 1000):
    """Stream large datasets efficiently."""
    async with db_pool.get_connection() as conn:
        cursor = await conn.execute(query)
        
        while True:
            batch = await cursor.fetchmany(batch_size)
            if not batch:
                break
            
            # Process batch
            yield [process_record(record) for record in batch]
```

### Caching Strategies

**Memory Caching**
```python
from cachetools import TTLCache
import asyncio

class PerformanceCache:
    def __init__(self):
        self.network_cache = TTLCache(maxsize=10000, ttl=300)  # 5 minutes
        self.location_cache = TTLCache(maxsize=1000, ttl=600)  # 10 minutes
        self.stats_cache = TTLCache(maxsize=100, ttl=60)       # 1 minute
    
    async def get_network_stats(self, bssid: str):
        """Get network statistics with caching."""
        if bssid in self.network_cache:
            return self.network_cache[bssid]
        
        stats = await self.compute_network_stats(bssid)
        self.network_cache[bssid] = stats
        return stats
    
    async def compute_network_stats(self, bssid: str):
        """Compute network statistics."""
        async with db_pool.get_connection() as conn:
            cursor = await conn.execute("""
                SELECT 
                    COUNT(*) as scan_count,
                    AVG(signal_strength) as avg_signal,
                    MAX(signal_strength) as max_signal,
                    MIN(signal_strength) as min_signal
                FROM wifi_networks 
                WHERE bssid = ?
            """, (bssid,))
            return await cursor.fetchone()
```

**Disk Caching**
```python
import sqlite3
from pathlib import Path

class DiskCache:
    def __init__(self, cache_dir: str = "/tmp/piwardrive_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_db = self.cache_dir / "cache.db"
        self.init_cache_db()
    
    def init_cache_db(self):
        """Initialize cache database."""
        with sqlite3.connect(self.cache_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_entries (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    expires_at INTEGER
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_cache_expires 
                ON cache_entries(expires_at)
            """)
    
    async def get(self, key: str):
        """Get cached value."""
        async with aiosqlite.connect(self.cache_db) as conn:
            cursor = await conn.execute("""
                SELECT value FROM cache_entries 
                WHERE key = ? AND expires_at > ?
            """, (key, time.time()))
            row = await cursor.fetchone()
            return pickle.loads(row[0]) if row else None
    
    async def set(self, key: str, value, ttl: int = 3600):
        """Set cached value."""
        expires_at = time.time() + ttl
        async with aiosqlite.connect(self.cache_db) as conn:
            await conn.execute("""
                INSERT OR REPLACE INTO cache_entries (key, value, expires_at)
                VALUES (?, ?, ?)
            """, (key, pickle.dumps(value), expires_at))
            await conn.commit()
```

### Resource Management

**Memory Management**
```python
import gc
import psutil
import asyncio

class ResourceMonitor:
    def __init__(self):
        self.memory_threshold = 0.8  # 80% memory usage
        self.check_interval = 60     # Check every minute
    
    async def start_monitoring(self):
        """Start resource monitoring."""
        while True:
            await self.check_memory_usage()
            await asyncio.sleep(self.check_interval)
    
    async def check_memory_usage(self):
        """Check and manage memory usage."""
        memory_percent = psutil.virtual_memory().percent / 100
        
        if memory_percent > self.memory_threshold:
            await self.cleanup_resources()
    
    async def cleanup_resources(self):
        """Clean up resources when memory is high."""
        # Clear caches
        performance_cache.network_cache.clear()
        performance_cache.location_cache.clear()
        
        # Force garbage collection
        gc.collect()
        
        # Log memory usage
        logging.info(f"Memory cleanup performed. Usage: {psutil.virtual_memory().percent}%")
```

**Connection Management**
```python
async def manage_external_connections():
    """Manage external service connections."""
    connector = aiohttp.TCPConnector(
        limit=100,              # Total connection limit
        limit_per_host=10,      # Per-host connection limit
        ttl_dns_cache=300,      # DNS cache TTL
        use_dns_cache=True,     # Enable DNS caching
        keepalive_timeout=30,   # Keep-alive timeout
        enable_cleanup_closed=True  # Clean up closed connections
    )
    
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:
        # Use session for all HTTP requests
        return session
```

## Hardware Optimization

### CPU Optimization

**Process Affinity**
```python
import os
import psutil

def optimize_cpu_affinity():
    """Optimize CPU affinity for performance."""
    # Get available CPUs
    cpu_count = psutil.cpu_count()
    
    if cpu_count > 2:
        # Pin to specific CPUs, leave others for system
        available_cpus = list(range(1, cpu_count))
        os.sched_setaffinity(0, available_cpus)
    
    # Set high priority for critical processes
    process = psutil.Process()
    process.nice(-5)  # Higher priority (requires privileges)
```

**Worker Process Management**
```python
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

class WorkerManager:
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()
        self.worker_count = max(2, self.cpu_count - 1)  # Leave one CPU for system
        self.executor = ProcessPoolExecutor(max_workers=self.worker_count)
    
    async def process_data_parallel(self, data_chunks):
        """Process data in parallel using worker processes."""
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(self.executor, self.process_chunk, chunk)
            for chunk in data_chunks
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    def process_chunk(self, chunk):
        """Process a chunk of data (runs in worker process)."""
        # CPU-intensive processing
        return [self.complex_calculation(item) for item in chunk]
```

### Memory Optimization

**Memory-Efficient Data Structures**
```python
import array
from collections import deque

class EfficientDataStore:
    def __init__(self):
        # Use arrays for numeric data
        self.signal_strengths = array.array('i')  # Integer array
        self.frequencies = array.array('i')
        
        # Use deque for FIFO operations
        self.recent_scans = deque(maxlen=1000)
        
        # Use slots for memory efficiency
        self.networks = []
    
    class NetworkRecord:
        __slots__ = ['bssid', 'ssid', 'signal_strength', 'frequency', 'timestamp']
        
        def __init__(self, bssid, ssid, signal_strength, frequency, timestamp):
            self.bssid = bssid
            self.ssid = ssid
            self.signal_strength = signal_strength
            self.frequency = frequency
            self.timestamp = timestamp
```

**Memory Monitoring**
```python
import tracemalloc
import logging

class MemoryProfiler:
    def __init__(self):
        self.enabled = False
    
    def start_profiling(self):
        """Start memory profiling."""
        tracemalloc.start()
        self.enabled = True
    
    def get_memory_stats(self):
        """Get current memory statistics."""
        if not self.enabled:
            return None
        
        current, peak = tracemalloc.get_traced_memory()
        return {
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024
        }
    
    def log_top_memory_usage(self, limit=10):
        """Log top memory usage."""
        if not self.enabled:
            return
        
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        logging.info(f"Top {limit} memory usage:")
        for stat in top_stats[:limit]:
            logging.info(f"  {stat}")
```

### Storage Optimization

**I/O Optimization**
```python
import aiofiles
import asyncio

class OptimizedFileIO:
    def __init__(self, buffer_size: int = 8192):
        self.buffer_size = buffer_size
    
    async def write_data_efficiently(self, file_path: str, data: bytes):
        """Write data efficiently with buffering."""
        async with aiofiles.open(file_path, 'wb', buffering=self.buffer_size) as f:
            await f.write(data)
            await f.fsync()  # Force write to disk
    
    async def read_data_chunks(self, file_path: str, chunk_size: int = 8192):
        """Read data in chunks to manage memory."""
        async with aiofiles.open(file_path, 'rb') as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
```

## Load Testing and Performance Monitoring

### Load Testing Framework

**Database Load Testing**
```python
import asyncio
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

class DatabaseLoadTester:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.results = []
    
    async def test_read_performance(self, concurrent_users: int = 10, operations: int = 1000):
        """Test database read performance."""
        async def read_worker():
            times = []
            for _ in range(operations // concurrent_users):
                start_time = time.perf_counter()
                await self.perform_read_operation()
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            return times
        
        tasks = [read_worker() for _ in range(concurrent_users)]
        all_times = await asyncio.gather(*tasks)
        
        # Flatten results
        flat_times = [t for times in all_times for t in times]
        
        return {
            'avg_time': statistics.mean(flat_times),
            'median_time': statistics.median(flat_times),
            'p95_time': statistics.quantiles(flat_times, n=20)[18],  # 95th percentile
            'max_time': max(flat_times),
            'operations_per_second': len(flat_times) / sum(flat_times)
        }
    
    async def perform_read_operation(self):
        """Perform a typical read operation."""
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("""
                SELECT bssid, ssid, signal_strength 
                FROM wifi_networks 
                WHERE last_seen > datetime('now', '-1 hour')
                ORDER BY signal_strength DESC 
                LIMIT 10
            """)
            return await cursor.fetchall()
```

**API Load Testing**
```python
import aiohttp
import asyncio
import time

class APILoadTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None
    
    async def setup(self):
        """Setup HTTP session."""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def test_api_endpoints(self, concurrent_users: int = 50, requests_per_user: int = 100):
        """Test API endpoints under load."""
        endpoints = [
            '/api/wifi',
            '/api/bluetooth',
            '/api/health',
            '/api/status'
        ]
        
        async def user_simulation():
            times = []
            for _ in range(requests_per_user):
                endpoint = random.choice(endpoints)
                start_time = time.perf_counter()
                
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    await response.read()
                    end_time = time.perf_counter()
                    times.append({
                        'endpoint': endpoint,
                        'response_time': end_time - start_time,
                        'status_code': response.status
                    })
            return times
        
        tasks = [user_simulation() for _ in range(concurrent_users)]
        results = await asyncio.gather(*tasks)
        
        return self.analyze_results(results)
    
    def analyze_results(self, results):
        """Analyze load test results."""
        flat_results = [r for user_results in results for r in user_results]
        
        response_times = [r['response_time'] for r in flat_results]
        status_codes = [r['status_code'] for r in flat_results]
        
        return {
            'total_requests': len(flat_results),
            'avg_response_time': statistics.mean(response_times),
            'p95_response_time': statistics.quantiles(response_times, n=20)[18],
            'success_rate': sum(1 for code in status_codes if code == 200) / len(status_codes),
            'requests_per_second': len(flat_results) / sum(response_times)
        }
```

### Performance Monitoring

**Real-time Metrics Collection**
```python
import psutil
import time
import json
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()
    
    async def collect_metrics(self):
        """Collect system performance metrics."""
        while True:
            timestamp = time.time()
            
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network metrics
            network_io = psutil.net_io_counters()
            
            metrics = {
                'timestamp': timestamp,
                'cpu_percent': cpu_percent,
                'cpu_freq': cpu_freq.current if cpu_freq else 0,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'disk_usage_percent': disk_usage.percent,
                'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
                'disk_write_bytes': disk_io.write_bytes if disk_io else 0,
                'network_bytes_sent': network_io.bytes_sent,
                'network_bytes_recv': network_io.bytes_recv,
            }
            
            self.record_metrics(metrics)
            await asyncio.sleep(5)  # Collect every 5 seconds
    
    def record_metrics(self, metrics):
        """Record metrics for analysis."""
        for key, value in metrics.items():
            self.metrics[key].append(value)
    
    def get_performance_report(self):
        """Generate performance report."""
        report = {}
        
        for metric, values in self.metrics.items():
            if metric == 'timestamp':
                continue
            
            if values:
                report[metric] = {
                    'avg': statistics.mean(values),
                    'min': min(values),
                    'max': max(values),
                    'current': values[-1] if values else 0
                }
        
        return report
```

**Database Performance Monitoring**
```python
class DatabasePerformanceMonitor:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.query_stats = defaultdict(list)
    
    async def monitor_queries(self):
        """Monitor database query performance."""
        async with aiosqlite.connect(self.db_path) as conn:
            # Enable query profiling
            await conn.execute("PRAGMA query_only = ON")
            
            # Get query statistics
            cursor = await conn.execute("""
                SELECT name, ncall, time, max_time
                FROM sqlite_stats
                WHERE type = 'query'
            """)
            
            stats = await cursor.fetchall()
            return stats
    
    async def analyze_slow_queries(self, threshold: float = 0.1):
        """Analyze slow queries."""
        slow_queries = []
        
        for query, times in self.query_stats.items():
            avg_time = statistics.mean(times)
            if avg_time > threshold:
                slow_queries.append({
                    'query': query,
                    'avg_time': avg_time,
                    'max_time': max(times),
                    'call_count': len(times)
                })
        
        return sorted(slow_queries, key=lambda x: x['avg_time'], reverse=True)
```

## Performance Optimization Checklist

### Database Optimization
- [ ] Configure SQLite pragmas for optimal performance
- [ ] Implement proper indexing strategy
- [ ] Use connection pooling
- [ ] Optimize query patterns
- [ ] Implement batch operations
- [ ] Regular database maintenance (VACUUM, ANALYZE)

### Application Optimization
- [ ] Implement async/await patterns
- [ ] Use appropriate caching strategies
- [ ] Optimize resource management
- [ ] Implement connection pooling
- [ ] Use efficient data structures
- [ ] Monitor memory usage

### Hardware Optimization
- [ ] Optimize CPU affinity
- [ ] Implement memory monitoring
- [ ] Use appropriate storage configuration
- [ ] Monitor I/O patterns
- [ ] Optimize network settings

### Monitoring and Testing
- [ ] Implement load testing
- [ ] Set up performance monitoring
- [ ] Create performance baselines
- [ ] Implement alerting for performance degradation
- [ ] Regular performance audits

## Troubleshooting Performance Issues

### Common Performance Problems

1. **Slow Database Queries**
   - Check query execution plans
   - Verify index usage
   - Consider query optimization

2. **High Memory Usage**
   - Monitor memory leaks
   - Optimize caching strategies
   - Implement memory cleanup

3. **CPU Bottlenecks**
   - Profile CPU usage
   - Optimize algorithms
   - Consider parallel processing

4. **I/O Bottlenecks**
   - Monitor disk usage
   - Optimize file operations
   - Consider SSD upgrades

### Performance Debugging Tools

```python
import cProfile
import pstats
import io

def profile_function(func):
    """Profile function execution."""
    pr = cProfile.Profile()
    pr.enable()
    
    result = func()
    
    pr.disable()
    
    # Print stats
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())
    
    return result
```

For more detailed performance analysis, consider using tools like:
- **py-spy**: Python profiler
- **memory_profiler**: Memory usage profiler
- **line_profiler**: Line-by-line profiler
- **SQLite EXPLAIN QUERY PLAN**: Query execution analysis

## Best Practices Summary

1. **Measure First**: Always measure performance before optimizing
2. **Optimize Bottlenecks**: Focus on the biggest performance bottlenecks
3. **Test Thoroughly**: Test optimizations under realistic conditions
4. **Monitor Continuously**: Implement continuous performance monitoring
5. **Document Changes**: Document performance optimizations and their impact
