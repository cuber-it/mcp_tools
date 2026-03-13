        # mcp-docker-tools

        Container management tools for MCP — containers, images, volumes, compose

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-docker-tools
        ```

        ## Usage

        ```bash
        mcp-docker-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "docker": { "command": "mcp-docker-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `container_list` | List containers |
| `container_start` | Start a stopped container |
| `container_stop` | Stop a running container |
| `container_restart` | Restart a container |
| `container_remove` | Remove a container |
| `container_logs` | Get container logs |
| `container_inspect` | Inspect container details |
| `image_list` | List local images |
| `image_pull` | Pull an image from registry |
| `image_remove` | Remove a local image |
| `volume_list` | List volumes |
| `network_list` | List networks |
| `compose_up` | Start services from compose file |
| `compose_down` | Stop and remove compose services |
| `compose_ps` | List compose service status |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
