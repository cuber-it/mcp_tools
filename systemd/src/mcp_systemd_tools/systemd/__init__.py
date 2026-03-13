"""Systemd — MCP plugin.

Systemd service management tools for MCP — services, journal, timers
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register systemd tools as MCP tools."""
    @mcp.tool()
    def service_list(state: str = "", user: bool = False) -> str:
        """List systemd services"""
        return tools.service_list(state, user)

    @mcp.tool()
    def service_status(service: str, user: bool = False) -> str:
        """Show status of a service"""
        return tools.service_status(service, user)

    @mcp.tool()
    def service_start(service: str, user: bool = False) -> str:
        """Start a service"""
        return tools.service_start(service, user)

    @mcp.tool()
    def service_stop(service: str, user: bool = False) -> str:
        """Stop a service"""
        return tools.service_stop(service, user)

    @mcp.tool()
    def service_restart(service: str, user: bool = False) -> str:
        """Restart a service"""
        return tools.service_restart(service, user)

    @mcp.tool()
    def service_enable(service: str, user: bool = False) -> str:
        """Enable a service to start on boot"""
        return tools.service_enable(service, user)

    @mcp.tool()
    def service_disable(service: str, user: bool = False) -> str:
        """Disable a service from starting on boot"""
        return tools.service_disable(service, user)

    @mcp.tool()
    def journal(service: str, lines: int = 50, since: str = "") -> str:
        """Read journal logs for a service"""
        return tools.journal(service, lines, since)

    @mcp.tool()
    def timer_list(user: bool = False) -> str:
        """List systemd timers"""
        return tools.timer_list(user)

    @mcp.tool()
    def timer_info(timer: str, user: bool = False) -> str:
        """Show details of a timer"""
        return tools.timer_info(timer, user)
