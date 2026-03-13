"""Tests for systemd tools."""

import pytest

from mcp_systemd_tools.systemd import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_service_list_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_list")
        assert callable(tools.service_list)

    def test_service_status_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_status")
        assert callable(tools.service_status)

    def test_service_start_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_start")
        assert callable(tools.service_start)

    def test_service_stop_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_stop")
        assert callable(tools.service_stop)

    def test_service_restart_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_restart")
        assert callable(tools.service_restart)

    def test_service_enable_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_enable")
        assert callable(tools.service_enable)

    def test_service_disable_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "service_disable")
        assert callable(tools.service_disable)

    def test_journal_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "journal")
        assert callable(tools.journal)

    def test_timer_list_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "timer_list")
        assert callable(tools.timer_list)

    def test_timer_info_exists(self):
        from mcp_systemd_tools.systemd import tools
        assert hasattr(tools, "timer_info")
        assert callable(tools.timer_info)


# TODO: add functional tests
