#!/usr/bin/env python3
"""MCP Tool Test Client — interactive GUI for testing MCP tool packages.

Loads tool packages via register() and lets you call tools interactively.
No MCP server, no LLM, no HTTP — just direct Python function calls.

Usage:
    python tools/testclient.py
    python tools/testclient.py --load mcp_onyx_tools.onyx
"""

from __future__ import annotations

import argparse
import asyncio
import importlib
import inspect
import json
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path
from datetime import datetime


class ToolCollector:
    """Fake MCP that collects tool registrations from register()."""

    def __init__(self):
        self.tools: dict[str, dict] = {}

    def tool(self, **kwargs):
        def decorator(fn):
            name = fn.__name__
            sig = inspect.signature(fn)
            params = []
            for pname, param in sig.parameters.items():
                p = {"name": pname}
                if param.annotation != inspect.Parameter.empty:
                    p["type"] = param.annotation.__name__ if hasattr(param.annotation, "__name__") else str(param.annotation)
                else:
                    p["type"] = "str"
                if param.default != inspect.Parameter.empty:
                    p["default"] = param.default
                params.append(p)
            self.tools[name] = {
                "name": name,
                "description": fn.__doc__ or "",
                "params": params,
                "handler": fn,
                "is_async": asyncio.iscoroutinefunction(fn),
            }
            return fn
        return decorator


