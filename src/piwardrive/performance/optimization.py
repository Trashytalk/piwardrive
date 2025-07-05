"""
PiWardrive Performance Optimization System

Comprehensive performance optimization including:
- Multi-threaded scanning and processing
- Memory optimization and garbage collection
- Database query optimization and indexing
- Intelligent caching and data compression
- System resource monitoring and tuning
- Performance profiling and bottleneck identification

Author: PiWardrive Development Team
License: MIT
"""

import gc
import logging
import multiprocessing
import os
import psutil
import threading
import time
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set, Any, Callable, Union
import sqlite3
import pickle
import gzip
import lz4.frame
import zlib
import hashlib
from pathlib import Path
import weakref
import cProfile
import pstats
import io

import numpy as np
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizationLevel(Enum):
    """Optimization levels"""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    EXTREME = "extreme"

class CacheStrategy(Enum):
    """Cache strategy options"""
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    ADAPTIVE = "adaptive"

class CompressionType(Enum):
    """Compression types"""
    NONE = "none"
    GZIP = "gzip"
    LZ4 = "lz4"
    ZLIB = "zlib"

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime = field(default_factory=datetime.now)
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_available: int = 0
    disk_usage: float = 0.0
    network_io: Dict[str, int] = field(default_factory=dict)
    thread_count: int = 0
    process_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_available': self.memory_available,
            'disk_usage': self.disk_usage,
            'network_io': self.network_io,
            'thread_count': self.thread_count,
            'process_count': self.process_count
        }

@dataclass
class PerformanceProfile:
    """Performance profiling data"""
    function_name: str
    call_count: int
    total_time: float
    cumulative_time: float
    average_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'function_name': self.function_name,
            'call_count': self.call_count,
            'total_time': self.total_time,
            'cumulative_time': self.cumulative_time,
            'average_time': self.average_time
        }

class SystemMonitor:
    """System resource monitoring"""
    
    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.metrics_history: deque = deque(maxlen=1000)
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.callbacks: List[Callable] = []
        
    def start_monitoring(self):
        """Start system monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            logger.info("System monitoring started")
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("System monitoring stopped")
    
    def add_callback(self, callback: Callable):
        """Add metrics callback"""
        self.callbacks.append(callback)
    
    def get_current_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=None)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_available = memory.available
        
        # Disk usage
        disk = psutil.disk_usage('.')
        disk_usage = (disk.used / disk.total) * 100
        
        # Network I/O
        network = psutil.net_io_counters()
        network_io = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv
        }
        
        # Process info
        process = psutil.Process()
        thread_count = process.num_threads()
        process_count = len(psutil.pids())
        
        return SystemMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_available=memory_available,
            disk_usage=disk_usage,
            network_io=network_io,
            thread_count=thread_count,
            process_count=process_count
        )
    
    def get_metrics_history(self, minutes: int = 5) -> List[SystemMetrics]:
        """Get metrics history"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            metric for metric in self.metrics_history
            if metric.timestamp >= cutoff_time
        ]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {}
        
        recent_metrics = self.get_metrics_history(minutes=5)
        
        if not recent_metrics:
            return {}
        
        return {
            'avg_cpu_percent': sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            'max_cpu_percent': max(m.cpu_percent for m in recent_metrics),
            'avg_memory_percent': sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
            'max_memory_percent': max(m.memory_percent for m in recent_metrics),
            'avg_disk_usage': sum(m.disk_usage for m in recent_metrics) / len(recent_metrics),
            'thread_count': recent_metrics[-1].thread_count if recent_metrics else 0,
            'samples_collected': len(recent_metrics)
        }
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                metrics = self.get_current_metrics()
                self.metrics_history.append(metrics)
                
                # Notify callbacks
                for callback in self.callbacks:
                    callback(metrics)
                
                time.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(self.update_interval)

