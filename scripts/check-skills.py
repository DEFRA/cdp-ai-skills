#!/usr/bin/env python3
"""Validate marketplace and skill layout conventions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    if len(parts) < 3 or parts[0].strip():
        raise ValueError("missing frontmatter block delimited by ---")
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    return fm if isinstance(fm, dict) else {}


def fail(errors: list[str]) -> None:
    print("Skill validation failed:", file=sys.stderr)
    for err in errors:
        print(f"- {err}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    errors: list[str] = []

    if not MARKETPLACE.exists():
        fail([f"missing marketplace file: {MARKETPLACE}"])

    try:
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail([f"invalid marketplace JSON: {exc}"])

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        fail(["marketplace.plugins must be a list"])

    # Each owner's plugin lists its owner folder, which Claude Code scans for skills.
    plugin_names: set[str] = set()
    for plugin in plugins:
        name = plugin.get("name")
        if not isinstance(name, str):
            errors.append("plugin name must be a string")
            continue
        plugin_names.add(name)
        expected = [f"./skills/{name}/"]
        if plugin.get("skills") != expected:
            errors.append(f"plugin '{name}' skills must be {json.dumps(expected)}")
        elif not (ROOT / "skills" / name).is_dir():
            errors.append(f"plugin '{name}' has no skills folder: skills/{name}/")

    for skill_md in ROOT.glob("skills/*/*/SKILL.md"):
        owner = skill_md.parent.parent.name
        skill_name = skill_md.parent.name
        rel = "./" + skill_md.parent.relative_to(ROOT).as_posix()

        if owner not in plugin_names:
            errors.append(f"owner '{owner}' has skill but no plugin entry: {rel}")
            continue

        try:
            fm = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{skill_md.relative_to(ROOT)}: {exc}")
            continue

        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append(f"{skill_md.relative_to(ROOT)}: missing frontmatter 'name'")
        elif name != skill_name:
            errors.append(
                f"{skill_md.relative_to(ROOT)}: frontmatter name '{name}' "
                f"must match folder '{skill_name}'"
            )
        elif not NAME_RE.fullmatch(name):
            errors.append(f"{skill_md.relative_to(ROOT)}: invalid name '{name}'")

        if not desc:
            errors.append(f"{skill_md.relative_to(ROOT)}: missing frontmatter 'description'")
        elif len(desc) > 1024:
            errors.append(
                f"{skill_md.relative_to(ROOT)}: description exceeds 1024 chars "
                f"({len(desc)})"
            )

    if errors:
        fail(errors)

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
