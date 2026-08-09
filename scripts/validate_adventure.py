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
    "90-meta",
)
REQUIRED_FILES = (
    "README.md",
    "00-input/original-request.md",
    "00-input/world.md",
    "00-input/plot.md",
    "00-input/constraints.md",
    "00-input/clarifications.md",
    "10-world/overview.md",
    "20-plot/overview.md",
    "20-plot/threads/index.md",
    "40-global/factions/index.md",
    "50-indexes/locations.md",
    "50-indexes/npcs.md",
    "50-indexes/objects.md",
    "50-indexes/information.md",
    "50-indexes/open-threads.md",
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
        "Reveals and consequences",
        "Player release",
        "Rendered output",
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
        ("Table purpose", "First impression", "Sensory details", "Access and boundaries", "Areas", "Inhabitants", "Objects", "Information and secrets", "Encounters and pressures", "Connections", "Changes over time", "DM notes"),
    ),
    "scene": spec(
        "scene-", "local", "scene.md", "scenes",
        ("primary_location", "participants", "related_threads", "danger"), ("primary_location",),
        ("Table purpose", "Entry state", "Participants and intentions", "Immediate tension", "Environment and opportunities", "Discoverable information", "Possible transitions", "Changes after the scene", "Related assets"),
    ),
    "npc": spec(
        "npc-", "local", "npc.md", "npcs",
        ("primary_location", "current_location", "origin_location", "appearance_locations", "factions", "influence", "reach"), ("primary_location",),
        ("Table purpose", "First impression", "Appearance and manner", "Voice cues", "Public role", "Locations and movement", "Motivation", "Fear and pressure", "Resources and leverage", "Knowledge", "Relationships", "Likely behavior", "Hooks and consequences", "Visual reference"),
    ),
    "creature": spec(
        "cre-", "local", "creature.md", "creatures",
        ("primary_location", "current_location", "origin_location", "appearance_locations", "danger", "rarity", "reach"), ("primary_location",),
        ("Table purpose", "First impression", "Recognizable features", "Habitat and movement", "Needs and behavior", "Signs and discoverability", "Risks and pressure", "Weaknesses and leverage", "Variations", "Hooks and consequences", "Visual reference"),
    ),
    "faction": spec(
        "fac-", "global", "faction.md", "40-global/factions",
        ("related_locations", "influence", "reach"), (),
        ("Table purpose", "Public identity", "Agenda", "Structure and reach", "Locations and presence", "Resources and leverage", "Methods", "Internal tensions", "Relationships", "Current pressure", "Escalation and consequences"),
    ),
    "object": spec(
        "obj-", "local", "object.md", "objects",
        ("primary_location", "current_location", "origin_location", "appearance_locations", "owner", "part_of", "components", "danger", "rarity", "accessibility"), ("primary_location",),
        ("Table purpose", "Appearance", "Context and origin", "Location, ownership, and components", "Discoverability", "Properties", "Uses and leverage", "Risks and costs", "Related information", "Consequences", "Visual reference"),
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
        ("Player-facing content", "Delivery", "DM-only context", "Reveals and consequences", "Player release", "Rendered output"),
    ),
    "visual": spec(
        "vis-", "subject-owned", "visual.md", "subject",
        ("subject_asset", "output_file"), ("subject_asset", "output_file"),
        ("Table purpose", "Subject", "Canonical visual facts", "Player visibility", "Output", "Provenance and revisions"),
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
    "owner": (False, frozenset({"npc", "faction"})),
    "factions": (True, frozenset({"faction"})),
    "known_by": (True, frozenset({"npc", "faction"})),
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
    elif record.asset_type == "handout":
        validate_handout_release(root, record, errors)


def validate_handout_release(
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
        if player.is_file():
            errors.append(
                diagnostic(
                    relative(player, root),
                    "PLAYER_RELEASE_BLOCKED",
                    "player.md exists although the canonical Handout is not approved.",
                    "Remove the player file or obtain explicit approval and document the current source version.",
                )
            )
        else:
            return

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
                "approved player.md is not linked from its canonical Handout.",
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
                "approved source version does not match the current Handout version.",
                f"Obtain explicit approval for version {current_version} before replacing player.md.",
            )
        )

    approval = PLAYER_RELEASE_APPROVAL.search(source)
    if approval is None or approval.group(1).strip().lower() in {
        "none",
        "pending",
        "not-approved",
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
        errors.append(
            diagnostic(
                player_rel,
                "PLAYER_FRONTMATTER",
                "player.md contains YAML frontmatter.",
                "Remove all metadata from the player-facing file.",
            )
        )
    if HTML_COMMENT.search(player_text):
        errors.append(
            diagnostic(
                player_rel,
                "PLAYER_COMMENT",
                "player.md contains an internal Markdown comment.",
                "Remove comments and working notes from the player-facing file.",
            )
        )
    if not re.search(r"^#\s+\S", player_text, re.MULTILINE):
        errors.append(
            diagnostic(
                player_rel,
                "PLAYER_TITLE",
                "player.md has no readable level-one title.",
                "Add one standalone '# Title' heading.",
            )
        )
    forbidden = PLAYER_FORBIDDEN_HEADINGS.intersection(HEADING.findall(player_text))
    for heading in sorted(forbidden):
        errors.append(
            diagnostic(
                player_rel,
                "PLAYER_DM_SECTION",
                f"player.md contains internal section '## {heading}'.",
                "Remove DM-only and workflow sections from the player-facing file.",
            )
        )
    for raw_target in LINK.findall(player_text) + IMAGE_LINK.findall(player_text):
        if resolve_link(player, raw_target) is not None:
            errors.append(
                diagnostic(
                    player_rel,
                    "PLAYER_INTERNAL_LINK",
                    f"player.md contains repository-relative link {raw_target!r}.",
                    "Remove internal links or express the required player-facing context directly.",
                )
            )


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
                errors.append(diagnostic(rel, "ASSET_TYPE", f"unknown or missing asset type {declared_type!r}.", "Use one of the 14 types from docs/asset-katalog.md."))
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
