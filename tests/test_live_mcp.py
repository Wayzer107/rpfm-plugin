"""Opt-in integration tests against installed local MCP runtimes.

Run with PLUGIN_MCP_INTEGRATION=1 after installing both plugin prerequisites.
Every test uses disposable code and configuration directories.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ("pub fn add(left: i32, right: i32) -> i32 {\n"
          "    left + right\n}\n\npub fn doubled(value: i32) -> i32 {\n"
          "    add(value, value)\n}\n")


@unittest.skipUnless(os.environ.get("PLUGIN_MCP_INTEGRATION") == "1",
                     "Set PLUGIN_MCP_INTEGRATION=1 to run installed MCP servers")
class LiveMcp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        missing = [name for name in ("serena", "rust-analyzer-mcp", "rust-analyzer", "cargo", "git")
                   if shutil.which(name) is None]
        if missing:
            raise unittest.SkipTest("Missing integration prerequisites: " + ", ".join(missing))

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="rpfm-plugin-mcp-test-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name) / "workspace"
        (self.workspace / "src").mkdir(parents=True)
        (self.workspace / "Cargo.toml").write_text(
            '[package]\nname = "plugin-verification-fixture"\nversion = "0.1.0"\n'
            'edition = "2021"\n\n[lib]\npath = "src/lib.rs"\n', encoding="utf-8")
        (self.workspace / "src/lib.rs").write_text(SOURCE, encoding="utf-8")
        self.environment = dict(os.environ)
        self.environment["SERENA_HOME"] = str(Path(self.temporary.name) / "serena-home")
        self.run_command(["git", "init", "--quiet", str(self.workspace)])

    def run_command(self, command):
        result = subprocess.run(command, cwd=self.workspace, env=self.environment,
                                capture_output=True, text=True, timeout=400)
        self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr[-6000:])
        return result.stdout

    def probe(self, plugin, calls):
        command = [sys.executable, str(ROOT / "scripts/check_stdio.py"),
                   str(ROOT / "plugins" / plugin), "--cwd", str(self.workspace), "--timeout", "90"]
        if plugin == "rust-analyzer-mcp":
            command.extend(["--diagnostic-attempts", "3"])
        for name, arguments in calls:
            command.extend(["--call", json.dumps({"name": name, "arguments": arguments})])
        return json.loads(self.run_command(command))

    @staticmethod
    def text(call):
        return "\n".join(item.get("text", "") for item in call["result"].get("content", []))

    def test_serena_activates_project_and_reads_symbols(self):
        self.run_command(["serena", "init"])
        config = Path(self.environment["SERENA_HOME"]) / "serena_config.yml"
        config.write_text(config.read_text(encoding="utf-8")
                          .replace("web_dashboard: true", "web_dashboard: false")
                          .replace("web_dashboard_open_on_launch: true", "web_dashboard_open_on_launch: false"),
                          encoding="utf-8")
        self.run_command(["serena", "project", "create", str(self.workspace), "--language", "rust"])
        result = self.probe("serena", [
            ("get_current_config", {}),
            ("get_symbols_overview", {"relative_path": "src/lib.rs"}),
        ])
        self.assertIn("activate_project", result["tools"])
        self.assertIn("Active context: codex", self.text(result["calls"][0]))
        self.assertIn("Language server status: ready", self.text(result["calls"][0]))
        symbols = json.loads(self.text(result["calls"][1]))
        self.assertEqual(set(symbols["Function"]), {"add", "doubled"})
        self.assertEqual((self.workspace / "src/lib.rs").read_text(encoding="utf-8"), SOURCE)

    def test_rust_analyzer_returns_semantics_and_unapplied_rename(self):
        result = self.probe("rust-analyzer-mcp", [
            ("rust_analyzer_set_workspace", {"workspace_path": str(self.workspace)}),
            ("rust_analyzer_symbols", {"file_path": "src/lib.rs"}),
            ("rust_analyzer_diagnostics", {"file_path": "src/lib.rs"}),
            ("rust_analyzer_hover", {"file_path": "src/lib.rs", "line": 0, "character": 8}),
            ("rust_analyzer_rename", {"file_path": "src/lib.rs", "line": 0, "character": 8, "new_name": "sum"}),
        ])
        symbols = json.loads(self.text(result["calls"][1]))
        self.assertEqual({symbol["name"] for symbol in symbols}, {"add", "doubled"})
        diagnostics = json.loads(self.text(result["calls"][2]))
        self.assertEqual(diagnostics["summary"]["errors"], 0)
        self.assertNotIn("note", diagnostics, "Cargo check must finish for this fixture")
        hover = json.loads(self.text(result["calls"][3]))
        self.assertIn("pub fn add(left: i32, right: i32) -> i32", hover["contents"]["value"])
        rename = json.loads(self.text(result["calls"][4]))
        self.assertFalse(rename["applied"])
        self.assertEqual(rename["summary"]["edits"], 2)
        edits = [edit for change in rename["changes"] for edit in change["edits"]]
        self.assertTrue(all(edit["new_text"] == "sum" and edit["old_text"] == "add" for edit in edits))
        self.assertEqual((self.workspace / "src/lib.rs").read_text(encoding="utf-8"), SOURCE)


if __name__ == "__main__":
    unittest.main()
