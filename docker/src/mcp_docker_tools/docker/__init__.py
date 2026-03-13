"""Docker — MCP plugin.

Container management tools for MCP — containers, images, volumes, compose

Config keys:
    base_url: (required)
"""

from __future__ import annotations

from .client import DockerClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register docker tools as MCP tools."""
    client = DockerClient(config)

    @mcp.tool()
    def container_list(all: bool = False) -> str:
        """List containers"""
        return tools.container_list(client, all)

    @mcp.tool()
    def container_start(container_id: str) -> str:
        """Start a stopped container"""
        return tools.container_start(client, container_id)

    @mcp.tool()
    def container_stop(container_id: str, timeout: int = 10) -> str:
        """Stop a running container"""
        return tools.container_stop(client, container_id, timeout)

    @mcp.tool()
    def container_restart(container_id: str) -> str:
        """Restart a container"""
        return tools.container_restart(client, container_id)

    @mcp.tool()
    def container_remove(container_id: str, force: bool = False) -> str:
        """Remove a container"""
        return tools.container_remove(client, container_id, force)

    @mcp.tool()
    def container_logs(container_id: str, tail: int = 100) -> str:
        """Get container logs"""
        return tools.container_logs(client, container_id, tail)

    @mcp.tool()
    def container_inspect(container_id: str) -> str:
        """Inspect container details"""
        return tools.container_inspect(client, container_id)

    @mcp.tool()
    def image_list() -> str:
        """List local images"""
        return tools.image_list(client)

    @mcp.tool()
    def image_pull(image: str) -> str:
        """Pull an image from registry"""
        return tools.image_pull(client, image)

    @mcp.tool()
    def image_remove(image: str, force: bool = False) -> str:
        """Remove a local image"""
        return tools.image_remove(client, image, force)

    @mcp.tool()
    def volume_list() -> str:
        """List volumes"""
        return tools.volume_list(client)

    @mcp.tool()
    def network_list() -> str:
        """List networks"""
        return tools.network_list(client)

    @mcp.tool()
    def compose_up(path: str, detach: bool = True) -> str:
        """Start services from compose file"""
        return tools.compose_up(client, path, detach)

    @mcp.tool()
    def compose_down(path: str) -> str:
        """Stop and remove compose services"""
        return tools.compose_down(client, path)

    @mcp.tool()
    def compose_ps(path: str) -> str:
        """List compose service status"""
        return tools.compose_ps(client, path)
