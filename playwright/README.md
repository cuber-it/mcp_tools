        # mcp-playwright-tools

        Playwright browser automation tools for MCP — navigation, interaction, content extraction, and semantic locators

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-playwright-tools
        ```

        ## Usage

        ```bash
        mcp-playwright-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "playwright": { "command": "mcp-playwright-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `navigate` | Navigate to a URL and wait for page load |
| `current_url` | Get the current page URL |
| `go_back` | Navigate back in browser history |
| `go_forward` | Navigate forward in browser history |
| `reload` | Reload the current page |
| `get_title` | Get the current page title |
| `get_text` | Get visible text of an element |
| `get_all_texts` | Get visible text of all matching elements |
| `get_page_content` | Get all visible text on the page |
| `get_html` | Get inner HTML of an element |
| `get_links` | Get all links on the page (text + href) |
| `get_attribute` | Get an attribute value from an element |
| `click` | Click an element |
| `fill` | Fill an input field with text |
| `type_text` | Type text character by character (for autocomplete etc.) |
| `press` | Press a keyboard key (Enter, Tab, Escape, etc.) |
| `select_option` | Select a dropdown option by value |
| `select_option_by_text` | Select a dropdown option by visible text |
| `check` | Check a checkbox |
| `uncheck` | Uncheck a checkbox |
| `hover` | Hover over an element |
| `focus` | Focus an element |
| `clear` | Clear an input field |
| `screenshot` | Take a screenshot of the page |
| `screenshot_element` | Take a screenshot of a specific element |
| `wait_for` | Wait for an element to appear |
| `wait_for_hidden` | Wait for an element to disappear |
| `wait_for_url` | Wait for the URL to match a pattern |
| `set_viewport` | Set the browser viewport size |
| `scroll_to` | Scroll an element into view |
| `scroll_page` | Scroll the page up or down |
| `find_by_role` | Find element by ARIA role (button, link, textbox, heading, etc.) |
| `find_by_text` | Find element by visible text |
| `find_by_label` | Find form element by its label text |
| `find_by_placeholder` | Find input element by placeholder text |
| `find_by_test_id` | Find element by data-testid attribute |
| `click_by_role` | Click element found by ARIA role |
| `click_by_text` | Click element found by visible text |
| `fill_by_label` | Fill input found by its label text |
| `describe_element` | Get ARIA role, text, and attributes of an element |
| `find_interactive_elements` | List all clickable and fillable elements on the page |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
