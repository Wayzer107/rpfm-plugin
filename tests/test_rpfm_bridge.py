"""Offline checks for the Claude Code RPFM stdio bridge and Codex isolation."""

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins/rpfm"
BRIDGE = PACKAGE / "scripts/rpfm_stdio_bridge.py"


def load_bridge():
    spec = importlib.util.spec_from_file_location("rpfm_stdio_bridge", BRIDGE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class RpfmBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bridge = load_bridge()

    def test_list_results_gain_required_cache_fields(self):
        for key in ("tools", "prompts", "resources", "resourceTemplates", "contents"):
            with self.subTest(key=key):
                message = self.bridge.patch({"jsonrpc": "2.0", "id": 1, "result": {key: []}})
                self.assertEqual(message["result"]["ttlMs"], 0)
                self.assertEqual(message["result"]["cacheScope"], "private")

    def test_existing_cache_fields_and_other_results_are_unchanged(self):
        kept = self.bridge.patch({"id": 1, "result": {"tools": [], "ttlMs": 5, "cacheScope": "public"}})
        self.assertEqual((kept["result"]["ttlMs"], kept["result"]["cacheScope"]), (5, "public"))
        call = {"id": 2, "result": {"content": [{"type": "text", "text": "{}"}]}}
        self.assertEqual(self.bridge.patch(json.loads(json.dumps(call))), call)
        error = {"id": 3, "error": {"code": -1, "message": "x"}}
        self.assertEqual(self.bridge.patch(dict(error)), error)

    def test_decodes_json_and_server_sent_events(self):
        sse = 'data: \nid: 0\nretry: 3000\n\ndata: {"jsonrpc":"2.0","id":1,"result":{}}\nid: 1/0\n'
        self.assertEqual(self.bridge.decode(sse, "text/event-stream"),
                         [{"jsonrpc": "2.0", "id": 1, "result": {}}])
        self.assertEqual(self.bridge.decode('{"id":1}', "application/json"), [{"id": 1}])
        self.assertEqual(self.bridge.decode("", "application/json"), [])

    def test_codex_configuration_still_uses_direct_http(self):
        codex = read_json(PACKAGE / ".codex-plugin/plugin.json")
        self.assertEqual(codex["mcpServers"], "./.mcp.json")
        for name in (".mcp.json", "mcp.json"):
            server = read_json(PACKAGE / name)["mcpServers"]["rpfm-tools"]
            self.assertEqual(server["type"], "streamable-http")
            self.assertEqual(server["url"], "http://127.0.0.1:45127/mcp")


if __name__ == "__main__":
    unittest.main()
