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

    catalog = ROOT / "docs" / "asset-katalog.md"
    required_asset_types = (
        "world",
        "location",
        "scene",
        "npc",
        "creature",
        "faction",
        "object",
        "information",
        "encounter",
        "plot-thread",
        "event",
        "handout",
        "visual",
        "random-table",
    )
    if not catalog.is_file():
        errors.append("missing canonical asset catalog: docs/asset-katalog.md")
    else:
        catalog_content = catalog.read_text(encoding="utf-8")
        for asset_type in required_asset_types:
            if f"| `{asset_type}` |" not in catalog_content:
                errors.append(f"asset catalog is missing type: {asset_type}")

    metadata_spec = ROOT / "docs" / "metadaten-und-werte.md"
    if not metadata_spec.is_file():
        errors.append("missing metadata specification: docs/metadaten-und-werte.md")

    agents_content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "docs/asset-katalog.md" not in agents_content:
        errors.append("AGENTS.md does not reference the canonical asset catalog")
    if "docs/metadaten-und-werte.md" not in agents_content:
        errors.append("AGENTS.md does not reference the metadata specification")

    if (ROOT / "adventures").exists():
        errors.append("legacy multi-adventure directory exists: adventures/")

    legacy_markers = ("adventures/", "--adventure")
    workflow_files = [ROOT / "README.md", ROOT / "AGENTS.md"]
    workflow_files.extend((ROOT / "docs").glob("*.md"))
    workflow_files.extend((ROOT / "scripts").glob("*.py"))
    workflow_files.extend(SKILLS.glob("*/SKILL.md"))
    for path in sorted(workflow_files):
        if path.resolve() == Path(__file__).resolve():
            continue
        content = path.read_text(encoding="utf-8")
        for marker in legacy_markers:
            if marker in content:
                errors.append(
                    f"legacy workspace marker {marker!r}: {path.relative_to(ROOT)}"
                )

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
        if "docs/asset-katalog.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill does not reference the canonical asset catalog: {skill_dir.name}")
        if "docs/metadaten-und-werte.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill does not reference the metadata specification: {skill_dir.name}")
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
