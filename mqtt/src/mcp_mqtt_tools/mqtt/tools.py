"""Pure tool logic for mqtt — no MCP dependency."""

from __future__ import annotations

from .client import MqttClient

def publish(client: MqttClient, topic: str, payload: str, retain: bool = False) -> str:
    """Publish a message to a topic"""
    # TODO: implement
    raise NotImplementedError("publish")


def subscribe(client: MqttClient, topic: str, timeout: int = 5, limit: int = 10) -> str:
    """Subscribe to a topic and return recent messages"""
    # TODO: implement
    raise NotImplementedError("subscribe")


def topics(client: MqttClient) -> str:
    """List known topics (via $SYS or recent activity)"""
    # TODO: implement
    raise NotImplementedError("topics")


def retained_get(client: MqttClient, topic: str) -> str:
    """Get retained message for a topic"""
    # TODO: implement
    raise NotImplementedError("retained_get")


def retained_clear(client: MqttClient, topic: str) -> str:
    """Clear retained message for a topic"""
    # TODO: implement
    raise NotImplementedError("retained_clear")


def broker_info(client: MqttClient) -> str:
    """Get broker information via $SYS topics"""
    # TODO: implement
    raise NotImplementedError("broker_info")

