"""Traefik — MCP plugin.

Traefik reverse proxy tools for MCP — routers, services, middlewares, certs

Config keys:
    url: (required)
"""

from __future__ import annotations

from .client import TraefikClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register traefik tools as MCP tools."""
    client = TraefikClient(config)

    @mcp.tool()
    def router_list() -> str:
        """List all Traefik routers"""
        return tools.router_list(client)

    @mcp.tool()
    def router_inspect(name: str) -> str:
        """Show details of a router"""
        return tools.router_inspect(client, name)

    @mcp.tool()
    def service_list() -> str:
        """List all Traefik services"""
        return tools.service_list(client)

    @mcp.tool()
    def service_health(name: str) -> str:
        """Show health status of a service"""
        return tools.service_health(client, name)

    @mcp.tool()
    def middleware_list() -> str:
        """List all middlewares"""
        return tools.middleware_list(client)

    @mcp.tool()
    def entrypoint_list() -> str:
        """List all entrypoints"""
        return tools.entrypoint_list(client)

    @mcp.tool()
    def cert_list() -> str:
        """List TLS certificates"""
        return tools.cert_list(client)

    @mcp.tool()
    def cert_expiry(domain: str = "") -> str:
        """Check certificate expiry dates"""
        return tools.cert_expiry(client, domain)

    @mcp.tool()
    def overview() -> str:
        """Traefik dashboard overview — routers, services, middlewares counts"""
        return tools.overview(client)
