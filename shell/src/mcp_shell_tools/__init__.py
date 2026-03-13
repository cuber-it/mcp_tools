"""mcp-shell-tools — 33 workstation tools as a standalone MCP server.

Built on mcp-server-framework. Can also be used as a plugin via register().
"""

__version__ = "3.0.0"


def main():
    from mcp_server_framework import load_config, create_server, run_server
    from mcp_shell_tools.shell import register

    config = load_config()
    mcp = create_server(config)
    register(mcp, config)
    run_server(mcp, config)
