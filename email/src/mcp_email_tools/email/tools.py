"""Pure tool logic for email — no MCP dependency."""

from __future__ import annotations

from .client import EmailClient

def inbox(client: EmailClient, limit: int = 20, folder: str = "INBOX") -> str:
    """List recent messages from inbox"""
    # TODO: implement
    raise NotImplementedError("inbox")


def search(client: EmailClient, query: str, folder: str = "INBOX", limit: int = 20) -> str:
    """Search emails by criteria"""
    # TODO: implement
    raise NotImplementedError("search")


def read(client: EmailClient, message_id: str, folder: str = "INBOX") -> str:
    """Read a specific email by ID"""
    # TODO: implement
    raise NotImplementedError("read")


def folders(client: EmailClient) -> str:
    """List available mail folders"""
    # TODO: implement
    raise NotImplementedError("folders")


def move(client: EmailClient, message_id: str, target_folder: str, source_folder: str = "INBOX") -> str:
    """Move a message to another folder"""
    # TODO: implement
    raise NotImplementedError("move")


def mark(client: EmailClient, message_id: str, flag: str, folder: str = "INBOX") -> str:
    """Mark a message as read/unread/flagged"""
    # TODO: implement
    raise NotImplementedError("mark")


def send(client: EmailClient, to: str, subject: str, body: str) -> str:
    """Send a plain text email"""
    # TODO: implement
    raise NotImplementedError("send")


def send_html(client: EmailClient, to: str, subject: str, html: str) -> str:
    """Send an HTML email"""
    # TODO: implement
    raise NotImplementedError("send_html")


def reply(client: EmailClient, message_id: str, body: str, folder: str = "INBOX") -> str:
    """Reply to a message"""
    # TODO: implement
    raise NotImplementedError("reply")

