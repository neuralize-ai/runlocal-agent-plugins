"""Check that both catalogs resolve to the same self-contained skill."""

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugin = root / "plugins/runlocal"


def read(path):
    return json.loads(path.read_text())


codex = read(plugin / ".codex-plugin/plugin.json")
claude = read(plugin / ".claude-plugin/plugin.json")
codex_entry = read(root / ".agents/plugins/marketplace.json")["plugins"][0]
claude_entry = read(root / ".claude-plugin/marketplace.json")["plugins"][0]
assert codex["name"] == claude["name"] == plugin.name
assert codex["version"] == claude["version"] == claude_entry["version"]
assert (root / codex_entry["source"]["path"]).resolve() == plugin
assert (root / claude_entry["source"]).resolve() == plugin
assert (plugin / codex["skills"]).resolve() == (plugin / claude["skills"][0]).resolve()
skills = list((plugin / codex["skills"]).glob("*/SKILL.md"))
assert len(skills) == 1
for path in plugin.rglob("*"):
    assert not path.is_symlink(), f"Plugin must not depend on external links: {path}"
    if path.is_file():
        assert "[TODO:" not in path.read_text(), f"Unfinished scaffold: {path}"
print("PASS: catalogs, versions, shared skill, self-contained package")
