"""Mqtt — MCP plugin.

MQTT messaging tools for MCP — publish, subscribe, topics

Config keys:
    host: (required)
    port: (required)
"""

from __future__ import annotations

from .client import MqttClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register mqtt tools as MCP tools."""
    client = MqttClient(config)

    @mcp.tool()
    def publish(topic: str, payload: str, retain: bool = False) -> str:
        """Publish a message to a topic"""
        return tools.publish(client, topic, payload, retain)

    @mcp.tool()
    def subscribe(topic: str, timeout: int = 5, limit: int = 10) -> str:
        """Subscribe to a topic and return recent messages"""
        return tools.subscribe(client, topic, timeout, limit)

    @mcp.tool()
    def topics() -> str:
        """List known topics (via $SYS or recent activity)"""
        return tools.topics(client)

    @mcp.tool()
    def retained_get(topic: str) -> str:
        """Get retained message for a topic"""
        return tools.retained_get(client, topic)

    @mcp.tool()
    def retained_clear(topic: str) -> str:
        """Clear retained message for a topic"""
        return tools.retained_clear(client, topic)

    @mcp.tool()
    def broker_info() -> str:
        """Get broker information via $SYS topics"""
        return tools.broker_info(client)
