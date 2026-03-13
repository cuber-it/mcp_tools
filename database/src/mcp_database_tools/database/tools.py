"""Pure tool logic for database — no MCP dependency."""

from __future__ import annotations

from .client import DatabaseClient

def query(client: DatabaseClient, sql: str, limit: int = 100) -> str:
    """Execute a read-only SQL query and return results"""
    # TODO: implement
    raise NotImplementedError("query")


def execute(client: DatabaseClient, sql: str) -> str:
    """Execute a write SQL statement (INSERT/UPDATE/DELETE, requires write_enabled config)"""
    # TODO: implement
    raise NotImplementedError("execute")


def schema(client: DatabaseClient, table: str = "") -> str:
    """Show database schema — tables, columns, types, indices"""
    # TODO: implement
    raise NotImplementedError("schema")


def tables(client: DatabaseClient) -> str:
    """List all tables in the database"""
    # TODO: implement
    raise NotImplementedError("tables")


def describe(client: DatabaseClient, table: str) -> str:
    """Describe a table — columns, types, constraints"""
    # TODO: implement
    raise NotImplementedError("describe")


def export_csv(client: DatabaseClient, sql: str, path: str) -> str:
    """Export query results as CSV"""
    # TODO: implement
    raise NotImplementedError("export_csv")


def export_json(client: DatabaseClient, sql: str, path: str) -> str:
    """Export query results as JSON"""
    # TODO: implement
    raise NotImplementedError("export_json")


def explain(client: DatabaseClient, sql: str) -> str:
    """Show query execution plan"""
    # TODO: implement
    raise NotImplementedError("explain")

