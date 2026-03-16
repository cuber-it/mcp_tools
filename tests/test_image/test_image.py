"""Tests for image tools."""

import pytest

from mcp_image_tools.image import register


class TestImport:
    def test_register_exists(self):
        assert callable(register)


class TestTools:
    def test_image_read_base64_exists(self):
        from mcp_image_tools.image import tools
        assert hasattr(tools, "image_read_base64")
        assert callable(tools.image_read_base64)

    def test_image_resize_exists(self):
        from mcp_image_tools.image import tools
        assert hasattr(tools, "image_resize")
        assert callable(tools.image_resize)

    def test_image_crop_exists(self):
        from mcp_image_tools.image import tools
        assert hasattr(tools, "image_crop")
        assert callable(tools.image_crop)

    def test_image_screenshot_exists(self):
        from mcp_image_tools.image import tools
        assert hasattr(tools, "image_screenshot")
        assert callable(tools.image_screenshot)

    def test_image_info_exists(self):
        from mcp_image_tools.image import tools
        assert hasattr(tools, "image_info")
        assert callable(tools.image_info)

    def test_image_convert_exists(self):
        from mcp_image_tools.image import tools
        assert hasattr(tools, "image_convert")
        assert callable(tools.image_convert)


# TODO: add functional tests
