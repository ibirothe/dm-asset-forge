#!/usr/bin/env python3
"""Validate repository templates and repo-scoped Codex skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
FIELD = re.compile(r"^([a-z_]+):\s*(.+)$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def metadata(path: Path) -> dict[str, str] | None:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = FIELD.match(line)
        if item:
            fields[item.group(1)] = item.group(2).strip().strip('"\'')
    return fields


def main() -> int:
    errors: list[str] = []
    names: set[str] = set()
    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        path = skill_dir / "SKILL.md"
        if not path.is_file():
            errors.append(f"missing SKILL.md: {skill_dir.relative_to(ROOT)}")
            continue
        data = metadata(path)
        if data is None:
            errors.append(f"missing frontmatter: {path.relative_to(ROOT)}")
            continue
        if set(data) != {"name", "description"}:
            errors.append(f"frontmatter must contain only name and description: {path.relative_to(ROOT)}")
        name = data.get("name", "")
        description = data.get("description", "")
        if not NAME.fullmatch(name):
            errors.append(f"invalid skill name: {name}")
        if name != skill_dir.name:
            errors.append(f"skill folder and name differ: {skill_dir.name} != {name}")
        if name in names:
            errors.append(f"duplicate skill name: {name}")
        names.add(name)
        if len(description) < 40:
            errors.append(f"skill description too short: {name}")

    required_templates = {
        "location.md",
        "npc.md",
        "object.md",
        "information.md",
        "encounter.md",
        "handout.md",
        "faction.md",
        "plot-thread.md",
        "image-brief.md",
    }
    existing_templates = {path.name for path in (ROOT / "templates" / "assets").glob("*.md")}
    for missing in sorted(required_templates - existing_templates):
        errors.append(f"missing asset template: templates/assets/{missing}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print(f"OK: {len(names)} skill(s), {len(required_templates)} asset template(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
