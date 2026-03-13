"""Email — MCP plugin.

Email tools for MCP — IMAP inbox, search, send via SMTP

Config keys:
    imap_host: (required)
    smtp_host: (required)
    username: (required)
    password: (required)
"""

from __future__ import annotations

from .client import EmailClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register email tools as MCP tools."""
    client = EmailClient(config)

    @mcp.tool()
    def inbox(limit: int = 20, folder: str = "INBOX") -> str:
        """List recent messages from inbox"""
        return tools.inbox(client, limit, folder)

    @mcp.tool()
    def search(query: str, folder: str = "INBOX", limit: int = 20) -> str:
        """Search emails by criteria"""
        return tools.search(client, query, folder, limit)

    @mcp.tool()
    def read(message_id: str, folder: str = "INBOX") -> str:
        """Read a specific email by ID"""
        return tools.read(client, message_id, folder)

    @mcp.tool()
    def folders() -> str:
        """List available mail folders"""
        return tools.folders(client)

    @mcp.tool()
    def move(message_id: str, target_folder: str, source_folder: str = "INBOX") -> str:
        """Move a message to another folder"""
        return tools.move(client, message_id, target_folder, source_folder)

    @mcp.tool()
    def mark(message_id: str, flag: str, folder: str = "INBOX") -> str:
        """Mark a message as read/unread/flagged"""
        return tools.mark(client, message_id, flag, folder)

    @mcp.tool()
    def send(to: str, subject: str, body: str) -> str:
        """Send a plain text email"""
        return tools.send(client, to, subject, body)

    @mcp.tool()
    def send_html(to: str, subject: str, html: str) -> str:
        """Send an HTML email"""
        return tools.send_html(client, to, subject, html)

    @mcp.tool()
    def reply(message_id: str, body: str, folder: str = "INBOX") -> str:
        """Reply to a message"""
        return tools.reply(client, message_id, body, folder)
