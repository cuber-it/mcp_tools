        # mcp-finance-tools

        Financial market data tools for MCP — quotes, history, fundamentals, news

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-finance-tools
        ```

        ## Usage

        ```bash
        mcp-finance-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "finance": { "command": "mcp-finance-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `quote` | Get current quote for a ticker |
| `history` | Get price history for a ticker |
| `compare` | Compare multiple tickers |
| `info` | Get company info and key stats |
| `financials` | Get income statement, balance sheet, cash flow |
| `dividends` | Get dividend history |
| `holders` | Get major holders and institutional holders |
| `recommendations` | Get analyst recommendations |
| `news` | Get recent news for a ticker |
| `sector_performance` | Get performance by market sector |
| `market_summary` | Get major index summary (DAX, S&P500, NASDAQ, etc.) |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
