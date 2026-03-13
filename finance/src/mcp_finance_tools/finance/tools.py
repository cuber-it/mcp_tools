"""Pure tool logic for finance — no MCP dependency."""

from __future__ import annotations

from .client import FinanceClient

def quote(client: FinanceClient, ticker: str) -> str:
    """Get current quote for a ticker"""
    # TODO: implement
    raise NotImplementedError("quote")


def history(client: FinanceClient, ticker: str, period: str = "1mo", interval: str = "1d") -> str:
    """Get price history for a ticker"""
    # TODO: implement
    raise NotImplementedError("history")


def compare(client: FinanceClient, tickers: str, period: str = "1mo") -> str:
    """Compare multiple tickers"""
    # TODO: implement
    raise NotImplementedError("compare")


def info(client: FinanceClient, ticker: str) -> str:
    """Get company info and key stats"""
    # TODO: implement
    raise NotImplementedError("info")


def financials(client: FinanceClient, ticker: str, statement: str = "income", quarterly: bool = False) -> str:
    """Get income statement, balance sheet, cash flow"""
    # TODO: implement
    raise NotImplementedError("financials")


def dividends(client: FinanceClient, ticker: str) -> str:
    """Get dividend history"""
    # TODO: implement
    raise NotImplementedError("dividends")


def holders(client: FinanceClient, ticker: str) -> str:
    """Get major holders and institutional holders"""
    # TODO: implement
    raise NotImplementedError("holders")


def recommendations(client: FinanceClient, ticker: str) -> str:
    """Get analyst recommendations"""
    # TODO: implement
    raise NotImplementedError("recommendations")


def news(client: FinanceClient, ticker: str) -> str:
    """Get recent news for a ticker"""
    # TODO: implement
    raise NotImplementedError("news")


def sector_performance(client: FinanceClient) -> str:
    """Get performance by market sector"""
    # TODO: implement
    raise NotImplementedError("sector_performance")


def market_summary(client: FinanceClient) -> str:
    """Get major index summary (DAX, S&P500, NASDAQ, etc.)"""
    # TODO: implement
    raise NotImplementedError("market_summary")

