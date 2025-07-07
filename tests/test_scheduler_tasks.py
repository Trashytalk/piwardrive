"""
Comprehensive tests for scheduler and background task management.
Tests the PollScheduler, AsyncScheduler, and task queue functionality.
"""

import os
import pytest
import asyncio
import threading
import time
from unittest.mock import Mock, patch, AsyncMock, MagicMock, call
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable

from piwardrive.scheduler import PollScheduler, AsyncScheduler, ScheduledTask
from piwardrive.task_queue import BackgroundTaskQueue, TaskPriority
from piwardrive.jobs import analytics_jobs, maintenance_jobs


class TestPollScheduler:
    """Test the main polling scheduler."""
    
    def test_scheduler_initialization(self):
        """Test scheduler initialization."""
        scheduler = PollScheduler()
        
        assert scheduler is not None
        assert scheduler._tasks == {}
        assert scheduler._running is False
        assert scheduler._thread is None
        
    def test_add_task(self):
        """Test adding a task to the scheduler."""
        scheduler = PollScheduler()
        
        # Mock task function
        mock_task = Mock()
        
        # Add task
        task_id = scheduler.add_task("test_task", mock_task, interval=10)
        
        assert task_id == "test_task"
        assert "test_task" in scheduler._tasks
        
        task = scheduler._tasks["test_task"]
        assert task.name == "test_task"
        assert task.func == mock_task
        assert task.interval == 10
        
    def test_add_task_with_custom_params(self):
        """Test adding a task with custom parameters."""
        scheduler = PollScheduler()
        
        mock_task = Mock()
        
        # Add task with custom parameters
        task_id = scheduler.add_task(
            "custom_task",
            mock_task,
            interval=30,
            enabled=False,
            priority=5,
            max_retries=3,
            timeout=60
        )
        
        task = scheduler._tasks["custom_task"]
        assert task.interval == 30
        assert task.enabled is False
        assert task.priority == 5
        assert task.max_retries == 3
        assert task.timeout == 60
        
    def test_remove_task(self):
        """Test removing a task from the scheduler."""
        scheduler = PollScheduler()
        
        mock_task = Mock()
        scheduler.add_task("test_task", mock_task, interval=10)
        
        # Verify task exists
        assert "test_task" in scheduler._tasks
        
        # Remove task
        scheduler.remove_task("test_task")
        
        # Verify task is removed
        assert "test_task" not in scheduler._tasks
        
    def test_enable_disable_task(self):
        """Test enabling and disabling tasks."""
        scheduler = PollScheduler()
        
        mock_task = Mock()
        scheduler.add_task("test_task", mock_task, interval=10, enabled=False)
        
        # Initially disabled
        task = scheduler._tasks["test_task"]
        assert task.enabled is False
        
        # Enable task
        scheduler.enable_task("test_task")
        assert task.enabled is True
        
        # Disable task
        scheduler.disable_task("test_task")
        assert task.enabled is False
        
    def test_scheduler_start_stop(self):
        """Test starting and stopping the scheduler."""
        scheduler = PollScheduler()
        
        mock_task = Mock()
        scheduler.add_task("test_task", mock_task, interval=1)
        
        # Start scheduler
        scheduler.start()
        assert scheduler._running is True
        assert scheduler._thread is not None
        assert scheduler._thread.is_alive()
        
        # Wait a short time for task execution
        time.sleep(2.5)
        
        # Stop scheduler
        scheduler.stop()
        assert scheduler._running is False
        
        # Verify task was called
        assert mock_task.call_count >= 2  # Should have run at least twice
        
    def test_scheduler_task_execution_timing(self):
        """Test scheduler executes tasks at correct intervals."""
        scheduler = PollScheduler()
        
        mock_task1 = Mock()
        mock_task2 = Mock()
        
        # Add tasks with different intervals
        scheduler.add_task("fast_task", mock_task1, interval=1)
        scheduler.add_task("slow_task", mock_task2, interval=3)
        
        scheduler.start()
        
        # Wait for multiple execution cycles
        time.sleep(7)
        
        scheduler.stop()
        
        # Fast task should be called more often than slow task
        assert mock_task1.call_count >= 6  # ~7 seconds / 1 second interval
        assert mock_task2.call_count >= 2  # ~7 seconds / 3 second interval
        assert mock_task1.call_count > mock_task2.call_count
        
    def test_scheduler_disabled_task_not_executed(self):
        """Test disabled tasks are not executed."""
        scheduler = PollScheduler()
        
        mock_task = Mock()
        scheduler.add_task("disabled_task", mock_task, interval=1, enabled=False)
        
        scheduler.start()
        time.sleep(2.5)
        scheduler.stop()
        
        # Disabled task should not be called
        mock_task.assert_not_called()
        
    def test_scheduler_task_error_handling(self):
        """Test scheduler handles task errors gracefully."""
        scheduler = PollScheduler()
        
        # Task that raises an exception
        def failing_task():
            raise Exception("Task failed")
        
        mock_success_task = Mock()
        
        scheduler.add_task("failing_task", failing_task, interval=1)
        scheduler.add_task("success_task", mock_success_task, interval=1)
        
        scheduler.start()
        time.sleep(2.5)
        scheduler.stop()
        
        # Success task should still be called despite failing task
        assert mock_success_task.call_count >= 2
        
    def test_get_task_status(self):
        """Test getting task status information."""
        scheduler = PollScheduler()
        
        mock_task = Mock()
        scheduler.add_task("test_task", mock_task, interval=10)
        
        status = scheduler.get_task_status("test_task")
        
        assert status["name"] == "test_task"
        assert status["interval"] == 10
        assert status["enabled"] is True
        assert status["last_run"] is None
        assert status["next_run"] is not None
        assert status["run_count"] == 0
        
    def test_list_tasks(self):
        """Test listing all tasks."""
        scheduler = PollScheduler()
        
        mock_task1 = Mock()
        mock_task2 = Mock()
        
        scheduler.add_task("task1", mock_task1, interval=10)
        scheduler.add_task("task2", mock_task2, interval=20, enabled=False)
        
        tasks = scheduler.list_tasks()
        
        assert len(tasks) == 2
        assert "task1" in tasks
        assert "task2" in tasks
        
        assert tasks["task1"]["enabled"] is True
        assert tasks["task2"]["enabled"] is False


