"""Offline structural validation / Validación estructural sin red."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = {"engineering-reliability", "engineering-review", "engineering-audit", "engineering-dependencies", "engineering-release"}

class RepositoryChecks(unittest.TestCase):
    def test_skills(self):
        paths = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual({p.parent.name for p in paths}, NAMES)
        for p in paths:
            content = p.read_text(encoding="utf-8")
            parts = content.split("---\n", 2)
            self.assertEqual(len(parts), 3, str(p))
            self.assertEqual(parts[0], "")
            self.assertIn("name: " + p.parent.name + "\n", parts[1])
            description = re.search(r"^description: (.+)$", parts[1], re.M)
            self.assertIsNotNone(description)
            self.assertLessEqual(len(description[1]), 1024)
            self.assertIn("## Español", parts[2])

    def test_state_transition_guidance(self):
        folder = ROOT / "skills" / "engineering-reliability"
        skill = (folder / "SKILL.md").read_text(encoding="utf-8")
        ref = (folder / "references" / "state-transitions.md").read_text(encoding="utf-8")
        self.assertIn("references/state-transitions.md", skill)
        self.assertIn("## Español", ref)
        for text in ("zero", "rollback", "cero", "reintento"):
            self.assertIn(text, skill + ref)

    def test_links(self):
        for p in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
                if link.startswith(("https://", "http://", "#")):
                    continue
                target = (p.parent / link.split("#")[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT) and target.exists(), f"{p}: {link}")

    def test_manifests(self):
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        for key in ("name", "version", "description"):
            self.assertEqual(claude[key], codex[key])
        self.assertEqual(claude["name"], "engineering-reliability")
        for skill in (ROOT / "skills").glob("*/SKILL.md"):
            self.assertIn('version: "' + claude["version"] + '"', skill.read_text(encoding="utf-8"))
        for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
            market = json.loads((ROOT / path).read_text(encoding="utf-8"))
            self.assertEqual(market["plugins"][0]["name"], claude["name"])

if __name__ == "__main__":
    unittest.main()
