"""Tests for database tools."""

import pytest

from mcp_database_tools.database import register
from mcp_database_tools.database.client import DatabaseClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert DatabaseClient is not None


class TestTools:
    def test_query_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "query")
        assert callable(tools.query)

    def test_execute_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "execute")
        assert callable(tools.execute)

    def test_schema_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "schema")
        assert callable(tools.schema)

    def test_tables_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "tables")
        assert callable(tools.tables)

    def test_describe_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "describe")
        assert callable(tools.describe)

    def test_export_csv_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "export_csv")
        assert callable(tools.export_csv)

    def test_export_json_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "export_json")
        assert callable(tools.export_json)

    def test_explain_exists(self):
        from mcp_database_tools.database import tools
        assert hasattr(tools, "explain")
        assert callable(tools.explain)


# TODO: add functional tests
