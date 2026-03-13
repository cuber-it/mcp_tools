        # mcp-traefik-tools

        Traefik reverse proxy tools for MCP — routers, services, middlewares, certs

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-traefik-tools
        ```

        ## Usage

        ```bash
        mcp-traefik-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "traefik": { "command": "mcp-traefik-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `router_list` | List all Traefik routers |
| `router_inspect` | Show details of a router |
| `service_list` | List all Traefik services |
| `service_health` | Show health status of a service |
| `middleware_list` | List all middlewares |
| `entrypoint_list` | List all entrypoints |
| `cert_list` | List TLS certificates |
| `cert_expiry` | Check certificate expiry dates |
| `overview` | Traefik dashboard overview — routers, services, middlewares counts |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
