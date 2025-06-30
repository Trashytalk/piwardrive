from __future__ import annotations

import json
from typing import Any

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 1883,
        topic: str = "piwardrive/status",
    ) -> None:
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.connected = False

    def connect(self) -> None:
        if not self.connected:
            self.client.connect(self.host, self.port)
            self.client.loop_start()
            self.connected = True

    def publish(self, payload: Any) -> None:
        if not self.connected:
            self.connect()
        self.client.publish(self.topic, json.dumps(payload))

    def disconnect(self) -> None:
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