class IntelligentCache:
    """Intelligent caching system"""
    
    def __init__(self, max_size: int = 1000, strategy: CacheStrategy = CacheStrategy.LRU):
        self.max_size = max_size
        self.strategy = strategy
        self.cache: Dict[str, Any] = {}
        self.access_times: Dict[str, datetime] = {}
        self.access_counts: Dict[str, int] = {}
        self.insertion_order: deque = deque()
        self.lock = threading.Lock()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        with self.lock:
            if key in self.cache:
                self.hits += 1
                self._update_access(key)
                return self.cache[key]
            else:
                self.misses += 1
                return None
    
    def put(self, key: str, value: Any):
        """Put item in cache"""
        with self.lock:
            if key in self.cache:
                self.cache[key] = value
                self._update_access(key)
            else:
                if len(self.cache) >= self.max_size:
                    self._evict()
                
                self.cache[key] = value
                self.access_times[key] = datetime.now()
                self.access_counts[key] = 1
                self.insertion_order.append(key)
    
    def invalidate(self, key: str):
        """Invalidate cache entry"""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                del self.access_times[key]
                del self.access_counts[key]
                
                # Remove from insertion order
                try:
                    self.insertion_order.remove(key)
                except ValueError:
                    pass
    
    def clear(self):
        """Clear cache"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
            self.access_counts.clear()
            self.insertion_order.clear()
            
            # Reset statistics
            self.hits = 0
            self.misses = 0
            self.evictions = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests) if total_requests > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'memory_usage': self._estimate_memory_usage()
        }
    
    def _update_access(self, key: str):
        """Update access statistics"""
        self.access_times[key] = datetime.now()
        self.access_counts[key] = self.access_counts.get(key, 0) + 1
    
    def _evict(self):
        """Evict items based on strategy"""
        if not self.cache:
            return
        
        if self.strategy == CacheStrategy.LRU:
            # Least Recently Used
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            self._remove_key(oldest_key)
        
        elif self.strategy == CacheStrategy.LFU:
            # Least Frequently Used
            least_used_key = min(self.access_counts.keys(), key=lambda k: self.access_counts[k])
            self._remove_key(least_used_key)
        
        elif self.strategy == CacheStrategy.FIFO:
            # First In, First Out
            if self.insertion_order:
                oldest_key = self.insertion_order.popleft()
                self._remove_key(oldest_key)
        
        elif self.strategy == CacheStrategy.ADAPTIVE:
            # Adaptive strategy based on access patterns
            now = datetime.now()
            scores = {}
            
            for key in self.cache:
                age = (now - self.access_times.get(key, now)).total_seconds()
                frequency = self.access_counts.get(key, 1)
                scores[key] = frequency / (age + 1)  # Higher is better
            
            worst_key = min(scores.keys(), key=lambda k: scores[k])
            self._remove_key(worst_key)
        
        self.evictions += 1
    
    def _remove_key(self, key: str):
        """Remove key from all data structures"""
        if key in self.cache:
            del self.cache[key]
        if key in self.access_times:
            del self.access_times[key]
        if key in self.access_counts:
            del self.access_counts[key]
        
        try:
            self.insertion_order.remove(key)
        except ValueError:
            pass
    
    def _estimate_memory_usage(self) -> int:
        """Estimate memory usage in bytes"""
        total_size = 0
        for key, value in self.cache.items():
            total_size += len(key.encode('utf-8'))
            total_size += len(pickle.dumps(value))
        return total_size

class DataCompressor:
    """Data compression utilities"""
    
    def __init__(self, compression_type: CompressionType = CompressionType.LZ4):
        self.compression_type = compression_type
        self.compression_stats = {
            'original_size': 0,
            'compressed_size': 0,
            'compression_ratio': 0,
            'operations': 0
        }
    
    def compress(self, data: bytes) -> bytes:
        """Compress data"""
        original_size = len(data)
        
        if self.compression_type == CompressionType.GZIP:
            compressed = gzip.compress(data)
        elif self.compression_type == CompressionType.LZ4:
            compressed = lz4.frame.compress(data)
        elif self.compression_type == CompressionType.ZLIB:
            compressed = zlib.compress(data)
        else:
            compressed = data
        
        # Update statistics
        self.compression_stats['original_size'] += original_size
        self.compression_stats['compressed_size'] += len(compressed)
        self.compression_stats['operations'] += 1
        
        if self.compression_stats['original_size'] > 0:
            self.compression_stats['compression_ratio'] = (
                self.compression_stats['compressed_size'] / 
                self.compression_stats['original_size']
            )
        
        return compressed
    
    def decompress(self, data: bytes) -> bytes:
        """Decompress data"""
        if self.compression_type == CompressionType.GZIP:
            return gzip.decompress(data)
        elif self.compression_type == CompressionType.LZ4:
            return lz4.frame.decompress(data)
        elif self.compression_type == CompressionType.ZLIB:
            return zlib.decompress(data)
        else:
            return data
    
    def get_stats(self) -> Dict[str, Any]:
        """Get compression statistics"""
        return self.compression_stats.copy()

class DatabaseOptimizer:
    """Database optimization utilities"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection_pool: List[sqlite3.Connection] = []
        self.pool_size = 5
        self.lock = threading.Lock()
        
        # Initialize connection pool
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        for _ in range(self.pool_size):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self.connection_pool.append(conn)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get connection from pool"""
        with self.lock:
            if self.connection_pool:
                return self.connection_pool.pop()
            else:
                # Create new connection if pool is empty
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row
                return conn
    
    def return_connection(self, conn: sqlite3.Connection):
        """Return connection to pool"""
        with self.lock:
            if len(self.connection_pool) < self.pool_size:
                self.connection_pool.append(conn)
            else:
                conn.close()
    
    def optimize_database(self):
        """Optimize database structure and performance"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Enable WAL mode for better concurrency
            cursor.execute("PRAGMA journal_mode = WAL")
            
            # Set optimal cache size
            cursor.execute("PRAGMA cache_size = 10000")
            
            # Enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # Optimize page size
            cursor.execute("PRAGMA page_size = 4096")
            
            # Synchronous mode for better performance
            cursor.execute("PRAGMA synchronous = NORMAL")
            
            # Memory-mapped I/O
            cursor.execute("PRAGMA mmap_size = 268435456")  # 256MB
            
            # Analyze database for query optimization
            cursor.execute("ANALYZE")
            
            # Vacuum database to reclaim space
            cursor.execute("VACUUM")
            
            conn.commit()
            logger.info("Database optimization completed")
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            conn.rollback()
        finally:
            self.return_connection(conn)
    
    def create_index(self, table_name: str, columns: List[str], 
                    unique: bool = False) -> bool:
        """Create database index"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            index_name = f"idx_{table_name}_{'_'.join(columns)}"
            unique_clause = "UNIQUE" if unique else ""
            columns_str = ', '.join(columns)
            
            query = f"CREATE {unique_clause} INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns_str})"
            cursor.execute(query)
            conn.commit()
            
            logger.info(f"Index created: {index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Index creation failed: {e}")
            conn.rollback()
            return False
        finally:
            self.return_connection(conn)
    
    def analyze_query_performance(self, query: str) -> Dict[str, Any]:
        """Analyze query performance"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Get query plan
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            query_plan = cursor.fetchall()
            
            # Execute query with timing
            start_time = time.time()
            cursor.execute(query)
            results = cursor.fetchall()
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            return {
                'query': query,
                'execution_time': execution_time,
                'row_count': len(results),
                'query_plan': [dict(row) for row in query_plan]
            }
            
        except Exception as e:
            logger.error(f"Query analysis failed: {e}")
            return {'error': str(e)}
        finally:
            self.return_connection(conn)
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Get table statistics"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            # Table size
            cursor.execute(f"SELECT SUM(pgsize) FROM dbstat WHERE name = '{table_name}'")
            table_size = cursor.fetchone()[0] or 0
            
            # Column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            return {
                'table_name': table_name,
                'row_count': row_count,
                'table_size': table_size,
                'columns': [dict(col) for col in columns]
            }
            
        except Exception as e:
            logger.error(f"Table stats failed: {e}")
            return {'error': str(e)}
        finally:
            self.return_connection(conn)

