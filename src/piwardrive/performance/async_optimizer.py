"""
Async performance optimization utilities for PiWardrive.

This module provides tools for optimizing async operations, managing
concurrent tasks, and monitoring async performance.
"""

import asyncio
import functools
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TypeVar
from weakref import WeakSet

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class AsyncMetrics:
    """Metrics for async operation performance."""

    operation_name: str
    execution_time: float
    queue_time: float
    success: bool
    error: Optional[str]
    timestamp: float


class AsyncPerformanceMonitor:
    """Monitor async operation performance and detect bottlenecks."""

    def __init__(self, max_metrics: int = 10000):
        """Initialize the async performance monitor.

        Args:
            max_metrics: Maximum number of metrics to store in memory.
        """
        self.metrics: deque[AsyncMetrics] = deque(maxlen=max_metrics)
        self.active_operations: Dict[str, float] = {}
        self.operation_counts: Dict[str, int] = defaultdict(int)
        self.slow_operations: List[AsyncMetrics] = []
        self.slow_threshold = 0.1  # 100ms

        # Queue time tracking
        self.queued_operations: Dict[str, float] = {}
        self.queue_metrics: Dict[str, List[float]] = defaultdict(list)

    def queue_operation(self, operation_name: str) -> str:
        """Queue an operation for execution tracking."""
        operation_id = f"{operation_name}_{time.time()}_{id(self)}"
        self.queued_operations[operation_id] = time.time()
        return operation_id

    def start_operation(self, operation_name: str) -> str:
        """Start tracking an async operation."""
        operation_id = f"{operation_name}_{time.time()}_{id(self)}"

        # Check if operation was previously queued
        if operation_id in self.queued_operations:
            # Calculate queue time
            queue_start = self.queued_operations.pop(operation_id)
            queue_time = time.time() - queue_start
            self.queue_metrics[operation_name].append(queue_time)

        self.active_operations[operation_id] = time.time()
        return operation_id

    def end_operation(
        self, operation_id: str, success: bool = True, error: Optional[str] = None
    ):
        """End tracking an async operation."""
        if operation_id not in self.active_operations:
            return

        start_time = self.active_operations.pop(operation_id)
        execution_time = time.time() - start_time

        # Extract operation name from ID
        operation_name = operation_id.split("_")[0]

        # Calculate queue time from metrics
        queue_time = 0.0
        if operation_name in self.queue_metrics and self.queue_metrics[operation_name]:
            queue_time = self.queue_metrics[operation_name].pop(0)

        metric = AsyncMetrics(
            operation_name=operation_name,
            execution_time=execution_time,
            queue_time=queue_time,
            success=success,
            error=error,
            timestamp=time.time(),
        )

        self.metrics.append(metric)
        self.operation_counts[operation_name] += 1

        # Track slow operations
        if execution_time > self.slow_threshold:
            self.slow_operations.append(metric)
            if len(self.slow_operations) > 100:  # Keep only recent slow operations
                self.slow_operations = self.slow_operations[-100:]

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of async performance metrics."""
        if not self.metrics:
            return {"message": "No metrics available"}

        # Group metrics by operation
        operation_metrics = defaultdict(list)
        for metric in self.metrics:
            operation_metrics[metric.operation_name].append(metric)

        summary = {
            "total_operations": len(self.metrics),
            "active_operations": len(self.active_operations),
            "slow_operations": len(self.slow_operations),
            "operation_summary": {},
        }

        for op_name, metrics in operation_metrics.items():
            successful = [m for m in metrics if m.success]
            [m for m in metrics if not m.success]

            if metrics:
                avg_time = sum(m.execution_time for m in metrics) / len(metrics)
                max_time = max(m.execution_time for m in metrics)
                min_time = min(m.execution_time for m in metrics)

                # Calculate queue time statistics
                queue_times = [m.queue_time for m in metrics if m.queue_time > 0]
                avg_queue_time = (
                    sum(queue_times) / len(queue_times) if queue_times else 0
                )
                max_queue_time = max(queue_times) if queue_times else 0

                summary["operation_summary"][op_name] = {
                    "count": len(metrics),
                    "success_rate": len(successful) / len(metrics) * 100,
                    "avg_time": avg_time,
                    "max_time": max_time,
                    "min_time": min_time,
                    "avg_queue_time": avg_queue_time,
                    "max_queue_time": max_queue_time,
                    "slow_count": len(
                        [m for m in metrics if m.execution_time > self.slow_threshold]
                    ),
                }

        return summary

    @asynccontextmanager
    async def monitor_queued_operation(self, operation_name: str):
        """Context manager for monitoring queued operations."""
        self.queue_operation(operation_name)
        try:
            # When entering the context, start the operation
            actual_id = self.start_operation(operation_name)
            yield actual_id
            # Success
            self.end_operation(actual_id, success=True)
        except Exception as e:
            # Error
            self.end_operation(actual_id, success=False, error=str(e))
            raise

    def get_queue_statistics(self) -> Dict[str, Any]:
        """Get queue time statistics."""
        if not self.queue_metrics:
            return {"message": "No queue metrics available"}

        queue_stats = {}
        for op_name, queue_times in self.queue_metrics.items():
            if queue_times:
                queue_stats[op_name] = {
                    "count": len(queue_times),
                    "avg_queue_time": sum(queue_times) / len(queue_times),
                    "max_queue_time": max(queue_times),
                    "min_queue_time": min(queue_times),
                }

        return {
            "queue_statistics": queue_stats,
            "total_queued_operations": sum(
                len(times) for times in self.queue_metrics.values()
            ),
            "operations_with_queue_time": len(queue_stats),
        }


def monitor_async_performance(
    operation_name: str, monitor: Optional[AsyncPerformanceMonitor] = None
):
    """Monitor async function performance with metrics collection."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            if monitor is None:
                return await func(*args, **kwargs)

            operation_id = monitor.start_operation(operation_name)
            try:
                result = await func(*args, **kwargs)
                monitor.end_operation(operation_id, success=True)
                return result
            except Exception as e:
                monitor.end_operation(operation_id, success=False, error=str(e))
                raise

        return wrapper

    return decorator