class ToolTestClient:
    """Tk GUI for testing MCP tools."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("MCP Tool Test Client")
        self.root.geometry("1100x750")

        self.plugins: dict[str, dict] = {}  # key = module_path
        self.all_tools: dict[str, dict] = {}
        self.selected_tool = None
        self.param_widgets: dict[str, tk.Widget] = {}
        self._logging_enabled = False
        self._log_file = None

        self._dark_mode = True
        self._setup_styles(dark=True)
        self._build_menu()
        self._build_ui()
        self._apply_theme()

    def _setup_styles(self, dark: bool = True):
        self._dark_mode = dark
        style = ttk.Style()
        style.theme_use("clam")

        if dark:
            bg, bg2, bg3 = "#1a1a2e", "#12121a", "#2a2a3e"
            fg, accent = "#e0e0e0", "#f59e0b"
        else:
            bg, bg2, bg3 = "#f5f5f5", "#ffffff", "#e0e0e0"
            fg, accent = "#1a1a1a", "#b47208"

        self._colors = {"bg": bg, "bg2": bg2, "bg3": bg3,
                        "fg": fg, "accent": accent}

        style.configure("Dark.TFrame", background=bg)
        style.configure("Dark.TLabel", background=bg, foreground=fg, font=("Monospace", 10))
        style.configure("Title.TLabel", background=bg, foreground=accent, font=("Monospace", 11, "bold"))
        style.configure("Dark.TButton", background=bg3, foreground=fg, font=("Monospace", 10))
        style.configure("Run.TButton", background=accent, foreground="#000" if dark else "#fff", font=("Monospace", 10, "bold"))
        style.configure("Dark.TEntry", fieldbackground=bg2, foreground=fg, font=("Monospace", 10))
        style.configure("Dark.Treeview", background=bg2, foreground=fg, fieldbackground=bg2, font=("Monospace", 10))
        style.configure("Dark.Treeview.Heading", background=bg3, foreground=accent, font=("Monospace", 10, "bold"))
        style.map("Dark.Treeview", background=[("selected", bg3)])

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Plugin...", command=self._load_from_entry)
        file_menu.add_command(label="Browse Toolsets...", command=self._browse_toolsets)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        self._theme_var = tk.StringVar(value="Dark")
        view_menu.add_radiobutton(label="Dark Mode", variable=self._theme_var,
                                  value="Dark", command=lambda: self._set_theme(True))
        view_menu.add_radiobutton(label="Light Mode", variable=self._theme_var,
                                  value="Light", command=lambda: self._set_theme(False))
        menubar.add_cascade(label="View", menu=view_menu)

        # Logging menu
        log_menu = tk.Menu(menubar, tearoff=0)
        self._log_var = tk.BooleanVar(value=False)
        log_menu.add_checkbutton(label="Enable Logging", variable=self._log_var,
                                 command=self._toggle_logging)
        log_menu.add_command(label="Set Log File...", command=self._set_log_file)
        menubar.add_cascade(label="Logging", menu=log_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def _build_ui(self):
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # LEFT: Tool tree
        left = ttk.Frame(paned, style="Dark.TFrame", width=350)
        paned.add(left, weight=1)

        ttk.Label(left, text="TOOLS", style="Title.TLabel").pack(anchor="w", padx=8, pady=(8, 4))

        # Load row
        btn_frame = ttk.Frame(left, style="Dark.TFrame")
        btn_frame.pack(fill=tk.X, padx=8, pady=4)

        self.load_entry = ttk.Entry(btn_frame, style="Dark.TEntry", width=25)
        self.load_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.load_entry.insert(0, "mcp_onyx_tools.onyx")

        ttk.Button(btn_frame, text="Load", style="Dark.TButton",
                   command=self._load_from_entry).pack(side=tk.LEFT, padx=(4, 0))
        ttk.Button(btn_frame, text="Browse", style="Dark.TButton",
                   command=self._browse_toolsets).pack(side=tk.LEFT, padx=(4, 0))

        # Tree
        self.tree = ttk.Treeview(left, style="Dark.Treeview", show="tree", selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
        self.tree.bind("<<TreeviewSelect>>", self._on_tool_select)

        # RIGHT
        right = ttk.Frame(paned, style="Dark.TFrame")
        paned.add(right, weight=2)

        # Tool info
        info_frame = ttk.Frame(right, style="Dark.TFrame")
        info_frame.pack(fill=tk.X, padx=8, pady=(8, 0))

        self.tool_name_label = ttk.Label(info_frame, text="Select a tool",
                                         style="Title.TLabel", font=("Monospace", 14, "bold"))
        self.tool_name_label.pack(anchor="w")

        self.tool_desc_label = ttk.Label(info_frame, text="", style="Dark.TLabel", wraplength=600)
        self.tool_desc_label.pack(anchor="w", pady=(4, 8))

        # Params
        self.params_frame = ttk.Frame(right, style="Dark.TFrame")
        self.params_frame.pack(fill=tk.X, padx=8)

        # Run
        self.run_btn = ttk.Button(right, text="Run", style="Run.TButton",
                                  command=self._run_tool, state=tk.DISABLED)
        self.run_btn.pack(anchor="w", padx=8, pady=8)

        # Output
        ttk.Label(right, text="OUTPUT", style="Title.TLabel").pack(anchor="w", padx=8)

        self.output = scrolledtext.ScrolledText(right, wrap=tk.WORD, height=20,
                                                font=("Monospace", 10), borderwidth=1, relief="solid")
        self.output.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 8))

        # REPL
        repl_frame = ttk.Frame(right, style="Dark.TFrame")
        repl_frame.pack(fill=tk.X, padx=8, pady=(0, 8))

        ttk.Label(repl_frame, text=">", style="Title.TLabel").pack(side=tk.LEFT)
        self.repl_entry = ttk.Entry(repl_frame, style="Dark.TEntry")
        self.repl_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        self.repl_entry.bind("<Return>", self._on_repl_enter)

    # --- Theme ---

    def _set_theme(self, dark: bool):
        self._setup_styles(dark=dark)
        self._apply_theme()

    def _apply_theme(self):
        c = self._colors
        self.root.configure(bg=c["bg"])
        self.output.configure(bg=c["bg2"], fg=c["fg"], insertbackground=c["accent"])

    # --- Logging ---

    def _toggle_logging(self):
        self._logging_enabled = self._log_var.get()
        if self._logging_enabled and not self._log_file:
            self._set_log_file()
        if self._logging_enabled and self._log_file:
            self._log(f"[Logging enabled → {self._log_file}]")
        elif not self._logging_enabled:
            self._log("[Logging disabled]")

    def _set_log_file(self):
        default = f"testclient_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        path = filedialog.asksaveasfilename(
            title="Log file",
            initialfile=default,
            defaultextension=".jsonl",
            filetypes=[("JSONL", "*.jsonl"), ("All", "*.*")],
        )
        if path:
            self._log_file = path
            self._log(f"[Log file set: {path}]")

    def _write_log(self, entry: dict):
        if not self._logging_enabled or not self._log_file:
            return
        entry["timestamp"] = datetime.now().isoformat()
        with open(self._log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

    # --- Plugin Loading ---

    def load_plugin(self, module_path: str, config: dict | None = None):
        """Load a tool plugin. Prevents duplicates by module_path."""
        if module_path in self.plugins:
            self._log(f"Already loaded: {module_path}")
            return

        try:
            module = importlib.import_module(module_path)
            if not hasattr(module, "register"):
                self._log(f"Error: {module_path} has no register() function")
                return

            collector = ToolCollector()
            module.register(collector, config or {})

            plugin_name = module_path.split(".")[-1]
            self.plugins[module_path] = {
                "name": plugin_name,
                "tools": collector.tools,
                "module_path": module_path,
            }
            self.all_tools.update(collector.tools)

            # Tree: show name + path
            display = f"{plugin_name} ({len(collector.tools)}) — {module_path}"
            node = self.tree.insert("", "end", text=display, open=True)
            for name in sorted(collector.tools.keys()):
                self.tree.insert(node, "end", text=name)

            self._log(f"Loaded: {module_path} — {len(collector.tools)} tools")
            self._write_log({"event": "load", "module": module_path, "tools": len(collector.tools)})
        except Exception as e:
            self._log(f"Error loading {module_path}: {e}")

    def _load_from_entry(self):
        module_path = self.load_entry.get().strip()
        if module_path:
            self.load_plugin(module_path)

    # --- Browse ---

    def _scan_directory(self, base: Path) -> list[dict]:
        """Scan a directory for valid toolsets."""
        toolsets = []
        for init_file in base.rglob("__init__.py"):
            try:
                content = init_file.read_text(encoding="utf-8")
            except Exception:
                continue
            if "def register(" not in content:
                continue
            inner = init_file.parent
            mod_parent = inner.parent
            if not (mod_parent / "__init__.py").exists():
                continue
            module_path = f"{mod_parent.name}.{inner.name}"
            tool_count = content.count("@mcp.tool()")
            toolsets.append({
                "name": inner.name,
                "module": module_path,
                "tools": tool_count,
                "path": str(inner),
            })
        return toolsets

    def _browse_toolsets(self):
        default_dir = str(Path(__file__).parent.parent)
        scan_dir = filedialog.askdirectory(title="Select directory to scan", initialdir=default_dir)
        if not scan_dir:
            return

        toolsets = self._scan_directory(Path(scan_dir))
        if not toolsets:
            messagebox.showinfo("Browse", f"No valid toolsets found in {scan_dir}")
            return

        dlg = tk.Toplevel(self.root)
        dlg.title("Available Toolsets")
        dlg.geometry("600x400")
        dlg.configure(bg=self._colors["bg"])
        dlg.transient(self.root)
        dlg.grab_set()

        ttk.Label(dlg, text="AVAILABLE TOOLSETS", style="Title.TLabel").pack(anchor="w", padx=12, pady=(12, 4))
        ttk.Label(dlg, text="Double-click to load", style="Dark.TLabel").pack(anchor="w", padx=12, pady=(0, 8))

        columns = ("name", "module", "tools", "path")
        tree = ttk.Treeview(dlg, columns=columns, show="headings", style="Dark.Treeview", selectmode="browse")
        tree.heading("name", text="Name")
        tree.heading("module", text="Module")
        tree.heading("tools", text="Tools")
        tree.heading("path", text="Path")
        tree.column("name", width=80)
        tree.column("module", width=200)
        tree.column("tools", width=50, anchor="center")
        tree.column("path", width=250)
        tree.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        for ts in toolsets:
            loaded = " *" if ts["module"] in self.plugins else ""
            tree.insert("", "end", values=(ts["name"] + loaded, ts["module"], ts["tools"], ts["path"]))

        def _load(event=None):
            sel = tree.selection()
            if sel:
                module_path = tree.item(sel[0])["values"][1]
                self.load_entry.delete(0, tk.END)
                self.load_entry.insert(0, module_path)
                dlg.destroy()
                self.load_plugin(module_path)

        tree.bind("<Double-1>", _load)

        btn_frame = ttk.Frame(dlg, style="Dark.TFrame")
        btn_frame.pack(fill=tk.X, padx=12, pady=(4, 12))
        ttk.Button(btn_frame, text="Load", style="Run.TButton", command=_load).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", style="Dark.TButton", command=dlg.destroy).pack(side=tk.LEFT, padx=(8, 0))

    # --- Tool Selection & Execution ---

    def _on_tool_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        name = self.tree.item(sel[0])["text"]
        if name in self.all_tools:
            self._show_tool(name)

    def _show_tool(self, name: str):
        tool = self.all_tools[name]
        self.selected_tool = tool
        self.tool_name_label.config(text=name)
        self.tool_desc_label.config(text=tool["description"])
        self.run_btn.config(state=tk.NORMAL)

        for w in self.params_frame.winfo_children():
            w.destroy()
        self.param_widgets.clear()

        for p in tool["params"]:
            row = ttk.Frame(self.params_frame, style="Dark.TFrame")
            row.pack(fill=tk.X, pady=2)
            default_str = f" = {p['default']}" if "default" in p else ""
            ttk.Label(row, text=f"{p['name']} ({p['type']}{default_str})",
                      style="Dark.TLabel", width=35, anchor="w").pack(side=tk.LEFT)
            entry = ttk.Entry(row, style="Dark.TEntry", width=40)
            if "default" in p and p["default"] != "":
                entry.insert(0, str(p["default"]))
            entry.pack(side=tk.LEFT, padx=(4, 0))
            self.param_widgets[p["name"]] = entry

    def _run_tool(self):
        if not self.selected_tool:
            return
        tool = self.selected_tool
        kwargs = self._collect_params(tool)

        call_str = f"{tool['name']}({', '.join(f'{k}={repr(v)}' for k, v in kwargs.items())})"
        self._log(f"\n> {call_str}")

        try:
            start = datetime.now()
            if tool["is_async"]:
                result = asyncio.get_event_loop().run_until_complete(tool["handler"](**kwargs))
            else:
                result = tool["handler"](**kwargs)
            duration = (datetime.now() - start).total_seconds()
            self._log(str(result))
            self._write_log({"event": "call", "tool": tool["name"], "params": kwargs,
                             "result": str(result)[:500], "duration_s": round(duration, 3)})
        except Exception as e:
            self._log(f"Error: {e}")
            self._write_log({"event": "error", "tool": tool["name"], "params": kwargs, "error": str(e)})

    def _collect_params(self, tool: dict) -> dict:
        kwargs = {}
        for p in tool["params"]:
            widget = self.param_widgets.get(p["name"])
            if not widget:
                continue
            val = widget.get().strip()
            if not val and "default" in p:
                continue
            if not val:
                continue
            ptype = p.get("type", "str")
            try:
                if ptype == "int":
                    val = int(val)
                elif ptype == "bool":
                    val = val.lower() in ("true", "1", "yes")
                elif ptype == "float":
                    val = float(val)
            except ValueError:
                pass
            kwargs[p["name"]] = val
        return kwargs

    # --- REPL ---

    def _on_repl_enter(self, event):
        line = self.repl_entry.get().strip()
        self.repl_entry.delete(0, tk.END)
        if not line:
            return
        self._log(f"\n> {line}")

        if "(" in line:
            name = line[:line.index("(")].strip()
            args_str = line[line.index("(") + 1:line.rindex(")")].strip()
        else:
            name = line
            args_str = ""

        if name == "tools":
            self._log("\n".join(sorted(self.all_tools.keys())))
            return
        elif name == "help" and args_str:
            tool = self.all_tools.get(args_str.strip())
            if tool:
                self._log(f"{tool['name']}: {tool['description']}")
                for p in tool["params"]:
                    d = f" = {p['default']}" if "default" in p else " (required)"
                    self._log(f"  {p['name']}: {p['type']}{d}")
            else:
                self._log(f"Unknown tool: {args_str}")
            return
        elif name == "quit":
            self.root.quit()
            return

        tool = self.all_tools.get(name)
        if not tool:
            self._log(f"Unknown: {name}. Type 'tools' for list.")
            return

        kwargs = {}
        if args_str:
            for arg in self._split_args(args_str):
                arg = arg.strip()
                if "=" in arg:
                    k, v = arg.split("=", 1)
                    kwargs[k.strip()] = self._parse_value(v.strip())
                else:
                    for p in tool["params"]:
                        if p["name"] not in kwargs:
                            kwargs[p["name"]] = self._parse_value(arg)
                            break

        try:
            start = datetime.now()
            if tool["is_async"]:
                result = asyncio.get_event_loop().run_until_complete(tool["handler"](**kwargs))
            else:
                result = tool["handler"](**kwargs)
            duration = (datetime.now() - start).total_seconds()
            self._log(str(result))
            self._write_log({"event": "call", "tool": name, "params": kwargs,
                             "result": str(result)[:500], "duration_s": round(duration, 3)})
        except Exception as e:
            self._log(f"Error: {e}")
            self._write_log({"event": "error", "tool": name, "params": kwargs, "error": str(e)})

    def _split_args(self, s: str) -> list[str]:
        args, current, in_q, qc = [], "", False, None
        for c in s:
            if c in ('"', "'") and not in_q:
                in_q, qc = True, c
            elif c == qc and in_q:
                in_q, qc = False, None
            elif c == "," and not in_q:
                args.append(current); current = ""; continue
            else:
                current += c
        if current:
            args.append(current)
        return args

    def _parse_value(self, v: str):
        v = v.strip().strip('"').strip("'")
        if v.lower() in ("true", "false"):
            return v.lower() == "true"
        try:
            return int(v)
        except ValueError:
            pass
        try:
            return float(v)
        except ValueError:
            pass
        return v

    # --- Helpers ---

    def _log(self, text: str):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def _show_about(self):
        messagebox.showinfo("About", (
            "MCP Tool Test Client\n\n"
            "Loads MCP tool packages and lets you call them interactively.\n\n"
            f"Loaded plugins: {len(self.plugins)}\n"
            f"Total tools: {len(self.all_tools)}\n\n"
            "Part of mcp_tools by Ulrich Cuber"
        ))


def main():
    parser = argparse.ArgumentParser(description="MCP Tool Test Client")
    parser.add_argument("--load", action="append", default=[],
                        help="Plugin module to load (e.g. mcp_onyx_tools.onyx)")
    parser.add_argument("--config", type=str, default="", help="Config YAML path")
    args = parser.parse_args()

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    root = tk.Tk()
    app = ToolTestClient(root)

    config = {}
    if args.config:
        import yaml
        with open(args.config) as f:
            config = yaml.safe_load(f) or {}

    for module_path in args.load:
        app.load_plugin(module_path, config)

    app._log("MCP Tool Test Client ready.")
    app._log("Type 'tools' for list, 'help <tool>' for details.")
    app._log("Use the tree on the left to browse and run tools.\n")

    root.mainloop()


if __name__ == "__main__":
    main()