class MultiThreadedScanner:
    """Multi-threaded scanning system"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, multiprocessing.cpu_count() * 2)
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.scan_queue = deque()
        self.results_queue = deque()
        self.active_scans = 0
        self.lock = threading.Lock()
        
    def submit_scan(self, scan_function: Callable, *args, **kwargs) -> Any:
        """Submit scan task"""
        with self.lock:
            self.active_scans += 1
        
        future = self.executor.submit(self._scan_wrapper, scan_function, *args, **kwargs)
        return future
    
    def submit_batch_scan(self, scan_function: Callable, 
                         batch_args: List[Tuple]) -> List[Any]:
        """Submit batch of scan tasks"""
        futures = []
        for args in batch_args:
            future = self.submit_scan(scan_function, *args)
            futures.append(future)
        
        # Wait for all tasks to complete
        results = []
        for future in futures:
            try:
                result = future.result(timeout=30)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch scan task failed: {e}")
                results.append(None)
        
        return results
    
    def get_scan_status(self) -> Dict[str, Any]:
        """Get scan status"""
        with self.lock:
            return {
                'active_scans': self.active_scans,
                'max_workers': self.max_workers,
                'queued_scans': len(self.scan_queue),
                'completed_results': len(self.results_queue)
            }
    
    def shutdown(self, wait: bool = True):
        """Shutdown scanner"""
        self.executor.shutdown(wait=wait)
    
    def _scan_wrapper(self, scan_function: Callable, *args, **kwargs):
        """Wrapper for scan functions"""
        try:
            start_time = time.time()
            result = scan_function(*args, **kwargs)
            end_time = time.time()
            
            wrapped_result = {
                'result': result,
                'execution_time': end_time - start_time,
                'timestamp': datetime.now(),
                'success': True
            }
            
            self.results_queue.append(wrapped_result)
            return wrapped_result
            
        except Exception as e:
            error_result = {
                'result': None,
                'error': str(e),
                'timestamp': datetime.now(),
                'success': False
            }
            
            self.results_queue.append(error_result)
            return error_result
        finally:
            with self.lock:
                self.active_scans -= 1

class MemoryOptimizer:
    """Memory optimization utilities"""
    
    def __init__(self):
        self.weak_refs: Set[weakref.ref] = set()
        self.memory_threshold = 0.8  # 80% memory usage threshold
        self.gc_frequency = 100  # Garbage collection frequency
        self.operation_count = 0
        
    def monitor_memory(self) -> Dict[str, Any]:
        """Monitor memory usage"""
        memory = psutil.virtual_memory()
        process = psutil.Process()
        
        return {
            'total_memory': memory.total,
            'available_memory': memory.available,
            'used_memory': memory.used,
            'memory_percent': memory.percent,
            'process_memory': process.memory_info().rss,
            'process_memory_percent': process.memory_percent(),
            'gc_stats': {
                'collections': gc.get_stats(),
                'objects': len(gc.get_objects()),
                'threshold': gc.get_threshold()
            }
        }
    
    def optimize_memory(self) -> Dict[str, Any]:
        """Optimize memory usage"""
        initial_memory = psutil.virtual_memory().percent
        
        # Force garbage collection
        collected = gc.collect()
        
        # Clean up weak references
        self._cleanup_weak_refs()
        
        # Optimize garbage collection thresholds
        gc.set_threshold(700, 10, 10)  # More aggressive collection
        
        final_memory = psutil.virtual_memory().percent
        memory_freed = initial_memory - final_memory
        
        return {
            'objects_collected': collected,
            'weak_refs_cleaned': len(self.weak_refs),
            'memory_freed_percent': memory_freed,
            'gc_threshold_optimized': True
        }
    
    def register_weak_ref(self, obj: Any) -> weakref.ref:
        """Register weak reference"""
        weak_ref = weakref.ref(obj, self._weak_ref_callback)
        self.weak_refs.add(weak_ref)
        return weak_ref
    
    def should_optimize(self) -> bool:
        """Check if memory optimization is needed"""
        self.operation_count += 1
        
        # Check memory threshold
        memory_usage = psutil.virtual_memory().percent / 100
        if memory_usage > self.memory_threshold:
            return True
        
        # Check operation count
        if self.operation_count % self.gc_frequency == 0:
            return True
        
        return False
    
    def _cleanup_weak_refs(self):
        """Clean up dead weak references"""
        dead_refs = set()
        for ref in self.weak_refs:
            if ref() is None:
                dead_refs.add(ref)
        
        self.weak_refs -= dead_refs
    
    def _weak_ref_callback(self, ref: weakref.ref):
        """Callback for weak reference cleanup"""
        self.weak_refs.discard(ref)

class PerformanceProfiler:
    """Performance profiling utilities"""
    
    def __init__(self):
        self.profiles: Dict[str, PerformanceProfile] = {}
        self.active_profiles: Dict[str, cProfile.Profile] = {}
        
    def start_profiling(self, profile_name: str):
        """Start profiling"""
        if profile_name not in self.active_profiles:
            self.active_profiles[profile_name] = cProfile.Profile()
            self.active_profiles[profile_name].enable()
    
    def stop_profiling(self, profile_name: str) -> Optional[PerformanceProfile]:
        """Stop profiling and get results"""
        if profile_name in self.active_profiles:
            profiler = self.active_profiles[profile_name]
            profiler.disable()
            
            # Generate profile statistics
            stats_buffer = io.StringIO()
            stats = pstats.Stats(profiler, stream=stats_buffer)
            stats.sort_stats('cumulative')
            stats.print_stats(10)  # Top 10 functions
            
            # Extract key metrics
            total_calls = stats.total_calls
            total_time = stats.total_tt
            
            # Get top function
            if stats.stats:
                top_func = list(stats.stats.keys())[0]
                top_stats = stats.stats[top_func]
                
                profile = PerformanceProfile(
                    function_name=f"{top_func[0]}:{top_func[1]}({top_func[2]})",
                    call_count=top_stats[0],
                    total_time=top_stats[2],
                    cumulative_time=top_stats[3],
                    average_time=top_stats[2] / top_stats[0] if top_stats[0] > 0 else 0
                )
                
                self.profiles[profile_name] = profile
                del self.active_profiles[profile_name]
                
                return profile
        
        return None
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get profile summary"""
        return {
            'active_profiles': list(self.active_profiles.keys()),
            'completed_profiles': len(self.profiles),
            'profile_data': [profile.to_dict() for profile in self.profiles.values()]
        }

