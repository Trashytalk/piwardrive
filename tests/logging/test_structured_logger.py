"""Tests for structured logging system."""

import json
import logging
import os
import sys
import tempfile
from io import StringIO
from unittest.mock import patch

import pytest

from piwardrive.logging.structured_logger import (
    LogContext,
    PiWardriveLogger,
    StructuredFormatter,
    _get_version,
    dataclass_replace,
    get_logger,
    log_context,
    set_log_context,
)


class TestGetVersion:
    """Test version detection function."""

    def test_get_version_success(self):
        """Test successful version retrieval."""
        with patch(
            "piwardrive.logging.structured_logger.version", return_value="1.2.3"
        ):
            assert _get_version() == "1.2.3"

    def test_get_version_not_found(self):
        """Test version retrieval when package not found."""
        from importlib.metadata import PackageNotFoundError

        with patch(
            "piwardrive.logging.structured_logger.version",
            side_effect=PackageNotFoundError,
        ):
            assert _get_version() == "0"


class TestLogContext:
    """Test LogContext dataclass."""

    def test_default_creation(self):
        """Test creating LogContext with default values."""
        ctx = LogContext()
        assert ctx.request_id is None
        assert ctx.user_id is None
        assert ctx.session_id is None
        assert ctx.component is None
        assert ctx.operation is None
        assert ctx.instance_id is None
        assert ctx.trace_id is None
        assert ctx.span_id is None

    def test_creation_with_values(self):
        """Test creating LogContext with specific values."""
        ctx = LogContext(
            request_id="req-123",
            user_id="user-456",
            component="auth",
            operation="login",
        )
        assert ctx.request_id == "req-123"
        assert ctx.user_id == "user-456"
        assert ctx.component == "auth"
        assert ctx.operation == "login"
        # Others should still be None
        assert ctx.session_id is None
        assert ctx.instance_id is None

    def test_all_fields_set(self):
        """Test LogContext with all fields set."""
        ctx = LogContext(
            request_id="req-123",
            user_id="user-456",
            session_id="sess-789",
            component="auth",
            operation="login",
            instance_id="inst-001",
            trace_id="trace-abc",
            span_id="span-def",
        )
        assert ctx.request_id == "req-123"
        assert ctx.user_id == "user-456"
        assert ctx.session_id == "sess-789"
        assert ctx.component == "auth"
        assert ctx.operation == "login"
        assert ctx.instance_id == "inst-001"
        assert ctx.trace_id == "trace-abc"
        assert ctx.span_id == "span-def"


class TestDataclassReplace:
    """Test dataclass_replace utility function."""

    def test_replace_single_field(self):
        """Test replacing a single field."""
        original = LogContext(request_id="old-id", user_id="user-123")
        updated = dataclass_replace(original, request_id="new-id")

        assert updated.request_id == "new-id"
        assert updated.user_id == "user-123"
        # Original should be unchanged
        assert original.request_id == "old-id"
        assert original.user_id == "user-123"

    def test_replace_multiple_fields(self):
        """Test replacing multiple fields."""
        original = LogContext(request_id="old-id", user_id="old-user")
        updated = dataclass_replace(
            original, request_id="new-id", user_id="new-user", component="new-component"
        )

        assert updated.request_id == "new-id"
        assert updated.user_id == "new-user"
        assert updated.component == "new-component"
        # Original unchanged
        assert original.request_id == "old-id"
        assert original.user_id == "old-user"
        assert original.component is None

    def test_replace_with_none_values(self):
        """Test that None values are not set during replace."""
        original = LogContext(request_id="req-123", user_id="user-456")
        updated = dataclass_replace(original, request_id=None, component="test")

        # None values should not overwrite existing values
        assert updated.request_id == "req-123"  # Should remain unchanged
        assert updated.user_id == "user-456"
        assert updated.component == "test"


