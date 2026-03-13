"""Finance — MCP plugin.

Financial market data tools for MCP — quotes, history, fundamentals, news
"""

from __future__ import annotations

from .client import FinanceClient
from . import tools


def register(mcp, config: dict) -> None:
    """Register finance tools as MCP tools."""
    client = FinanceClient(config)

    @mcp.tool()
    def quote(ticker: str) -> str:
        """Get current quote for a ticker"""
        return tools.quote(client, ticker)

    @mcp.tool()
    def history(ticker: str, period: str = "1mo", interval: str = "1d") -> str:
        """Get price history for a ticker"""
        return tools.history(client, ticker, period, interval)

    @mcp.tool()
    def compare(tickers: str, period: str = "1mo") -> str:
        """Compare multiple tickers"""
        return tools.compare(client, tickers, period)

    @mcp.tool()
    def info(ticker: str) -> str:
        """Get company info and key stats"""
        return tools.info(client, ticker)

    @mcp.tool()
    def financials(ticker: str, statement: str = "income", quarterly: bool = False) -> str:
        """Get income statement, balance sheet, cash flow"""
        return tools.financials(client, ticker, statement, quarterly)

    @mcp.tool()
    def dividends(ticker: str) -> str:
        """Get dividend history"""
        return tools.dividends(client, ticker)

    @mcp.tool()
    def holders(ticker: str) -> str:
        """Get major holders and institutional holders"""
        return tools.holders(client, ticker)

    @mcp.tool()
    def recommendations(ticker: str) -> str:
        """Get analyst recommendations"""
        return tools.recommendations(client, ticker)

    @mcp.tool()
    def news(ticker: str) -> str:
        """Get recent news for a ticker"""
        return tools.news(client, ticker)

    @mcp.tool()
    def sector_performance() -> str:
        """Get performance by market sector"""
        return tools.sector_performance(client)

    @mcp.tool()
    def market_summary() -> str:
        """Get major index summary (DAX, S&P500, NASDAQ, etc.)"""
        return tools.market_summary(client)