class AsyncTaskQueue:
    """Priority-based async task queue for background processing."""

    def __init__(self, max_workers: int = 4, name: str = "TaskQueue"):
        self.max_workers = max_workers
        self.name = name
        self.queue = asyncio.PriorityQueue()
        self.workers: List[asyncio.Task] = []
        self.running = False
        self._stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_execution_time": 0,
            "queue_size": 0,
        }

    async def start(self):
        """Start the task queue workers."""
        if self.running:
            return

        self.running = True
        self.workers = [
            asyncio.create_task(self._worker(i)) for i in range(self.max_workers)
        ]
        logger.info(f"Started {self.name} with {self.max_workers} workers")

    async def stop(self):
        """Stop the task queue workers."""
        if not self.running:
            return

        self.running = False

        # Cancel all workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()

        logger.info(f"Stopped {self.name}")

    async def add_task(self, priority: int, coro: Callable[..., Any], *args, **kwargs):
        """Add a task to the queue with given priority (lower number = higher priority)."""
        task_item = (priority, time.time(), coro, args, kwargs)
        await self.queue.put(task_item)
        self._stats["queue_size"] = self.queue.qsize()

    async def _worker(self, worker_id: int):
        """Worker coroutine that processes tasks from the queue."""
        logger.debug(f"Worker {worker_id} started for {self.name}")

        while self.running:
            try:
                # Get task from queue with timeout
                task_item = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                priority, queued_time, coro, args, kwargs = task_item

                # Execute the task
                start_time = time.time()
                try:
                    if asyncio.iscoroutinefunction(coro):
                        await coro(*args, **kwargs)
                    else:
                        # Run sync function in thread pool
                        await asyncio.get_event_loop().run_in_executor(
                            None, coro, *args, **kwargs
                        )

                    execution_time = time.time() - start_time
                    self._stats["tasks_completed"] += 1
                    self._stats["total_execution_time"] += execution_time

                    logger.debug(
                        f"Worker {worker_id} completed task in {execution_time:.3f}s"
                    )

                except Exception as e:
                    self._stats["tasks_failed"] += 1
                    logger.error(f"Worker {worker_id} task failed: {e}")
                finally:
                    self.queue.task_done()
                    self._stats["queue_size"] = self.queue.qsize()

            except asyncio.TimeoutError:
                # No task available, continue
                continue
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                if self.running:
                    await asyncio.sleep(1)  # Brief pause before retrying

    def get_stats(self) -> Dict[str, Any]:
        """Get task queue statistics."""
        _stats = dict(self.stats)
        _stats["workers"] = len(self.workers)
        _stats["running"] = self.running
        if _stats["tasks_completed"] > 0:
            _stats["avg_execution_time"] = (
                _stats["total_execution_time"] / _stats["tasks_completed"]
            )
        return _stats


