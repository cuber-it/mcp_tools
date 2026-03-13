"""Pure tool logic for homeassistant — no MCP dependency."""

from __future__ import annotations

from .client import HomeAssistantClient

def entity_list(client: HomeAssistantClient, domain: str = "") -> str:
    """List all entities"""
    # TODO: implement
    raise NotImplementedError("entity_list")


def entity_state(client: HomeAssistantClient, entity_id: str) -> str:
    """Get current state of an entity"""
    # TODO: implement
    raise NotImplementedError("entity_state")


def entity_set(client: HomeAssistantClient, entity_id: str, state: str) -> str:
    """Set state of an entity"""
    # TODO: implement
    raise NotImplementedError("entity_set")


def service_call(client: HomeAssistantClient, domain: str, service: str, entity_id: str = "") -> str:
    """Call a Home Assistant service"""
    # TODO: implement
    raise NotImplementedError("service_call")


def automation_list(client: HomeAssistantClient) -> str:
    """List all automations"""
    # TODO: implement
    raise NotImplementedError("automation_list")


def automation_trigger(client: HomeAssistantClient, entity_id: str) -> str:
    """Trigger an automation"""
    # TODO: implement
    raise NotImplementedError("automation_trigger")


def automation_enable(client: HomeAssistantClient, entity_id: str) -> str:
    """Enable an automation"""
    # TODO: implement
    raise NotImplementedError("automation_enable")


def automation_disable(client: HomeAssistantClient, entity_id: str) -> str:
    """Disable an automation"""
    # TODO: implement
    raise NotImplementedError("automation_disable")


def history(client: HomeAssistantClient, entity_id: str, hours: int = 24) -> str:
    """Get state history for an entity"""
    # TODO: implement
    raise NotImplementedError("history")


def logbook(client: HomeAssistantClient, hours: int = 24, entity_id: str = "") -> str:
    """Get logbook entries"""
    # TODO: implement
    raise NotImplementedError("logbook")