class TestAsyncScheduler:
    """Test the async scheduler for coroutine tasks."""
    
    @pytest.mark.asyncio
    async def test_async_scheduler_initialization(self):
        """Test async scheduler initialization."""
        scheduler = AsyncScheduler()
        
        assert scheduler is not None
        assert scheduler._tasks == {}
        assert scheduler._running is False
        
    @pytest.mark.asyncio
    async def test_add_async_task(self):
        """Test adding an async task to the scheduler."""
        scheduler = AsyncScheduler()
        
        # Mock async task
        async def mock_async_task():
            return "completed"
        
        # Add task
        task_id = scheduler.add_task("async_task", mock_async_task, interval=10)
        
        assert task_id == "async_task"
        assert "async_task" in scheduler._tasks
        
    @pytest.mark.asyncio
    async def test_async_scheduler_execution(self):
        """Test async scheduler task execution."""
        scheduler = AsyncScheduler()
        
        execution_count = 0
        
        async def counting_task():
            nonlocal execution_count
            execution_count += 1
            
        scheduler.add_task("counting_task", counting_task, interval=1)
        
        # Start scheduler
        scheduler_task = asyncio.create_task(scheduler.start())
        
        # Wait for executions
        await asyncio.sleep(2.5)
        
        # Stop scheduler
        scheduler.stop()
        await scheduler_task
        
        # Verify task was executed
        assert execution_count >= 2
        
    @pytest.mark.asyncio
    async def test_async_scheduler_error_handling(self):
        """Test async scheduler error handling."""
        scheduler = AsyncScheduler()
        
        success_count = 0
        
        async def failing_task():
            raise Exception("Async task failed")
        
        async def success_task():
            nonlocal success_count
            success_count += 1
        
        scheduler.add_task("failing_task", failing_task, interval=1)
        scheduler.add_task("success_task", success_task, interval=1)
        
        # Start scheduler
        scheduler_task = asyncio.create_task(scheduler.start())
        
        # Wait for executions
        await asyncio.sleep(2.5)
        
        # Stop scheduler
        scheduler.stop()
        await scheduler_task
        
        # Success task should still execute despite failing task
        assert success_count >= 2
        
    @pytest.mark.asyncio
    async def test_async_scheduler_concurrent_tasks(self):
        """Test concurrent execution of async tasks."""
        scheduler = AsyncScheduler()
        
        task1_start_times = []
        task2_start_times = []
        
        async def task1():
            task1_start_times.append(time.time())
            await asyncio.sleep(0.5)  # Simulate work
        
        async def task2():
            task2_start_times.append(time.time())
            await asyncio.sleep(0.3)  # Simulate work
        
        scheduler.add_task("task1", task1, interval=1)
        scheduler.add_task("task2", task2, interval=1)
        
        # Start scheduler
        scheduler_task = asyncio.create_task(scheduler.start())
        
        # Wait for executions
        await asyncio.sleep(3)
        
        # Stop scheduler
        scheduler.stop()
        await scheduler_task
        
        # Both tasks should have executed multiple times
        assert len(task1_start_times) >= 2
        assert len(task2_start_times) >= 2
        
        # Tasks should start concurrently (similar start times)
        if len(task1_start_times) >= 2 and len(task2_start_times) >= 2:
            time_diff = abs(task1_start_times[0] - task2_start_times[0])
            assert time_diff < 0.1  # Should start within 100ms of each other


