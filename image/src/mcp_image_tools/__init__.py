"""mcp-image-tools — Image processing tools for MCP — read, resize, crop, convert, return as base64

Built on mcp-server-framework. Can also be used as a plugin via register().
"""

__version__ = "1.0.0"


def main():
    from mcp_server_framework import load_config, create_server, run_server
    from mcp_image_tools.image import register

    config = load_config()
    mcp = create_server(config)
    register(mcp, config)
    run_server(mcp, config)
