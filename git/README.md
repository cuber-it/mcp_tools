        # mcp-git-tools

        Git version control tools for MCP — status, log, diff, commit, branch, stash, remote, blame

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install mcp-git-tools
        ```

        ## Usage

        ```bash
        mcp-git-tools    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {
          "mcpServers": {
            "git": { "command": "mcp-git-tools" }
          }
        }
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        | `git_status` | Show working tree status |
| `git_log` | Show commit log |
| `git_diff` | Show changes |
| `git_blame` | Show line-by-line authorship |
| `git_add` | Stage files for commit |
| `git_commit` | Create a commit |
| `git_reset` | Unstage files |
| `git_branch_list` | List branches |
| `git_branch_create` | Create a new branch |
| `git_checkout` | Switch branch or restore files |
| `git_merge` | Merge a branch into current |
| `git_stash` | Stash working changes |
| `git_stash_list` | List stashes |
| `git_stash_pop` | Apply and drop top stash |
| `git_remote_list` | List remotes |
| `git_pull` | Pull from remote |
| `git_tag_list` | List tags |

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