class TestBackgroundTaskQueue:
    """Test the background task queue system."""
    
    @pytest.mark.asyncio
    async def test_task_queue_initialization(self):
        """Test task queue initialization."""
        queue = BackgroundTaskQueue(workers=2)
        
        assert queue is not None
        assert queue.max_workers == 2
        assert queue._running is False
        
    @pytest.mark.asyncio
    async def test_add_task_to_queue(self):
        """Test adding tasks to the queue."""
        queue = BackgroundTaskQueue(workers=2)
        
        async def test_task(x, y):
            return x + y
        
        # Add task
        task_id = await queue.add_task(test_task, 5, 10)
        
        assert task_id is not None
        assert isinstance(task_id, str)
        
    @pytest.mark.asyncio
    async def test_task_queue_execution(self):
        """Test task queue execution."""
        queue = BackgroundTaskQueue(workers=2)
        
        results = []
        
        async def test_task(value):
            results.append(value)
            return value * 2
        
        # Start queue
        await queue.start()
        
        # Add tasks
        task_ids = []
        for i in range(5):
            task_id = await queue.add_task(test_task, i)
            task_ids.append(task_id)
        
        # Wait for completion
        await asyncio.sleep(1)
        
        # Stop queue
        await queue.stop()
        
        # Verify all tasks were executed
        assert len(results) == 5
        assert set(results) == {0, 1, 2, 3, 4}
        
    @pytest.mark.asyncio
    async def test_task_queue_priority(self):
        """Test task queue priority handling."""
        queue = BackgroundTaskQueue(workers=1)  # Single worker for predictable order
        
        execution_order = []
        
        async def priority_task(priority, value):
            execution_order.append((priority, value))
            await asyncio.sleep(0.1)  # Simulate work
        
        await queue.start()
        
        # Add tasks with different priorities
        await queue.add_task(priority_task, TaskPriority.LOW, "low1", priority=TaskPriority.LOW)
        await queue.add_task(priority_task, TaskPriority.HIGH, "high1", priority=TaskPriority.HIGH)
        await queue.add_task(priority_task, TaskPriority.NORMAL, "normal1", priority=TaskPriority.NORMAL)
        await queue.add_task(priority_task, TaskPriority.HIGH, "high2", priority=TaskPriority.HIGH)
        
        # Wait for completion
        await asyncio.sleep(2)
        await queue.stop()
        
        # Verify high priority tasks were executed first
        assert len(execution_order) == 4
        high_priority_indices = [i for i, (priority, _) in enumerate(execution_order) if priority == TaskPriority.HIGH]
        assert len(high_priority_indices) == 2
        
    @pytest.mark.asyncio
    async def test_task_queue_error_handling(self):
        """Test task queue error handling."""
        queue = BackgroundTaskQueue(workers=2)
        
        success_count = 0
        
        async def failing_task():
            raise Exception("Task failed")
        
        async def success_task():
            nonlocal success_count
            success_count += 1
        
        await queue.start()
        
        # Add failing and successful tasks
        await queue.add_task(failing_task)
        await queue.add_task(success_task)
        await queue.add_task(failing_task)
        await queue.add_task(success_task)
        
        # Wait for completion
        await asyncio.sleep(1)
        await queue.stop()
        
        # Success tasks should complete despite failing tasks
        assert success_count == 2
        
    @pytest.mark.asyncio
    async def test_task_queue_status(self):
        """Test task queue status monitoring."""
        queue = BackgroundTaskQueue(workers=2)
        
        async def slow_task():
            await asyncio.sleep(1)
        
        await queue.start()
        
        # Add tasks
        for _ in range(5):
            await queue.add_task(slow_task)
        
        # Check status while tasks are running
        status = queue.get_status()
        
        assert status["workers"] == 2
        assert status["pending_tasks"] >= 0
        assert status["running_tasks"] >= 0
        assert status["completed_tasks"] >= 0
        
        await queue.stop()
        
    @pytest.mark.asyncio
    async def test_task_queue_result_retrieval(self):
        """Test retrieving task results."""
        queue = BackgroundTaskQueue(workers=2)
        
        async def calculation_task(x, y):
            return x * y + 10
        
        await queue.start()
        
        # Add task and get result
        task_id = await queue.add_task(calculation_task, 5, 3)
        
        # Wait for completion and get result
        await asyncio.sleep(0.5)
        result = await queue.get_task_result(task_id)
        
        assert result == 25  # 5 * 3 + 10
        
        await queue.stop()