class AsyncResourcePool:
    """Generic async resource pool for managing limited resources."""

    def __init__(
        self,
        create_resource: Callable[[], T],
        max_size: int = 10,
        name: str = "ResourcePool",
    ):
        self.create_resource = create_resource
        self.max_size = max_size
        self.name = name
        self.pool: asyncio.Queue[T] = asyncio.Queue(maxsize=max_size)
        self.created_count = 0
        self.active_resources: WeakSet[T] = WeakSet()
        self._stats = {
            "acquired": 0,
            "released": 0,
            "created": 0,
            "pool_size": 0,
            "active_count": 0,
        }

    async def acquire(self) -> T:
        """Acquire a resource from the pool."""
        try:
            # Try to get an existing resource
            resource = self.pool.get_nowait()
            self._stats["acquired"] += 1
            self._stats["pool_size"] = self.pool.qsize()
            self.active_resources.add(resource)
            return resource
        except asyncio.QueueEmpty:
            # Create new resource if under limit
            if self.created_count < self.max_size:
                resource = await self._create_resource()
                self.active_resources.add(resource)
                self._stats["acquired"] += 1
                self._stats["created"] += 1
                self.created_count += 1
                return resource
            else:
                # Wait for a resource to become available
                resource = await self.pool.get()
                self._stats["acquired"] += 1
                self._stats["pool_size"] = self.pool.qsize()
                self.active_resources.add(resource)
                return resource

    async def release(self, resource: T):
        """Release a resource back to the pool."""
        if resource in self.active_resources:
            self.active_resources.discard(resource)
            await self.pool.put(resource)
            self._stats["released"] += 1
            self._stats["pool_size"] = self.pool.qsize()

    async def _create_resource(self) -> T:
        """Create a new resource."""
        if asyncio.iscoroutinefunction(self.create_resource):
            return await self.create_resource()
        else:
            return self.create_resource()

    @asynccontextmanager
    async def get_resource(self):
        """Context manager for acquiring and releasing resources."""
        resource = await self.acquire()
        try:
            yield resource
        finally:
            await self.release(resource)

    def get_stats(self) -> Dict[str, Any]:
        """Get resource pool statistics."""
        _stats = dict(self.stats)
        _stats["max_size"] = self.max_size
        _stats["created_count"] = self.created_count
        _stats["active_count"] = len(self.active_resources)
        return _stats


