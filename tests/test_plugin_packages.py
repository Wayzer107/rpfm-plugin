"""Offline packaging checks. Run: python3 -m unittest discover -s tests -v."""

import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / ".agents/plugins/marketplace.json"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class PluginPackages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = read_json(CATALOG)["plugins"]
        cls.packages = [ROOT / entry["source"]["path"] for entry in cls.entries]

    def test_catalog_sources_are_unique_and_contained(self):
        names = [entry["name"] for entry in self.entries]
        self.assertTrue({"rpfm", "serena", "rust-analyzer-mcp"}.issubset(names))
        self.assertEqual(len(names), len(set(names)))
        for entry, package in zip(self.entries, self.packages):
            with self.subTest(plugin=entry["name"]):
                self.assertEqual(entry["source"]["source"], "local")
                self.assertTrue(package.resolve().is_relative_to(ROOT))
                self.assertTrue(package.is_dir())
                self.assertEqual(read_json(package / "plugin.json")["name"], entry["name"])

    def test_manifests_and_interfaces_stay_synchronized(self):
        for package in self.packages:
            with self.subTest(plugin=package.name):
                portable = read_json(package / "plugin.json")
                legacy = read_json(package / ".codex-plugin/plugin.json")
                for field in ("name", "version", "description", "author", "keywords", "homepage", "license"):
                    self.assertEqual(portable[field], legacy[field], field)
                self.assertEqual(portable["extensions"]["com.openai"]["interface"], legacy["interface"])
                self.assertEqual(portable["extensions"]["com.openai"]["onboardingSkill"],
                                 legacy["extensions"]["com.openai"]["onboardingSkill"])
                self.assertNotIn("skills", portable)
                self.assertNotIn("mcpServers", portable)

    def test_manifest_paths_resolve_inside_each_package(self):
        for package in self.packages:
            with self.subTest(plugin=package.name):
                manifest = read_json(package / ".codex-plugin/plugin.json")
                paths = [manifest["skills"], manifest["mcpServers"],
                         manifest["extensions"]["com.openai"]["onboardingSkill"]]
                for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
                    if manifest["interface"].get(field):
                        paths.append(manifest["interface"][field])
                for value in paths:
                    path = (package / value).resolve()
                    self.assertTrue(path.is_relative_to(package.resolve()), value)
                    self.assertTrue(path.exists(), value)

    def test_listing_constraints(self):
        for package in self.packages:
            with self.subTest(plugin=package.name):
                manifest = read_json(package / "plugin.json")
                self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
                self.assertRegex(manifest["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(manifest["name"]), 64)
                interface = manifest["extensions"]["com.openai"]["interface"]
                self.assertLessEqual(len(interface["shortDescription"]), 30)
                prompts = interface["defaultPrompt"]
                prompts = [prompts] if isinstance(prompts, str) else prompts
                self.assertTrue(1 <= len(prompts) <= 3)
                self.assertTrue(all(isinstance(prompt, str) and prompt.strip() for prompt in prompts))

    def test_mcp_configurations_stay_synchronized(self):
        for package in self.packages:
            with self.subTest(plugin=package.name):
                portable = read_json(package / "mcp.json")
                legacy = read_json(package / ".mcp.json")
                # HTTP clients may serialize omitted headers as an empty object.
                for config in (portable, legacy):
                    for server in config["mcpServers"].values():
                        if server["type"] in ("streamable-http", "sse"):
                            server.setdefault("headers", {})
                self.assertEqual(portable["mcpServers"], legacy["mcpServers"])
                self.assertTrue(portable["mcpServers"])
                for server in portable["mcpServers"].values():
                    if server["type"] == "stdio":
                        self.assertTrue(server["command"].strip())
                        self.assertTrue(all(isinstance(arg, str) for arg in server.get("args", [])))
                        self.assertNotIn("url", server)
                    else:
                        self.assertIn(server["type"], ("streamable-http", "sse"))
                        self.assertIn(urlsplit(server["url"]).scheme, ("http", "https"))

    def test_skill_names_and_descriptions(self):
        for package in self.packages:
            skills = list((package / "skills").glob("*/SKILL.md"))
            self.assertTrue(skills, package.name)
            for path in skills:
                with self.subTest(skill=str(path.relative_to(ROOT))):
                    text = path.read_text(encoding="utf-8")
                    self.assertTrue(text.startswith("---\n"))
                    frontmatter = text.split("---", 2)[1]
                    name = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
                    description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
                    self.assertIsNotNone(name)
                    self.assertEqual(name.group(1), path.parent.name)
                    self.assertIsNotNone(description)
                    self.assertTrue(description.group(1).strip())

    def test_new_documentation_local_links_resolve(self):
        paths = [ROOT / "README.md"]
        for package in self.packages:
            if package.name != "rpfm":
                paths.extend(package.rglob("*.md"))
        for path in paths:
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                target = target.strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or not parsed.path:
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), link=target):
                    destination = (path.parent / unquote(parsed.path)).resolve()
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.exists())


if __name__ == "__main__":
    unittest.main()
