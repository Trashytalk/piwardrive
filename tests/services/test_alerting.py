"""Tests for the alerting service module."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from piwardrive.services.alerting import (
    AlertManager,
    AlertRule,
    send_discord_notification,
    send_email_alert,
    send_slack_notification,
    send_sms_alert,
    send_webhook_notification,
)


class TestAlertFunctions:
    """Test suite for individual alert functions."""

    @pytest.mark.asyncio
    async def test_send_email_alert(self):
        """Test email alert sending logs correctly."""
        with (
            patch("piwardrive.services.alerting.logger.warning") as mock_warning,
            patch("piwardrive.services.alerting.logger.debug") as mock_debug,
        ):

            await send_email_alert("test@example.com", "Test Alert", "Test message")

            mock_warning.assert_called_once_with(
                "Email alert to %s: %s", "test@example.com", "Test Alert"
            )
            mock_debug.assert_called_once_with("Email body: %s", "Test message")

    @pytest.mark.asyncio
    async def test_send_sms_alert(self):
        """Test SMS alert sending logs correctly."""
        with patch("piwardrive.services.alerting.logger.warning") as mock_warning:
            await send_sms_alert("+1234567890", "Test SMS message")

            mock_warning.assert_called_once_with(
                "SMS alert to %s: %s", "+1234567890", "Test SMS message"
            )

    @pytest.mark.asyncio
    async def test_send_webhook_notification_success(self):
        """Test successful webhook notification."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_client.return_value.__aenter__.return_value.post = mock_response

            payload = {"alert": "test", "value": 42}
            await send_webhook_notification("https://example.com/webhook", payload)

            mock_response.assert_called_once_with(
                "https://example.com/webhook", json={"alert": "test", "value": 42}
            )

    @pytest.mark.asyncio
    async def test_send_webhook_notification_failure(self):
        """Test webhook notification failure handling."""
        with (
            patch("httpx.AsyncClient") as mock_client,
            patch("piwardrive.services.alerting.logger.error") as mock_error,
        ):

            mock_client.return_value.__aenter__.return_value.post.side_effect = (
                Exception("Network error")
            )

            await send_webhook_notification(
                "https://example.com/webhook", {"test": "data"}
            )

            mock_error.assert_called_once_with(
                "Webhook %s failed: %s",
                "https://example.com/webhook",
                mock_client.return_value.__aenter__.return_value.post.side_effect,
            )

    @pytest.mark.asyncio
    async def test_send_slack_notification(self):
        """Test Slack notification sends correct webhook payload."""
        with patch(
            "piwardrive.services.alerting.send_webhook_notification"
        ) as mock_webhook:
            await send_slack_notification(
                "https://hooks.slack.com/test", "Test message"
            )

            mock_webhook.assert_called_once_with(
                "https://hooks.slack.com/test", {"text": "Test message"}
            )

    @pytest.mark.asyncio
    async def test_send_discord_notification(self):
        """Test Discord notification sends correct webhook payload."""
        with patch(
            "piwardrive.services.alerting.send_webhook_notification"
        ) as mock_webhook:
            await send_discord_notification(
                "https://discord.com/api/webhooks/test", "Test message"
            )

            mock_webhook.assert_called_once_with(
                "https://discord.com/api/webhooks/test", {"content": "Test message"}
            )


class TestAlertRule:
    """Test suite for AlertRule dataclass."""

    def test_alert_rule_creation(self):
        """Test AlertRule creation with default values."""
        rule = AlertRule(
            metric="cpu_usage", threshold=80.0, channels=["mailto:admin@example.com"]
        )

        assert rule.metric == "cpu_usage"
        assert rule.threshold == 80.0
        assert rule.channels == ["mailto:admin@example.com"]
        assert rule.level == "warning"

    def test_alert_rule_creation_custom_level(self):
        """Test AlertRule creation with custom level."""
        rule = AlertRule(
            metric="memory_usage",
            threshold=90.0,
            channels=["sms:+1234567890"],
            level="critical",
        )

        assert rule.metric == "memory_usage"
        assert rule.threshold == 90.0
        assert rule.channels == ["sms:+1234567890"]
        assert rule.level == "critical"

    def test_alert_rule_multiple_channels(self):
        """Test AlertRule with multiple channels."""
        channels = [
            "mailto:admin@example.com",
            "sms:+1234567890",
            "https://webhook.example.com",
        ]
        rule = AlertRule(metric="disk_usage", threshold=85.0, channels=channels)

        assert rule.channels == channels