class PerformanceOptimizer:
    """Main performance optimization system"""
    
    def __init__(self, optimization_level: OptimizationLevel = OptimizationLevel.BALANCED):
        self.optimization_level = optimization_level
        self.system_monitor = SystemMonitor()
        self.cache = IntelligentCache(max_size=1000)
        self.compressor = DataCompressor()
        self.memory_optimizer = MemoryOptimizer()
        self.profiler = PerformanceProfiler()
        self.scanner = MultiThreadedScanner()
        
        # Optimization statistics
        self.optimization_stats = {
            'optimizations_performed': 0,
            'memory_optimizations': 0,
            'cache_optimizations': 0,
            'database_optimizations': 0
        }
        
        # Start monitoring
        self.system_monitor.start_monitoring()
        self.system_monitor.add_callback(self._on_metrics_update)
    
    def optimize_system(self) -> Dict[str, Any]:
        """Perform comprehensive system optimization"""
        start_time = time.time()
        results = {}
        
        # Memory optimization
        if self.memory_optimizer.should_optimize():
            memory_results = self.memory_optimizer.optimize_memory()
            results['memory_optimization'] = memory_results
            self.optimization_stats['memory_optimizations'] += 1
        
        # Cache optimization
        cache_stats = self.cache.get_stats()
        if cache_stats['hit_rate'] < 0.8:  # Low hit rate
            self.cache.clear()  # Reset cache
            results['cache_optimization'] = {'cache_cleared': True}
            self.optimization_stats['cache_optimizations'] += 1
        
        # Garbage collection
        gc_collected = gc.collect()
        results['garbage_collection'] = {'objects_collected': gc_collected}
        
        # Update statistics
        self.optimization_stats['optimizations_performed'] += 1
        
        end_time = time.time()
        results['optimization_time'] = end_time - start_time
        
        return results
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        return {
            'system_metrics': self.system_monitor.get_performance_summary(),
            'cache_stats': self.cache.get_stats(),
            'compression_stats': self.compressor.get_stats(),
            'memory_stats': self.memory_optimizer.monitor_memory(),
            'scanner_status': self.scanner.get_scan_status(),
            'optimization_stats': self.optimization_stats,
            'profile_summary': self.profiler.get_profile_summary()
        }
    
    def configure_optimization_level(self, level: OptimizationLevel):
        """Configure optimization level"""
        self.optimization_level = level
        
        if level == OptimizationLevel.CONSERVATIVE:
            self.cache.max_size = 500
            self.memory_optimizer.memory_threshold = 0.9
            self.memory_optimizer.gc_frequency = 200
        elif level == OptimizationLevel.BALANCED:
            self.cache.max_size = 1000
            self.memory_optimizer.memory_threshold = 0.8
            self.memory_optimizer.gc_frequency = 100
        elif level == OptimizationLevel.AGGRESSIVE:
            self.cache.max_size = 2000
            self.memory_optimizer.memory_threshold = 0.7
            self.memory_optimizer.gc_frequency = 50
        elif level == OptimizationLevel.EXTREME:
            self.cache.max_size = 5000
            self.memory_optimizer.memory_threshold = 0.6
            self.memory_optimizer.gc_frequency = 25
    
    def shutdown(self):
        """Shutdown optimization system"""
        self.system_monitor.stop_monitoring()
        self.scanner.shutdown()
        self.cache.clear()
    
    def _on_metrics_update(self, metrics: SystemMetrics):
        """Handle metrics update"""
        # Auto-optimize based on metrics
        if metrics.memory_percent > 85:
            self.memory_optimizer.optimize_memory()
        
        if metrics.cpu_percent > 90:
            # Reduce scanning threads
            if self.scanner.max_workers > 2:
                self.scanner.max_workers = max(2, self.scanner.max_workers - 1)

