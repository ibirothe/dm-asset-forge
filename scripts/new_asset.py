#!/usr/bin/env python3
"""Create one canonical adventure asset from its type-aware template."""

from __future__ import annotations

import argparse
import datetime as dt
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

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    if args.type == "location":
        for child in LOCATION_CHILD_DIRS:
            (target.parent / child).mkdir(exist_ok=True)
    elif args.type == "world":
        (target.parent / "events").mkdir(exist_ok=True)

    if visual_prompt_target is not None and visual_prompt_content is not None:
        visual_prompt_target.write_text(visual_prompt_content, encoding="utf-8")

    print(target.relative_to(ROOT))
    if visual_prompt_target is not None:
        print(visual_prompt_target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
