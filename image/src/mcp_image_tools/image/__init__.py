"""Image — MCP plugin.

Image processing tools for MCP — read, resize, crop, convert, return as base64
"""

from __future__ import annotations

from . import tools


def register(mcp, config: dict) -> None:
    """Register image tools as MCP tools."""
    @mcp.tool()
    def image_read_base64(path: str, max_width: int = 0) -> str:
        """Read an image file and return as base64-encoded PNG"""
        return tools.image_read_base64(path, max_width)

    @mcp.tool()
    def image_resize(path: str, width: int, height: int = 0) -> str:
        """Resize an image and return as base64-encoded PNG"""
        return tools.image_resize(path, width, height)

    @mcp.tool()
    def image_crop(path: str, x: int, y: int, width: int, height: int) -> str:
        """Crop a region from an image and return as base64-encoded PNG"""
        return tools.image_crop(path, x, y, width, height)

    @mcp.tool()
    def image_screenshot(region: str = "", max_width: int = 1280) -> str:
        """Take a desktop screenshot and return as base64-encoded PNG"""
        return tools.image_screenshot(region, max_width)

    @mcp.tool()
    def image_info(path: str) -> str:
        """Get image metadata (size, format, mode)"""
        return tools.image_info(path)

    @mcp.tool()
    def image_convert(path: str, format: str = "PNG", quality: int = 85) -> str:
        """Convert image format and return as base64"""
        return tools.image_convert(path, format, quality)
