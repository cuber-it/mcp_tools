#!/usr/bin/env python3
"""Generate a new MCP tool package from a story YAML file.

Usage:
    python scripts/new-tool.py stories/docker.yaml
    python scripts/new-tool.py stories/docker.yaml --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from textwrap import dedent

import yaml


# --- Validation ---

def load_story(path: Path) -> dict:
    """Load and validate a story YAML file."""
    with open(path) as f:
        story = yaml.safe_load(f)

    errors = []
    if not story or not isinstance(story, dict):
        print("Error: Story file is empty or not a YAML dict")
        sys.exit(1)
    if not story.get("name"):
        errors.append("'name' is required")
    elif not re.match(r"^[a-z][a-z0-9_]*$", story["name"]):
        errors.append(f"'name' must be lowercase alphanumeric with underscores, got: {story['name']}")
    if not story.get("description"):
        errors.append("'description' is required")
    if not story.get("tools"):
        errors.append("at least one tool is required")
    else:
        tool_names = set()
        for i, tool in enumerate(story["tools"]):
            if not tool.get("name"):
                errors.append(f"tool[{i}] has no 'name'")
            elif tool["name"] in tool_names:
                errors.append(f"duplicate tool name: {tool['name']}")
            else:
                tool_names.add(tool["name"])
            if not tool.get("description"):
                errors.append(f"tool '{tool.get('name', i)}' has no 'description'")
            for j, p in enumerate(tool.get("params", [])):
                if not p.get("name"):
                    errors.append(f"tool '{tool.get('name', i)}' param[{j}] has no 'name'")
                if not p.get("type"):
                    errors.append(f"tool '{tool.get('name', i)}' param '{p.get('name', j)}' has no 'type'")

    if errors:
        print(f"Story validation failed ({path}):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    return story


def check_target(name: str, root: Path, force: bool = False) -> None:
    """Check if target directory already exists."""
    target = root / name
    if target.exists() and not force:
        print(f"Error: {target}/ already exists.")
        print(f"  Use --force to overwrite, or remove the directory first.")
        sys.exit(1)


# --- Helpers ---

def pypi_name(story: dict) -> str:
    return story.get("pypi_name", f"mcp-{story['name']}-tools")


def module_name(story: dict) -> str:
    return f"mcp_{story['name']}_tools"


def class_name_from(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


def _param_signature(params: list[dict]) -> str:
    """Build function signature from params."""
    parts = []
    required = [p for p in params if "default" not in p]
    optional = [p for p in params if "default" in p]
    for p in required + optional:
        typ = p.get("type", "str")
        if "default" in p:
            default = p["default"]
            if isinstance(default, str):
                default = f'"{default}"'
            elif isinstance(default, bool):
                default = str(default)
            parts.append(f"{p['name']}: {typ} = {default}")
        else:
            parts.append(f"{p['name']}: {typ}")
    return ", ".join(parts)


# --- Generators ---

def gen_pyproject(story: dict) -> str:
    name = story["name"]
    deps = ['    "mcp-server-framework>=1.3.0",']
    for dep in story.get("dependencies", []):
        deps.append(f'    "{dep}",')
    deps_str = "\n".join(deps)
    mod = module_name(story)

    return dedent(f"""\
        [project]
        name = "{pypi_name(story)}"
        version = "{story.get('version', '1.0.0')}"
        description = "{story['description']}"
        readme = "README.md"
        license = "MIT"
        requires-python = ">=3.10"
        authors = [
            {{ name = "Ulrich Berkmueller", email = "ulrich@cuber-it.de" }},
        ]
        keywords = ["mcp", "{name}", "tools"]
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ]
        dependencies = [
        {deps_str}
        ]

        [project.urls]
        Homepage = "https://github.com/cuber-it/mcp_tools"
        Repository = "https://github.com/cuber-it/mcp_tools"

        [project.scripts]
        {pypi_name(story)} = "{mod}:main"

        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [tool.hatch.build.targets.wheel]
        packages = ["src/{mod}"]
    """)


def gen_init(story: dict) -> str:
    mod = module_name(story)
    name = story["name"]
    return dedent(f'''\
        """{pypi_name(story)} — {story["description"]}

        Built on mcp-server-framework. Can also be used as a plugin via register().
        """

        __version__ = "{story.get("version", "1.0.0")}"


        def main():
            from mcp_server_framework import load_config, create_server, run_server
            from {mod}.{name} import register

            config = load_config()
            mcp = create_server(config)
            register(mcp, config)
            run_server(mcp, config)
    ''')


def gen_register(story: dict) -> str:
    name = story["name"]
    has_client = "client" in story
    client_cfg = story.get("client", {})
    client_cls = client_cfg.get("class_name", class_name_from(name) + "Client")
    config_keys = client_cfg.get("config_keys", [])

    lines = []
    lines.append(f'"""{class_name_from(name)} — MCP plugin.')
    lines.append(f"")
    lines.append(f"{story['description']}")
    if config_keys:
        lines.append(f"")
        lines.append(f"Config keys:")
        for k in config_keys:
            lines.append(f"    {k}: (required)")
    lines.append(f'"""')
    lines.append(f"")
    lines.append(f"from __future__ import annotations")
    lines.append(f"")
    if has_client:
        lines.append(f"from .client import {client_cls}")
    lines.append(f"from . import tools")
    lines.append(f"")
    lines.append(f"")
    lines.append(f"def register(mcp, config: dict) -> None:")
    lines.append(f'    """Register {name} tools as MCP tools."""')

    if has_client:
        lines.append(f"    client = {client_cls}(config)")
        lines.append(f"")

    for tool in story["tools"]:
        params = tool.get("params", [])
        sig = _param_signature(params)
        tool_name = tool["name"]
        desc = tool.get("description", tool_name)

        lines.append(f"    @mcp.tool()")
        lines.append(f"    def {tool_name}({sig}) -> str:")
        lines.append(f'        """{desc}"""')
        args = ", ".join(p["name"] for p in params)
        if has_client:
            lines.append(f"        return tools.{tool_name}(client, {args})" if args else f"        return tools.{tool_name}(client)")
        else:
            lines.append(f"        return tools.{tool_name}({args})" if args else f"        return tools.{tool_name}()")
        lines.append(f"")

    return "\n".join(lines)


