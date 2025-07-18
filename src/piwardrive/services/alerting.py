"""Alerting utilities for system monitoring.

This module provides comprehensive alerting functionality including email
notifications, webhook integrations, and rule-based alert management for
the PiWardrive monitoring system.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import httpx

logger = logging.getLogger(__name__)


async def send_email_alert(address: str, subject: str, message: str) -> None:
    """Send an email alert.

    This is a simple stub that logs the alert. Integrate with an SMTP
    library or service in a production environment.
    """
    logger.warning("Email alert to %s: %s", address, subject)
    logger.debug("Email body: %s", message)


async def send_sms_alert(number: str, message: str) -> None:
    """Send an SMS alert.

    This implementation only logs the alert for now.
    """
    logger.warning("SMS alert to %s: %s", number, message)


async def send_webhook_notification(url: str, payload: Mapping[str, Any]) -> None:
    """POST ``payload`` to the given webhook ``url``."""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=dict(payload))
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Webhook %s failed: %s", url, exc)


async def send_slack_notification(webhook_url: str, message: str) -> None:
    """Send a Slack message via webhook."""
    await send_webhook_notification(webhook_url, {"text": message})


async def send_discord_notification(webhook_url: str, message: str) -> None:
    """Send a Discord message via webhook."""
    await send_webhook_notification(webhook_url, {"content": message})


@dataclass
class AlertRule:
    """Threshold based alert rule."""

    metric: str
    threshold: float
    channels: Iterable[str]
    level: str = "warning"


class AlertManager:
    """Evaluate metrics against configured alert rules."""

    def __init__(self, rules: Iterable[AlertRule] | None = None) -> None:
        """Initialize alert manager with optional rules.

        Args:
            rules: Initial set of alert rules to load.
        """
        self.rules = list(rules or [])

    def add_rule(self, rule: AlertRule) -> None:
        """Add an alert rule to the manager."""
        self.rules.append(rule)

    async def evaluate(self, metrics: Mapping[str, float]) -> None:
        """Evaluate all rules against the provided metrics and trigger alerts."""
        for rule in self.rules:
            value = metrics.get(rule.metric)
            if value is None or value < rule.threshold:
                continue
            msg = (
                f"Metric '{rule.metric}' value {value:.2f} "
                f"exceeded threshold {rule.threshold:.2f}"
            )
            for ch in rule.channels:
                if ch.startswith("mailto:"):
                    await send_email_alert(ch[7:], f"{rule.level.upper()} alert", msg)
                elif ch.startswith("sms:"):
                    await send_sms_alert(ch[4:], msg)
                elif ch.startswith("http"):
                    await send_webhook_notification(ch, {"message": msg})
                elif ch.startswith("slack:"):
                    await send_slack_notification(ch[6:], msg)
                elif ch.startswith("discord:"):
                    await send_discord_notification(ch[8:], msg)
            logger.warning(msg)


__all__ = [
    "send_email_alert",
    "send_sms_alert",
    "send_webhook_notification",
    "send_slack_notification",
    "send_discord_notification",
    "AlertRule",
    "AlertManager",
]