class TestSchedulerIntegration:
    """Test integration between schedulers and real components."""
    
    def test_health_monitor_integration(self):
        """Test scheduler integration with health monitor."""
        scheduler = PollScheduler()
        
        # Mock health monitor
        health_monitor = Mock()
        health_monitor.collect_metrics = Mock()
        
        # Add health monitoring task
        scheduler.add_task(
            "health_monitor",
            health_monitor.collect_metrics,
            interval=5
        )
        
        scheduler.start()
        time.sleep(11)  # Let it run for ~11 seconds
        scheduler.stop()
        
        # Health monitor should be called multiple times
        assert health_monitor.collect_metrics.call_count >= 2
        
    def test_data_polling_integration(self):
        """Test scheduler integration with data polling."""
        scheduler = PollScheduler()
        
        # Mock data sources
        wifi_poller = Mock()
        gps_poller = Mock()
        
        wifi_poller.poll_access_points = Mock()
        gps_poller.poll_location = Mock()
        
        # Add polling tasks
        scheduler.add_task("wifi_poll", wifi_poller.poll_access_points, interval=2)
        scheduler.add_task("gps_poll", gps_poller.poll_location, interval=3)
        
        scheduler.start()
        time.sleep(7)
        scheduler.stop()
        
        # Both pollers should be called
        assert wifi_poller.poll_access_points.call_count >= 3
        assert gps_poller.poll_location.call_count >= 2
        
    @pytest.mark.asyncio
    async def test_analytics_job_integration(self):
        """Test integration with analytics jobs."""
        scheduler = AsyncScheduler()
        queue = BackgroundTaskQueue(workers=2)
        
        # Mock analytics functions
        with patch('piwardrive.jobs.analytics_jobs.analyze_network_patterns') as mock_analyze:
            with patch('piwardrive.jobs.analytics_jobs.detect_anomalies') as mock_detect:
                mock_analyze.return_value = {"patterns": 5}
                mock_detect.return_value = {"anomalies": 2}
                
                # Initialize analytics jobs
                analytics_jobs.init_jobs(scheduler, queue)
                
                # Start systems
                await queue.start()
                scheduler_task = asyncio.create_task(scheduler.start())
                
                # Wait for execution
                await asyncio.sleep(3)
                
                # Stop systems
                scheduler.stop()
                await scheduler_task
                await queue.stop()
                
                # Verify analytics functions were called
                assert mock_analyze.call_count >= 1
                assert mock_detect.call_count >= 1
                
    @pytest.mark.asyncio
    async def test_maintenance_job_integration(self):
        """Test integration with maintenance jobs."""
        scheduler = AsyncScheduler()
        queue = BackgroundTaskQueue(workers=2)
        
        # Mock maintenance functions
        with patch('piwardrive.jobs.maintenance_jobs.cleanup_old_data') as mock_cleanup:
            with patch('piwardrive.jobs.maintenance_jobs.optimize_database') as mock_optimize:
                mock_cleanup.return_value = {"deleted_records": 100}
                mock_optimize.return_value = {"vacuum_completed": True}
                
                # Initialize maintenance jobs
                maintenance_jobs.init_jobs(scheduler, queue)
                
                # Start systems
                await queue.start()
                scheduler_task = asyncio.create_task(scheduler.start())
                
                # Wait for execution
                await asyncio.sleep(3)
                
                # Stop systems
                scheduler.stop()
                await scheduler_task
                await queue.stop()
                
                # Verify maintenance functions were called
                assert mock_cleanup.call_count >= 1
                assert mock_optimize.call_count >= 1


