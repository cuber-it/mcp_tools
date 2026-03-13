"""mcp-python-tools — Python environment tools for MCP — venvs, pip, packages, interpreter info

Built on mcp-server-framework. Can also be used as a plugin via register().
"""

__version__ = "1.0.0"


def main():
    from mcp_server_framework import load_config, create_server, run_server
    from mcp_python_tools.python import register

    config = load_config()
    mcp = create_server(config)
    register(mcp, config)
    run_server(mcp, config)
