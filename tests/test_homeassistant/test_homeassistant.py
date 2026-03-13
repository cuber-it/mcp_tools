"""Tests for homeassistant tools."""

import pytest

from mcp_homeassistant_tools.homeassistant import register
from mcp_homeassistant_tools.homeassistant.client import HomeAssistantClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert HomeAssistantClient is not None


class TestTools:
    def test_entity_list_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "entity_list")
        assert callable(tools.entity_list)

    def test_entity_state_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "entity_state")
        assert callable(tools.entity_state)

    def test_entity_set_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "entity_set")
        assert callable(tools.entity_set)

    def test_service_call_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "service_call")
        assert callable(tools.service_call)

    def test_automation_list_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "automation_list")
        assert callable(tools.automation_list)

    def test_automation_trigger_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "automation_trigger")
        assert callable(tools.automation_trigger)

    def test_automation_enable_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "automation_enable")
        assert callable(tools.automation_enable)

    def test_automation_disable_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "automation_disable")
        assert callable(tools.automation_disable)

    def test_history_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "history")
        assert callable(tools.history)

    def test_logbook_exists(self):
        from mcp_homeassistant_tools.homeassistant import tools
        assert hasattr(tools, "logbook")
        assert callable(tools.logbook)


# TODO: add functional tests
