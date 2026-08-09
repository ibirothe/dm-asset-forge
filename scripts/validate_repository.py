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

    authoring_guide = ROOT / "docs" / "asset-authoring-guide.md"
    if not authoring_guide.is_file():
        errors.append("missing asset authoring guide: docs/asset-authoring-guide.md")
    else:
        authoring_content = authoring_guide.read_text(encoding="utf-8")
        for asset_type in required_asset_types:
            if f"## `{asset_type}`" not in authoring_content:
                errors.append(f"asset authoring guide is missing type: {asset_type}")

    structure_guide = ROOT / "docs" / "adventure-structure-guide.md"
    required_structure_sections = (
        "## Einstieg und flexible Spieler-Hooks",
        "## Bedeutungsvolle Entscheidungen",
        "## Robuste Informationswege",
        "## Scheitern, Rückzug und Ignorieren",
        "## Notwendige Voraussetzungen und optionale Szenen",
        "## Plot-Threads und Weltdynamik",
        "## Auflösungen und offene Enden",
        "## Asset-Rollen im Verlauf",
        "## Umfang skalieren",
        "## Definition of Done",
    )
    if not structure_guide.is_file():
        errors.append("missing adventure structure guide: docs/adventure-structure-guide.md")
    else:
        structure_content = structure_guide.read_text(encoding="utf-8")
        for section in required_structure_sections:
            if section not in structure_content:
                errors.append(f"adventure structure guide is missing section: {section}")

    metadata_spec = ROOT / "docs" / "metadaten-und-werte.md"
    if not metadata_spec.is_file():
        errors.append("missing metadata specification: docs/metadaten-und-werte.md")

    relationship_spec = ROOT / "docs" / "beziehungen-und-speicherorte.md"
    if not relationship_spec.is_file():
        errors.append("missing relationship specification: docs/beziehungen-und-speicherorte.md")

    intake_spec = ROOT / "docs" / "intake-workflow.md"
    if not intake_spec.is_file():
        errors.append("missing intake workflow: docs/intake-workflow.md")

    validation_spec = ROOT / "docs" / "validierung.md"
    if not validation_spec.is_file():
        errors.append("missing validation guide: docs/validierung.md")

    agents_content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "docs/asset-katalog.md" not in agents_content:
        errors.append("AGENTS.md does not reference the canonical asset catalog")
    if "docs/asset-authoring-guide.md" not in agents_content:
        errors.append("AGENTS.md does not reference the asset authoring guide")
    if "docs/adventure-structure-guide.md" not in agents_content:
        errors.append("AGENTS.md does not reference the adventure structure guide")
    if "docs/metadaten-und-werte.md" not in agents_content:
        errors.append("AGENTS.md does not reference the metadata specification")
    if "docs/beziehungen-und-speicherorte.md" not in agents_content:
        errors.append("AGENTS.md does not reference the relationship specification")
    if "docs/intake-workflow.md" not in agents_content:
        errors.append("AGENTS.md does not reference the intake workflow")
    if "docs/validierung.md" not in agents_content:
        errors.append("AGENTS.md does not reference the validation guide")

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
        if "docs/asset-authoring-guide.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill does not reference the asset authoring guide: {skill_dir.name}")
        if "docs/adventure-structure-guide.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill does not reference the adventure structure guide: {skill_dir.name}")
        if "docs/metadaten-und-werte.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill does not reference the metadata specification: {skill_dir.name}")
        if "docs/beziehungen-und-speicherorte.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"skill does not reference the relationship specification: {skill_dir.name}")
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

    create_adventure_skill = SKILLS / "dm-create-adventure" / "SKILL.md"
    if create_adventure_skill.is_file() and "docs/intake-workflow.md" not in create_adventure_skill.read_text(encoding="utf-8"):
        errors.append("dm-create-adventure does not reference the intake workflow")

    audit_skill = SKILLS / "dm-audit-adventure" / "SKILL.md"
    if audit_skill.is_file() and "docs/validierung.md" not in audit_skill.read_text(encoding="utf-8"):
        errors.append("dm-audit-adventure does not reference the validation guide")

    validator_tests = ROOT / "tests" / "test_validate_adventure.py"
    if not validator_tests.is_file():
        errors.append("missing validator regression tests: tests/test_validate_adventure.py")

    required_templates = {f"{asset_type}.md" for asset_type in required_asset_types}
    existing_templates = {path.name for path in (ROOT / "templates" / "assets").glob("*.md")}
    for missing in sorted(required_templates - existing_templates):
        errors.append(f"missing asset template: templates/assets/{missing}")
    unexpected_templates = existing_templates - required_templates
    for unexpected in sorted(unexpected_templates):
        errors.append(f"unexpected asset template: templates/assets/{unexpected}")

    if not (ROOT / "templates" / "visual-prompt.md").is_file():
        errors.append("missing visual prompt template: templates/visual-prompt.md")

    plot_overview = ROOT / "templates" / "adventure" / "20-plot" / "overview.md"
    required_plot_sections = (
        "## Inciting situation",
        "## Flexible player hooks",
        "## Decision landscape",
        "## Information paths",
        "## Failure, retreat, and neglect",
        "## Possible outcomes",
        "## Scope and pacing",
    )
    if not plot_overview.is_file():
        errors.append("missing plot overview template: templates/adventure/20-plot/overview.md")
    else:
        plot_content = plot_overview.read_text(encoding="utf-8")
        for section in required_plot_sections:
            if section not in plot_content:
                errors.append(f"plot overview template is missing section: {section}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print(f"OK: {len(names)} skill(s), {len(required_templates)} asset template(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
