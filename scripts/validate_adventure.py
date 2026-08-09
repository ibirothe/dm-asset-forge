#!/usr/bin/env python3
"""Validate the structure and internal consistency of one adventure."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
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
ASSET_FILENAMES = {
    "location.md",
    "npc.md",
    "object.md",
    "information.md",
    "encounter.md",
    "handout.md",
    "faction.md",
    "plot-thread.md",
}
COMMON_REQUIRED_KEYS = {"id", "type", "title", "status", "created", "updated"}
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
KEY_VALUE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_]+\}\}")
SYSTEM_TERMS = re.compile(
    r"\b(?:armor class|hit points?|challenge rating|difficulty class|spell slots?|saving throw|"
    r"initiative modifier|trefferpunkte|rüstungsklasse|schwierigkeitsgrad)\b",
    re.IGNORECASE,
)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER.match(text)
    if not match:
        return None
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = KEY_VALUE.match(line)
        if item:
            result[item.group(1)] = item.group(2).strip().strip('"\'')
    return result


def resolve_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    target = target.replace("%20", " ")
    return (source.parent / target).resolve()


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids: defaultdict[str, list[Path]] = defaultdict(list)

    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"missing directory: {relative}")
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing file: {relative}")

    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".gif", ".webp"}:
            errors.append(f"non-PNG image format: {path.relative_to(root)}")
        if not path.is_file() or path.suffix != ".md":
            continue

        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER.search(text):
            errors.append(f"unresolved template placeholder: {relative}")
        if SYSTEM_TERMS.search(text):
            warnings.append(f"possible system-specific term: {relative}")

        is_asset = path.name in ASSET_FILENAMES and "50-indexes" not in relative.parts
        if is_asset or path.name.endswith(".prompt.md") or path == root / "README.md":
            metadata = parse_frontmatter(text)
            if metadata is None:
                errors.append(f"missing YAML frontmatter: {relative}")
            else:
                required = COMMON_REQUIRED_KEYS if path != root / "README.md" else {"id", "type", "title", "status", "created", "updated"}
                missing = sorted(required - metadata.keys())
                if missing:
                    errors.append(f"missing frontmatter keys in {relative}: {', '.join(missing)}")
                if metadata.get("id"):
                    ids[metadata["id"]].append(path)
                if path.name.endswith(".prompt.md") and not metadata.get("output_file", "").lower().endswith(".png"):
                    errors.append(f"image brief output_file must be PNG: {relative}")

        for raw_target in LINK.findall(text):
            resolved = resolve_link(path, raw_target)
            if resolved is not None and not resolved.exists():
                errors.append(f"broken link in {relative}: {raw_target}")

    for asset_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            rendered = ", ".join(str(path.relative_to(root)) for path in paths)
            errors.append(f"duplicate id {asset_id}: {rendered}")

    return errors, warnings


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
