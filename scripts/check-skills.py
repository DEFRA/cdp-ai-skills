#!/usr/bin/env python3
"""Validate marketplace and skill layout conventions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("missing frontmatter block delimited by ---")

    fm: dict[str, str] = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        i += 1
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    else:
        raise ValueError("frontmatter block is not closed")

    return fm


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

    plugin_to_skills: dict[str, set[str]] = {}
    listed_paths: set[str] = set()
    for plugin in plugins:
        name = plugin.get("name")
        skills = plugin.get("skills")
        if not isinstance(name, str):
            errors.append("plugin name must be a string")
            continue
        if not isinstance(skills, list):
            errors.append(f"plugin '{name}' skills must be a list")
            continue
        plugin_paths: set[str] = set()
        for skill_path in skills:
            if not isinstance(skill_path, str):
                errors.append(f"plugin '{name}' has non-string skill path")
                continue
            listed_paths.add(skill_path)
            plugin_paths.add(skill_path)
            full = ROOT / skill_path.lstrip("./")
            if not full.exists():
                errors.append(f"listed skill path does not exist: {skill_path}")
                continue
            expected_prefix = f"./skills/{name}/"
            if not skill_path.startswith(expected_prefix):
                errors.append(
                    f"plugin '{name}' path must start with '{expected_prefix}': {skill_path}"
                )
        plugin_to_skills[name] = plugin_paths

    discovered_paths: set[str] = set()
    for skill_md in ROOT.glob("skills/*/*/SKILL.md"):
        owner = skill_md.parent.parent.name
        skill_name = skill_md.parent.name
        rel = "./" + skill_md.parent.relative_to(ROOT).as_posix()
        discovered_paths.add(rel)

        if owner not in plugin_to_skills:
            errors.append(f"owner '{owner}' has skill but no plugin entry: {rel}")
            continue
        if rel not in plugin_to_skills[owner]:
            errors.append(f"skill not listed in plugin '{owner}': {rel}")

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

    for listed in sorted(listed_paths - discovered_paths):
        errors.append(f"marketplace lists missing skill directory: {listed}")

    if errors:
        fail(errors)

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
