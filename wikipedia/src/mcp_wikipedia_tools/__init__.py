"""mcp-wikipedia-tools — Wikipedia tools for MCP — search, articles, summaries, multilingual

Built on mcp-server-framework. Can also be used as a plugin via register().
"""

__version__ = "1.0.0"


def main():
    from mcp_server_framework import load_config, create_server, run_server
    from mcp_wikipedia_tools.wikipedia import register

    config = load_config()
    mcp = create_server(config)
    register(mcp, config)
    run_server(mcp, config)
