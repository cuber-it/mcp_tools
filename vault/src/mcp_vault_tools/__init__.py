"""MCP Vault Tools — headless Obsidian-compatible vault operations."""

from mcp_server_framework import create_server


def main():
    """Entry point for standalone MCP server."""
    server = create_server(
        name="mcp-vault-tools",
        plugin="mcp_vault_tools.vault",
    )
    server.run()