def demo_performance_optimization():
    """Demonstrate performance optimization capabilities"""
    print("PiWardrive Performance Optimization Demo")
    print("=" * 50)
    
    # Create performance optimizer
    optimizer = PerformanceOptimizer(OptimizationLevel.BALANCED)
    
    # Wait for initial metrics
    time.sleep(2)
    
    # Test system monitoring
    print("\n1. System Monitoring:")
    current_metrics = optimizer.system_monitor.get_current_metrics()
    print(f"   CPU Usage: {current_metrics.cpu_percent:.1f}%")
    print(f"   Memory Usage: {current_metrics.memory_percent:.1f}%")
    print(f"   Available Memory: {current_metrics.memory_available // (1024*1024):.0f} MB")
    print(f"   Thread Count: {current_metrics.thread_count}")
    
    # Test intelligent caching
    print("\n2. Intelligent Caching:")
    
    # Add some test data to cache
    for i in range(100):
        optimizer.cache.put(f"key_{i}", f"value_{i}")
    
    # Test cache retrieval
    hit_count = 0
    for i in range(50):
        if optimizer.cache.get(f"key_{i}"):
            hit_count += 1
    
    cache_stats = optimizer.cache.get_stats()
    print(f"   Cache Size: {cache_stats['cache_size']}")
    print(f"   Hit Rate: {cache_stats['hit_rate']:.2f}")
    print(f"   Memory Usage: {cache_stats['memory_usage']} bytes")
    
    # Test data compression
    print("\n3. Data Compression:")
    
    # Create test data
    test_data = b"This is a test string that will be compressed. " * 100
    compressed_data = optimizer.compressor.compress(test_data)
    decompressed_data = optimizer.compressor.decompress(compressed_data)
    
    compression_stats = optimizer.compressor.get_stats()
    print(f"   Original Size: {len(test_data)} bytes")
    print(f"   Compressed Size: {len(compressed_data)} bytes")
    print(f"   Compression Ratio: {compression_stats['compression_ratio']:.2f}")
    print(f"   Data Integrity: {'OK' if test_data == decompressed_data else 'FAILED'}")
    
    # Test multi-threaded scanning
    print("\n4. Multi-threaded Scanning:")
    
    def dummy_scan_function(scan_id: int) -> Dict[str, Any]:
        """Dummy scan function for testing"""
        time.sleep(0.1)  # Simulate scan work
        return {
            'scan_id': scan_id,
            'devices_found': np.random.randint(1, 10),
            'scan_time': time.time()
        }
    
    # Submit batch scan
    batch_args = [(i,) for i in range(10)]
    start_time = time.time()
    results = optimizer.scanner.submit_batch_scan(dummy_scan_function, batch_args)
    end_time = time.time()
    
    successful_scans = sum(1 for r in results if r and r['success'])
    print(f"   Batch Scans: {len(batch_args)}")
    print(f"   Successful Scans: {successful_scans}")
    print(f"   Total Time: {end_time - start_time:.2f} seconds")
    print(f"   Average Time per Scan: {(end_time - start_time) / len(batch_args):.3f} seconds")
    
    # Test memory optimization
    print("\n5. Memory Optimization:")
    
    # Create some objects to optimize
    test_objects = [list(range(1000)) for _ in range(100)]
    
    memory_before = optimizer.memory_optimizer.monitor_memory()
    optimization_results = optimizer.memory_optimizer.optimize_memory()
    memory_after = optimizer.memory_optimizer.monitor_memory()
    
    print(f"   Objects Collected: {optimization_results['objects_collected']}")
    print(f"   Memory Before: {memory_before['memory_percent']:.1f}%")
    print(f"   Memory After: {memory_after['memory_percent']:.1f}%")
    print(f"   GC Objects: {memory_after['gc_stats']['objects']}")
    
    # Test performance profiling
    print("\n6. Performance Profiling:")
    
    def test_function():
        """Test function for profiling"""
        data = []
        for i in range(10000):
            data.append(i * 2)
        return sum(data)
    
    optimizer.profiler.start_profiling('test_profile')
    result = test_function()
    profile_data = optimizer.profiler.stop_profiling('test_profile')
    
    if profile_data:
        print(f"   Function: {profile_data.function_name}")
        print(f"   Call Count: {profile_data.call_count}")
        print(f"   Total Time: {profile_data.total_time:.6f} seconds")
        print(f"   Average Time: {profile_data.average_time:.6f} seconds")
    
    # Test database optimization
    print("\n7. Database Optimization:")
    
    db_path = "test_performance.db"
    db_optimizer = DatabaseOptimizer(db_path)
    
    # Create test table
    conn = db_optimizer.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value INTEGER,
            timestamp DATETIME
        )
    ''')
    
    # Insert test data
    test_data = [
        (i, f"name_{i}", i * 10, datetime.now())
        for i in range(1000)
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO test_table (id, name, value, timestamp) VALUES (?, ?, ?, ?)",
        test_data
    )
    conn.commit()
    db_optimizer.return_connection(conn)
    
    # Optimize database
    db_optimizer.optimize_database()
    
    # Create index
    index_created = db_optimizer.create_index('test_table', ['name', 'value'])
    
    # Analyze query performance
    query_stats = db_optimizer.analyze_query_performance(
        "SELECT * FROM test_table WHERE name LIKE 'name_1%' ORDER BY value"
    )
    
    table_stats = db_optimizer.get_table_stats('test_table')
    
    print(f"   Table Rows: {table_stats['row_count']}")
    print(f"   Table Size: {table_stats['table_size']} bytes")
    print(f"   Index Created: {index_created}")
    print(f"   Query Time: {query_stats.get('execution_time', 0):.6f} seconds")
    
    # Clean up
    Path(db_path).unlink(missing_ok=True)
    
    # Test system optimization
    print("\n8. System Optimization:")
    
    optimization_results = optimizer.optimize_system()
    print(f"   Optimization Time: {optimization_results['optimization_time']:.3f} seconds")
    
    if 'memory_optimization' in optimization_results:
        print(f"   Memory Objects Collected: {optimization_results['memory_optimization']['objects_collected']}")
    
    if 'cache_optimization' in optimization_results:
        print(f"   Cache Cleared: {optimization_results['cache_optimization']['cache_cleared']}")
    
    # Get comprehensive performance report
    print("\n9. Performance Report:")
    
    report = optimizer.get_performance_report()
    print(f"   Total Optimizations: {report['optimization_stats']['optimizations_performed']}")
    print(f"   Memory Optimizations: {report['optimization_stats']['memory_optimizations']}")
    print(f"   Cache Hit Rate: {report['cache_stats']['hit_rate']:.2f}")
    
    if report['system_metrics']:
        print(f"   Average CPU: {report['system_metrics'].get('avg_cpu_percent', 0):.1f}%")
        print(f"   Average Memory: {report['system_metrics'].get('avg_memory_percent', 0):.1f}%")
    
    # Shutdown
    optimizer.shutdown()
    
    print("\nPerformance Optimization Demo Complete!")
    return {
        'optimizer': optimizer,
        'cache_hit_rate': cache_stats['hit_rate'],
        'compression_ratio': compression_stats['compression_ratio'],
        'successful_scans': successful_scans,
        'objects_collected': optimization_results.get('garbage_collection', {}).get('objects_collected', 0)
    }

if __name__ == "__main__":
    demo_performance_optimization()
