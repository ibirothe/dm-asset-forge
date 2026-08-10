#!/usr/bin/env python3
"""Create one canonical adventure asset from its type-aware template."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "assets"
VISUAL_PROMPT_TEMPLATE = ROOT / "templates" / "visual-prompt.md"
ADVENTURE = ROOT / "adventure"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
ID_FIELD = re.compile(r"^id:\s*[\"']?([^\"'\s]+)[\"']?\s*$", re.MULTILINE)
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class AssetSpec:
    prefix: str
    scope: str
    placement: str


ASSET_SPECS = {
    "world": AssetSpec("world-", "singleton", "world"),
    "location": AssetSpec("loc-", "local", "location"),
    "scene": AssetSpec("scene-", "local", "local"),
    "npc": AssetSpec("npc-", "local", "local"),
    "player-character": AssetSpec("pc-", "global", "global"),
    "creature": AssetSpec("cre-", "local", "local"),
    "faction": AssetSpec("fac-", "global", "global"),
    "object": AssetSpec("obj-", "local", "local"),
    "information": AssetSpec("info-", "local", "local"),
    "encounter": AssetSpec("enc-", "local", "local"),
    "plot-thread": AssetSpec("plot-", "global", "global"),
    "event": AssetSpec("event-", "global", "global"),
    "handout": AssetSpec("hand-", "local", "local"),
    "visual": AssetSpec("vis-", "subject-owned", "subject"),
    "random-table": AssetSpec("table-", "global", "global"),
}

LOCAL_DIRS = {
    "scene": "scenes",
    "npc": "npcs",
    "creature": "creatures",
    "object": "objects",
    "information": "information",
    "encounter": "encounters",
    "handout": "handouts",
}

GLOBAL_TARGETS = {
    "faction": Path("40-global/factions"),
    "player-character": Path("40-global/player-characters"),
    "plot-thread": Path("20-plot/threads"),
    "event": Path("10-world/events"),
    "random-table": Path("40-global/random-tables"),
}

LOCATION_CHILD_DIRS = (
    "scenes",
    "npcs",
    "creatures",
    "objects",
    "information",
    "encounters",
    "handouts",
    "visuals",
)

LOCATION_SECTION_BY_TYPE = {
    "scene": "Areas",
    "npc": "Inhabitants",
    "creature": "Inhabitants",
    "object": "Objects",
    "information": "Information and secrets",
    "encounter": "Encounters and pressures",
    "handout": "Information and secrets",
}

ASSET_LOCATION_SECTION = {
    "scene": "Related assets",
    "npc": "Locations and movement",
    "creature": "Habitat and movement",
    "object": "Location, ownership, and components",
    "information": "Discovery points",
    "encounter": "Follow-up links",
    "handout": "Delivery",
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
CLUE_MATRIX_PATH = Path("50-indexes/clue-matrix.md")


def require_slug(parser: argparse.ArgumentParser, label: str, value: str) -> None:
    if not SLUG_PATTERN.fullmatch(value):
        parser.error(f"{label} must use lowercase ASCII kebab-case")


def frontmatter_id(path: Path) -> str | None:
    if not path.is_file() or path.suffix != ".md" or path.name.endswith(".prompt.md"):
        return None
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    id_match = ID_FIELD.search(match.group(1))
    return id_match.group(1) if id_match else None


def frontmatter_value(path: Path, key: str) -> str | None:
    if not path.is_file():
        return None
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return None
    field = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", match.group(1), re.MULTILINE)
    if not field:
        return None
    value = field.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value.replace('\\"', '"').replace("\\\\", "\\")


def relative_target(source: Path, target: Path) -> str:
    return os.path.relpath(target, source.parent).replace(os.sep, "/")


def link_resolves_to(source: Path, raw_target: str, target: Path) -> bool:
    value = raw_target.split("#", 1)[0].strip().strip("<>")
    if not value or value.startswith(("http://", "https://", "mailto:")):
        return False
    return (source.parent / value.replace("%20", " ")).resolve() == target.resolve()


def upsert_section_link(
    parser: argparse.ArgumentParser,
    content: str,
    source: Path,
    target: Path,
    label: str,
    heading: str,
    descriptor: str | None = None,
    allow_new_section: bool = False,
) -> str:
    rendered_link = f"[{label}]({relative_target(source, target)})"
    for match in MARKDOWN_LINK.finditer(content):
        if link_resolves_to(source, match.group(2), target):
            return content[: match.start()] + rendered_link + content[match.end() :]

    entry = f"- {descriptor}: {rendered_link}" if descriptor else f"- {rendered_link}"
    section = re.search(
        rf"(^##\s+{re.escape(heading)}\s*$)(.*?)(?=^##\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if section is None:
        if allow_new_section:
            return content.rstrip() + f"\n\n## {heading}\n\n{entry}\n"
        parser.error(f"navigation section '## {heading}' not found: {source}")

    body = section.group(2).rstrip()
    replacement = body + f"\n\n{entry}\n\n"
    return content[: section.start(2)] + replacement + content[section.end(2) :]


def update_existing_link(
    parser: argparse.ArgumentParser,
    source: Path,
    target: Path,
    label: str,
    heading: str,
    descriptor: str | None = None,
    allow_new_section: bool = False,
) -> bool:
    content = source.read_text(encoding="utf-8")
    updated = upsert_section_link(
        parser,
        content,
        source,
        target,
        label,
        heading,
        descriptor,
        allow_new_section,
    )
    if updated == content:
        return False
    source.write_text(updated, encoding="utf-8")
    return True


def index_row(
    asset_type: str,
    asset_id: str,
    title: str,
    target: Path,
    index: Path,
    location_id: str | None,
) -> str:
    link = f"[{title}]({relative_target(index, target)})"
    if asset_type == "location":
        return f"| {asset_id} | {title} | draft | unknown | — | {link} |"
    if asset_type in {"npc", "object"}:
        return f"| {asset_id} | {title} | draft | {location_id} | — | {link} |"
    if asset_type == "player-character":
        return f"| {asset_id} | {title} | draft | — | — | {link} |"
    if asset_type == "information":
        return f"| {asset_id} | {title} | established | {location_id} | — | — | {link} |"
    if asset_type == "plot-thread" and index.name == "open-threads.md":
        return f"| {asset_id} | {title} | draft | — | — | — | {link} |"
    return f"| {asset_id} | {title} | draft | — | {link} |"


def upsert_index_row(index: Path, target: Path, asset_id: str, row: str) -> bool:
    content = index.read_text(encoding="utf-8")
    lines = content.splitlines()
    updated: list[str] = []
    replaced = False
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        target_match = any(
            link_resolves_to(index, match.group(2), target)
            for match in MARKDOWN_LINK.finditer(line)
        )
        id_match = bool(cells) and cells[0] == asset_id
        if target_match or id_match:
            if not replaced:
                generated = [cell.strip() for cell in row.strip().strip("|").split("|")]
                if len(cells) == len(generated):
                    for number in range(1, len(generated) - 1):
                        if generated[number] == "—" and cells[number] not in {"", "—"}:
                            generated[number] = cells[number]
                    row = "| " + " | ".join(generated) + " |"
                updated.append(row)
                replaced = True
            continue
        updated.append(line)
    if not replaced:
        insert_at = max(
            (number for number, line in enumerate(updated) if line.lstrip().startswith("|")),
            default=len(updated) - 1,
        ) + 1
        updated.insert(insert_at, row)
    rendered = "\n".join(updated).rstrip() + "\n"
    if rendered == content:
        return False
    index.write_text(rendered, encoding="utf-8")
    return True


def ensure_clue_matrix_row(
    matrix: Path,
    target: Path,
    location: Path,
    asset_id: str,
    location_id: str,
) -> bool:
    content = matrix.read_text(encoding="utf-8")
    if any(
        link_resolves_to(matrix, match.group(2), target)
        for match in MARKDOWN_LINK.finditer(content)
    ):
        return False
    row = (
        f"| {asset_id} | open | [{asset_id}]({relative_target(matrix, target)}) | — | "
        f"[{location_id}]({relative_target(matrix, location)}) | open | open | none | — | — | — |"
    )
    lines = content.splitlines()
    insert_at = max(
        (number for number, line in enumerate(lines) if line.lstrip().startswith("|")),
        default=len(lines) - 1,
    ) + 1
    lines.insert(insert_at, row)
    rendered = "\n".join(lines).rstrip() + "\n"
    matrix.write_text(rendered, encoding="utf-8")
    return True


def find_asset_paths(asset_id: str) -> list[Path]:
    return sorted(
        path
        for path in ADVENTURE.rglob("*.md")
        if frontmatter_id(path) == asset_id
    )


def location_file(slug: str) -> Path:
    return ADVENTURE / "30-locations" / slug / "location.md"


def require_location(parser: argparse.ArgumentParser, slug: str, label: str) -> Path:
    path = location_file(slug)
    if not path.is_file():
        parser.error(f"{label} not found: {path}")
    if frontmatter_id(path) != f"loc-{slug}":
        parser.error(f"{label} has missing or unexpected ID: {path}")
    return path


def resolve_subject(parser: argparse.ArgumentParser, subject_id: str) -> Path:
    matches = find_asset_paths(subject_id)
    if not matches:
        parser.error(f"--subject asset ID not found: {subject_id}")
    if len(matches) > 1:
        rendered = ", ".join(str(path.relative_to(ROOT)) for path in matches)
        parser.error(f"--subject asset ID is duplicated: {subject_id}: {rendered}")
    return matches[0]


def validate_arguments(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    require_slug(parser, "--slug", args.slug)
    if args.location:
        require_slug(parser, "--location", args.location)
    if args.parent_location:
        require_slug(parser, "--parent-location", args.parent_location)
    if not args.title.strip():
        parser.error("--title must not be empty")
    if "\n" in args.title or "\r" in args.title:
        parser.error("--title must be a single line")
    if "|" in args.title or "]" in args.title:
        parser.error("--title must not contain '|' or ']' because navigation uses Markdown tables and links")

    local_types = set(LOCAL_DIRS)
    if args.type in local_types and not args.location:
        parser.error(f"--location is required for {args.type}")
    if args.type not in local_types and args.location:
        parser.error(f"--location is not valid for {args.type}")
    if args.type != "location" and args.parent_location:
        parser.error(f"--parent-location is not valid for {args.type}")
    if args.type == "visual" and not args.subject:
        parser.error("--subject is required for visual and must be an existing asset ID")
    if args.type != "visual" and args.subject:
        parser.error(f"--subject is not valid for {args.type}")


def destination(
    asset_type: str,
    slug: str,
    location: str | None,
    subject_path: Path | None,
) -> Path:
    if asset_type == "world":
        return ADVENTURE / "10-world" / "overview.md"
    if asset_type == "location":
        return ADVENTURE / "30-locations" / slug / "location.md"
    if asset_type in LOCAL_DIRS:
        assert location is not None
        return (
            ADVENTURE
            / "30-locations"
            / location
            / LOCAL_DIRS[asset_type]
            / slug
            / f"{asset_type}.md"
        )
    if asset_type in GLOBAL_TARGETS:
        return ADVENTURE / GLOBAL_TARGETS[asset_type] / slug / f"{asset_type}.md"
    if asset_type == "visual":
        assert subject_path is not None
        return subject_path.parent / "visuals" / slug / "visual.md"
    raise AssertionError(f"unsupported asset type: {asset_type}")


def render_template(
    parser: argparse.ArgumentParser,
    template: Path,
    values: dict[str, str],
) -> str:
    if not template.is_file():
        parser.error(f"asset template not found: {template}")
    content = template.read_text(encoding="utf-8")
    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)
    unresolved = sorted(set(PLACEHOLDER.findall(content)))
    if unresolved:
        parser.error(
            f"unresolved template placeholders in {template}: {', '.join(unresolved)}"
        )
    return content


def validate_target(
    parser: argparse.ArgumentParser,
    target: Path,
    asset_id: str,
    overwrite: bool,
) -> None:
    matches = find_asset_paths(asset_id)
    other_matches = [path for path in matches if path.resolve() != target.resolve()]
    if other_matches:
        rendered = ", ".join(str(path.relative_to(ROOT)) for path in other_matches)
        parser.error(f"asset ID already exists: {asset_id}: {rendered}")

    if target.exists():
        if not target.is_file():
            parser.error(f"asset target is not a file: {target}")
        target_id = frontmatter_id(target)
        if target_id is not None and target_id != asset_id:
            parser.error(
                f"target contains a different asset ID: {target_id}: {target}"
            )
        if not overwrite:
            parser.error(
                f"asset already exists: {target}; pass --overwrite to replace it"
            )
        return

    if target.parent.exists() and any(target.parent.iterdir()):
        parser.error(f"asset slug directory already contains files: {target.parent}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=(
            "Examples: --type npc --location old-harbor --slug mara --title 'Mara'; "
            "--type visual --subject npc-mara --slug portrait --title 'Mara portrait'"
        ),
    )
    parser.add_argument("--type", required=True, choices=tuple(ASSET_SPECS))
    parser.add_argument("--slug", required=True, help="asset slug")
    parser.add_argument("--title", required=True, help="human-readable asset title")
    parser.add_argument("--location", help="primary location slug for a local asset")
    parser.add_argument("--parent-location", help="optional parent slug for a location")
    parser.add_argument("--subject", help="existing Subject-Asset ID for a visual")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="explicitly replace the canonical target and visual prompt if they exist",
    )
    args = parser.parse_args()

    validate_arguments(parser, args)
    if not ADVENTURE.is_dir():
        parser.error(
            "adventure workspace not found; initialize this repository first: "
            f"{ADVENTURE}"
        )

    if args.location:
        require_location(parser, args.location, "primary location")
    if args.parent_location:
        require_location(parser, args.parent_location, "parent location")

    subject_path = resolve_subject(parser, args.subject) if args.subject else None
    target = destination(args.type, args.slug, args.location, subject_path)
    spec = ASSET_SPECS[args.type]
    asset_id = spec.prefix + args.slug
    validate_target(parser, target, asset_id, args.overwrite)

    visual_prompt_target: Path | None = None
    if args.type == "visual":
        visual_prompt_target = target.parent / f"{args.slug}.prompt.md"
        if visual_prompt_target.exists() and not args.overwrite:
            parser.error(
                f"visual prompt already exists: {visual_prompt_target}; "
                "pass --overwrite to replace it"
            )
        if visual_prompt_target.exists() and not visual_prompt_target.is_file():
            parser.error(f"visual prompt target is not a file: {visual_prompt_target}")

    values = {
        "SLUG": args.slug,
        "TITLE": args.title.strip().replace("\\", "\\\\").replace('"', '\\"'),
        "LOCATION_ID": f"loc-{args.location}" if args.location else "",
        "PARENT_LOCATION_ID": (
            f'"loc-{args.parent_location}"' if args.parent_location else "null"
        ),
        "SUBJECT_ID": args.subject or "",
        "DATE": dt.date.today().isoformat(),
    }
    template = TEMPLATES / f"{args.type}.md"
    content = render_template(parser, template, values)
    visual_prompt_content = (
        render_template(parser, VISUAL_PROMPT_TEMPLATE, values)
        if visual_prompt_target is not None
        else None
    )

    navigation_updates: list[tuple[Path, Path, str, str, str | None, bool]] = []
    if args.type in LOCAL_DIRS:
        assert args.location is not None
        owner = location_file(args.location)
        owner_title = frontmatter_value(owner, "title") or args.location
        content = upsert_section_link(
            parser,
            content,
            target,
            owner,
            owner_title,
            ASSET_LOCATION_SECTION[args.type],
            "Primary location",
        )
        navigation_updates.append(
            (
                owner,
                target,
                args.title.strip(),
                LOCATION_SECTION_BY_TYPE[args.type],
                None,
                False,
            )
        )

    if args.type == "location" and args.parent_location:
        parent = location_file(args.parent_location)
        parent_title = frontmatter_value(parent, "title") or args.parent_location
        content = upsert_section_link(
            parser,
            content,
            target,
            parent,
            parent_title,
            "Connections",
            "Parent location",
        )
        navigation_updates.append(
            (parent, target, args.title.strip(), "Areas", "Child location", False)
        )

    if args.type == "visual" and subject_path is not None:
        subject_title = frontmatter_value(subject_path, "title") or args.subject or "Subject"
        content = upsert_section_link(
            parser,
            content,
            target,
            subject_path,
            subject_title,
            "Subject",
            "Canonical subject",
        )
        subject_content = subject_path.read_text(encoding="utf-8")
        subject_headings = set(SECTION.findall(subject_content))
        visual_heading = (
            "Visual reference"
            if "Visual reference" in subject_headings
            else "Related assets"
            if "Related assets" in subject_headings
            else "Visuals"
        )
        navigation_updates.append(
            (
                subject_path,
                target,
                args.title.strip(),
                visual_heading,
                "Visual",
                visual_heading == "Visuals",
            )
        )

    index_updates: list[tuple[Path, str]] = []
    for relative_index in INDEX_PATHS.get(args.type, ()):
        index = ADVENTURE / relative_index
        if not index.is_file():
            parser.error(f"navigation index not found: {index}")
        index_updates.append(
            (
                index,
                index_row(
                    args.type,
                    asset_id,
                    args.title.strip(),
                    target,
                    index,
                    f"loc-{args.location}" if args.location else None,
                ),
            )
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    if args.type == "location":
        for child in LOCATION_CHILD_DIRS:
            (target.parent / child).mkdir(exist_ok=True)
    elif args.type == "world":
        (target.parent / "events").mkdir(exist_ok=True)

    if visual_prompt_target is not None and visual_prompt_content is not None:
        visual_prompt_target.write_text(visual_prompt_content, encoding="utf-8")

    changed_navigation: set[Path] = set()
    for source, linked_target, label, heading, descriptor, allow_new_section in navigation_updates:
        if update_existing_link(
            parser,
            source,
            linked_target,
            label,
            heading,
            descriptor,
            allow_new_section,
        ):
            changed_navigation.add(source)
    for index, row in index_updates:
        if upsert_index_row(index, target, asset_id, row):
            changed_navigation.add(index)
    if args.type == "information":
        assert args.location is not None
        clue_matrix = ADVENTURE / CLUE_MATRIX_PATH
        if not clue_matrix.is_file():
            parser.error(f"global clue matrix not found: {clue_matrix}")
        location = location_file(args.location)
        if ensure_clue_matrix_row(
            clue_matrix,
            target,
            location,
            asset_id,
            f"loc-{args.location}",
        ):
            changed_navigation.add(clue_matrix)

    print(target.relative_to(ROOT))
    if visual_prompt_target is not None:
        print(visual_prompt_target.relative_to(ROOT))
    for path in sorted(changed_navigation):
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