def gen_tools(story: dict) -> str:
    name = story["name"]
    has_client = "client" in story
    client_cfg = story.get("client", {})
    client_cls = client_cfg.get("class_name", class_name_from(name) + "Client")

    lines = []
    lines.append(f'"""Pure tool logic for {name} — no MCP dependency."""')
    lines.append(f"")
    lines.append(f"from __future__ import annotations")
    lines.append(f"")
    if has_client:
        lines.append(f"from .client import {client_cls}")
        lines.append(f"")

    for tool in story["tools"]:
        params = tool.get("params", [])
        tool_name = tool["name"]
        desc = tool.get("description", tool_name)

        if has_client:
            all_params = f"client: {client_cls}, " + _param_signature(params) if params else f"client: {client_cls}"
        else:
            all_params = _param_signature(params)

        lines.append(f"def {tool_name}({all_params}) -> str:")
        lines.append(f'    """{desc}"""')
        lines.append(f'    # TODO: implement')
        lines.append(f'    raise NotImplementedError("{tool_name}")')
        lines.append(f"")
        lines.append(f"")

    return "\n".join(lines)


def gen_client(story: dict) -> str:
    name = story["name"]
    client_cfg = story.get("client", {})
    client_cls = client_cfg.get("class_name", class_name_from(name) + "Client")
    config_keys = client_cfg.get("config_keys", [])

    lines = []
    lines.append(f'"""{client_cls} — HTTP client for {name}."""')
    lines.append(f"")
    lines.append(f"from __future__ import annotations")
    lines.append(f"")
    lines.append(f"import httpx")
    lines.append(f"")
    lines.append(f"")
    lines.append(f"class {client_cls}:")
    lines.append(f"    def __init__(self, config: dict) -> None:")
    for key in config_keys:
        lines.append(f'        self.{key} = config["{key}"]')
    if not config_keys:
        lines.append(f"        self.config = config")
    lines.append(f"        self._client = httpx.Client()")
    lines.append(f"")
    lines.append(f"    # TODO: implement API methods")
    lines.append(f"")

    return "\n".join(lines)


def gen_readme(story: dict) -> str:
    name = story["name"]
    pname = pypi_name(story)
    tool_rows = []
    for t in story["tools"]:
        tool_rows.append(f"| `{t['name']}` | {t.get('description', '')} |")
    tools_table = "\n".join(tool_rows)

    return dedent(f"""\
        # {pname}

        {story['description']}

        Built on [mcp-server-framework](https://pypi.org/project/mcp-server-framework/).

        ## Installation

        ```bash
        pip install {pname}
        ```

        ## Usage

        ```bash
        {pname}    # stdio (default)
        ```

        ### Claude Code / Claude Desktop

        ```json
        {{
          "mcpServers": {{
            "{name}": {{ "command": "{pname}" }}
          }}
        }}
        ```

        ## Tools

        | Tool | Description |
        |------|-------------|
        {tools_table}

        ## License

        MIT — Part of [mcp_tools](https://github.com/cuber-it/mcp_tools)
    """)


