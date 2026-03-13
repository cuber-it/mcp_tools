"""Tests for finance tools."""

import pytest

from mcp_finance_tools.finance import register
from mcp_finance_tools.finance.client import FinanceClient


class TestImport:
    def test_register_exists(self):
        assert callable(register)

    def test_client_class_exists(self):
        assert FinanceClient is not None


class TestTools:
    def test_quote_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "quote")
        assert callable(tools.quote)

    def test_history_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "history")
        assert callable(tools.history)

    def test_compare_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "compare")
        assert callable(tools.compare)

    def test_info_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "info")
        assert callable(tools.info)

    def test_financials_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "financials")
        assert callable(tools.financials)

    def test_dividends_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "dividends")
        assert callable(tools.dividends)

    def test_holders_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "holders")
        assert callable(tools.holders)

    def test_recommendations_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "recommendations")
        assert callable(tools.recommendations)

    def test_news_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "news")
        assert callable(tools.news)

    def test_sector_performance_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "sector_performance")
        assert callable(tools.sector_performance)

    def test_market_summary_exists(self):
        from mcp_finance_tools.finance import tools
        assert hasattr(tools, "market_summary")
        assert callable(tools.market_summary)


# TODO: add functional tests
