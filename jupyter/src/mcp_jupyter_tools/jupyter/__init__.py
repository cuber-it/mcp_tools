"""Jupyter — MCP plugin.

Jupyter tools for MCP — notebooks, kernels, JupyterHub users and servers

Config keys:
    url: (required)
    token: (required)
"""

from __future__ import annotations

from .client import JupyterClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register jupyter tools as MCP tools."""
    client = JupyterClient(config)

    @mcp.tool()
    def notebook_list(path: str = "") -> str:
        """List notebooks in a directory"""
        return tools.notebook_list(client, path)

    @mcp.tool()
    def notebook_read(path: str) -> str:
        """Read a notebook (cells with outputs)"""
        return tools.notebook_read(client, path)

    @mcp.tool()
    def notebook_create(path: str, kernel: str = "python3") -> str:
        """Create a new notebook"""
        return tools.notebook_create(client, path, kernel)

    @mcp.tool()
    def notebook_add_cell(path: str, source: str, cell_type: str = "code", position: int = -1) -> str:
        """Add a cell to a notebook"""
        return tools.notebook_add_cell(client, path, source, cell_type, position)

    @mcp.tool()
    def notebook_execute(path: str, cell_index: int = -1) -> str:
        """Execute a notebook or specific cell"""
        return tools.notebook_execute(client, path, cell_index)

    @mcp.tool()
    def notebook_export(path: str, format: str = "html") -> str:
        """Export notebook to another format"""
        return tools.notebook_export(client, path, format)

    @mcp.tool()
    def kernel_list() -> str:
        """List running kernels"""
        return tools.kernel_list(client)

    @mcp.tool()
    def kernel_start(kernel_name: str = "python3") -> str:
        """Start a new kernel"""
        return tools.kernel_start(client, kernel_name)

    @mcp.tool()
    def kernel_interrupt(kernel_id: str) -> str:
        """Interrupt a running kernel"""
        return tools.kernel_interrupt(client, kernel_id)

    @mcp.tool()
    def kernel_restart(kernel_id: str) -> str:
        """Restart a kernel"""
        return tools.kernel_restart(client, kernel_id)

    @mcp.tool()
    def hub_user_list() -> str:
        """List JupyterHub users"""
        return tools.hub_user_list(client)

    @mcp.tool()
    def hub_user_info(username: str) -> str:
        """Get info about a JupyterHub user"""
        return tools.hub_user_info(client, username)

    @mcp.tool()
    def hub_server_start(username: str) -> str:
        """Start a user's JupyterHub server"""
        return tools.hub_server_start(client, username)

    @mcp.tool()
    def hub_server_stop(username: str) -> str:
        """Stop a user's JupyterHub server"""
        return tools.hub_server_stop(client, username)