def gen_test(story: dict) -> str:
    name = story["name"]
    mod = module_name(story)
    has_client = "client" in story

    lines = []
    lines.append(f'"""Tests for {name} tools."""')
    lines.append(f"")
    lines.append(f"import pytest")
    lines.append(f"")
    lines.append(f"from {mod}.{name} import register")
    if has_client:
        client_cfg = story.get("client", {})
        client_cls = client_cfg.get("class_name", class_name_from(name) + "Client")
        lines.append(f"from {mod}.{name}.client import {client_cls}")
    lines.append(f"")
    lines.append(f"")
    lines.append(f"class TestImport:")
    lines.append(f"    def test_register_exists(self):")
    lines.append(f"        assert callable(register)")
    lines.append(f"")
    if has_client:
        lines.append(f"    def test_client_class_exists(self):")
        lines.append(f"        assert {client_cls} is not None")
        lines.append(f"")
    lines.append(f"")
    lines.append(f"class TestTools:")
    for tool in story["tools"]:
        tool_name = tool["name"]
        lines.append(f"    def test_{tool_name}_exists(self):")
        lines.append(f"        from {mod}.{name} import tools")
        lines.append(f"        assert hasattr(tools, \"{tool_name}\")")
        lines.append(f"        assert callable(tools.{tool_name})")
        lines.append(f"")
    lines.append(f"")
    lines.append(f"# TODO: add functional tests")
    lines.append(f"")

    return "\n".join(lines)


def gen_test_init() -> str:
    return ""


# --- README update ---

def update_monorepo_readme(story: dict, root: Path, dry_run: bool = False) -> bool:
    """Add the new package to the monorepo README.md table."""
    readme_path = root / "README.md"
    if not readme_path.exists():
        return False

    name = story["name"]
    pname = pypi_name(story)
    tool_count = len(story["tools"])
    desc = story["description"]
    new_row = f"| [{name}]({name}/) | `{pname}` | {tool_count} | {desc} |"

    content = readme_path.read_text()

    # Check if already listed
    if f"| [{name}]" in content or f"| `{pname}`" in content:
        print(f"  [SKIP] README.md ('{name}' already listed)")
        return False

    # Find the table end (last row before a blank line after the header table)
    table_pattern = re.compile(
        r"(\| Package \| PyPI \| Tools \| Description \|\n\|[-| ]+\|\n(?:\|.*\|\n)*)"
    )
    match = table_pattern.search(content)
    if not match:
        print(f"  [SKIP] README.md (package table not found)")
        return False

    if dry_run:
        print(f"  [DRY] README.md (add row for '{name}')")
        return True

    # Insert new row at end of table
    table_end = match.end()
    updated = content[:table_end] + new_row + "\n" + content[table_end:]
    readme_path.write_text(updated)
    print(f"  [OK] README.md (added '{name}' to package table)")
    return True


# --- Main generator ---

def generate(story: dict, root: Path, dry_run: bool = False) -> list[str]:
    name = story["name"]
    mod = module_name(story)
    has_client = "client" in story

    files = {
        f"{name}/pyproject.toml": gen_pyproject(story),
        f"{name}/README.md": gen_readme(story),
        f"{name}/src/{mod}/__init__.py": gen_init(story),
        f"{name}/src/{mod}/{name}/__init__.py": gen_register(story),
        f"{name}/src/{mod}/{name}/tools.py": gen_tools(story),
        f"tests/test_{name}/__init__.py": gen_test_init(),
        f"tests/test_{name}/test_{name}.py": gen_test(story),
    }

    if has_client:
        files[f"{name}/src/{mod}/{name}/client.py"] = gen_client(story)

    created = []
    for rel_path, content in files.items():
        full_path = root / rel_path
        if dry_run:
            print(f"  [DRY] {rel_path}")
            created.append(rel_path)
            continue
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        print(f"  [OK] {rel_path}")
        created.append(rel_path)

    update_monorepo_readme(story, root, dry_run=dry_run)

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Generate MCP tool package from story YAML",
        epilog="Example: python scripts/new-tool.py stories/docker.yaml",
    )
    parser.add_argument("story", type=Path, help="Path to story YAML file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    parser.add_argument("--force", action="store_true", help="Overwrite existing package directory")
    parser.add_argument("--root", type=Path, default=None, help="Monorepo root (default: auto-detect)")
    args = parser.parse_args()

    if not args.story.exists():
        print(f"Error: {args.story} not found")
        sys.exit(1)

    root = args.root or Path(__file__).parent.parent
    story = load_story(args.story)
    name = story["name"]

    if not args.dry_run:
        check_target(name, root, force=args.force)

    tool_count = len(story["tools"])
    print(f"Generating: {pypi_name(story)} v{story.get('version', '1.0.0')} ({tool_count} tools)")
    print(f"Module:     {module_name(story)}")
    print(f"Target:     {root / name}/")
    print()

    created = generate(story, root, dry_run=args.dry_run)

    print()
    action = "Would create" if args.dry_run else "Created"
    print(f"{action} {len(created)} files.")
    if not args.dry_run:
        print(f"\nNext steps:")
        print(f"  1. Implement tools in {name}/src/{module_name(story)}/{name}/tools.py")
        if "client" in story:
            print(f"  2. Implement client in {name}/src/{module_name(story)}/{name}/client.py")
        print(f"  3. pip install -e {name}/")
        print(f"  4. {pypi_name(story)}  # test it")
        print(f"  5. pytest tests/test_{name}/  # run tests")


if __name__ == "__main__":
    main()
