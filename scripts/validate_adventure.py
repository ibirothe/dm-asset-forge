#!/usr/bin/env python3
"""Validate one adventure without modifying it."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRS = (
    "00-input",
    "10-world",
    "20-plot",
    "30-locations",
    "40-global",
    "50-indexes",
    "60-session",
    "90-meta",
)
REQUIRED_FILES = (
    "README.md",
    "00-input/original-request.md",
    "00-input/world.md",
    "00-input/plot.md",
    "00-input/constraints.md",
    "00-input/session-preflight.md",
    "00-input/clarifications.md",
    "10-world/overview.md",
    "20-plot/overview.md",
    "20-plot/threads/index.md",
    "40-global/factions/index.md",
    "50-indexes/locations.md",
    "50-indexes/npcs.md",
    "50-indexes/player-characters.md",
    "50-indexes/objects.md",
    "50-indexes/information.md",
    "50-indexes/clue-matrix.md",
    "50-indexes/open-threads.md",
    "60-session/dm-cheat-sheet.md",
    "60-session/run-sheet.md",
    "60-session/readiness-report.md",
    "90-meta/decisions.md",
    "90-meta/assumptions.md",
    "90-meta/open-questions.md",
    "90-meta/change-log.md",
)
COMMON_REQUIRED_KEYS = frozenset(
    {
        "id",
        "type",
        "title",
        "status",
        "version",
        "scope",
        "tags",
        "themes",
        "created",
        "updated",
    }
)
COMMON_OPTIONAL_KEYS = frozenset({"aliases", "provenance", "source_refs"})
COMMON_KEYS = COMMON_REQUIRED_KEYS | COMMON_OPTIONAL_KEYS
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
KEY_VALUE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
NAMED_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
IMAGE_LINK = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
PLAYER_RELEASE_STATUS = re.compile(
    r"^- Status:\s*(not-approved|approved)\s*$", re.MULTILINE
)
PLAYER_RELEASE_VERSION = re.compile(
    r"^- Approved source version:\s*([^\s]+)\s*$", re.MULTILINE
)
PLAYER_RELEASE_APPROVAL = re.compile(r"^- Approval:\s*(.+?)\s*$", re.MULTILINE)
PLAYER_FORBIDDEN_HEADINGS = frozenset(
    {
        "Player-facing content",
        "Delivery",
        "DM-only context",
        "DM-only connections",
        "Reveals and consequences",
        "Player release",
        "Rendered output",
    }
)
SESSION_PREFLIGHT_STATUS = re.compile(
    r"^- Preflight status:\s*(open|blocked|ready)\s*$", re.MULTILINE
)
SESSION_PREFLIGHT_SECTIONS = frozenset(
    {
        "Group and rules",
        "Schedule",
        "Safety and accessibility",
        "Table and technology",
        "Materials",
        "Player releases",
        "Open blockers",
        "Ready for session",
    }
)
DM_CHEAT_SHEET_SECTIONS = frozenset(
    {
        "Opening and pressure",
        "Key locations",
        "Key NPCs",
        "Critical conclusions",
        "Escalation",
        "Safe cuts",
        "Minimum resolution",
        "Possible endings",
    }
)
DM_CHEAT_SHEET_MARKERS = frozenset(
    {
        "| NPC | Immediate intent | Voice cue | Source |",
        "| Conclusion | Independent paths | Fallback | Source |",
        "| Cut | Trigger | Preserved resolution | Source |",
        "| Ending state | Trigger | Consequence | Source |",
    }
)
SESSION_RUN_SHEET_SECTIONS = frozenset(
    {
        "Session frame",
        "Opening options",
        "Flexible phases",
        "Checkpoints",
        "Late pressure",
        "Safe cuts",
        "Finale trigger",
        "Resolution",
        "Live notes",
    }
)
SESSION_RUN_SHEET_MARKERS = frozenset(
    {
        "| Entry state | Player-facing cue | Use when | Source |",
        "| Phase or window | Desired state | Available transitions | Pressure if delayed | Source |",
        "| Checkpoint | Observe | If behind | If ahead | Source |",
        "| Trigger | Visible state change | Preserved choices | Source |",
        "| Cut | Trigger | Must preserve | Impact | Source |",
        "| Ending state | Trigger | Consequence | Source |",
    }
)
READINESS_REPORT_SECTIONS = frozenset(
    {
        "Prüfbasis",
        "Verbleibende Blocker",
        "Nächste Aktion",
    }
)
READINESS_REPORT_HEADER = "| Prüfung | Ergebnis | Geprüft am | Quelle |"
READINESS_OVERALL_STATUS = re.compile(
    r"^- Gesamtstatus:\s*(open|blocked|ready)\s*$", re.MULTILINE
)
READINESS_BLOCKER_STATUS = re.compile(
    r"^- Blockerstatus:\s*(open|present|none)\s*$", re.MULTILINE
)
READINESS_NEXT_ACTION = re.compile(r"^- Priorität:\s*(\S.+?)\s*$", re.MULTILINE)
READINESS_CHECKS = {
    "Session-Preflight": frozenset({"open", "blocked", "ready"}),
    "Technische Validierung": frozenset({"not-run", "failed", "passed"}),
    "Fachlicher Audit": frozenset({"not-run", "blocking", "clear"}),
}
CLUE_MATRIX_HEADER = (
    "| Conclusion key | Requirement | Information asset | Presentation clue | "
    "Source and discovery location | Access method | Independence group | "
    "Preconditions | Fail-forward | Consequence when learned, late, or missed | "
    "Plot threads |"
)
CLUE_REQUIREMENTS = frozenset({"necessary", "optional", "open"})
VISUAL_GENERATION_STATUS = re.compile(
    r"^- Status:\s*(not-approved|approved)\s*$", re.MULTILINE
)
VISUAL_PNG_STATE = re.compile(
    r"^- PNG state:\s*(not-created|current|stale)\s*$", re.MULTILINE
)
VISUAL_APPROVED_VERSION = re.compile(
    r"^- Approved visual version:\s*([^\s]+)\s*$", re.MULTILINE
)
VISUAL_APPROVAL = re.compile(r"^- Approval:\s*(.+?)\s*$", re.MULTILINE)
VISUAL_PROMPT_OUTPUT = re.compile(
    r"^- Relative output path:\s*`([^`]+)`\s*$", re.MULTILINE
)
VISUAL_PROMPT_SECTIONS = frozenset(
    {
        "Prompt",
        "Identity anchors",
        "Depicted state",
        "Allowed variation",
        "Composition and viewpoint",
        "Style, palette, and lighting",
        "Narrative details",
        "Exclusions",
        "Canon checks",
        "Output",
    }
)
SYSTEM_TERMS = re.compile(
    r"\b(?:armor class|hit points?|challenge rating|difficulty class|spell slots?|saving throw|"
    r"initiative modifier|trefferpunkte|rüstungsklasse|schwierigkeitsgrad)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class AssetSpec:
    prefix: str
    scope: str
    filename: str
    placement: str
    allowed_keys: frozenset[str]
    required_keys: frozenset[str]
    sections: tuple[str, ...]


@dataclass(frozen=True)
class AssetRecord:
    path: Path
    metadata: dict[str, str]
    asset_type: str


def spec(
    prefix: str,
    scope: str,
    filename: str,
    placement: str,
    keys: tuple[str, ...],
    required: tuple[str, ...],
    sections: tuple[str, ...],
) -> AssetSpec:
    return AssetSpec(
        prefix,
        scope,
        filename,
        placement,
        frozenset(keys),
        frozenset(required),
        sections,
    )


ASSET_SPECS = {
    "world": spec(
        "world-", "singleton", "overview.md", "world", (), (),
        ("Core premise", "Established truths", "Working assumptions", "Everyday life", "Powers and tensions", "Unknowns"),
    ),
    "location": spec(
        "loc-", "local", "location.md", "location",
        ("parent_location", "function", "danger", "accessibility"), (),
        ("Table purpose", "First impression", "Sensory details", "Access and boundaries", "Areas", "Inhabitants", "Objects", "Information and secrets", "Encounters and pressures", "Connections", "Changes over time"),
    ),
    "scene": spec(
        "scene-", "local", "scene.md", "scenes",
        ("primary_location", "participants", "related_threads", "danger"), ("primary_location",),
        ("Table purpose", "Entry state", "Participants and intentions", "Immediate tension", "Environment and opportunities", "Discoverable information", "Possible transitions", "Related assets"),
    ),
    "npc": spec(
        "npc-", "local", "npc.md", "npcs",
        ("primary_location", "current_location", "origin_location", "appearance_locations", "factions", "influence", "reach"), ("primary_location",),
        ("Table purpose", "First impression", "Appearance and manner", "Voice cues", "Public role", "Locations and movement", "Motivation", "Fear and pressure", "Resources and leverage", "Knowledge", "Relationships", "Likely behavior", "Hooks and consequences"),
    ),
    "player-character": spec(
        "pc-", "global", "player-character.md", "40-global/player-characters",
        ("related_locations", "related_factions", "related_threads"), (),
        ("Table purpose", "Player-facing concept", "Starting situation", "Personal hooks", "Established background", "Open choices", "Strengths and approaches", "Limits and complications", "Starting knowledge", "Relationships", "DM-only connections", "Player release"),
    ),
    "creature": spec(
        "cre-", "local", "creature.md", "creatures",
        ("primary_location", "current_location", "origin_location", "appearance_locations", "danger", "rarity", "reach"), ("primary_location",),
        ("Table purpose", "First impression", "Recognizable features", "Habitat and movement", "Needs and behavior", "Signs and discoverability", "Risks and pressure", "Weaknesses and leverage", "Hooks and consequences"),
    ),
    "faction": spec(
        "fac-", "global", "faction.md", "40-global/factions",
        ("related_locations", "influence", "reach"), (),
        ("Table purpose", "Public identity", "Agenda", "Structure and reach", "Locations and presence", "Resources and leverage", "Methods", "Internal tensions", "Relationships", "Current pressure", "Escalation and consequences"),
    ),
    "object": spec(
        "obj-", "local", "object.md", "objects",
        ("primary_location", "current_location", "origin_location", "appearance_locations", "owner", "part_of", "components", "danger", "rarity", "accessibility"), ("primary_location",),
        ("Table purpose", "Appearance", "Context and origin", "Location, ownership, and components", "Discoverability", "Properties", "Uses and leverage", "Risks and costs", "Related information", "Consequences"),
    ),
    "information": spec(
        "info-", "local", "information.md", "information",
        ("truth_status", "confidence", "accessibility", "primary_location", "discovery_locations", "known_by", "related_threads"), ("truth_status", "primary_location"),
        ("Statement", "Truth and limits", "Discovery points", "Preconditions", "Presentation clues", "Interpretation risks", "Consequences when learned", "Consequences when missed", "Related assets"),
    ),
    "encounter": spec(
        "enc-", "local", "encounter.md", "encounters",
        ("primary_location", "participants", "related_threads", "danger"), ("primary_location",),
        ("Table purpose", "Trigger", "Situation", "Participants and intentions", "Environment and leverage", "Escalation", "Approaches", "Consequences", "Follow-up links"),
    ),
    "plot-thread": spec(
        "plot-", "global", "plot-thread.md", "20-plot/threads",
        ("entry_locations", "related_factions", "danger", "reach"), (),
        ("Dramatic question", "Entry points", "Current state", "Pressures and progression", "Information path", "Involved assets", "Player choices", "Possible resolutions", "Consequences of neglect"),
    ),
    "event": spec(
        "event-", "global", "event.md", "10-world/events",
        ("related_locations", "participants", "affected_assets", "danger", "reach"), (),
        ("Table purpose", "Timing and status", "Trigger and causes", "Participants", "Sequence", "Visible signs", "Immediate consequences", "Lasting consequences", "Prevention or alteration", "Related assets"),
    ),
    "handout": spec(
        "hand-", "local", "handout.md", "handouts",
        ("primary_location", "delivery_locations", "reveals", "accessibility"), ("primary_location",),
        ("Player-facing content", "Delivery", "DM-only context", "Reveals and consequences", "Player release"),
    ),
    "visual": spec(
        "vis-", "subject-owned", "visual.md", "subject",
        ("subject_asset", "output_file"), ("subject_asset", "output_file"),
        ("Table purpose", "Subject", "Identity source", "Stable identity anchors", "Depicted state", "Allowed variation", "Player visibility", "Generation approval", "Output", "Provenance and revisions"),
    ),
    "random-table": spec(
        "table-", "global", "random-table.md", "40-global/random-tables",
        ("related_locations", "applicable_contexts"), (),
        ("Table purpose", "Applicable contexts", "Selection method", "Entries", "Constraints", "Canonicalization"),
    ),
}
ASSET_FILENAMES = frozenset(item.filename for item in ASSET_SPECS.values())
ENUM_VALUES = {
    "status": frozenset({"draft", "ready", "retired"}),
    "scope": frozenset({"singleton", "global", "local", "subject-owned"}),
    "truth_status": frozenset({"established", "partial", "false", "contested", "unknown"}),
    "provenance": frozenset({"user-authored", "agent-inferred", "agent-generated", "imported", "mixed", "unknown"}),
    "danger": frozenset({"none", "limited", "significant", "severe", "existential", "unknown"}),
    "influence": frozenset({"none", "limited", "notable", "strong", "dominant", "unknown"}),
    "reach": frozenset({"personal", "local", "regional", "widespread", "world-spanning", "unknown"}),
    "rarity": frozenset({"common", "uncommon", "rare", "unique", "unknown"}),
    "accessibility": frozenset({"open", "limited", "restricted", "hidden", "sealed", "unknown"}),
    "confidence": frozenset({"unverified", "weak", "supported", "corroborated", "confirmed", "unknown"}),
}
LIST_KEYS = frozenset(
    {
        "tags", "themes", "aliases", "source_refs", "appearance_locations",
        "factions", "participants", "related_threads", "components",
        "discovery_locations", "known_by", "delivery_locations", "reveals",
        "related_locations", "entry_locations", "related_factions",
        "affected_assets", "applicable_contexts",
    }
)
RELATION_RULES = {
    "primary_location": (False, frozenset({"location"})),
    "parent_location": (False, frozenset({"location"})),
    "current_location": (False, frozenset({"location"})),
    "origin_location": (False, frozenset({"location"})),
    "appearance_locations": (True, frozenset({"location"})),
    "discovery_locations": (True, frozenset({"location"})),
    "delivery_locations": (True, frozenset({"location"})),
    "entry_locations": (True, frozenset({"location"})),
    "related_locations": (True, frozenset({"location"})),
    "owner": (False, frozenset({"npc", "player-character", "faction"})),
    "factions": (True, frozenset({"faction"})),
    "known_by": (True, frozenset({"npc", "faction", "player-character"})),
    "participants": (True, None),
    "reveals": (True, frozenset({"information"})),
    "related_threads": (True, frozenset({"plot-thread"})),
    "related_factions": (True, frozenset({"faction"})),
    "part_of": (False, frozenset({"object"})),
    "components": (True, frozenset({"object"})),
    "subject_asset": (False, None),
    "affected_assets": (True, None),
}
INDEX_PATHS = {
    "location": (Path("50-indexes/locations.md"),),
    "npc": (Path("50-indexes/npcs.md"),),
    "player-character": (Path("50-indexes/player-characters.md"),),
    "object": (Path("50-indexes/objects.md"),),
    "information": (Path("50-indexes/information.md"),),
    "plot-thread": (
        Path("20-plot/threads/index.md"),
        Path("50-indexes/open-threads.md"),
    ),
    "faction": (Path("40-global/factions/index.md"),),
}
NAVIGATION_RELATIONS = frozenset(
    {
        "primary_location",
        "parent_location",
        "current_location",
        "appearance_locations",
        "discovery_locations",
        "delivery_locations",
        "entry_locations",
        "related_locations",
        "owner",
        "factions",
        "known_by",
        "part_of",
        "components",
        "reveals",
        "subject_asset",
    }
)
NULL_VALUES = frozenset({"null", "unknown"})


def diagnostic(path: Path | str, rule: str, message: str, hint: str) -> str:
    return f"{path} [{rule}]: {message} Fix: {hint}"


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, list[tuple[str, str]]]:
    match = FRONTMATTER.match(text)
    if not match:
        return None, []
    result: dict[str, str] = {}
    problems: list[tuple[str, str]] = []
    for number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = KEY_VALUE.match(line)
        if not item:
            problems.append(("FM_SYNTAX", f"unsupported frontmatter syntax on line {number}"))
            continue
        key, value = item.group(1), item.group(2).strip()
        if key in result:
            problems.append(("FM_DUPLICATE_KEY", f"duplicate frontmatter key {key!r} on line {number}"))
        result[key] = value
    return result, problems


def scalar(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
        if raw.strip().startswith('"'):
            value = value.replace('\\"', '"').replace("\\\\", "\\")
    return value


def parse_list(raw: str) -> list[str] | None:
    value = raw.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [scalar(item.strip()) for item in inner.split(",") if item.strip()]


def resolve_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.split("#", 1)[0].strip().strip("<>")
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    target = target.replace("%20", " ")
    return (source.parent / target).resolve()


def relative(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def expected_path(
    root: Path,
    record: AssetRecord,
    assets_by_id: dict[str, AssetRecord],
) -> Path | None:
    item = ASSET_SPECS[record.asset_type]
    asset_id = scalar(record.metadata.get("id", ""))
    if not asset_id.startswith(item.prefix):
        return None
    slug = asset_id[len(item.prefix):]
    if item.placement == "world":
        return root / "10-world" / "overview.md"
    if item.placement == "location":
        return root / "30-locations" / slug / item.filename
    if item.placement in {"scenes", "npcs", "creatures", "objects", "information", "encounters", "handouts"}:
        owner_id = scalar(record.metadata.get("primary_location", ""))
        if not owner_id.startswith("loc-"):
            return None
        owner_slug = owner_id.removeprefix("loc-")
        return root / "30-locations" / owner_slug / item.placement / slug / item.filename
    if item.placement == "subject":
        subject_id = scalar(record.metadata.get("subject_asset", ""))
        subject = assets_by_id.get(subject_id)
        if subject is None:
            return None
        return subject.path.parent / "visuals" / slug / item.filename
    return root / item.placement / slug / item.filename


def validate_common_metadata(
    rel: Path,
    metadata: dict[str, str],
    allowed_keys: frozenset[str],
    required_keys: frozenset[str],
    errors: list[str],
) -> None:
    for key in sorted(required_keys - metadata.keys()):
        errors.append(diagnostic(rel, "FM_REQUIRED", f"missing required key {key!r}.", f"Add {key!r} with a schema-valid value."))
    for key in sorted(metadata.keys() - allowed_keys):
        errors.append(diagnostic(rel, "FM_UNKNOWN_KEY", f"unknown key {key!r}.", "Remove it or define it in docs/metadaten-und-werte.md first."))
    for key, raw in metadata.items():
        value = scalar(raw)
        if raw.strip() in {'""', "''"}:
            errors.append(diagnostic(rel, "FM_EMPTY", f"key {key!r} uses an empty string.", "Use unknown, null, [], or record an open question as appropriate."))
        if key in LIST_KEYS and parse_list(raw) is None:
            errors.append(diagnostic(rel, "FM_LIST", f"key {key!r} must be an inline list.", f"Use {key}: [] or a comma-separated list in brackets."))
        if key in ENUM_VALUES and value not in ENUM_VALUES[key]:
            choices = ", ".join(sorted(ENUM_VALUES[key]))
            errors.append(diagnostic(rel, "FM_ENUM", f"invalid {key!r} value {value!r}.", f"Use one of: {choices}."))
    version = scalar(metadata.get("version", ""))
    if "version" in metadata and (not version.isdigit() or int(version) < 1):
        errors.append(diagnostic(rel, "FM_VERSION", f"version must be a positive integer, got {version!r}.", "Set version to 1 or a higher integer."))
    for key in ("created", "updated"):
        if key not in metadata:
            continue
        value = scalar(metadata[key])
        try:
            parsed = dt.date.fromisoformat(value)
        except ValueError:
            parsed = None
        if parsed is None or parsed.isoformat() != value:
            errors.append(diagnostic(rel, "FM_DATE", f"{key} must use YYYY-MM-DD, got {value!r}.", f"Replace {key} with a valid ISO date."))
    if all(key in metadata for key in ("created", "updated")):
        try:
            created = dt.date.fromisoformat(scalar(metadata["created"]))
            updated = dt.date.fromisoformat(scalar(metadata["updated"]))
            if updated < created:
                errors.append(diagnostic(rel, "FM_DATE_ORDER", "updated predates created.", "Set updated to created or a later date."))
        except ValueError:
            pass
    for key in ("tags", "themes"):
        values = parse_list(metadata.get(key, ""))
        if values is not None:
            for value in values:
                if not SLUG_PATTERN.fullmatch(value):
                    errors.append(diagnostic(rel, "FM_KEBAB_LIST", f"{key} contains non-kebab-case value {value!r}.", "Use lowercase ASCII kebab-case values."))


def validate_asset_record(
    root: Path,
    record: AssetRecord,
    assets_by_id: dict[str, AssetRecord],
    manifest: dict[str, str] | None,
    errors: list[str],
) -> None:
    rel = relative(record.path, root)
    item = ASSET_SPECS[record.asset_type]
    validate_common_metadata(rel, record.metadata, COMMON_KEYS | item.allowed_keys, COMMON_REQUIRED_KEYS | item.required_keys, errors)

    asset_id = scalar(record.metadata.get("id", ""))
    slug = asset_id[len(item.prefix):] if asset_id.startswith(item.prefix) else ""
    if not asset_id.startswith(item.prefix) or not SLUG_PATTERN.fullmatch(slug):
        errors.append(diagnostic(rel, "ASSET_ID", f"ID {asset_id!r} does not match prefix {item.prefix!r} plus a kebab-case slug.", f"Use an ID such as {item.prefix}example."))
    if scalar(record.metadata.get("type", "")) != record.asset_type:
        errors.append(diagnostic(rel, "ASSET_TYPE", f"type does not match the selected {record.asset_type!r} schema.", f"Set type: {record.asset_type}."))
    actual_scope = scalar(record.metadata.get("scope", ""))
    if actual_scope and actual_scope != item.scope:
        errors.append(diagnostic(rel, "ASSET_SCOPE", f"scope {actual_scope!r} does not match required scope {item.scope!r}.", f"Set scope: {item.scope}."))
    if not scalar(record.metadata.get("title", "")):
        errors.append(diagnostic(rel, "ASSET_TITLE", "title is empty.", "Provide a non-empty human-readable title."))

    headings = frozenset(HEADING.findall(record.path.read_text(encoding="utf-8")))
    for section in item.sections:
        if section not in headings:
            errors.append(diagnostic(rel, "SECTION_REQUIRED", f"missing required section '## {section}'.", f"Add the heading '## {section}' from templates/assets/{record.asset_type}.md."))

    target = expected_path(root, record, assets_by_id)
    if target is not None and record.path.resolve() != target.resolve():
        errors.append(diagnostic(rel, "ASSET_PATH", f"asset is outside its canonical path; expected {relative(target, root)}.", "Move the single canonical file to the expected catalog path and update links."))

    if record.asset_type == "world" and manifest:
        adventure_id = scalar(manifest.get("id", ""))
        if adventure_id.startswith("adv-"):
            expected_id = "world-" + adventure_id.removeprefix("adv-")
            if asset_id != expected_id:
                errors.append(diagnostic(rel, "WORLD_ID", f"World ID {asset_id!r} does not match adventure ID {adventure_id!r}.", f"Use id: {expected_id}."))

    if record.asset_type == "visual":
        output_file = scalar(record.metadata.get("output_file", ""))
        if not output_file.lower().endswith(".png"):
            errors.append(diagnostic(rel, "VISUAL_PNG", f"output_file {output_file!r} is not a PNG.", "Use a neighboring filename ending in .png."))
        elif Path(output_file).name != output_file:
            errors.append(diagnostic(rel, "VISUAL_OUTPUT_PATH", "output_file must name a neighboring file.", "Remove directory components from output_file."))
        else:
            prompt = record.path.parent / f"{Path(output_file).stem}.prompt.md"
            if not prompt.is_file():
                errors.append(diagnostic(rel, "VISUAL_PROMPT", f"matching prompt is missing at {relative(prompt, root)}.", "Create the prompt companion from templates/visual-prompt.md."))
            else:
                validate_visual_generation(root, record, prompt, errors)
    elif record.asset_type in {"handout", "player-character"}:
        validate_player_release(root, record, errors)


def validate_player_release(
    root: Path,
    record: AssetRecord,
    errors: list[str],
) -> None:
    rel = relative(record.path, root)
    source = record.path.read_text(encoding="utf-8")
    player = record.path.parent / "player.md"
    status_match = PLAYER_RELEASE_STATUS.search(source)
    if status_match is None:
        errors.append(
            diagnostic(
                rel,
                "PLAYER_RELEASE_STATUS",
                "Player release has no valid status.",
                "Use '- Status: not-approved' or '- Status: approved'.",
            )
        )
        return

    status = status_match.group(1)
    if status == "not-approved":
        if not player.is_file():
            return
        errors.append(
            diagnostic(
                relative(player, root),
                "PLAYER_RELEASE_BLOCKED",
                "player.md exists although the canonical source asset is not approved.",
                "Remove the player file or obtain explicit approval and document the current source version.",
            )
        )

    if not player.is_file():
        errors.append(
            diagnostic(
                rel,
                "PLAYER_FILE_MISSING",
                "Player release is approved but player.md is missing.",
                "Create the approved neighboring player.md or reset the release to not-approved.",
            )
        )
        return
    if player.resolve() not in resolved_markdown_links(record.path):
        errors.append(
            diagnostic(
                rel,
                "PLAYER_SOURCE_LINK",
                "approved player.md is not linked from its canonical source asset.",
                "Set '- Player file: [player.md](player.md)' in Player release.",
            )
        )

    approved_version = PLAYER_RELEASE_VERSION.search(source)
    current_version = scalar(record.metadata.get("version", ""))
    if approved_version is None or approved_version.group(1) != current_version:
        errors.append(
            diagnostic(
                rel,
                "PLAYER_SOURCE_VERSION",
                "approved source version does not match the current asset version.",
                f"Obtain explicit approval for version {current_version} before replacing player.md.",
            )
        )
    approval = PLAYER_RELEASE_APPROVAL.search(source)
    if approval is None or approval.group(1).strip().lower() in {
        "none", "pending", "not-approved"
    }:
        errors.append(
            diagnostic(
                rel,
                "PLAYER_APPROVAL_RECORD",
                "approved release has no concrete approval record.",
                "Record the user's explicit approval for this exact source version.",
            )
        )

    player_text = player.read_text(encoding="utf-8")
    player_rel = relative(player, root)
    if FRONTMATTER.match(player_text):
        errors.append(diagnostic(player_rel, "PLAYER_FRONTMATTER", "player.md contains YAML frontmatter.", "Remove all metadata from the player-facing file."))
    if HTML_COMMENT.search(player_text):
        errors.append(diagnostic(player_rel, "PLAYER_COMMENT", "player.md contains an internal Markdown comment.", "Remove comments and working notes from the player-facing file."))
    if not re.search(r"^#\s+\S", player_text, re.MULTILINE):
        errors.append(diagnostic(player_rel, "PLAYER_TITLE", "player.md has no readable level-one title.", "Add one standalone '# Title' heading."))
    forbidden = PLAYER_FORBIDDEN_HEADINGS.intersection(HEADING.findall(player_text))
    for heading in sorted(forbidden):
        errors.append(diagnostic(player_rel, "PLAYER_DM_SECTION", f"player.md contains internal section '## {heading}'.", "Remove DM-only and workflow sections from the player-facing file."))
    for raw_target in LINK.findall(player_text) + IMAGE_LINK.findall(player_text):
        if resolve_link(player, raw_target) is not None:
            errors.append(diagnostic(player_rel, "PLAYER_INTERNAL_LINK", f"player.md contains repository-relative link {raw_target!r}.", "Remove internal links or express the required player-facing context directly."))


def validate_visual_generation(
    root: Path,
    record: AssetRecord,
    prompt: Path,
    errors: list[str],
) -> None:
    rel = relative(record.path, root)
    visual_text = record.path.read_text(encoding="utf-8")
    prompt_text = prompt.read_text(encoding="utf-8")
    prompt_rel = relative(prompt, root)
    output_file = scalar(record.metadata.get("output_file", ""))
    png = record.path.parent / Path(output_file).name

    prompt_headings = frozenset(HEADING.findall(prompt_text))
    for section in sorted(VISUAL_PROMPT_SECTIONS - prompt_headings):
        errors.append(diagnostic(prompt_rel, "VISUAL_PROMPT_SECTION", f"missing reproducibility section '## {section}'.", f"Add '## {section}' from templates/visual-prompt.md."))
    if record.path.resolve() not in resolved_markdown_links(prompt):
        errors.append(diagnostic(prompt_rel, "VISUAL_PROMPT_SOURCE", "prompt does not link its canonical visual.md source.", "Add the relative source link '[Visual asset](visual.md)'."))
    prompt_output = VISUAL_PROMPT_OUTPUT.search(prompt_text)
    if prompt_output is None or prompt_output.group(1) != output_file:
        errors.append(diagnostic(prompt_rel, "VISUAL_PROMPT_OUTPUT", "prompt output path does not match visual metadata.", f"Set the relative output path to `{output_file}`."))

    status_match = VISUAL_GENERATION_STATUS.search(visual_text)
    state_match = VISUAL_PNG_STATE.search(visual_text)
    if status_match is None:
        errors.append(diagnostic(rel, "VISUAL_APPROVAL_STATUS", "Generation approval has no valid status.", "Use '- Status: not-approved' or '- Status: approved'."))
    if state_match is None:
        errors.append(diagnostic(rel, "VISUAL_PNG_STATE", "Generation approval has no valid PNG state.", "Use not-created, current, or stale."))
    if status_match is None or state_match is None:
        return

    status = status_match.group(1)
    state = state_match.group(1)
    exists = png.is_file()
    if state == "not-created" and exists:
        errors.append(diagnostic(rel, "VISUAL_PNG_STATE", f"PNG state is not-created but {png.name!r} exists.", "Document an approved current PNG or a stale previous PNG."))
    if state in {"current", "stale"} and not exists:
        errors.append(diagnostic(rel, "VISUAL_PNG_MISSING", f"PNG state is {state} but {png.name!r} is missing.", "Restore the PNG or set PNG state to not-created."))
    if exists and state != "stale" and status != "approved":
        errors.append(diagnostic(rel, "VISUAL_PNG_APPROVAL", "a non-stale PNG exists without approval for the documented Visual version.", "Obtain explicit approval or mark the older PNG stale."))
    if status == "approved" and state != "current":
        errors.append(diagnostic(rel, "VISUAL_APPROVAL_STATE", "approved status is only valid for a current PNG.", "Set the matching current state or reset approval to not-approved."))
    if state == "stale" and status != "not-approved":
        errors.append(diagnostic(rel, "VISUAL_APPROVAL_STATE", "a stale PNG must await a new approval.", "Set Status to not-approved until replacement is explicitly approved."))

    approved_version_match = VISUAL_APPROVED_VERSION.search(visual_text)
    approved_version = approved_version_match.group(1) if approved_version_match else ""
    current_version = scalar(record.metadata.get("version", ""))
    approval_match = VISUAL_APPROVAL.search(visual_text)
    approval = approval_match.group(1).strip() if approval_match else ""
    concrete_approval = approval.lower() not in {"", "none", "pending", "not-approved"}

    if state == "current":
        if approved_version != current_version:
            errors.append(diagnostic(rel, "VISUAL_APPROVED_VERSION", "current PNG approval does not match the current Visual version.", f"Obtain explicit approval for version {current_version}."))
        if not concrete_approval:
            errors.append(diagnostic(rel, "VISUAL_APPROVAL_RECORD", "current PNG has no concrete approval record.", "Record the user's approval for this exact Visual version and prompt."))
        if scalar(record.metadata.get("provenance", "unknown")) == "unknown":
            errors.append(diagnostic(rel, "VISUAL_PROVENANCE", "current PNG has unknown provenance.", "Set provenance to the documented actual origin and record the revision."))
    elif state == "stale":
        if not approved_version.isdigit() or approved_version == current_version:
            errors.append(diagnostic(rel, "VISUAL_APPROVED_VERSION", "stale PNG must identify an older approved Visual version.", "Record the prior numeric version that produced the retained PNG."))
        if not concrete_approval:
            errors.append(diagnostic(rel, "VISUAL_APPROVAL_RECORD", "stale PNG has no record of its prior approval.", "Preserve the approval record for the older retained PNG."))
    elif approved_version != "none" or approval.lower() != "none":
        errors.append(diagnostic(rel, "VISUAL_APPROVAL_RECORD", "not-created PNG must not claim an approval or approved version.", "Use Approved visual version: none and Approval: none."))


def validate_relations(
    root: Path,
    records: list[AssetRecord],
    assets_by_id: dict[str, AssetRecord],
    errors: list[str],
) -> None:
    for record in records:
        rel = relative(record.path, root)
        source_id = scalar(record.metadata.get("id", ""))
        for key, (is_list, allowed_types) in RELATION_RULES.items():
            if key not in record.metadata:
                continue
            raw = record.metadata[key]
            if is_list:
                values = parse_list(raw)
                if values is None:
                    continue
            else:
                value = scalar(raw)
                values = [] if value in NULL_VALUES or not value else [value]
                if key in ASSET_SPECS[record.asset_type].required_keys and not values:
                    errors.append(diagnostic(rel, "REL_REQUIRED", f"required relation {key!r} has no target.", "Reference one existing asset ID of the required type."))
            for target_id in values:
                target = assets_by_id.get(target_id)
                if target is None:
                    errors.append(diagnostic(rel, "REL_NOT_FOUND", f"relation {key!r} references missing asset ID {target_id!r}.", "Create the target asset or replace/remove the stale ID."))
                    continue
                if target_id == source_id:
                    errors.append(diagnostic(rel, "REL_SELF", f"relation {key!r} references the source asset itself.", "Reference a different asset or remove the relation."))
                if allowed_types is not None and target.asset_type not in allowed_types:
                    choices = ", ".join(sorted(allowed_types))
                    errors.append(diagnostic(rel, "REL_TARGET_TYPE", f"relation {key!r} targets type {target.asset_type!r}, expected {choices}.", "Replace the ID with an asset of an allowed type."))


def resolved_markdown_links(path: Path) -> set[Path]:
    result: set[Path] = set()
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK.findall(text):
        target = resolve_link(path, raw_target)
        if target is not None:
            result.add(target)
    return result


def relation_values(record: AssetRecord, key: str) -> list[str]:
    if key not in record.metadata:
        return []
    is_list, _ = RELATION_RULES[key]
    if is_list:
        return parse_list(record.metadata[key]) or []
    value = scalar(record.metadata[key])
    return [] if value in NULL_VALUES or not value else [value]


def validate_navigation_links(
    root: Path,
    records: list[AssetRecord],
    assets_by_id: dict[str, AssetRecord],
    errors: list[str],
) -> None:
    link_cache: dict[Path, set[Path]] = {}
    checked_directions: set[tuple[Path, Path]] = set()

    def links(path: Path) -> set[Path]:
        if path not in link_cache:
            link_cache[path] = resolved_markdown_links(path)
        return link_cache[path]

    for record in records:
        source_id = scalar(record.metadata.get("id", ""))
        for key in NAVIGATION_RELATIONS:
            if key not in RELATION_RULES:
                continue
            _, allowed_types = RELATION_RULES[key]
            for target_id in relation_values(record, key):
                target = assets_by_id.get(target_id)
                if target is None or target.path == record.path:
                    continue
                if allowed_types is not None and target.asset_type not in allowed_types:
                    continue

                forward = (record.path, target.path)
                if forward not in checked_directions:
                    checked_directions.add(forward)
                    if target.path.resolve() not in links(record.path):
                        errors.append(
                            diagnostic(
                                relative(record.path, root),
                                "REL_LINK_MISSING",
                                f"relation to {target_id!r} has no relative Markdown link in the source asset.",
                                f"Add a relative link to {relative(target.path, root)} in the relevant section.",
                            )
                        )

                reverse = (target.path, record.path)
                if reverse not in checked_directions:
                    checked_directions.add(reverse)
                    if record.path.resolve() not in links(target.path):
                        errors.append(
                            diagnostic(
                                relative(target.path, root),
                                "BACKLINK_MISSING",
                                f"required backlink to {source_id!r} is missing.",
                                f"Add a relative link to {relative(record.path, root)} in the relevant section.",
                            )
                        )

                if key == "part_of":
                    components = parse_list(target.metadata.get("components", "[]")) or []
                    if source_id not in components:
                        errors.append(
                            diagnostic(
                                relative(target.path, root),
                                "REL_RECIPROCAL",
                                f"components does not include part {source_id!r}.",
                                f"Add {source_id!r} to components or remove the part_of relation.",
                            )
                        )
                elif key == "components":
                    if scalar(target.metadata.get("part_of", "")) != source_id:
                        errors.append(
                            diagnostic(
                                relative(target.path, root),
                                "REL_RECIPROCAL",
                                f"part_of does not point back to whole object {source_id!r}.",
                                f"Set part_of: {source_id!r} or remove the component relation.",
                            )
                        )


def expected_index_prefix(record: AssetRecord) -> list[str]:
    metadata = record.metadata
    asset_id = scalar(metadata.get("id", ""))
    title = scalar(metadata.get("title", ""))
    status = scalar(metadata.get("status", ""))
    if record.asset_type == "location":
        return [asset_id, title, status, scalar(metadata.get("function", ""))]
    if record.asset_type in {"npc", "object"}:
        return [asset_id, title, status, scalar(metadata.get("primary_location", ""))]
    if record.asset_type == "information":
        return [
            asset_id,
            title,
            scalar(metadata.get("truth_status", "")),
            scalar(metadata.get("primary_location", "")),
        ]
    return [asset_id, title, status]


def validate_indexes(
    root: Path,
    records: list[AssetRecord],
    errors: list[str],
) -> None:
    records_by_path = {record.path.resolve(): record for record in records}
    records_by_type: defaultdict[str, list[AssetRecord]] = defaultdict(list)
    for record in records:
        records_by_type[record.asset_type].append(record)

    for asset_type, index_paths in INDEX_PATHS.items():
        for index_rel in index_paths:
            index = root / index_rel
            if not index.is_file():
                continue
            rows_by_target: defaultdict[Path, list[list[str]]] = defaultdict(list)
            for line in index.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not stripped.startswith("|"):
                    continue
                cells = [cell.strip() for cell in stripped.strip("|").split("|")]
                if not cells or cells[0] == "ID" or set(cells[0]) <= {"-", ":"}:
                    continue
                links = LINK.findall(line)
                if len(links) != 1:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_LINK",
                            f"index row for {cells[0]!r} must contain exactly one relative Markdown link.",
                            "Add one link to the canonical asset file and remove extra links.",
                        )
                    )
                    continue
                target = resolve_link(index, links[0])
                if target is None:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_LINK",
                            f"index row for {cells[0]!r} does not use a relative asset link.",
                            "Use one portable relative Markdown link to the canonical asset file.",
                        )
                    )
                    continue
                record = records_by_path.get(target.resolve())
                if record is None:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_TARGET",
                            f"index row for {cells[0]!r} does not target a canonical asset.",
                            "Remove the stale row or link it to the canonical asset file.",
                        )
                    )
                    continue
                if record.asset_type != asset_type:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_TYPE",
                            f"index row targets type {record.asset_type!r}, expected {asset_type!r}.",
                            "Move the row to the correct index.",
                        )
                    )
                    continue
                rows_by_target[record.path.resolve()].append(cells)

            for record in records_by_type[asset_type]:
                rows = rows_by_target.get(record.path.resolve(), [])
                if not rows:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_MISSING",
                            f"asset {scalar(record.metadata.get('id', ''))!r} is not listed.",
                            f"Add one row linking to {relative(record.path, root)}.",
                        )
                    )
                    continue
                if len(rows) > 1:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_DUPLICATE",
                            f"asset {scalar(record.metadata.get('id', ''))!r} is listed more than once.",
                            "Keep exactly one current index row.",
                        )
                    )
                    continue
                expected = expected_index_prefix(record)
                actual = rows[0][: len(expected)]
                if actual != expected:
                    errors.append(
                        diagnostic(
                            index_rel,
                            "INDEX_STALE",
                            f"index values for {expected[0]!r} are stale: expected {expected}, got {actual}.",
                            "Refresh the row from the canonical asset metadata without copying descriptive content.",
                        )
                        )


def validate_clue_matrix(
    root: Path,
    records: list[AssetRecord],
    assets_by_id: dict[str, AssetRecord],
    errors: list[str],
) -> None:
    path = root / "50-indexes" / "clue-matrix.md"
    if not path.is_file():
        return

    rel = relative(path, root)
    content = path.read_text(encoding="utf-8")
    if "## Conclusion paths" not in content or CLUE_MATRIX_HEADER not in content:
        errors.append(
            diagnostic(
                rel,
                "CLUE_MATRIX_STRUCTURE",
                "required conclusion-path section or table header is missing.",
                "Restore the section and table header from templates/adventure/50-indexes/clue-matrix.md.",
            )
        )

    records_by_path = {record.path.resolve(): record for record in records}
    information_records = {
        scalar(record.metadata.get("id", "")): record
        for record in records
        if record.asset_type == "information"
    }
    linked_information: set[str] = set()
    linked_locations: defaultdict[str, set[str]] = defaultdict(set)
    linked_threads: defaultdict[str, set[str]] = defaultdict(set)
    requirements: defaultdict[str, set[str]] = defaultdict(set)
    independence_groups: defaultdict[str, set[str]] = defaultdict(set)
    path_signatures: defaultdict[str, set[tuple[tuple[str, ...], str]]] = defaultdict(set)

    def linked_records(cell: str, row_key: str, role: str) -> list[AssetRecord]:
        result: list[AssetRecord] = []
        for label, raw_target in NAMED_LINK.findall(cell):
            target = resolve_link(path, raw_target)
            if target is None:
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_LINK",
                        f"row {row_key!r} uses a non-relative {role} link.",
                        "Use a relative link to one canonical adventure asset.",
                    )
                )
                continue
            record = records_by_path.get(target.resolve())
            if record is None:
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_TARGET",
                        f"row {row_key!r} {role} link does not target a canonical asset.",
                        "Link the stable ID to its canonical asset file.",
                    )
                )
                continue
            target_id = scalar(record.metadata.get("id", ""))
            if label != target_id:
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_ID",
                        f"row {row_key!r} labels {role} target {target_id!r} as {label!r}.",
                        f"Use the stable ID {target_id!r} as the Markdown link text.",
                    )
                )
            result.append(record)
        return result

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0] == "Conclusion key" or set(cells[0]) <= {"-", ":"}:
            continue
        row_key = cells[0] or "<empty>"
        if len(cells) != 11:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_STRUCTURE",
                    f"row {row_key!r} has {len(cells)} cells; expected 11.",
                    "Restore all clue-matrix columns and escape prose that contains a table separator.",
                )
            )
            continue
        if not SLUG_PATTERN.fullmatch(cells[0]):
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_KEY",
                    f"invalid conclusion key {cells[0]!r}.",
                    "Use one stable lowercase ASCII kebab-case key for all paths to the same conclusion.",
                )
            )
        requirement = cells[1]
        if requirement not in CLUE_REQUIREMENTS:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_REQUIREMENT",
                    f"row {row_key!r} has invalid requirement {requirement!r}.",
                    "Use necessary, optional, or open.",
                )
            )
        requirements[row_key].add(requirement)

        information_links = NAMED_LINK.findall(cells[2])
        information_targets = linked_records(cells[2], row_key, "information")
        information: AssetRecord | None = None
        if len(information_links) != 1 or len(information_targets) != 1:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_INFORMATION",
                    f"row {row_key!r} must contain exactly one valid Information-asset link.",
                    "Link one stable info-* ID to its canonical information.md file.",
                )
            )
        elif information_targets[0].asset_type != "information":
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_INFORMATION",
                    f"row {row_key!r} targets type {information_targets[0].asset_type!r} instead of information.",
                    "Link one canonical Information asset.",
                )
            )
        else:
            information = information_targets[0]
            linked_information.add(scalar(information.metadata.get("id", "")))

        source_links = NAMED_LINK.findall(cells[4])
        source_targets = linked_records(cells[4], row_key, "source")
        if not source_links or len(source_targets) != len(source_links):
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_SOURCE",
                    f"row {row_key!r} must link every source and discovery location to canonical assets.",
                    "Add relative stable-ID links, including the applicable loc-* discovery location.",
                )
            )
        source_ids = tuple(
            sorted(scalar(record.metadata.get("id", "")) for record in source_targets)
        )
        location_ids = {
            scalar(record.metadata.get("id", ""))
            for record in source_targets
            if record.asset_type == "location"
        }
        if not location_ids:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_SOURCE",
                    f"row {row_key!r} has no linked discovery location.",
                    "Link at least one canonical loc-* discovery location in the source cell.",
                )
            )

        thread_links = NAMED_LINK.findall(cells[10])
        thread_targets = linked_records(cells[10], row_key, "plot-thread")
        if thread_links and len(thread_targets) != len(thread_links):
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_THREAD",
                    f"row {row_key!r} contains an invalid Plot-Thread link.",
                    "Link every plot-* ID to its canonical plot-thread.md file.",
                )
            )
        for thread in thread_targets:
            if thread.asset_type != "plot-thread":
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_THREAD",
                        f"row {row_key!r} links type {thread.asset_type!r} as a Plot Thread.",
                        "Use only canonical plot-thread assets in the final column.",
                    )
                )

        if information is not None:
            information_id = scalar(information.metadata.get("id", ""))
            linked_locations[information_id].update(location_ids)
            valid_threads = {
                scalar(thread.metadata.get("id", ""))
                for thread in thread_targets
                if thread.asset_type == "plot-thread"
            }
            linked_threads[information_id].update(valid_threads)
            expected_locations = set(
                parse_list(information.metadata.get("discovery_locations", "[]")) or []
            )
            primary_location = scalar(information.metadata.get("primary_location", ""))
            if primary_location:
                expected_locations.add(primary_location)
            unexpected_locations = location_ids - expected_locations
            if unexpected_locations:
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_LOCATION_RELATION",
                        f"row {row_key!r} links discovery locations not declared by {information_id!r}: {sorted(unexpected_locations)}.",
                        "Update the canonical Information discovery_locations relation or correct the matrix link.",
                    )
                )
            expected_threads = set(
                parse_list(information.metadata.get("related_threads", "[]")) or []
            )
            unexpected_threads = valid_threads - expected_threads
            if unexpected_threads:
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_THREAD_RELATION",
                        f"row {row_key!r} links Plot Threads not declared by {information_id!r}: {sorted(unexpected_threads)}.",
                        "Update the canonical Information related_threads relation or correct the matrix link.",
                    )
                )

        if requirement == "necessary":
            required_cells = {
                "Presentation clue": cells[3],
                "Access method": cells[5],
                "Independence group": cells[6],
                "Fail-forward": cells[8],
                "Consequence": cells[9],
            }
            missing = [
                name
                for name, value in required_cells.items()
                if value.strip().lower() in {"", "—", "open"}
            ]
            if missing:
                errors.append(
                    diagnostic(
                        rel,
                        "CLUE_MATRIX_REQUIRED_FIELD",
                        f"necessary row {row_key!r} has no concrete value for: {', '.join(missing)}.",
                        "Describe the presentable clue, access, independence, fail-forward, and consequences.",
                    )
                )
            group = cells[6].strip().lower()
            access = cells[5].strip().lower()
            if group not in {"", "—", "open"}:
                independence_groups[row_key].add(group)
            if source_ids and access not in {"", "—", "open"}:
                path_signatures[row_key].add((source_ids, access))

    for key, values in requirements.items():
        if len(values) > 1:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_REQUIREMENT",
                    f"conclusion {key!r} uses inconsistent requirements: {sorted(values)}.",
                    "Use the same requirement on every path for one conclusion key.",
                )
            )
        if "necessary" in values and (
            len(independence_groups[key]) < 2 or len(path_signatures[key]) < 2
        ):
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_INDEPENDENCE",
                    f"necessary conclusion {key!r} lacks two independent groups with distinct source/access paths.",
                    "Add a second concretely presentable path with a different independence group and source or access method.",
                )
            )

    for information_id, information in information_records.items():
        if scalar(information.metadata.get("status", "")) == "retired":
            continue
        if information_id not in linked_information:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_MISSING_INFO",
                    f"Information asset {information_id!r} is not represented.",
                    f"Add at least one row linking to {relative(information.path, root)}.",
                )
            )
            continue
        expected_locations = set(
            parse_list(information.metadata.get("discovery_locations", "[]")) or []
        )
        primary_location = scalar(information.metadata.get("primary_location", ""))
        if primary_location:
            expected_locations.add(primary_location)
        missing_locations = expected_locations - linked_locations[information_id]
        if missing_locations:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_LOCATION_COVERAGE",
                    f"Information asset {information_id!r} is missing discovery-location links: {sorted(missing_locations)}.",
                    "Add rows or source-cell links for every canonical discovery location.",
                )
            )
        expected_threads = set(
            parse_list(information.metadata.get("related_threads", "[]")) or []
        )
        missing_threads = expected_threads - linked_threads[information_id]
        if missing_threads:
            errors.append(
                diagnostic(
                    rel,
                    "CLUE_MATRIX_THREAD_COVERAGE",
                    f"Information asset {information_id!r} is missing related Plot-Thread links: {sorted(missing_threads)}.",
                    "Link every canonical related_threads target in at least one matrix row.",
                )
            )

    for route, rule, message, hint in (
        (
            root / "README.md",
            "CLUE_MATRIX_README_LINK",
            "Adventure overview does not link the global clue matrix.",
            "Add a direct relative link to 50-indexes/clue-matrix.md.",
        ),
        (
            root / "50-indexes" / "information.md",
            "CLUE_MATRIX_INDEX_LINK",
            "Information index does not link the global clue matrix.",
            "Add a relative companion link to clue-matrix.md.",
        ),
    ):
        if route.is_file() and path.resolve() not in resolved_markdown_links(route):
            errors.append(diagnostic(relative(route, root), rule, message, hint))


def validate_session_preflight(root: Path, errors: list[str]) -> None:
    path = root / "00-input" / "session-preflight.md"
    if not path.is_file():
        return

    rel = relative(path, root)
    content = path.read_text(encoding="utf-8")
    headings = frozenset(HEADING.findall(content))
    for section in sorted(SESSION_PREFLIGHT_SECTIONS - headings):
        errors.append(
            diagnostic(
                rel,
                "PREFLIGHT_SECTION",
                f"missing required section '## {section}'.",
                f"Restore '## {section}' from templates/adventure/00-input/session-preflight.md.",
            )
        )

    if SESSION_PREFLIGHT_STATUS.search(content) is None:
        errors.append(
            diagnostic(
                rel,
                "PREFLIGHT_STATUS",
                "Preflight status is missing or invalid.",
                "Use '- Preflight status: open', 'blocked', or 'ready'.",
            )
        )

    constraints = root / "00-input" / "constraints.md"
    if constraints.resolve() not in resolved_markdown_links(path):
        errors.append(
            diagnostic(
                rel,
                "PREFLIGHT_CONSTRAINTS_LINK",
                "Session preflight does not link the canonical constraints file.",
                "Link to constraints.md instead of copying target duration or content boundaries.",
            )
        )


def validate_dm_cheat_sheet(root: Path, errors: list[str]) -> None:
    path = root / "60-session" / "dm-cheat-sheet.md"
    if not path.is_file():
        return

    rel = relative(path, root)
    content = path.read_text(encoding="utf-8")
    headings = frozenset(HEADING.findall(content))
    for section in sorted(DM_CHEAT_SHEET_SECTIONS - headings):
        errors.append(
            diagnostic(
                rel,
                "DM_SHEET_SECTION",
                f"missing required section '## {section}'.",
                f"Restore '## {section}' from templates/adventure/60-session/dm-cheat-sheet.md.",
            )
        )

    for marker in sorted(DM_CHEAT_SHEET_MARKERS):
        if marker not in content:
            errors.append(
                diagnostic(
                    rel,
                    "DM_SHEET_STRUCTURE",
                    f"missing compact table header {marker!r}.",
                    "Restore the table header from templates/adventure/60-session/dm-cheat-sheet.md.",
                )
            )

    required_sources = (
        root / "20-plot" / "overview.md",
        root / "50-indexes" / "locations.md",
        root / "50-indexes" / "npcs.md",
        root / "50-indexes" / "information.md",
        root / "50-indexes" / "open-threads.md",
    )
    linked = resolved_markdown_links(path)
    for source in required_sources:
        if source.resolve() not in linked:
            errors.append(
                diagnostic(
                    rel,
                    "DM_SHEET_SOURCE_LINK",
                    f"required canonical source is not linked: {relative(source, root)}.",
                    "Add a relative link to the canonical Plot or matching index.",
                )
            )

    readme = root / "README.md"
    if path.resolve() not in resolved_markdown_links(readme):
        errors.append(
            diagnostic(
                "README.md",
                "DM_SHEET_README_LINK",
                "Adventure overview does not link the DM cheat sheet.",
                "Add a direct relative link to 60-session/dm-cheat-sheet.md.",
            )
        )


def validate_session_run_sheet(root: Path, errors: list[str]) -> None:
    path = root / "60-session" / "run-sheet.md"
    if not path.is_file():
        return

    rel = relative(path, root)
    content = path.read_text(encoding="utf-8")
    headings = frozenset(HEADING.findall(content))
    for section in sorted(SESSION_RUN_SHEET_SECTIONS - headings):
        errors.append(
            diagnostic(
                rel,
                "RUN_SHEET_SECTION",
                f"missing required section '## {section}'.",
                f"Restore '## {section}' from templates/adventure/60-session/run-sheet.md.",
            )
        )

    for marker in sorted(SESSION_RUN_SHEET_MARKERS):
        if marker not in content:
            errors.append(
                diagnostic(
                    rel,
                    "RUN_SHEET_STRUCTURE",
                    f"missing operational table header {marker!r}.",
                    "Restore the table header from templates/adventure/60-session/run-sheet.md.",
                )
            )

    required_sources = (
        root / "00-input" / "session-preflight.md",
        root / "20-plot" / "overview.md",
        root / "50-indexes" / "information.md",
        root / "50-indexes" / "open-threads.md",
        root / "60-session" / "dm-cheat-sheet.md",
    )
    linked = resolved_markdown_links(path)
    for source in required_sources:
        if source.resolve() not in linked:
            errors.append(
                diagnostic(
                    rel,
                    "RUN_SHEET_SOURCE_LINK",
                    f"required source is not linked: {relative(source, root)}.",
                    "Add a relative link to the canonical source or companion runtime view.",
                )
            )

    readme = root / "README.md"
    if path.resolve() not in resolved_markdown_links(readme):
        errors.append(
            diagnostic(
                "README.md",
                "RUN_SHEET_README_LINK",
                "Adventure overview does not link the Session run sheet.",
                "Add a direct relative link to 60-session/run-sheet.md.",
            )
        )

    cheat_sheet = root / "60-session" / "dm-cheat-sheet.md"
    if cheat_sheet.is_file() and path.resolve() not in resolved_markdown_links(cheat_sheet):
        errors.append(
            diagnostic(
                relative(cheat_sheet, root),
                "RUN_SHEET_COMPANION_LINK",
                "DM cheat sheet does not link the Session run sheet.",
                "Add the companion relative link to run-sheet.md.",
            )
        )


def validate_readiness_report(root: Path, errors: list[str]) -> None:
    path = root / "60-session" / "readiness-report.md"
    if not path.is_file():
        return

    rel = relative(path, root)
    content = path.read_text(encoding="utf-8")
    headings = frozenset(HEADING.findall(content))
    for section in sorted(READINESS_REPORT_SECTIONS - headings):
        errors.append(
            diagnostic(
                rel,
                "READINESS_SECTION",
                f"missing required section '## {section}'.",
                f"Restore '## {section}' from templates/adventure/60-session/readiness-report.md.",
            )
        )

    if READINESS_REPORT_HEADER not in content:
        errors.append(
            diagnostic(
                rel,
                "READINESS_BASIS",
                "readiness basis table header is missing or changed.",
                "Restore the compact four-column table from the readiness template.",
            )
        )

    overall_match = READINESS_OVERALL_STATUS.search(content)
    if overall_match is None:
        errors.append(
            diagnostic(
                rel,
                "READINESS_STATUS",
                "overall readiness status is missing or invalid.",
                "Use '- Gesamtstatus: open', 'blocked', or 'ready'.",
            )
        )

    rows: dict[str, tuple[str, str]] = {}
    for line in content.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] in READINESS_CHECKS:
            rows[cells[0]] = (cells[1], cells[2])

    for check, allowed_results in READINESS_CHECKS.items():
        if check not in rows:
            errors.append(
                diagnostic(
                    rel,
                    "READINESS_BASIS",
                    f"readiness basis is missing the {check!r} row.",
                    "Restore the three fixed check rows from the readiness template.",
                )
            )
            continue
        result, checked_on = rows[check]
        if result not in allowed_results:
            errors.append(
                diagnostic(
                    rel,
                    "READINESS_RESULT",
                    f"{check} has invalid result {result!r}.",
                    f"Use one of: {', '.join(sorted(allowed_results))}.",
                )
            )
        if checked_on == "not-run":
            if result not in {"open", "not-run"}:
                errors.append(
                    diagnostic(
                        rel,
                        "READINESS_DATE",
                        f"{check} result {result!r} requires a check date.",
                        "Use the actual ISO date YYYY-MM-DD.",
                    )
                )
        else:
            try:
                dt.date.fromisoformat(checked_on)
            except ValueError:
                errors.append(
                    diagnostic(
                        rel,
                        "READINESS_DATE",
                        f"{check} has invalid check date {checked_on!r}.",
                        "Use not-run or a valid ISO date YYYY-MM-DD.",
                    )
                )

    blocker_match = READINESS_BLOCKER_STATUS.search(content)
    if blocker_match is None:
        errors.append(
            diagnostic(
                rel,
                "READINESS_BLOCKER_STATUS",
                "remaining blockers have no valid summary status.",
                "Use '- Blockerstatus: open', 'present', or 'none'.",
            )
        )

    if len(READINESS_NEXT_ACTION.findall(content)) != 1:
        errors.append(
            diagnostic(
                rel,
                "READINESS_NEXT_ACTION",
                "readiness report must contain exactly one non-empty prioritized next action.",
                "Keep one '- Priorität: ...' line under '## Nächste Aktion'.",
            )
        )

    required_sources = (
        root / "00-input" / "session-preflight.md",
        root / "90-meta" / "open-questions.md",
        root.parent / "docs" / "validierung.md",
        root.parent / "docs" / "adventure-audit-guide.md",
    )
    linked = resolved_markdown_links(path)
    for source in required_sources:
        if source.resolve() not in linked:
            errors.append(
                diagnostic(
                    rel,
                    "READINESS_SOURCE_LINK",
                    f"required readiness source is not linked: {source.name}.",
                    "Restore the source link from the readiness template instead of copying source content.",
                )
            )

    readme = root / "README.md"
    if path.resolve() not in resolved_markdown_links(readme):
        errors.append(
            diagnostic(
                "README.md",
                "READINESS_README_LINK",
                "Adventure overview does not link the readiness report.",
                "Add a direct relative link to 60-session/readiness-report.md.",
            )
        )

    if overall_match is not None and overall_match.group(1) == "ready":
        ready_basis = {
            "Session-Preflight": "ready",
            "Technische Validierung": "passed",
            "Fachlicher Audit": "clear",
        }
        basis_ready = all(
            rows.get(check, (None, None))[0] == expected
            and rows.get(check, (None, "not-run"))[1] != "not-run"
            for check, expected in ready_basis.items()
        )
        blockers_clear = blocker_match is not None and blocker_match.group(1) == "none"
        if not basis_ready or not blockers_clear:
            errors.append(
                diagnostic(
                    rel,
                    "READINESS_READY",
                    "overall status ready is not supported by all three checks and a clear blocker state.",
                    "Require preflight ready, validation passed, audit clear, dated results, and Blockerstatus none.",
                )
            )


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids: defaultdict[str, list[Path]] = defaultdict(list)
    records: list[AssetRecord] = []
    metadata_by_path: dict[Path, dict[str, str]] = {}

    for item in REQUIRED_DIRS:
        if not (root / item).is_dir():
            errors.append(diagnostic(item, "STRUCT_DIR", "required directory is missing.", "Restore it from templates/adventure/."))
    for item in REQUIRED_FILES:
        if not (root / item).is_file():
            errors.append(diagnostic(item, "STRUCT_FILE", "required file is missing.", "Restore it from templates/adventure/."))

    for path in sorted(root.rglob("*")):
        rel = relative(path, root)
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}:
            errors.append(diagnostic(rel, "IMAGE_FORMAT", "non-PNG image file found.", "Convert the image to PNG and update references."))
        if path.is_file() and path.suffix.lower() == ".png":
            if not (path.parent / "visual.md").is_file():
                errors.append(
                    diagnostic(
                        rel,
                        "PNG_ORPHAN",
                        "PNG has no neighboring Visual asset.",
                        "Move it into a Subject-owned Visual directory beside visual.md and its prompt.",
                    )
                )
        if not path.is_file() or path.suffix != ".md":
            continue

        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER.search(text):
            errors.append(diagnostic(rel, "CONTENT_PLACEHOLDER", "unresolved template placeholder found.", "Replace every {{TOKEN}} with a concrete value."))
        if SYSTEM_TERMS.search(text):
            warnings.append(diagnostic(rel, "CONTENT_SYSTEM_SPECIFIC", "possible system-specific term found.", "Review and replace it with system-neutral narrative language when applicable."))
        for raw_target in LINK.findall(text) + IMAGE_LINK.findall(text):
            resolved = resolve_link(path, raw_target)
            if resolved is not None and not resolved.exists():
                errors.append(diagnostic(rel, "LINK_BROKEN", f"relative link target does not exist: {raw_target}.", "Correct the relative path or create the intended target."))
        for raw_target in IMAGE_LINK.findall(text):
            target = raw_target.split("#", 1)[0].strip().strip("<>")
            if target and not target.lower().endswith(".png"):
                errors.append(diagnostic(rel, "IMAGE_LINK_FORMAT", f"image link is not PNG: {raw_target}.", "Link to a .png image."))

        metadata, problems = parse_frontmatter(text)
        for rule, message in problems:
            errors.append(diagnostic(rel, rule, message + ".", "Use simple top-level YAML key-value entries."))
        if metadata is not None:
            metadata_by_path[path] = metadata

        if path.name.endswith(".prompt.md"):
            if not (path.parent / "visual.md").is_file():
                errors.append(diagnostic(rel, "PROMPT_ORPHAN", "visual prompt has no sibling visual.md.", "Create the canonical Visual asset or move the prompt beside it."))
            continue

        declared_type = scalar(metadata.get("type", "")) if metadata else ""
        catalog_filename = (
            path.name in ASSET_FILENAMES
            and "50-indexes" not in rel.parts
            and path.name != "overview.md"
        )
        looks_like_asset = catalog_filename or declared_type in ASSET_SPECS
        if looks_like_asset:
            if metadata is None:
                errors.append(diagnostic(rel, "FM_MISSING", "asset has no YAML frontmatter.", "Add frontmatter from the matching asset template."))
                continue
            if declared_type not in ASSET_SPECS:
                errors.append(diagnostic(rel, "ASSET_TYPE", f"unknown or missing asset type {declared_type!r}.", "Use one of the 15 types from docs/asset-katalog.md."))
                continue
            record = AssetRecord(path, metadata, declared_type)
            records.append(record)
            asset_id = scalar(metadata.get("id", ""))
            if asset_id:
                ids[asset_id].append(path)

    manifest = metadata_by_path.get(root / "README.md")
    if manifest is None:
        errors.append(diagnostic("README.md", "FM_MISSING", "adventure manifest has no YAML frontmatter.", "Restore the manifest frontmatter from templates/adventure/README.md."))
    else:
        validate_common_metadata(Path("README.md"), manifest, COMMON_KEYS, COMMON_REQUIRED_KEYS, errors)
        if scalar(manifest.get("type", "")) != "adventure":
            errors.append(diagnostic("README.md", "MANIFEST_TYPE", "manifest type must be 'adventure'.", "Set type: adventure."))
        manifest_id = scalar(manifest.get("id", ""))
        if not manifest_id.startswith("adv-") or not SLUG_PATTERN.fullmatch(manifest_id.removeprefix("adv-")):
            errors.append(diagnostic("README.md", "MANIFEST_ID", f"invalid adventure ID {manifest_id!r}.", "Use adv- followed by a lowercase kebab-case slug."))
        if scalar(manifest.get("scope", "")) != "singleton":
            errors.append(diagnostic("README.md", "MANIFEST_SCOPE", "manifest scope must be 'singleton'.", "Set scope: singleton."))
        if manifest_id:
            ids[manifest_id].append(root / "README.md")

    assets_by_id: dict[str, AssetRecord] = {}
    for record in records:
        asset_id = scalar(record.metadata.get("id", ""))
        if asset_id and len(ids[asset_id]) == 1:
            assets_by_id[asset_id] = record

    for record in records:
        validate_asset_record(root, record, assets_by_id, manifest, errors)
    validate_relations(root, records, assets_by_id, errors)
    validate_navigation_links(root, records, assets_by_id, errors)
    validate_indexes(root, records, errors)
    validate_clue_matrix(root, records, assets_by_id, errors)
    validate_session_preflight(root, errors)
    validate_dm_cheat_sheet(root, errors)
    validate_session_run_sheet(root, errors)
    validate_readiness_report(root, errors)

    for asset_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            rendered = ", ".join(str(relative(path, root)) for path in paths)
            errors.append(diagnostic(rendered, "ID_DUPLICATE", f"ID {asset_id!r} is used more than once.", "Keep one canonical asset and update all references to its stable ID."))

    return sorted(set(errors)), sorted(set(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=ROOT / "adventure",
        help="path to an adventure directory (default: ./adventure)",
    )
    args = parser.parse_args()
    root = args.path.resolve()
    if not root.is_dir():
        parser.error(f"adventure directory not found: {root}")

    errors, warnings = validate(root)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
