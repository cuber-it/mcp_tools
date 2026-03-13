"""Homeassistant — MCP plugin.

Home Assistant tools for MCP — entities, services, automations, history

Config keys:
    url: (required)
    token: (required)
"""

from __future__ import annotations

from .client import HomeAssistantClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register homeassistant tools as MCP tools."""
    client = HomeAssistantClient(config)

    @mcp.tool()
    def entity_list(domain: str = "") -> str:
        """List all entities"""
        return tools.entity_list(client, domain)

    @mcp.tool()
    def entity_state(entity_id: str) -> str:
        """Get current state of an entity"""
        return tools.entity_state(client, entity_id)

    @mcp.tool()
    def entity_set(entity_id: str, state: str) -> str:
        """Set state of an entity"""
        return tools.entity_set(client, entity_id, state)

    @mcp.tool()
    def service_call(domain: str, service: str, entity_id: str = "") -> str:
        """Call a Home Assistant service"""
        return tools.service_call(client, domain, service, entity_id)

    @mcp.tool()
    def automation_list() -> str:
        """List all automations"""
        return tools.automation_list(client)

    @mcp.tool()
    def automation_trigger(entity_id: str) -> str:
        """Trigger an automation"""
        return tools.automation_trigger(client, entity_id)

    @mcp.tool()
    def automation_enable(entity_id: str) -> str:
        """Enable an automation"""
        return tools.automation_enable(client, entity_id)

    @mcp.tool()
    def automation_disable(entity_id: str) -> str:
        """Disable an automation"""
        return tools.automation_disable(client, entity_id)

    @mcp.tool()
    def history(entity_id: str, hours: int = 24) -> str:
        """Get state history for an entity"""
        return tools.history(client, entity_id, hours)

    @mcp.tool()
    def logbook(hours: int = 24, entity_id: str = "") -> str:
        """Get logbook entries"""
        return tools.logbook(client, hours, entity_id)
