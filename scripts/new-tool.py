#!/usr/bin/env python3
"""Generate a new MCP tool package from a story YAML file.

Usage:
    python scripts/new-tool.py stories/docker.yaml
    python scripts/new-tool.py stories/docker.yaml --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from textwrap import dedent, indent

import yaml


def load_story(path: Path) -> dict:
    with open(path) as f:
        story = yaml.safe_load(f)
    assert story.get("name"), "Story braucht ein 'name' Feld"
    assert story.get("description"), "Story braucht ein 'description' Feld"
    assert story.get("tools"), "Story braucht mindestens ein Tool"
    return story


def pypi_name(story: dict) -> str:
    return story.get("pypi_name", f"mcp-{story['name']}-tools")


def module_name(story: dict) -> str:
    return f"mcp_{story['name']}_tools"


def class_name_from(name: str) -> str:
    return "".join(w.capitalize() for w in name.split("_"))


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


def _param_signature(params: list[dict]) -> str:
    """Build function signature from params."""
    parts = []
    # Required params first, then optional (with defaults)
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


def _param_docstring(params: list[dict]) -> str:
    lines = []
    for p in params:
        lines.append(f"        {p['name']}: {p.get('description', '')}")
    return "\n".join(lines)


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
        # Build call to tools function
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
        if full_path.exists():
            print(f"  [SKIP] {rel_path} (exists)")
            continue
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        print(f"  [OK] {rel_path}")
        created.append(rel_path)

    return created


def main():
    parser = argparse.ArgumentParser(description="Generate MCP tool package from story")
    parser.add_argument("story", type=Path, help="Path to story YAML file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    parser.add_argument("--root", type=Path, default=None, help="Monorepo root (default: auto-detect)")
    args = parser.parse_args()

    if not args.story.exists():
        print(f"Error: {args.story} not found")
        sys.exit(1)

    root = args.root or Path(__file__).parent.parent
    story = load_story(args.story)
    name = story["name"]

    print(f"Generating: {pypi_name(story)} v{story.get('version', '1.0.0')}")
    print(f"Module:     {module_name(story)}")
    print(f"Target:     {root / name}/")
    print()

    created = generate(story, root, dry_run=args.dry_run)

    print()
    print(f"{'Would create' if args.dry_run else 'Created'} {len(created)} files.")
    if not args.dry_run:
        print(f"\nNext steps:")
        print(f"  1. Implement tools in {name}/src/{module_name(story)}/{name}/tools.py")
        print(f"  2. pip install -e {name}/")
        print(f"  3. {pypi_name(story)}  # test it")


if __name__ == "__main__":
    main()