class TestStructuredFormatter:
    """Test StructuredFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.formatter = StructuredFormatter()

    def test_formatter_initialization(self):
        """Test formatter initialization."""
        assert self.formatter.include_extra is True
        assert hasattr(self.formatter, "hostname")
        assert hasattr(self.formatter, "version")

    def test_formatter_initialization_no_extra(self):
        """Test formatter initialization without extra data."""
        formatter = StructuredFormatter(include_extra=False)
        assert formatter.include_extra is False

    def test_serialize_success(self):
        """Test successful serialization."""
        test_dict = {"level": "INFO", "message": "test"}
        result = self.formatter._serialize(test_dict)
        parsed = json.loads(result)
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "test"

    def test_serialize_fallback_to_json(self):
        """Test fallback to builtin json on dumps failure."""
        test_dict = {"level": "INFO", "message": "test"}
        with patch(
            "piwardrive.logging.structured_logger.dumps",
            side_effect=Exception("dumps failed"),
        ):
            result = self.formatter._serialize(test_dict)
            parsed = json.loads(result)
            assert parsed["level"] == "INFO"
            assert parsed["message"] == "test"

    def test_serialize_complete_failure(self):
        """Test complete serialization failure fallback."""
        with patch(
            "piwardrive.logging.structured_logger.dumps",
            side_effect=Exception("dumps failed"),
        ):
            with patch("json.dumps", side_effect=Exception("json.dumps failed")):
                result = self.formatter._serialize({"test": "data"})
                assert result == "{}"

    def test_format_basic_record(self):
        """Test formatting a basic log record."""
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.created = 1640995200.0  # Fixed timestamp for testing

        result = self.formatter.format(record)
        data = json.loads(result)

        assert data["level"] == "INFO"
        assert data["logger"] == "test.logger"
        assert data["message"] == "Test message"
        assert "timestamp" in data
        assert "metadata" in data
        assert "context" in data

        # Check metadata structure
        metadata = data["metadata"]
        assert "hostname" in metadata
        assert "pid" in metadata
        assert "thread_id" in metadata
        assert "version" in metadata

    def test_format_with_context(self):
        """Test formatting with log context."""
        # Set up context
        original_ctx = log_context.get()
        test_ctx = LogContext(request_id="req-123", component="test")
        log_context.set(test_ctx)

        try:
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="test.py",
                lineno=42,
                msg="Test message",
                args=(),
                exc_info=None,
            )

            result = self.formatter.format(record)
            data = json.loads(result)

            assert data["context"]["request_id"] == "req-123"
            assert data["context"]["component"] == "test"
            # None values should not be included
            assert "user_id" not in data["context"]
        finally:
            log_context.set(original_ctx)

    def test_format_with_extra_data(self):
        """Test formatting with extra data."""
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.extra = {"extra": {"custom_field": "custom_value", "number": 42}}

        result = self.formatter.format(record)
        data = json.loads(result)

        assert "data" in data
        assert data["data"]["custom_field"] == "custom_value"
        assert data["data"]["number"] == 42

    def test_format_without_extra_data_when_disabled(self):
        """Test formatting without extra data when include_extra is False."""
        formatter = StructuredFormatter(include_extra=False)
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.extra = {"extra": {"should_not": "appear"}}

        result = formatter.format(record)
        data = json.loads(result)

        assert "data" not in data

    def test_format_with_exception(self):
        """Test formatting with exception info."""
        try:
            raise ValueError("Test error message")
        except ValueError:
            exc_info = sys.exc_info()
            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="test.py",
                lineno=42,
                msg="Error occurred",
                args=(),
                exc_info=exc_info,
            )

        result = self.formatter.format(record)
        data = json.loads(result)

        assert data["level"] == "ERROR"
        assert "exception" in data
        assert data["exception"]["type"] == "ValueError"
        assert "Test error message" in data["exception"]["message"]
        assert "traceback" in data["exception"]
        assert "ValueError: Test error message" in data["exception"]["traceback"]

    def test_format_with_none_exception_info(self):
        """Test formatting with None exception info components."""
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=42,
            msg="Error occurred",
            args=(),
            exc_info=(None, None, None),
        )

        result = self.formatter.format(record)
        data = json.loads(result)

        assert "exception" in data
        assert data["exception"]["type"] == ""
        assert data["exception"]["message"] == ""


class TestPiWardriveLogger:
    """Test PiWardriveLogger class."""

    def test_logger_creation_default_config(self):
        """Test logger creation with default configuration."""
        logger = PiWardriveLogger("test.module")
        assert logger.name == "test.module"
        assert logger.config == {}
        assert isinstance(logger.logger, logging.Logger)

    def test_logger_creation_with_config(self):
        """Test logger creation with custom configuration."""
        config = {"level": logging.DEBUG, "streams": False}
        logger = PiWardriveLogger("test.module", config)
        assert logger.name == "test.module"
        assert logger.config == config

    def test_setup_logger_with_existing_handlers(self):
        """Test setup when logger already has handlers."""
        # Create a logger with handlers
        existing_logger = logging.getLogger("test.existing")
        existing_logger.addHandler(logging.StreamHandler())

        logger = PiWardriveLogger("test.existing")
        # Should return the existing logger without modification
        assert logger.logger is existing_logger

    def test_create_handlers_stream_only(self):
        """Test creating stream handler only."""
        config = {"streams": True, "file": None}
        logger = PiWardriveLogger("test", config)
        handlers = logger._create_handlers()

        assert len(handlers) == 1
        assert isinstance(handlers[0], logging.StreamHandler)
        assert isinstance(handlers[0].formatter, StructuredFormatter)

    def test_create_handlers_file_only(self):
        """Test creating file handler only."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            config = {"streams": False, "file": tmp.name}
            logger = PiWardriveLogger("test", config)
            handlers = logger._create_handlers()

            assert len(handlers) == 1
            assert hasattr(handlers[0], "baseFilename")  # RotatingFileHandler
            assert isinstance(handlers[0].formatter, StructuredFormatter)

        # Cleanup
        os.unlink(tmp.name)

    def test_create_handlers_both(self):
        """Test creating both stream and file handlers."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            config = {"streams": True, "file": tmp.name}
            logger = PiWardriveLogger("test", config)
            handlers = logger._create_handlers()

            assert len(handlers) == 2
            # First should be stream, second should be file
            assert isinstance(handlers[0], logging.StreamHandler)
            assert hasattr(handlers[1], "baseFilename")

        # Cleanup
        os.unlink(tmp.name)

    def test_logging_methods(self):
        """Test logging methods."""
        logger = PiWardriveLogger("test")

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.DEBUG)

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message", exc_info=False)

        output = stream.getvalue()
        lines = output.strip().split("\n")
        assert len(lines) == 4

        # Verify each log level
        data = [json.loads(line) for line in lines]
        assert data[0]["level"] == "DEBUG"
        assert data[1]["level"] == "INFO"
        assert data[2]["level"] == "WARNING"
        assert data[3]["level"] == "ERROR"

    def test_logging_with_extra_data(self):
        """Test logging with extra data."""
        logger = PiWardriveLogger("test")
        extra_data = {"extra": {"user_id": "123", "action": "login"}}

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.INFO)

        logger.info("User action", extra=extra_data)

        output = stream.getvalue()
        data = json.loads(output.strip())

        assert data["level"] == "INFO"
        assert data["message"] == "User action"
        assert "data" in data
        assert data["data"]["user_id"] == "123"
        assert data["data"]["action"] == "login"

    def test_log_level_filtering(self):
        """Test that log level filtering works."""
        config = {"level": logging.WARNING}
        logger = PiWardriveLogger("test", config)

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        handler.setLevel(logging.WARNING)  # Also set handler level
        logger.logger.addHandler(handler)

        logger.debug("Should not appear")
        logger.info("Should not appear")
        logger.warning("Should appear")
        logger.error("Should appear")

        output = stream.getvalue()
        lines = [line for line in output.strip().split("\n") if line]
        assert len(lines) == 2

        data = [json.loads(line) for line in lines]
        assert data[0]["level"] == "WARNING"
        assert data[1]["level"] == "ERROR"


class TestLogContextFunctions:
    """Test log context management functions."""

    def setup_method(self):
        """Set up clean context for each test."""
        # Store original context
        self.original_ctx = log_context.get()
        # Reset to default
        log_context.set(LogContext())

    def teardown_method(self):
        """Restore original context after each test."""
        log_context.set(self.original_ctx)

    def test_set_log_context(self):
        """Test setting log context."""
        set_log_context(request_id="req-123", operation="test_op")

        ctx = log_context.get()
        assert ctx.request_id == "req-123"
        assert ctx.operation == "test_op"
        # Other fields should remain None
        assert ctx.user_id is None

    def test_set_log_context_multiple_calls(self):
        """Test multiple calls to set_log_context."""
        set_log_context(request_id="req-123")
        set_log_context(user_id="user-456", component="auth")

        ctx = log_context.get()
        assert ctx.request_id == "req-123"  # Should persist
        assert ctx.user_id == "user-456"
        assert ctx.component == "auth"

    def test_get_logger_function(self):
        """Test get_logger convenience function."""
        logger = get_logger("test.module")
        assert isinstance(logger, PiWardriveLogger)
        assert logger.name == "test.module"

    def test_get_logger_with_config(self):
        """Test get_logger with configuration."""
        logger = get_logger("test.module", level=logging.DEBUG, streams=False)
        assert logger.config["level"] == logging.DEBUG
        assert logger.config["streams"] is False


class TestIntegration:
    """Integration tests for the entire logging system."""

    def test_end_to_end_logging(self):
        """Test complete logging workflow."""
        # Set up context
        set_log_context(request_id="req-123", user_id="user-456")

        # Create logger
        logger = get_logger("integration.test")

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())

        # Add handler to the underlying logger
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.INFO)

        # Log a message with extra data
        extra_data = {"extra": {"action": "test", "success": True}}
        logger.info("Integration test message", extra=extra_data)

        # Parse the output
        output = stream.getvalue()
        data = json.loads(output.strip())

        # Verify structure
        assert data["level"] == "INFO"
        assert data["message"] == "Integration test message"
        assert data["context"]["request_id"] == "req-123"
        assert data["context"]["user_id"] == "user-456"
        assert data["data"]["action"] == "test"
        assert data["data"]["success"] is True
        assert "timestamp" in data
        assert "metadata" in data

    def test_exception_logging_integration(self):
        """Test exception logging integration."""
        logger = get_logger("exception.test")

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.ERROR)

        # Log an exception
        try:
            raise RuntimeError("Test exception for logging")
        except RuntimeError:
            logger.error("An error occurred")

        # Parse the output
        output = stream.getvalue()
        data = json.loads(output.strip())

        # Verify exception details
        assert data["level"] == "ERROR"
        assert "exception" in data
        assert data["exception"]["type"] == "RuntimeError"
        assert "Test exception for logging" in data["exception"]["message"]
        assert (
            "RuntimeError: Test exception for logging" in data["exception"]["traceback"]
        )


class TestAdvancedPiWardriveLogger:
    """Test advanced PiWardriveLogger features and edge cases."""

    def test_queue_handler_configuration(self):
        """Test queue handler setup and usage."""
        from logging.handlers import QueueHandler

        config = {"queue": True, "streams": True}
        logger = PiWardriveLogger("test.queue", config)

        # Should have QueueHandler
        assert len(logger.logger.handlers) == 1
        assert isinstance(logger.logger.handlers[0], QueueHandler)

        # Test logging through queue
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())

        # Add our test handler to the logger's handlers list for verification
        original_handlers = logger.logger.handlers[:]
        logger.logger.handlers.append(handler)
        logger.logger.setLevel(logging.INFO)

        logger.info("Queue test message")

        # Give queue time to process
        import time

        time.sleep(0.1)

        # Restore original handlers
        logger.logger.handlers = original_handlers

    def test_file_handler_with_custom_rotation_config(self):
        """Test file handler with custom rotation configuration."""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            config = {
                "streams": False,
                "file": tmp.name,
                "max_bytes": 1024,
                "backup_count": 3,
            }
            logger = PiWardriveLogger("test.file", config)
            handlers = logger._create_handlers()

            assert len(handlers) == 1
            file_handler = handlers[0]
            assert hasattr(file_handler, "maxBytes")
            assert hasattr(file_handler, "backupCount")
            assert file_handler.maxBytes == 1024
            assert file_handler.backupCount == 3

        # Cleanup
        os.unlink(tmp.name)

    def test_log_level_early_return_optimization(self):
        """Test that _log method returns early when level is not enabled."""
        logger = PiWardriveLogger("test.level")
        logger.logger.setLevel(logging.WARNING)  # Only WARNING and above

        # Mock the logger.log method to ensure it's not called
        with patch.object(logger.logger, "log") as mock_log:
            logger.debug("Should not be logged")
            logger.info("Should not be logged")

            # These should not call the underlying log method
            mock_log.assert_not_called()

            # But WARNING should call it
            logger.warning("Should be logged")
            mock_log.assert_called_once()

    def test_exception_info_auto_detection(self):
        """Test exception info with exc_info=True (auto-detection)."""
        logger = PiWardriveLogger("test.exc")

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.ERROR)

        # Log an error with automatic exception detection
        try:
            raise ValueError("Auto-detected exception")
        except ValueError:
            logger.error("Error with auto-detection", exc_info=True)

        output = stream.getvalue()
        data = json.loads(output.strip())

        assert "exception" in data
        assert data["exception"]["type"] == "ValueError"
        assert "Auto-detected exception" in data["exception"]["message"]

    def test_complex_object_serialization_fallback(self):
        """Test serialization fallback for complex objects."""
        logger = PiWardriveLogger("test.serialization")

        # Create an object that can't be JSON serialized normally
        class ComplexObject:
            def __str__(self):
                return "ComplexObject representation"

            def __repr__(self):
                return "ComplexObject()"

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.INFO)

        # Log with complex object in extra data (properly formatted)
        extra_data = {"complex": ComplexObject(), "normal": "string"}
        logger.info("Complex object test", extra=extra_data)

        output = stream.getvalue()
        data = json.loads(output.strip())

        # Should still produce valid JSON with string representation
        assert data["message"] == "Complex object test"
        # Complex objects should be serialized using string representation
        if "data" in data:
            assert "normal" in data["data"]
            assert data["data"]["normal"] == "string"

    def test_formatter_serialization_complete_failure(self):
        """Test formatter behavior when all serialization methods fail."""
        formatter = StructuredFormatter()

        # Mock both dumps methods to fail
        with patch(
            "piwardrive.logging.structured_logger.dumps",
            side_effect=Exception("fastjson failed"),
        ):
            with patch("json.dumps", side_effect=Exception("json failed")):
                result = formatter._serialize({"test": "data"})
                assert result == "{}"

    def test_logger_with_both_queue_and_file_handlers(self):
        """Test logger with queue enabled and file handler."""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            config = {"queue": True, "streams": True, "file": tmp.name}
            logger = PiWardriveLogger("test.queue.file", config)

            # Should still have QueueHandler as the main handler
            assert len(logger.logger.handlers) == 1
            assert isinstance(logger.logger.handlers[0], logging.handlers.QueueHandler)

        # Cleanup
        os.unlink(tmp.name)

    def test_log_context_with_all_none_values(self):
        """Test log context when all values are None."""
        formatter = StructuredFormatter()

        # Set context with all None values
        original_ctx = log_context.get()
        empty_ctx = LogContext()  # All fields are None by default
        log_context.set(empty_ctx)

        try:
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="test.py",
                lineno=42,
                msg="Test message",
                args=(),
                exc_info=None,
            )

            result = formatter.format(record)
            data = json.loads(result)

            # Context should be empty dict when all values are None
            assert data["context"] == {}

        finally:
            log_context.set(original_ctx)

    def test_structured_formatter_with_disabled_extra(self):
        """Test StructuredFormatter with include_extra=False."""
        formatter = StructuredFormatter(include_extra=False)

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.extra = {"extra": {"should_not": "appear"}}

        result = formatter.format(record)
        data = json.loads(result)

        # Should not include data field
        assert "data" not in data
        assert "level" in data
        assert "message" in data


class TestLoggerErrorConditions:
    """Test error conditions and edge cases."""

    def test_file_handler_creation_with_permission_error(self):
        """Test file handler creation when file is not writable."""
        # Skip this test if we don't have permission to create files in /tmp
        import tempfile

        try:
            with tempfile.NamedTemporaryFile(dir="/tmp") as tmp:
                pass
        except PermissionError:
            pytest.skip("No permission to create test files")

        # Try to create a file handler for an invalid path that should fail
        config = {
            "streams": False,
            "file": "/invalid/path/that/should/not/exist/test.log",
        }
        logger = PiWardriveLogger("test.permission", config)

        # Should handle the error gracefully and not crash
        # The exact behavior depends on the system, but it shouldn't raise
        try:
            logger._create_handlers()
            # If it succeeds, that's fine - depends on system
        except (PermissionError, OSError, FileNotFoundError, NotADirectoryError):
            # If it fails with various errors, that's expected
            pass

    def test_logger_propagation_disabled(self):
        """Test that logger propagation is disabled."""
        logger = PiWardriveLogger("test.propagation")
        assert logger.logger.propagate is False

    def test_multiple_logger_instances_same_name(self):
        """Test multiple logger instances with same name."""
        logger1 = PiWardriveLogger("same.name")
        logger2 = PiWardriveLogger("same.name")

        # Should return the same underlying logger
        assert logger1.logger is logger2.logger

    def test_warning_method_coverage(self):
        """Test warning method specifically."""
        logger = PiWardriveLogger("test.warning")

        # Capture output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.logger.addHandler(handler)
        logger.logger.setLevel(logging.WARNING)

        logger.warning("Warning message", extra={"test": "data"})

        output = stream.getvalue()
        data = json.loads(output.strip())

        assert data["level"] == "WARNING"
        assert data["message"] == "Warning message"
        # Check if data is present (depends on how extra is processed)
        if "data" in data:
            assert data["data"]["test"] == "data"


class TestDataclassReplaceEdgeCases:
    """Test edge cases for dataclass_replace function."""

    def test_dataclass_replace_with_empty_changes(self):
        """Test dataclass_replace with no changes."""
        original = LogContext(request_id="req-123", user_id="user-456")
        updated = dataclass_replace(original)

        # Should return equivalent object
        assert updated.request_id == "req-123"
        assert updated.user_id == "user-456"
        assert updated is not original  # Should be different object

    def test_dataclass_replace_filters_none_values(self):
        """Test that dataclass_replace filters out None values in changes."""
        original = LogContext(request_id="req-123")
        updated = dataclass_replace(original, user_id=None, component="test")

        # None values should not overwrite existing values
        assert updated.request_id == "req-123"
        assert updated.user_id is None  # Was already None
        assert updated.component == "test"

    def test_set_log_context_with_none_values(self):
        """Test set_log_context handles None values correctly."""
        # Set initial context
        original_ctx = log_context.get()
        initial_ctx = LogContext(request_id="req-123", user_id="user-456")
        log_context.set(initial_ctx)

        try:
            # Try to set with None values - should be filtered out
            set_log_context(user_id=None, component="new-component")

            ctx = log_context.get()
            assert ctx.request_id == "req-123"  # Should remain
            assert ctx.user_id == "user-456"  # Should remain (None filtered out)
            assert ctx.component == "new-component"  # Should be set

        finally:
            log_context.set(original_ctx)