class AsyncRateLimiter:
    """Rate limiter for async operations to prevent overwhelming resources."""

    def __init__(self, max_requests: int, time_window: float = 1.0):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: deque[float] = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Acquire permission to proceed (blocks if rate limit exceeded)."""
        async with self.lock:
            now = time.time()

            # Remove old requests outside the time window
            while self.requests and self.requests[0] <= now - self.time_window:
                self.requests.popleft()

            # If we're at the limit, wait until we can proceed
            if len(self.requests) >= self.max_requests:
                sleep_time = self.requests[0] + self.time_window - now
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    return await self.acquire()  # Recursively try again

            # Record this request
            self.requests.append(now)

    @asynccontextmanager
    async def limit(self):
        """Context manager for rate limiting."""
        await self.acquire()
        yield


class AsyncCircuitBreaker:
    """Circuit breaker for async operations to handle service failures."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        name: str = "CircuitBreaker",
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.lock = asyncio.Lock()

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Call a function through the circuit breaker."""
        async with self.lock:
            if self.state == "OPEN":
                if (
                    self.last_failure_time
                    and time.time() - self.last_failure_time > self.recovery_timeout
                ):
                    self.state = "HALF_OPEN"
                    logger.info(f"Circuit breaker {self.name} entering HALF_OPEN state")
                else:
                    raise Exception(f"Circuit breaker {self.name} is OPEN")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Success - reset failure count
            async with self.lock:
                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    logger.info(
                        f"Circuit breaker {self.name} returning to CLOSED state"
                    )
                self.failure_count = 0

            return result

        except Exception:
            async with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logger.warning(
                        f"Circuit breaker {self.name} opening due to {self.failure_count} failures"
                    )

            raise

    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "last_failure_time": self.last_failure_time,
            "recovery_timeout": self.recovery_timeout,
        }


class AsyncBatchProcessor:
    """Batch processor for async operations to improve throughput."""

    def __init__(
        self,
        batch_size: int = 100,
        flush_interval: float = 1.0,
        processor: Callable[[List[T]], Any] = None,
    ):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.processor = processor
        self.batch: List[T] = []
        self.last_flush = time.time()
        self.lock = asyncio.Lock()
        self._stats = {
            "items_processed": 0,
            "batches_processed": 0,
            "total_processing_time": 0,
        }

    async def add_item(self, item: T):
        """Add an item to the batch."""
        async with self.lock:
            self.batch.append(item)

            # Flush if batch is full or enough time has passed
            if (
                len(self.batch) >= self.batch_size
                or time.time() - self.last_flush >= self.flush_interval
            ):
                await self._flush_batch()

    async def flush(self):
        """Manually flush the current batch."""
        async with self.lock:
            await self._flush_batch()

    async def _flush_batch(self):
        """Internal method to flush the current batch."""
        if not self.batch:
            return

        batch_to_process = self.batch.copy()
        self.batch.clear()
        self.last_flush = time.time()

        if self.processor:
            start_time = time.time()
            try:
                if asyncio.iscoroutinefunction(self.processor):
                    await self.processor(batch_to_process)
                else:
                    self.processor(batch_to_process)

                processing_time = time.time() - start_time
                self._stats["items_processed"] += len(batch_to_process)
                self._stats["batches_processed"] += 1
                self._stats["total_processing_time"] += processing_time

            except Exception as e:
                logger.error(f"Batch processing failed: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get batch processing statistics."""
        _stats = dict(self.stats)
        _stats["current_batch_size"] = len(self.batch)
        _stats["batch_size_limit"] = self.batch_size
        _stats["flush_interval"] = self.flush_interval
        if _stats["batches_processed"] > 0:
            _stats["avg_processing_time"] = (
                _stats["total_processing_time"] / _stats["batches_processed"]
            )
            _stats["avg_batch_size"] = (
                _stats["items_processed"] / _stats["batches_processed"]
            )
        return _stats


class AsyncOptimizer:
    """Main async optimization coordinator that combines all async optimization tools."""

    def __init__(
        self,
        max_concurrent_tasks: int = 100,
        max_queue_size: int = 1000,
        monitor_slow_threshold: float = 0.1,
        enable_circuit_breaker: bool = True,
        enable_rate_limiting: bool = True,
    ):
        self.monitor = AsyncPerformanceMonitor()
        self.monitor.slow_threshold = monitor_slow_threshold

        self.task_queue = AsyncTaskQueue(max_size=max_queue_size)
        self.resource_pool = AsyncResourcePool(max_size=max_concurrent_tasks)

        self.circuit_breaker = None
        self.rate_limiter = None

        if enable_circuit_breaker:
            self.circuit_breaker = AsyncCircuitBreaker(
                failure_threshold=5, recovery_timeout=30.0, call_timeout=10.0
            )

        if enable_rate_limiting:
            self.rate_limiter = AsyncRateLimiter(
                rate=100, per=1.0  # 100 requests per second
            )

    async def optimize_coroutine(
        self, coro: Callable[..., Any], *args, **kwargs
    ) -> Any:
        """Optimize execution of a coroutine with monitoring and protection."""
        operation_name = getattr(coro, "__name__", "unknown")
        operation_id = self.monitor.start_operation(operation_name)

        try:
            # Apply rate limiting if enabled
            if self.rate_limiter:
                await self.rate_limiter.acquire()

            # Execute through circuit breaker if enabled
            if self.circuit_breaker:
                _result = await self.circuit_breaker.call(coro, *args, **kwargs)
            else:
                _result = await coro(*args, **kwargs)

            self.monitor.end_operation(operation_id, success=True)
            return _result

        except Exception as e:
            self.monitor.end_operation(operation_id, success=False, error=str(e))
            raise

    async def optimize_batch(
        self, coros: List[Callable[..., Any]], batch_size: int = 10
    ) -> List[Any]:
        """Optimize batch execution of coroutines."""
        processor = AsyncBatchProcessor(batch_size=batch_size)

        async def _execute_coro(coro_func):
            return await self.optimize_coroutine(coro_func)

        tasks = [_execute_coro(coro) for coro in coros]
        return await processor.process_batch(tasks)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return self.monitor.get_summary()

    async def cleanup(self):
        """Clean up resources."""
        if hasattr(self.task_queue, "cleanup"):
            await self.task_queue.cleanup()
        if hasattr(self.resource_pool, "cleanup"):
            await self.resource_pool.cleanup()


