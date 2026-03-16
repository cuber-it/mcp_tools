        # mcp-image-tools

        Image processing tools for MCP — read, resize, crop, convert, return as base64

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-image-tools
        ```

        ## Usage

        ```bash
        mcp-image-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "image": { "command": "mcp-image-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `image_read_base64` | Read an image file and return as base64-encoded PNG |
| `image_resize` | Resize an image and return as base64-encoded PNG |
| `image_crop` | Crop a region from an image and return as base64-encoded PNG |
| `image_screenshot` | Take a desktop screenshot and return as base64-encoded PNG |
| `image_info` | Get image metadata (size, format, mode) |
| `image_convert` | Convert image format and return as base64 |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