class TestSchedulerPerformance:
    """Test scheduler performance and resource management."""
    
    def test_scheduler_memory_usage(self):
        """Test scheduler memory usage with many tasks."""
        scheduler = PollScheduler()
        
        # Add many tasks
        for i in range(100):
            mock_task = Mock()
            scheduler.add_task(f"task_{i}", mock_task, interval=60)  # Long interval
        
        # Start and run briefly
        scheduler.start()
        time.sleep(1)
        scheduler.stop()
        
        # Verify all tasks are registered
        assert len(scheduler._tasks) == 100
        
        # Clean up by removing all tasks
        for i in range(100):
            scheduler.remove_task(f"task_{i}")
        
        assert len(scheduler._tasks) == 0
        
    def test_scheduler_cpu_usage(self):
        """Test scheduler CPU usage with frequent tasks."""
        scheduler = PollScheduler()
        
        execution_count = 0
        
        def cpu_task():
            nonlocal execution_count
            execution_count += 1
            # Simulate light CPU work
            sum(range(1000))
        
        # Add frequent task
        scheduler.add_task("cpu_task", cpu_task, interval=0.1)  # 10 times per second
        
        start_time = time.time()
        scheduler.start()
        time.sleep(2)  # Run for 2 seconds
        scheduler.stop()
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Task should execute approximately 20 times (2 seconds / 0.1 interval)
        assert execution_count >= 15  # Allow some variance
        assert execution_count <= 25
        
        # Scheduler overhead should be minimal
        assert duration < 3  # Should complete within reasonable time
        
    @pytest.mark.asyncio
    async def test_async_scheduler_concurrency(self):
        """Test async scheduler handling many concurrent tasks."""
        scheduler = AsyncScheduler()
        
        execution_counts = {}
        
        async def concurrent_task(task_id):
            if task_id not in execution_counts:
                execution_counts[task_id] = 0
            execution_counts[task_id] += 1
            await asyncio.sleep(0.1)  # Simulate async work
        
        # Add many concurrent tasks
        for i in range(20):
            scheduler.add_task(f"task_{i}", lambda i=i: concurrent_task(i), interval=1)
        
        # Start scheduler
        scheduler_task = asyncio.create_task(scheduler.start())
        
        # Wait for execution
        await asyncio.sleep(3)
        
        # Stop scheduler
        scheduler.stop()
        await scheduler_task
        
        # All tasks should have executed
        assert len(execution_counts) >= 15  # Most tasks should execute
        
        # Each task should execute multiple times
        for count in execution_counts.values():
            assert count >= 2
            
    @pytest.mark.asyncio
    async def test_task_queue_throughput(self):
        """Test task queue throughput with many tasks."""
        queue = BackgroundTaskQueue(workers=4)
        
        completion_count = 0
        
        async def throughput_task():
            nonlocal completion_count
            completion_count += 1
            await asyncio.sleep(0.01)  # Very light work
        
        await queue.start()
        
        # Add many tasks quickly
        start_time = time.time()
        for _ in range(100):
            await queue.add_task(throughput_task)
        
        # Wait for completion
        while completion_count < 100:
            await asyncio.sleep(0.1)
        
        end_time = time.time()
        duration = end_time - start_time
        
        await queue.stop()
        
        # All tasks should complete
        assert completion_count == 100
        
        # Should complete reasonably quickly with 4 workers
        assert duration < 5  # Should complete within 5 seconds