# Global performance monitor instance
_global_monitor = AsyncPerformanceMonitor()


def get_global_monitor() -> AsyncPerformanceMonitor:
    """Get the global async performance monitor."""
    return _global_monitor


async def optimize_async_operations():
    """Apply async performance optimizations."""
    # Set optimal event loop policy
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Optimize task creation
    loop = asyncio.get_event_loop()
    loop.slow_callback_duration = 0.1  # Log slow callbacks

    logger.info("Applied async performance optimizations")


if __name__ == "__main__":
    import random

    async def test_async_performance():
        """Test async performance monitoring."""
        monitor = AsyncPerformanceMonitor()

        @monitor_async_performance("test_operation", monitor)
        async def test_operation(delay: float):
            await asyncio.sleep(delay)
            if random.random() < 0.1:  # 10% failure rate
                raise Exception("Random failure")

        # Test queued operations
        async def test_queued_operation(delay: float):
            operation_id = monitor.queue_operation("queued_test")
            await asyncio.sleep(0.01)  # Simulate queue wait time
            monitor.start_operation("queued_test")
            try:
                await asyncio.sleep(delay)
                monitor.end_operation(operation_id, success=True)
            except Exception as e:
                monitor.end_operation(operation_id, success=False, error=str(e))

        # Run test operations
        tasks = []
        for i in range(100):
            delay = random.uniform(0.01, 0.2)
            tasks.append(test_operation(delay))

        # Run some queued operations
        for i in range(20):
            delay = random.uniform(0.01, 0.1)
            tasks.append(test_queued_operation(delay))

        # Execute with some failures
        _results = await asyncio.gather(*tasks, return_exceptions=True)

        # Print performance summary
        summary = monitor.get_performance_summary()
        print("Async Performance Test Results:")
        print(f"Total operations: {summary['total_operations']}")
        print(f"Slow operations: {summary['slow_operations']}")

        for op_name, stats in summary["operation_summary"].items():
            print(f"\n{op_name}:")
            print(f"  Count: {stats['count']}")
            print(f"  Success rate: {stats['success_rate']:.1f}%")
            print(f"  Avg time: {stats['avg_time']:.3f}s")
            print(f"  Max time: {stats['max_time']:.3f}s")
            print(f"  Avg queue time: {stats['avg_queue_time']:.3f}s")
            print(f"  Max queue time: {stats['max_queue_time']:.3f}s")
            print(f"  Slow count: {stats['slow_count']}")

        # Print queue statistics
        queue_stats = monitor.get_queue_statistics()
        print(f"\nQueue Statistics:")
        print(
            f"Total queued operations: {queue_stats.get('total_queued_operations', 0)}"
        )
        print(
            f"Operations with queue time: {queue_stats.get('operations_with_queue_time', 0)}"
        )
        for op_name, stats in queue_stats.get("queue_statistics", {}).items():
            print(
                f"  {op_name}: avg={stats['avg_queue_time']:.3f}s, max={stats['max_queue_time']:.3f}s"
            )

    asyncio.run(test_async_performance())
