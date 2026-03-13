"""Tests for mqtt tools."""

import pytest

from mcp_mqtt_tools.mqtt import register
from mcp_mqtt_tools.mqtt.client import MqttClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert MqttClient is not None


class TestTools:
    def test_publish_exists(self):
        from mcp_mqtt_tools.mqtt import tools
        assert hasattr(tools, "publish")
        assert callable(tools.publish)

    def test_subscribe_exists(self):
        from mcp_mqtt_tools.mqtt import tools
        assert hasattr(tools, "subscribe")
        assert callable(tools.subscribe)

    def test_topics_exists(self):
        from mcp_mqtt_tools.mqtt import tools
        assert hasattr(tools, "topics")
        assert callable(tools.topics)

    def test_retained_get_exists(self):
        from mcp_mqtt_tools.mqtt import tools
        assert hasattr(tools, "retained_get")
        assert callable(tools.retained_get)

    def test_retained_clear_exists(self):
        from mcp_mqtt_tools.mqtt import tools
        assert hasattr(tools, "retained_clear")
        assert callable(tools.retained_clear)

    def test_broker_info_exists(self):
        from mcp_mqtt_tools.mqtt import tools
        assert hasattr(tools, "broker_info")
        assert callable(tools.broker_info)


# TODO: add functional tests
