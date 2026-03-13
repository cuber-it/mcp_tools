"""Database — MCP plugin.

Database tools for MCP — query, schema, export for SQLite and PostgreSQL

Config keys:
    uri: (required)
"""

from __future__ import annotations

from .client import DatabaseClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register database tools as MCP tools."""
    client = DatabaseClient(config)

    @mcp.tool()
    def query(sql: str, limit: int = 100) -> str:
        """Execute a read-only SQL query and return results"""
        return tools.query(client, sql, limit)

    @mcp.tool()
    def execute(sql: str) -> str:
        """Execute a write SQL statement (INSERT/UPDATE/DELETE, requires write_enabled config)"""
        return tools.execute(client, sql)

    @mcp.tool()
    def schema(table: str = "") -> str:
        """Show database schema — tables, columns, types, indices"""
        return tools.schema(client, table)

    @mcp.tool()
    def tables() -> str:
        """List all tables in the database"""
        return tools.tables(client)

    @mcp.tool()
    def describe(table: str) -> str:
        """Describe a table — columns, types, constraints"""
        return tools.describe(client, table)

    @mcp.tool()
    def export_csv(sql: str, path: str) -> str:
        """Export query results as CSV"""
        return tools.export_csv(client, sql, path)

    @mcp.tool()
    def export_json(sql: str, path: str) -> str:
        """Export query results as JSON"""
        return tools.export_json(client, sql, path)

    @mcp.tool()
    def explain(sql: str) -> str:
        """Show query execution plan"""
        return tools.explain(client, sql)
