"""
Tests for the scheduler and task queue system.
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from piwardrive.scheduler import ScheduledTask, Scheduler, TaskStatus
from piwardrive.task_queue import Task, TaskPriority, TaskQueue


class TestScheduler:
    """Test the main scheduler functionality."""

    def setup_method(self):
        """Setup test scheduler."""
        self.scheduler = Scheduler()

    def test_scheduler_initialization(self):
        """Test scheduler initialization."""
        assert self.scheduler is not None
        assert hasattr(self.scheduler, "tasks")
        assert hasattr(self.scheduler, "running")
        assert not self.scheduler.running

    def test_scheduler_start_stop(self):
        """Test scheduler start and stop."""
        assert not self.scheduler.running

        self.scheduler.start()
        assert self.scheduler.running

        self.scheduler.stop()
        assert not self.scheduler.running

    def test_add_task(self):
        """Test adding tasks to scheduler."""
        task = ScheduledTask(name="test_task", func=lambda: "test", interval=60)

        self.scheduler.add_task(task)
        assert len(self.scheduler.tasks) == 1
        assert self.scheduler.tasks[0].name == "test_task"

    def test_remove_task(self):
        """Test removing tasks from scheduler."""
        task = ScheduledTask(name="test_task", func=lambda: "test", interval=60)

        self.scheduler.add_task(task)
        assert len(self.scheduler.tasks) == 1

        self.scheduler.remove_task("test_task")
        assert len(self.scheduler.tasks) == 0

    def test_scheduled_task_execution(self):
        """Test scheduled task execution."""
        executed = []

        def test_func():
            executed.append(datetime.now())

        task = ScheduledTask(name="test_task", func=test_func, interval=0.1)  # 100ms

        self.scheduler.add_task(task)
        self.scheduler.start()

        # Wait for task to execute
        time.sleep(0.2)

        self.scheduler.stop()

        assert len(executed) > 0

    def test_task_error_handling(self):
        """Test task error handling."""

        def failing_task():
            raise Exception("Task failed")

        task = ScheduledTask(name="failing_task", func=failing_task, interval=0.1)

        self.scheduler.add_task(task)
        self.scheduler.start()

        # Wait for task to fail
        time.sleep(0.2)

        self.scheduler.stop()

        # Task should still be in scheduler but marked as failed
        assert len(self.scheduler.tasks) == 1
        assert self.scheduler.tasks[0].status == TaskStatus.FAILED

    def test_task_priority_execution(self):
        """Test task priority execution."""
        execution_order = []

        def high_priority_task():
            execution_order.append("high")

        def low_priority_task():
            execution_order.append("low")

        high_task = ScheduledTask(
            name="high_task",
            func=high_priority_task,
            interval=0.1,
            priority=TaskPriority.HIGH,
        )

        low_task = ScheduledTask(
            name="low_task",
            func=low_priority_task,
            interval=0.1,
            priority=TaskPriority.LOW,
        )

        # Add low priority task first
        self.scheduler.add_task(low_task)
        self.scheduler.add_task(high_task)

        self.scheduler.start()
        time.sleep(0.2)
        self.scheduler.stop()

        # High priority task should execute first
        if execution_order:
            assert execution_order[0] == "high"

    def test_task_dependency_handling(self):
        """Test task dependency handling."""
        execution_order = []

        def task_a():
            execution_order.append("A")

        def task_b():
            execution_order.append("B")

        task_a_obj = ScheduledTask(name="task_a", func=task_a, interval=0.1)

        task_b_obj = ScheduledTask(
            name="task_b", func=task_b, interval=0.1, dependencies=["task_a"]
        )

        self.scheduler.add_task(task_a_obj)
        self.scheduler.add_task(task_b_obj)

        self.scheduler.start()
        time.sleep(0.2)
        self.scheduler.stop()

        # Task A should execute before Task B
        if len(execution_order) >= 2:
            assert execution_order.index("A") < execution_order.index("B")

    def test_scheduler_context_manager(self):
        """Test scheduler as context manager."""
        with self.scheduler:
            assert self.scheduler.running

        assert not self.scheduler.running

    def test_scheduler_statistics(self):
        """Test scheduler statistics collection."""

        def test_task():
            pass

        task = ScheduledTask(name="test_task", func=test_task, interval=0.1)

        self.scheduler.add_task(task)
        self.scheduler.start()
        time.sleep(0.2)
        self.scheduler.stop()

        stats = self.scheduler.get_statistics()
        assert "total_tasks" in stats
        assert "executed_tasks" in stats
        assert "failed_tasks" in stats

    def test_scheduler_health_check(self):
        """Test scheduler health check."""
        health = self.scheduler.health_check()
        assert "status" in health
        assert "running" in health
        assert "task_count" in health


class TestTaskQueue:
    """Test the task queue system."""

    def setup_method(self):
        """Setup test task queue."""
        self.queue = TaskQueue()

    def test_task_queue_initialization(self):
        """Test task queue initialization."""
        assert self.queue is not None
        assert hasattr(self.queue, "tasks")
        assert len(self.queue.tasks) == 0

    def test_enqueue_task(self):
        """Test enqueuing tasks."""
        task = Task(name="test_task", func=lambda: "test", priority=TaskPriority.NORMAL)

        self.queue.enqueue(task)
        assert len(self.queue.tasks) == 1

    def test_dequeue_task(self):
        """Test dequeuing tasks."""
        task = Task(name="test_task", func=lambda: "test", priority=TaskPriority.NORMAL)

        self.queue.enqueue(task)
        dequeued = self.queue.dequeue()

        assert dequeued.name == "test_task"
        assert len(self.queue.tasks) == 0

    def test_task_priority_ordering(self):
        """Test task priority ordering."""
        high_task = Task(
            name="high_task", func=lambda: "high", priority=TaskPriority.HIGH
        )

        low_task = Task(name="low_task", func=lambda: "low", priority=TaskPriority.LOW)

        normal_task = Task(
            name="normal_task", func=lambda: "normal", priority=TaskPriority.NORMAL
        )

        # Add in reverse priority order
        self.queue.enqueue(low_task)
        self.queue.enqueue(normal_task)
        self.queue.enqueue(high_task)

        # Should dequeue in priority order
        first = self.queue.dequeue()
        second = self.queue.dequeue()
        third = self.queue.dequeue()

        assert first.name == "high_task"
        assert second.name == "normal_task"
        assert third.name == "low_task"

    def test_task_execution(self):
        """Test task execution."""
        result = []

        def test_func():
            result.append("executed")

        task = Task(name="test_task", func=test_func, priority=TaskPriority.NORMAL)

        self.queue.enqueue(task)
        executed_task = self.queue.dequeue()
        executed_task.execute()

        assert result == ["executed"]

    def test_task_error_handling(self):
        """Test task error handling."""

        def failing_task():
            raise Exception("Task failed")

        task = Task(
            name="failing_task", func=failing_task, priority=TaskPriority.NORMAL
        )

        self.queue.enqueue(task)
        executed_task = self.queue.dequeue()

        # Task should handle error gracefully
        try:
            executed_task.execute()
        except Exception:
            pass  # Expected to fail

        assert executed_task.status == TaskStatus.FAILED

    def test_task_retry_mechanism(self):
        """Test task retry mechanism."""
        attempts = []

        def flaky_task():
            attempts.append(len(attempts))
            if len(attempts) < 3:
                raise Exception("Temporary failure")
            return "success"

        task = Task(
            name="flaky_task",
            func=flaky_task,
            priority=TaskPriority.NORMAL,
            max_retries=3,
        )

        self.queue.enqueue(task)
        executed_task = self.queue.dequeue()

        # Execute with retries
        for _ in range(4):  # Allow for retries
            try:
                executed_task.execute()
                break
            except Exception:
                if executed_task.retry_count < executed_task.max_retries:
                    executed_task.retry_count += 1
                else:
                    break

        assert len(attempts) == 3
        assert executed_task.status == TaskStatus.COMPLETED

    def test_task_timeout_handling(self):
        """Test task timeout handling."""

        def long_running_task():
            time.sleep(1)
            return "completed"

        task = Task(
            name="long_task",
            func=long_running_task,
            priority=TaskPriority.NORMAL,
            timeout=0.1,  # 100ms timeout
        )

        self.queue.enqueue(task)
        executed_task = self.queue.dequeue()

        start_time = time.time()
        executed_task.execute()
        end_time = time.time()

        # Should timeout quickly
        assert end_time - start_time < 0.5
        assert executed_task.status == TaskStatus.FAILED

    def test_queue_statistics(self):
        """Test queue statistics."""
        for i in range(5):
            task = Task(
                name=f"task_{i}", func=lambda: "test", priority=TaskPriority.NORMAL
            )
            self.queue.enqueue(task)

        stats = self.queue.get_statistics()
        assert stats["total_tasks"] == 5
        assert stats["pending_tasks"] == 5
        assert stats["completed_tasks"] == 0


class TestAsyncTaskQueue:
    """Test async task queue functionality."""

    def setup_method(self):
        """Setup async task queue."""
        self.queue = TaskQueue(async_mode=True)

    @pytest.mark.asyncio
    async def test_async_task_execution(self):
        """Test async task execution."""
        result = []

        async def async_task():
            result.append("async_executed")

        task = Task(name="async_task", func=async_task, priority=TaskPriority.NORMAL)

        self.queue.enqueue(task)
        executed_task = self.queue.dequeue()
        await executed_task.execute()

        assert result == ["async_executed"]

    @pytest.mark.asyncio
    async def test_async_task_error_handling(self):
        """Test async task error handling."""

        async def failing_async_task():
            raise Exception("Async task failed")

        task = Task(
            name="failing_async_task",
            func=failing_async_task,
            priority=TaskPriority.NORMAL,
        )

        self.queue.enqueue(task)
        executed_task = self.queue.dequeue()

        try:
            await executed_task.execute()
        except Exception:
            pass  # Expected to fail

        assert executed_task.status == TaskStatus.FAILED

    @pytest.mark.asyncio
    async def test_async_task_concurrency(self):
        """Test async task concurrency."""
        results = []

        async def concurrent_task(task_id):
            await asyncio.sleep(0.1)
            results.append(task_id)

        tasks = []
        for i in range(3):
            task = Task(
                name=f"concurrent_task_{i}",
                func=lambda tid=i: concurrent_task(tid),
                priority=TaskPriority.NORMAL,
            )
            tasks.append(task)
            self.queue.enqueue(task)

        # Execute all tasks concurrently
        executed_tasks = [self.queue.dequeue() for _ in range(3)]
        await asyncio.gather(*[task.execute() for task in executed_tasks])

        assert len(results) == 3


class TestSchedulerIntegration:
    """Test scheduler integration with other systems."""

    def setup_method(self):
        """Setup test scheduler."""
        self.scheduler = Scheduler()

    @patch("piwardrive.scheduler.DatabaseManager")
    def test_database_integration(self, mock_db):
        """Test scheduler integration with database."""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance

        def db_task():
            mock_db_instance.execute_query("SELECT 1")

        task = ScheduledTask(name="db_task", func=db_task, interval=0.1)

        self.scheduler.add_task(task)
        self.scheduler.start()
        time.sleep(0.2)
        self.scheduler.stop()

        mock_db_instance.execute_query.assert_called()

    @patch("piwardrive.scheduler.WidgetManager")
    def test_widget_integration(self, mock_widgets):
        """Test scheduler integration with widgets."""
        mock_widget_manager = Mock()
        mock_widgets.return_value = mock_widget_manager

        def widget_task():
            mock_widget_manager.refresh_widgets()

        task = ScheduledTask(name="widget_task", func=widget_task, interval=0.1)

        self.scheduler.add_task(task)
        self.scheduler.start()
        time.sleep(0.2)
        self.scheduler.stop()

        mock_widget_manager.refresh_widgets.assert_called()

    @patch("piwardrive.scheduler.NotificationManager")
    def test_notification_integration(self, mock_notifications):
        """Test scheduler integration with notifications."""
        mock_notification_manager = Mock()
        mock_notifications.return_value = mock_notification_manager

        def notification_task():
            mock_notification_manager.send_alert("Test alert")

        task = ScheduledTask(
            name="notification_task", func=notification_task, interval=0.1
        )

        self.scheduler.add_task(task)
        self.scheduler.start()
        time.sleep(0.2)
        self.scheduler.stop()

        mock_notification_manager.send_alert.assert_called()


class TestSchedulerPerformance:
    """Test scheduler performance characteristics."""

    def setup_method(self):
        """Setup test scheduler."""
        self.scheduler = Scheduler()

    def test_high_frequency_tasks(self):
        """Test scheduler with high frequency tasks."""
        execution_count = 0

        def high_freq_task():
            nonlocal execution_count
            execution_count += 1

        task = ScheduledTask(
            name="high_freq_task", func=high_freq_task, interval=0.01  # 10ms interval
        )

        self.scheduler.add_task(task)
        self.scheduler.start()
        time.sleep(0.5)  # Run for 500ms
        self.scheduler.stop()

        # Should execute multiple times
        assert execution_count > 10

    def test_many_tasks_performance(self):
        """Test scheduler performance with many tasks."""
        execution_counts = {}

        def create_task_func(task_id):
            def task_func():
                execution_counts[task_id] = execution_counts.get(task_id, 0) + 1

            return task_func

        # Add many tasks
        for i in range(50):
            task = ScheduledTask(
                name=f"task_{i}", func=create_task_func(i), interval=0.1
            )
            self.scheduler.add_task(task)

        self.scheduler.start()
        time.sleep(0.5)
        self.scheduler.stop()

        # All tasks should execute
        assert len(execution_counts) == 50

    def test_memory_usage(self):
        """Test scheduler memory usage."""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Add many tasks
        for i in range(100):
            task = ScheduledTask(
                name=f"memory_task_{i}", func=lambda: None, interval=1.0
            )
            self.scheduler.add_task(task)

        self.scheduler.start()
        time.sleep(0.1)
        self.scheduler.stop()

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 10MB)
        assert memory_increase < 10 * 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__])
