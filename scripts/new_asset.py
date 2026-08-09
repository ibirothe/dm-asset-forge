#!/usr/bin/env python3
"""Create a structured adventure asset from a canonical template."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "assets"
ADVENTURES = ROOT / "adventures"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_TYPES = {"npc", "object", "information", "encounter", "handout", "image-brief"}
SUPPORTED_TYPES = {
    "location",
    "npc",
    "object",
    "information",
    "encounter",
    "handout",
    "faction",
    "plot-thread",
    "image-brief",
}


def require_slug(parser: argparse.ArgumentParser, label: str, value: str) -> None:
    if not SLUG_PATTERN.fullmatch(value):
        parser.error(f"{label} must use lowercase ASCII kebab-case")


def destination(adventure: Path, asset_type: str, slug: str, location: str | None) -> Path:
    if asset_type == "location":
        return adventure / "30-locations" / slug / "location.md"
    if asset_type == "faction":
        return adventure / "40-global" / "factions" / slug / "faction.md"
    if asset_type == "plot-thread":
        return adventure / "20-plot" / "threads" / slug / "plot-thread.md"

    assert location is not None
    base = adventure / "30-locations" / location
    if asset_type == "image-brief":
        return base / "images" / f"{slug}.prompt.md"
    plural = {
        "npc": "npcs",
        "object": "objects",
        "information": "information",
        "encounter": "encounters",
        "handout": "handouts",
    }[asset_type]
    return base / plural / slug / f"{asset_type}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adventure", required=True, help="adventure slug")
    parser.add_argument("--type", required=True, choices=sorted(SUPPORTED_TYPES))
    parser.add_argument("--slug", required=True, help="asset slug")
    parser.add_argument("--title", required=True, help="human-readable asset title")
    parser.add_argument("--location", help="primary location slug for local assets")
    args = parser.parse_args()

    require_slug(parser, "--adventure", args.adventure)
    require_slug(parser, "--slug", args.slug)
    if args.location:
        require_slug(parser, "--location", args.location)
    if not args.title.strip():
        parser.error("--title must not be empty")
    if args.type in LOCAL_TYPES and not args.location:
        parser.error(f"--location is required for {args.type}")

    adventure = ADVENTURES / args.adventure
    if not adventure.is_dir():
        parser.error(f"adventure not found: {adventure}")
    if args.location:
        location_file = adventure / "30-locations" / args.location / "location.md"
        if not location_file.is_file():
            parser.error(f"primary location not found: {location_file}")

    template = TEMPLATES / f"{args.type}.md"
    if not template.is_file():
        parser.error(f"asset template not found: {template}")
    target = destination(adventure, args.type, args.slug, args.location)
    if target.exists():
        parser.error(f"asset already exists: {target}")

    values = {
        "SLUG": args.slug,
        "TITLE": args.title.strip(),
        "LOCATION_ID": f"loc-{args.location}" if args.location else "",
        "DATE": dt.date.today().isoformat(),
    }
    content = template.read_text(encoding="utf-8")
    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    if args.type == "location":
        for child in ("npcs", "objects", "information", "encounters", "handouts", "images"):
            (target.parent / child).mkdir(exist_ok=True)

    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
