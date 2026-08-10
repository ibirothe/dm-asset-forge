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
SKILL_REFERENCE_REQUIREMENTS = {
    "dm-audit-adventure": (
        "docs/adventure-audit-guide.md",
        "docs/validierung.md",
    ),
    "dm-create-adventure": (
        "docs/intake-workflow.md",
        "docs/adventure-structure-guide.md",
        "docs/player-character-workflow.md",
    ),
    "dm-create-asset": (
        "docs/asset-katalog.md",
        "docs/asset-authoring-guide.md",
        "docs/player-character-workflow.md",
    ),
    "dm-develop-location": (
        "docs/asset-katalog.md",
        "docs/asset-authoring-guide.md",
    ),
}


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
        "player-character",
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
        "## One-Shot-Umfang begrenzen",
        "## Pacing und sichere Kürzbarkeit",
        "## Definition of Done",
    )
    if not structure_guide.is_file():
        errors.append("missing adventure structure guide: docs/adventure-structure-guide.md")
    else:
        structure_content = structure_guide.read_text(encoding="utf-8")
        for section in required_structure_sections:
            if section not in structure_content:
                errors.append(f"adventure structure guide is missing section: {section}")

    audit_guide = ROOT / "docs" / "adventure-audit-guide.md"
    required_audit_sections = (
        "## Prüfreihenfolge",
        "## Technische Basisprüfung",
        "## Kanon und Kontinuität",
        "## Informationswege",
        "## Plot-Threads und Spielerwirksamkeit",
        "## Spielerausgaben und Visuals",
        "## Pacing und sichere Kürzbarkeit",
        "## Übersichten und Navigationswege",
        "## Tischreife",
        "## Schweregrade",
        "## Format eines Findings",
        "## Audit-Bericht",
        "## Fix-Aufträge",
        "## Definition of Done",
    )
    if not audit_guide.is_file():
        errors.append("missing adventure audit guide: docs/adventure-audit-guide.md")
    else:
        audit_content = audit_guide.read_text(encoding="utf-8")
        for section in required_audit_sections:
            if section not in audit_content:
                errors.append(f"adventure audit guide is missing section: {section}")

    metadata_spec = ROOT / "docs" / "metadaten-und-werte.md"
    if not metadata_spec.is_file():
        errors.append("missing metadata specification: docs/metadaten-und-werte.md")

    relationship_spec = ROOT / "docs" / "beziehungen-und-speicherorte.md"
    if not relationship_spec.is_file():
        errors.append("missing relationship specification: docs/beziehungen-und-speicherorte.md")
    else:
        relationship_content = relationship_spec.read_text(encoding="utf-8")
        for section in (
            "### Gemeinsamer Preflight",
            "### Titel ändern",
            "### Dauerhafte Änderung der Ownership",
            "### Asset retiren",
            "### Assets zusammenführen",
        ):
            if section not in relationship_content:
                errors.append(f"relationship specification is missing lifecycle section: {section}")

    intake_spec = ROOT / "docs" / "intake-workflow.md"
    if not intake_spec.is_file():
        errors.append("missing intake workflow: docs/intake-workflow.md")
    else:
        intake_content = intake_spec.read_text(encoding="utf-8")
        for unsupported_path in (
            "10-world/themes.md",
            "10-world/timeline.md",
        ):
            if unsupported_path in intake_content:
                errors.append(
                    "intake workflow requires a file absent from the adventure scaffold: "
                    f"{unsupported_path}"
                )
        for canonical_target in (
            "00-input/constraints.md",
            "scripts/new_asset.py --type event",
        ):
            if canonical_target not in intake_content:
                errors.append(
                    "intake workflow does not name the minimal canonical target: "
                    f"{canonical_target}"
                )

    validation_spec = ROOT / "docs" / "validierung.md"
    if not validation_spec.is_file():
        errors.append("missing validation guide: docs/validierung.md")

    player_handout_guide = ROOT / "docs" / "player-handout-workflow.md"
    required_player_handout_sections = (
        "## Dateimodell",
        "## Freigabestatus in der Quelle",
        "## Freigabeworkflow",
        "## Safety-Check",
        "## Optionale PNG-Ausgabe",
        "## Definition of Done",
    )
    if not player_handout_guide.is_file():
        errors.append("missing player Handout workflow: docs/player-handout-workflow.md")
    else:
        player_handout_content = player_handout_guide.read_text(encoding="utf-8")
        for section in required_player_handout_sections:
            if section not in player_handout_content:
                errors.append(f"player Handout workflow is missing section: {section}")

    player_character_guide = ROOT / "docs" / "player-character-workflow.md"
    required_player_character_sections = (
        "## Dateimodell",
        "## Fachliche Grenzen",
        "## Freigabestatus in der Quelle",
        "## Freigabeworkflow",
        "## Safety-Check",
        "## Visuals",
        "## Definition of Done",
    )
    if not player_character_guide.is_file():
        errors.append("missing Player Character workflow: docs/player-character-workflow.md")
    else:
        player_character_content = player_character_guide.read_text(encoding="utf-8")
        for section in required_player_character_sections:
            if section not in player_character_content:
                errors.append(f"Player Character workflow is missing section: {section}")

    image_workflow = ROOT / "docs" / "bild-workflow.md"
    required_image_workflow_sections = (
        "## Dateimodell",
        "## Kanonische Identitätsquelle",
        "## Zustandsvarianten im One-Shot",
        "## Reproduzierbares Briefing",
        "## PNG-Status",
        "## Freigabe und Erzeugung",
        "## Definition of Done",
    )
    if not image_workflow.is_file():
        errors.append("missing image workflow: docs/bild-workflow.md")
    else:
        image_workflow_content = image_workflow.read_text(encoding="utf-8")
        for section in required_image_workflow_sections:
            if section not in image_workflow_content:
                errors.append(f"image workflow is missing section: {section}")

    agents_content = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "docs/asset-katalog.md" not in agents_content:
        errors.append("AGENTS.md does not reference the canonical asset catalog")
    if "docs/asset-authoring-guide.md" not in agents_content:
        errors.append("AGENTS.md does not reference the asset authoring guide")
    if "docs/adventure-structure-guide.md" not in agents_content:
        errors.append("AGENTS.md does not reference the adventure structure guide")
    if "docs/adventure-audit-guide.md" not in agents_content:
        errors.append("AGENTS.md does not reference the adventure audit guide")
    if "docs/metadaten-und-werte.md" not in agents_content:
        errors.append("AGENTS.md does not reference the metadata specification")
    if "docs/beziehungen-und-speicherorte.md" not in agents_content:
        errors.append("AGENTS.md does not reference the relationship specification")
    if "docs/intake-workflow.md" not in agents_content:
        errors.append("AGENTS.md does not reference the intake workflow")
    if "docs/validierung.md" not in agents_content:
        errors.append("AGENTS.md does not reference the validation guide")
    if "docs/player-handout-workflow.md" not in agents_content:
        errors.append("AGENTS.md does not reference the player Handout workflow")
    if "docs/player-character-workflow.md" not in agents_content:
        errors.append("AGENTS.md does not reference the Player Character workflow")
    if "docs/bild-workflow.md" not in agents_content:
        errors.append("AGENTS.md does not reference the image workflow")

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

    one_shot_files = (
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "docs" / "intake-workflow.md",
        ROOT / "docs" / "adventure-structure-guide.md",
        SKILLS / "dm-create-adventure" / "SKILL.md",
    )
    for path in one_shot_files:
        if "one-shot" not in path.read_text(encoding="utf-8").lower():
            errors.append(f"one-shot scope is not explicit: {path.relative_to(ROOT)}")

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
        content = path.read_text(encoding="utf-8")
        references = SKILL_REFERENCE_REQUIREMENTS.get(name)
        if references is None:
            errors.append(f"missing skill-specific reference policy: {name}")
        else:
            for reference in references:
                if reference not in content:
                    errors.append(f"skill {name} does not reference required guide: {reference}")

    for missing_skill in sorted(SKILL_REFERENCE_REQUIREMENTS.keys() - names):
        errors.append(f"configured skill is missing: {missing_skill}")

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
    else:
        visual_prompt_content = (ROOT / "templates" / "visual-prompt.md").read_text(encoding="utf-8")
        for section in (
            "## Identity anchors",
            "## Depicted state",
            "## Allowed variation",
            "## Canon checks",
        ):
            if section not in visual_prompt_content:
                errors.append(f"visual prompt template is missing section: {section}")
    if not (ROOT / "templates" / "player-handout.md").is_file():
        errors.append("missing player Handout template: templates/player-handout.md")
    if not (ROOT / "templates" / "player-character-player.md").is_file():
        errors.append("missing Player Character player template: templates/player-character-player.md")

    session_preflight = ROOT / "templates" / "adventure" / "00-input" / "session-preflight.md"
    required_preflight_sections = (
        "## Group and rules",
        "## Schedule",
        "## Safety and accessibility",
        "## Table and technology",
        "## Materials",
        "## Player releases",
        "## Open blockers",
        "## Ready for session",
    )
    if not session_preflight.is_file():
        errors.append("missing session preflight template: templates/adventure/00-input/session-preflight.md")
    else:
        preflight_content = session_preflight.read_text(encoding="utf-8")
        for section in required_preflight_sections:
            if section not in preflight_content:
                errors.append(f"session preflight template is missing section: {section}")

    dm_cheat_sheet = ROOT / "templates" / "adventure" / "60-session" / "dm-cheat-sheet.md"
    required_dm_sheet_markers = (
        "## Opening and pressure",
        "## Key locations",
        "## Key NPCs",
        "| NPC | Immediate intent | Voice cue | Source |",
        "## Critical conclusions",
        "| Conclusion | Independent paths | Fallback | Source |",
        "## Escalation",
        "## Safe cuts",
        "## Minimum resolution",
        "## Possible endings",
    )
    if not dm_cheat_sheet.is_file():
        errors.append("missing DM cheat sheet template: templates/adventure/60-session/dm-cheat-sheet.md")
    else:
        dm_sheet_content = dm_cheat_sheet.read_text(encoding="utf-8")
        for marker in required_dm_sheet_markers:
            if marker not in dm_sheet_content:
                errors.append(f"DM cheat sheet template is missing marker: {marker}")

    session_run_sheet = ROOT / "templates" / "adventure" / "60-session" / "run-sheet.md"
    required_run_sheet_markers = (
        "## Session frame",
        "## Opening options",
        "## Flexible phases",
        "| Phase or window | Desired state | Available transitions | Pressure if delayed | Source |",
        "## Checkpoints",
        "| Checkpoint | Observe | If behind | If ahead | Source |",
        "## Late pressure",
        "## Safe cuts",
        "## Finale trigger",
        "## Resolution",
        "## Live notes",
    )
    if not session_run_sheet.is_file():
        errors.append("missing Session run sheet template: templates/adventure/60-session/run-sheet.md")
    else:
        run_sheet_content = session_run_sheet.read_text(encoding="utf-8")
        for marker in required_run_sheet_markers:
            if marker not in run_sheet_content:
                errors.append(f"Session run sheet template is missing marker: {marker}")

    clue_matrix = ROOT / "templates" / "adventure" / "50-indexes" / "clue-matrix.md"
    required_clue_matrix_markers = (
        "## Conclusion paths",
        "| Conclusion key | Requirement | Information asset | Presentation clue | Source and discovery location | Access method | Independence group | Preconditions | Fail-forward | Consequence when learned, late, or missed | Plot threads |",
        "necessary",
        "optional",
        "Independence group",
    )
    if not clue_matrix.is_file():
        errors.append("missing global clue matrix template: templates/adventure/50-indexes/clue-matrix.md")
    else:
        clue_matrix_content = clue_matrix.read_text(encoding="utf-8")
        for marker in required_clue_matrix_markers:
            if marker not in clue_matrix_content:
                errors.append(f"Global clue matrix template is missing marker: {marker}")

    create_asset_skill = SKILLS / "dm-create-asset" / "SKILL.md"
    if (
        create_asset_skill.is_file()
        and "docs/player-handout-workflow.md"
        not in create_asset_skill.read_text(encoding="utf-8")
    ):
        errors.append("dm-create-asset does not reference the player Handout workflow")
    if (
        create_asset_skill.is_file()
        and "docs/player-character-workflow.md"
        not in create_asset_skill.read_text(encoding="utf-8")
    ):
        errors.append("dm-create-asset does not reference the Player Character workflow")
    if (
        create_asset_skill.is_file()
        and "docs/bild-workflow.md"
        not in create_asset_skill.read_text(encoding="utf-8")
    ):
        errors.append("dm-create-asset does not reference the image workflow")

    plot_overview = ROOT / "templates" / "adventure" / "20-plot" / "overview.md"
    required_plot_sections = (
        "## Inciting situation",
        "## Flexible player hooks",
        "## Decision landscape",
        "## Information paths",
        "## Failure, retreat, and neglect",
        "## Possible outcomes",
        "## One-shot scope and pacing",
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