class TestAlertManager:
    """Test suite for AlertManager class."""

    def test_alert_manager_initialization_empty(self):
        """Test AlertManager initialization with no rules."""
        manager = AlertManager()
        assert manager.rules == []

    def test_alert_manager_initialization_with_rules(self):
        """Test AlertManager initialization with rules."""
        rules = [
            AlertRule("cpu_usage", 80.0, ["mailto:admin@example.com"]),
            AlertRule("memory_usage", 90.0, ["sms:+1234567890"]),
        ]
        manager = AlertManager(rules)

        assert len(manager.rules) == 2
        assert manager.rules[0].metric == "cpu_usage"
        assert manager.rules[1].metric == "memory_usage"

    def test_add_rule(self):
        """Test adding rules to AlertManager."""
        manager = AlertManager()
        rule = AlertRule("disk_usage", 85.0, ["https://webhook.example.com"])

        manager.add_rule(rule)

        assert len(manager.rules) == 1
        assert manager.rules[0] == rule

    @pytest.mark.asyncio
    async def test_evaluate_no_rules(self):
        """Test evaluation with no rules configured."""
        manager = AlertManager()
        metrics = {"cpu_usage": 85.0, "memory_usage": 75.0}

        # Should not raise any exceptions
        await manager.evaluate(metrics)

    @pytest.mark.asyncio
    async def test_evaluate_no_threshold_exceeded(self):
        """Test evaluation when no thresholds are exceeded."""
        rule = AlertRule("cpu_usage", 90.0, ["mailto:admin@example.com"])
        manager = AlertManager([rule])
        metrics = {"cpu_usage": 85.0}

        with patch("piwardrive.services.alerting.logger.warning") as mock_warning:
            await manager.evaluate(metrics)

            # No alerts should be triggered
            mock_warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_evaluate_missing_metric(self):
        """Test evaluation when metric is missing from data."""
        rule = AlertRule("cpu_usage", 80.0, ["mailto:admin@example.com"])
        manager = AlertManager([rule])
        metrics = {"memory_usage": 75.0}  # cpu_usage is missing

        with patch("piwardrive.services.alerting.logger.warning") as mock_warning:
            await manager.evaluate(metrics)

            # No alerts should be triggered for missing metrics
            mock_warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_evaluate_email_alert_triggered(self):
        """Test evaluation triggers email alert."""
        rule = AlertRule("cpu_usage", 80.0, ["mailto:admin@example.com"])
        manager = AlertManager([rule])
        metrics = {"cpu_usage": 85.0}

        with (
            patch("piwardrive.services.alerting.send_email_alert") as mock_email,
            patch("piwardrive.services.alerting.logger.warning") as mock_warning,
        ):

            await manager.evaluate(metrics)

            mock_email.assert_called_once_with(
                "admin@example.com",
                "WARNING alert",
                "Metric 'cpu_usage' value 85.00 exceeded threshold 80.00",
            )
            mock_warning.assert_called_once_with(
                "Metric 'cpu_usage' value 85.00 exceeded threshold 80.00"
            )

    @pytest.mark.asyncio
    async def test_evaluate_sms_alert_triggered(self):
        """Test evaluation triggers SMS alert."""
        rule = AlertRule("memory_usage", 90.0, ["sms:+1234567890"])
        manager = AlertManager([rule])
        metrics = {"memory_usage": 95.0}

        with patch("piwardrive.services.alerting.send_sms_alert") as mock_sms:
            await manager.evaluate(metrics)

            mock_sms.assert_called_once_with(
                "+1234567890",
                "Metric 'memory_usage' value 95.00 exceeded threshold 90.00",
            )

    @pytest.mark.asyncio
    async def test_evaluate_webhook_alert_triggered(self):
        """Test evaluation triggers webhook alert."""
        rule = AlertRule("disk_usage", 85.0, ["https://webhook.example.com"])
        manager = AlertManager([rule])
        metrics = {"disk_usage": 90.0}

        with patch(
            "piwardrive.services.alerting.send_webhook_notification"
        ) as mock_webhook:
            await manager.evaluate(metrics)

            mock_webhook.assert_called_once_with(
                "https://webhook.example.com",
                {"message": "Metric 'disk_usage' value 90.00 exceeded threshold 85.00"},
            )

    @pytest.mark.asyncio
    async def test_evaluate_slack_alert_triggered(self):
        """Test evaluation triggers Slack alert."""
        rule = AlertRule("cpu_temp", 70.0, ["slack:https://hooks.slack.com/test"])
        manager = AlertManager([rule])
        metrics = {"cpu_temp": 75.0}

        with patch(
            "piwardrive.services.alerting.send_slack_notification"
        ) as mock_slack:
            await manager.evaluate(metrics)

            mock_slack.assert_called_once_with(
                "https://hooks.slack.com/test",
                "Metric 'cpu_temp' value 75.00 exceeded threshold 70.00",
            )

    @pytest.mark.asyncio
    async def test_evaluate_discord_alert_triggered(self):
        """Test evaluation triggers Discord alert."""
        rule = AlertRule(
            "network_errors", 10.0, ["discord:https://discord.com/api/webhooks/test"]
        )
        manager = AlertManager([rule])
        metrics = {"network_errors": 15.0}

        with patch(
            "piwardrive.services.alerting.send_discord_notification"
        ) as mock_discord:
            await manager.evaluate(metrics)

            mock_discord.assert_called_once_with(
                "https://discord.com/api/webhooks/test",
                "Metric 'network_errors' value 15.00 exceeded threshold 10.00",
            )

    @pytest.mark.asyncio
    async def test_evaluate_multiple_channels(self):
        """Test evaluation with multiple channels for single rule."""
        channels = [
            "mailto:admin@example.com",
            "sms:+1234567890",
            "https://webhook.example.com",
        ]
        rule = AlertRule("cpu_usage", 80.0, channels)
        manager = AlertManager([rule])
        metrics = {"cpu_usage": 85.0}

        with (
            patch("piwardrive.services.alerting.send_email_alert") as mock_email,
            patch("piwardrive.services.alerting.send_sms_alert") as mock_sms,
            patch(
                "piwardrive.services.alerting.send_webhook_notification"
            ) as mock_webhook,
        ):

            await manager.evaluate(metrics)

            mock_email.assert_called_once()
            mock_sms.assert_called_once()
            mock_webhook.assert_called_once()

    @pytest.mark.asyncio
    async def test_evaluate_multiple_rules(self):
        """Test evaluation with multiple rules."""
        rules = [
            AlertRule("cpu_usage", 80.0, ["mailto:admin@example.com"]),
            AlertRule("memory_usage", 90.0, ["sms:+1234567890"]),
            AlertRule("disk_usage", 85.0, ["https://webhook.example.com"]),
        ]
        manager = AlertManager(rules)
        metrics = {"cpu_usage": 85.0, "memory_usage": 95.0, "disk_usage": 90.0}

        with (
            patch("piwardrive.services.alerting.send_email_alert") as mock_email,
            patch("piwardrive.services.alerting.send_sms_alert") as mock_sms,
            patch(
                "piwardrive.services.alerting.send_webhook_notification"
            ) as mock_webhook,
        ):

            await manager.evaluate(metrics)

            mock_email.assert_called_once()
            mock_sms.assert_called_once()
            mock_webhook.assert_called_once()

    @pytest.mark.asyncio
    async def test_evaluate_custom_alert_level(self):
        """Test evaluation with custom alert level."""
        rule = AlertRule(
            "cpu_usage", 80.0, ["mailto:admin@example.com"], level="critical"
        )
        manager = AlertManager([rule])
        metrics = {"cpu_usage": 85.0}

        with patch("piwardrive.services.alerting.send_email_alert") as mock_email:
            await manager.evaluate(metrics)

            mock_email.assert_called_once_with(
                "admin@example.com",
                "CRITICAL alert",
                "Metric 'cpu_usage' value 85.00 exceeded threshold 80.00",
            )

    @pytest.mark.asyncio
    async def test_evaluate_exact_threshold_no_alert(self):
        """Test that exact threshold match triggers alert."""
        rule = AlertRule("cpu_usage", 80.0, ["mailto:admin@example.com"])
        manager = AlertManager([rule])
        metrics = {"cpu_usage": 80.0}

        with (
            patch("piwardrive.services.alerting.send_email_alert") as mock_email,
            patch("piwardrive.services.alerting.logger.warning") as mock_warning,
        ):
            await manager.evaluate(metrics)

            # Alerts should be triggered for exact threshold match
            mock_email.assert_called_once()
            mock_warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_evaluate_unknown_channel_type(self):
        """Test evaluation with unknown channel type (should be ignored)."""
        rule = AlertRule("cpu_usage", 80.0, ["unknown:channel"])
        manager = AlertManager([rule])
        metrics = {"cpu_usage": 85.0}

        with patch("piwardrive.services.alerting.logger.warning") as mock_warning:
            await manager.evaluate(metrics)

            # Should still log the alert message
            mock_warning.assert_called_once_with(
                "Metric 'cpu_usage' value 85.00 exceeded threshold 80.00"
            )


class TestAlertingModule:
    """Test suite for module-level functionality."""

    def test_module_exports(self):
        """Test that all expected functions and classes are exported."""
        from piwardrive.services.alerting import __all__

        expected_exports = [
            "send_email_alert",
            "send_sms_alert",
            "send_webhook_notification",
            "send_slack_notification",
            "send_discord_notification",
            "AlertRule",
            "AlertManager",
        ]

        assert set(__all__) == set(expected_exports)

    def test_alert_rule_repr(self):
        """Test AlertRule string representation."""
        rule = AlertRule("cpu_usage", 80.0, ["mailto:admin@example.com"])
        repr_str = repr(rule)

        assert "AlertRule" in repr_str
        assert "cpu_usage" in repr_str
        assert "80.0" in repr_str