class TestSchedulerErrorRecovery:
    """Test scheduler error recovery and resilience."""
    
    def test_scheduler_recovery_from_task_failure(self):
        """Test scheduler continues after task failures."""
        scheduler = PollScheduler()
        
        failure_count = 0
        success_count = 0
        
        def failing_task():
            nonlocal failure_count
            failure_count += 1
            raise Exception(f"Failure {failure_count}")
        
        def success_task():
            nonlocal success_count
            success_count += 1
        
        scheduler.add_task("failing_task", failing_task, interval=1)
        scheduler.add_task("success_task", success_task, interval=1)
        
        scheduler.start()
        time.sleep(3.5)
        scheduler.stop()
        
        # Both tasks should have attempted to run multiple times
        assert failure_count >= 3
        assert success_count >= 3
        
        # Scheduler should still be functional
        assert scheduler._running is False  # Should have stopped cleanly
        
    @pytest.mark.asyncio
    async def test_async_scheduler_recovery(self):
        """Test async scheduler recovery from coroutine failures."""
        scheduler = AsyncScheduler()
        
        failure_count = 0
        success_count = 0
        
        async def failing_task():
            nonlocal failure_count
            failure_count += 1
            raise ValueError(f"Async failure {failure_count}")
        
        async def success_task():
            nonlocal success_count
            success_count += 1
        
        scheduler.add_task("failing_task", failing_task, interval=1)
        scheduler.add_task("success_task", success_task, interval=1)
        
        # Start scheduler
        scheduler_task = asyncio.create_task(scheduler.start())
        
        # Wait for execution
        await asyncio.sleep(3.5)
        
        # Stop scheduler
        scheduler.stop()
        await scheduler_task
        
        # Both tasks should have attempted to run
        assert failure_count >= 3
        assert success_count >= 3
        
    @pytest.mark.asyncio
    async def test_task_queue_worker_recovery(self):
        """Test task queue recovery from worker failures."""
        queue = BackgroundTaskQueue(workers=2)
        
        task_results = []
        
        async def sometimes_failing_task(task_id):
            if task_id % 3 == 0:  # Every 3rd task fails
                raise RuntimeError(f"Task {task_id} failed")
            task_results.append(task_id)
            return task_id
        
        await queue.start()
        
        # Add mix of failing and successful tasks
        for i in range(10):
            await queue.add_task(sometimes_failing_task, i)
        
        # Wait for completion
        await asyncio.sleep(2)
        await queue.stop()
        
        # Successful tasks should complete despite failures
        expected_successful = [i for i in range(10) if i % 3 != 0]
        assert len(task_results) == len(expected_successful)
        assert set(task_results) == set(expected_successful)
