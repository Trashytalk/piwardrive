#!/usr/bin/env python3
"""Comprehensive test suite for piwardrive.scheduler module.

This test suite provides complete coverage for the scheduler module including:
- PollScheduler functionality
- Geofence loading and management
- Periodic callback scheduling
- Task management and cleanup
- Schedule rule parsing
- Event handling
- Error conditions and edge cases
"""

import json
import os
import tempfile
import unittest.mock as mock
from datetime import time as dt_time
from unittest.mock import AsyncMock, patch

import pytest

from piwardrive import scheduler
from piwardrive.core import config


class MockUpdatable:
    """Mock class implementing Updatable protocol for testing."""

    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.update_called = 0
        self.update_exception = None

    async def update(self) -> None:
        """Mock update method."""
        self.update_called += 1
        if self.update_exception:
            raise self.update_exception


class TestPollScheduler:
    """Test suite for PollScheduler class."""

    def test_init(self):
        """Test PollScheduler initialization."""
        scheduler_instance = scheduler.PollScheduler()
        assert scheduler_instance._tasks == {}
        assert scheduler_instance._next_runs == {}
        assert scheduler_instance._durations == {}
        assert scheduler_instance._rules == {}

    def test_load_geofences_file_exists(self):
        """Test loading geofences when file exists."""
        test_data = [
            {"name": "zone1", "points": [[40.7128, -74.0060], [40.7580, -73.9855]]},
            {"name": "zone2", "points": [[34.0522, -118.2437], [34.0901, -118.2437]]},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name

        try:
            with patch.object(config, "CONFIG_DIR", os.path.dirname(temp_path)):
                with patch("os.path.join", return_value=temp_path):
                    result = scheduler.PollScheduler._load_geofences()
                    expected = {
                        "zone1": [(40.7128, -74.0060), (40.7580, -73.9855)],
                        "zone2": [(34.0522, -118.2437), (34.0901, -118.2437)],
                    }
                    assert result == expected
        finally:
            os.unlink(temp_path)

    def test_load_geofences_file_not_exists(self):
        """Test loading geofences when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(config, "CONFIG_DIR", temp_dir):
                result = scheduler.PollScheduler._load_geofences()
                assert result == {}

    def test_load_geofences_invalid_json(self):
        """Test loading geofences with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            with patch.object(config, "CONFIG_DIR", os.path.dirname(temp_path)):
                with patch("os.path.join", return_value=temp_path):
                    result = scheduler.PollScheduler._load_geofences()
                    assert result == {}
        finally:
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_schedule_periodic_callback(self):
        """Test scheduling a periodic callback."""
        scheduler_instance = scheduler.PollScheduler()
        mock_callback = AsyncMock()

        # Schedule the callback
        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.schedule("test_task", mock_callback, interval=1.0)

            assert "test_task" in scheduler_instance._tasks
            assert scheduler_instance._tasks["test_task"] == mock_task
            mock_create_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_schedule_with_updatable(self):
        """Test scheduling with Updatable protocol."""
        scheduler_instance = scheduler.PollScheduler()
        mock_updatable = MockUpdatable(update_interval=2.0)

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.schedule(
                "test_updatable",
                mock_updatable.update,
                interval=mock_updatable.update_interval,
            )

            assert "test_updatable" in scheduler_instance._tasks
            mock_create_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_cancel_existing_task(self):
        """Test cancelling an existing task."""
        scheduler_instance = scheduler.PollScheduler()
        mock_task = AsyncMock()

        scheduler_instance._tasks["test_task"] = mock_task

        scheduler_instance.cancel("test_task")

        mock_task.cancel.assert_called_once()
        assert "test_task" not in scheduler_instance._tasks

    def test_cancel_nonexistent_task(self):
        """Test cancelling a non-existent task."""
        scheduler_instance = scheduler.PollScheduler()

        # Should not raise an exception
        scheduler_instance.cancel("nonexistent_task")
        assert "nonexistent_task" not in scheduler_instance._tasks

    @pytest.mark.asyncio
    async def test_reschedule_existing_task(self):
        """Test rescheduling an existing task."""
        scheduler_instance = scheduler.PollScheduler()
        mock_task = AsyncMock()

        def mock_callback(dt):
            return None

        scheduler_instance._tasks["test_task"] = mock_task

        with patch("asyncio.create_task") as mock_create_task:
            new_mock_task = AsyncMock()
            mock_create_task.return_value = new_mock_task

            scheduler_instance.schedule("test_task", mock_callback, 1.0)

            # Old task should be cancelled
            mock_task.cancel.assert_called_once()
            # New task should be created
            assert scheduler_instance._tasks["test_task"] == new_mock_task

    @pytest.mark.asyncio
    async def test_cancel_all_tasks(self):
        """Test cancelling all scheduled tasks."""
        scheduler_instance = scheduler.PollScheduler()
        mock_task1 = AsyncMock()
        mock_task2 = AsyncMock()

        scheduler_instance._tasks["task1"] = mock_task1
        scheduler_instance._tasks["task2"] = mock_task2

        scheduler_instance.cancel_all()

        mock_task1.cancel.assert_called_once()
        mock_task2.cancel.assert_called_once()
        assert scheduler_instance._tasks == {}

    def test_get_metrics(self):
        """Test getting scheduler metrics."""
        scheduler_instance = scheduler.PollScheduler()
        mock_task = AsyncMock()

        scheduler_instance._tasks["test_task"] = mock_task
        scheduler_instance._next_runs["test_task"] = 1000.0
        scheduler_instance._durations["test_task"] = 0.5

        metrics = scheduler_instance.get_metrics()

        assert "test_task" in metrics
        assert metrics["test_task"]["next_run"] == 1000.0
        assert metrics["test_task"]["last_duration"] == 0.5

    def test_check_rules_no_rules(self):
        """Test check_rules with no rules."""
        result = scheduler.PollScheduler.check_rules({})
        assert result is True

    def test_check_rules_with_time_ranges(self):
        """Test check_rules with time ranges."""
        # Mock current time
        with patch("piwardrive.scheduler.datetime") as mock_datetime:
            mock_datetime.now.return_value.time.return_value = dt_time(12, 0, 0)

            # Test time range that includes current time
            rules = {"time_ranges": [["11:00:00", "13:00:00"]]}
            result = scheduler.PollScheduler.check_rules(rules)
            assert result is True

            # Test time range that excludes current time
            rules = {"time_ranges": [["14:00:00", "16:00:00"]]}
            result = scheduler.PollScheduler.check_rules(rules)
            assert result is False

    def test_schedule_widget(self):
        """Test scheduling a widget."""
        scheduler_instance = scheduler.PollScheduler()
        mock_widget = MockUpdatable(update_interval=2.0)

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.register_widget(mock_widget)

            # Should schedule the widget
            assert len(scheduler_instance._tasks) == 1
            task_name = next(iter(scheduler_instance._tasks.keys()))
            assert task_name.startswith("MockUpdatable-")

    def test_schedule_widget_with_name(self):
        """Test scheduling a widget with custom name."""
        scheduler_instance = scheduler.PollScheduler()
        mock_widget = MockUpdatable(update_interval=2.0)

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.register_widget(mock_widget, "custom_widget")

            # Should schedule the widget with custom name
            assert "custom_widget" in scheduler_instance._tasks

    def test_schedule_widget_missing_interval(self):
        """Test scheduling a widget without update_interval."""
        scheduler_instance = scheduler.PollScheduler()

        class BadWidget:
            def update(self):
                pass

        bad_widget = BadWidget()

        with pytest.raises(ValueError, match="missing 'update_interval'"):
            scheduler_instance.register_widget(bad_widget)

    def test_schedule_zero_interval_raises_error(self):
        """Test scheduling with zero interval raises error."""
        scheduler_instance = scheduler.PollScheduler()

        def mock_callback(dt):
            return None

        with pytest.raises(ValueError, match="interval must be greater than 0"):
            scheduler_instance.schedule("test_task", mock_callback, 0.0)

    def test_schedule_negative_interval_raises_error(self):
        """Test scheduling with negative interval raises error."""
        scheduler_instance = scheduler.PollScheduler()

        def mock_callback(dt):
            return None

        with pytest.raises(ValueError, match="interval must be greater than 0"):
            scheduler_instance.schedule("test_task", mock_callback, -1.0)


class TestAsyncScheduler:
    """Test suite for AsyncScheduler class."""

    def test_init(self):
        """Test AsyncScheduler initialization."""
        scheduler_instance = scheduler.AsyncScheduler()
        assert scheduler_instance._tasks == {}
        assert scheduler_instance._next_runs == {}
        assert scheduler_instance._durations == {}

    def test_schedule_task(self):
        """Test scheduling a task."""
        scheduler_instance = scheduler.AsyncScheduler()

        async def mock_callback():
            return None

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.schedule("test_task", mock_callback, 1.0)

            assert "test_task" in scheduler_instance._tasks
            assert scheduler_instance._tasks["test_task"] == mock_task

    def test_schedule_widget(self):
        """Test scheduling a widget with AsyncScheduler."""
        scheduler_instance = scheduler.AsyncScheduler()
        mock_widget = MockUpdatable(update_interval=2.0)

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.register_widget(mock_widget)

            # Should schedule the widget
            assert len(scheduler_instance._tasks) == 1
            task_name = next(iter(scheduler_instance._tasks.keys()))
            assert task_name.startswith("MockUpdatable-")

    def test_cancel_task(self):
        """Test cancelling a task."""
        scheduler_instance = scheduler.AsyncScheduler()
        mock_task = AsyncMock()

        scheduler_instance._tasks["test_task"] = mock_task
        scheduler_instance._next_runs["test_task"] = 1000.0
        scheduler_instance._durations["test_task"] = 0.5

        scheduler_instance.cancel("test_task")

        mock_task.cancel.assert_called_once()
        assert "test_task" not in scheduler_instance._tasks
        assert "test_task" not in scheduler_instance._next_runs
        assert "test_task" not in scheduler_instance._durations

    @pytest.mark.asyncio
    async def test_cancel_all_tasks(self):
        """Test cancelling all tasks."""
        scheduler_instance = scheduler.AsyncScheduler()
        mock_task1 = AsyncMock()
        mock_task2 = AsyncMock()

        scheduler_instance._tasks["task1"] = mock_task1
        scheduler_instance._tasks["task2"] = mock_task2

        await scheduler_instance.cancel_all()

        mock_task1.cancel.assert_called_once()
        mock_task2.cancel.assert_called_once()
        assert scheduler_instance._tasks == {}

    def test_get_metrics(self):
        """Test getting AsyncScheduler metrics."""
        scheduler_instance = scheduler.AsyncScheduler()
        mock_task = AsyncMock()

        scheduler_instance._tasks["test_task"] = mock_task
        scheduler_instance._next_runs["test_task"] = 1000.0
        scheduler_instance._durations["test_task"] = 0.5

        metrics = scheduler_instance.get_metrics()

        assert "test_task" in metrics
        assert metrics["test_task"]["next_run"] == 1000.0
        assert metrics["test_task"]["last_duration"] == 0.5


class TestSchedulerUtilities:
    """Test suite for scheduler utility functions."""

    def test_clock_event_creation(self):
        """Test ClockEvent creation."""
        event = scheduler.ClockEvent()
        assert event is not None
        assert isinstance(event, object)

    def test_updatable_protocol_compliance(self):
        """Test that MockUpdatable complies with Updatable protocol."""
        mock_updatable = MockUpdatable(update_interval=1.5)

        assert hasattr(mock_updatable, "update_interval")
        assert mock_updatable.update_interval == 1.5
        assert hasattr(mock_updatable, "update")
        assert callable(mock_updatable.update)

    @pytest.mark.asyncio
    async def test_updatable_update_method(self):
        """Test calling update method on Updatable."""
        mock_updatable = MockUpdatable(update_interval=1.0)

        await mock_updatable.update()

        assert mock_updatable.update_called == 1

    @pytest.mark.asyncio
    async def test_updatable_update_with_exception(self):
        """Test Updatable update method with exception."""
        mock_updatable = MockUpdatable(update_interval=1.0)
        mock_updatable.update_exception = ValueError("Test exception")

        with pytest.raises(ValueError, match="Test exception"):
            await mock_updatable.update()


class TestSchedulerIntegration:
    """Integration tests for scheduler with other components."""

    def test_scheduler_with_gps_client(self):
        """Test scheduler integration with GPS client."""
        scheduler_instance = scheduler.PollScheduler()

        # Test check_rules without geofences (should return True)
        rules = {}
        result = scheduler_instance.check_rules(rules)
        assert result is True

        # Test check_rules with time ranges but no geofences
        rules = {"time_ranges": [["09:00", "17:00"]]}
        with patch("piwardrive.scheduler.PollScheduler._match_time") as mock_match:
            mock_match.return_value = True
            result = scheduler_instance.check_rules(rules)
            assert result is True

            mock_match.return_value = False
            result = scheduler_instance.check_rules(rules)
            assert result is False

    def test_scheduler_with_config_integration(self):
        """Test scheduler integration with config module."""
        scheduler_instance = scheduler.PollScheduler()

        with patch.object(config, "CONFIG_DIR", "/tmp/test_config"):
            # Test loading geofences uses config
            with patch("os.path.join") as mock_join:
                with patch(
                    "builtins.open", mock.mock_open(read_data="[]")
                ) as mock_file:
                    mock_join.return_value = "/tmp/test_config/geofences.json"

                    result = scheduler_instance._load_geofences()

                    mock_join.assert_called_with("/tmp/test_config", "geofences.json")
                    mock_file.assert_called_with(
                        "/tmp/test_config/geofences.json", "r", encoding="utf-8"
                    )
                    assert result == {}


class TestSchedulerEdgeCases:
    """Test edge cases and error conditions."""

    def test_schedule_none_callback(self):
        """Test scheduling with None callback."""
        scheduler_instance = scheduler.PollScheduler()

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.schedule("none_task", None, 1.0)

            assert "none_task" in scheduler_instance._tasks

    def test_schedule_empty_task_name(self):
        """Test scheduling with empty task name."""
        scheduler_instance = scheduler.PollScheduler()

        def mock_callback(dt):
            return None

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            scheduler_instance.schedule("", mock_callback, 1.0)

            assert "" in scheduler_instance._tasks

    def test_multiple_cancel_all_calls(self):
        """Test calling cancel_all multiple times."""
        scheduler_instance = scheduler.PollScheduler()
        mock_task = AsyncMock()

        scheduler_instance._tasks["test_task"] = mock_task

        # First cancel_all
        scheduler_instance.cancel_all()
        assert scheduler_instance._tasks == {}

        # Second cancel_all (should not raise exception)
        scheduler_instance.cancel_all()
        assert scheduler_instance._tasks == {}

    def test_concurrent_schedule_cancel(self):
        """Test concurrent scheduling and cancelling."""
        scheduler_instance = scheduler.PollScheduler()

        def mock_callback(dt):
            return None

        with patch("asyncio.create_task") as mock_create_task:
            mock_task = AsyncMock()
            mock_create_task.return_value = mock_task

            # Schedule
            scheduler_instance.schedule("test_task", mock_callback, 1.0)
            assert "test_task" in scheduler_instance._tasks

            # Cancel
            scheduler_instance.cancel("test_task")
            assert "test_task" not in scheduler_instance._tasks

            # Re-schedule
            scheduler_instance.schedule("test_task", mock_callback, 1.0)
            assert "test_task" in scheduler_instance._tasks


if __name__ == "__main__":
    pytest.main([__file__])
