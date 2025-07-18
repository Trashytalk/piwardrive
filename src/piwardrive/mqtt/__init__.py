"""MQTT client for publishing detection events."""

from __future__ import annotations

import json
from typing import Any

import paho.mqtt.client as mqtt


class MQTTClient:
    """Simple MQTT client for publishing status updates."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1883,
        topic: str = "piwardrive/status",
    ) -> None:
        """Initialize MQTT client.

        Args:
            host: MQTT broker host
            port: MQTT broker port
            topic: Default topic for publishing
        """
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.connected = False

    def connect(self) -> None:
        """Connect to the MQTT broker."""
        if not self.connected:
            self.client.connect(self.host, self.port)
            self.client.loop_start()
            self.connected = True

    def publish(self, payload: Any) -> None:
        """Publish a payload to the default topic.

        Args:
            payload: Data to publish (will be JSON encoded)
        """
        if not self.connected:
            self.connect()
        self.client.publish(self.topic, json.dumps(payload))

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
