"""mcp-homematic-tools — 55 HomeMatic/OpenCCU tools as a standalone MCP server.

Full JSON-RPC API coverage for HomeMatic CCU3/OpenCCU:
devices, channels, interfaces, rooms, programs, system variables,
events, and system management.

Built on mcp-server-framework. Can also be used as a plugin via register().
"""

__version__ = "1.0.0"


def main():
    from mcp_server_framework import load_config, create_server, run_server
    from mcp_homematic_tools.homematic import register

    config = load_config()
    mcp = create_server(config)
    register(mcp, config)
    run_server(mcp, config)
