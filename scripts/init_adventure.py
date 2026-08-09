#!/usr/bin/env python3
"""Create a new adventure directory from the repository template."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "adventure"
ADVENTURE = ROOT / "adventure"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def replace_tokens(path: Path, values: dict[str, str]) -> None:
    if path.suffix != ".md":
        return
    content = path.read_text(encoding="utf-8")
    for token, value in values.items():
        content = content.replace("{{" + token + "}}", value)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="lowercase ASCII kebab-case slug")
    parser.add_argument("--title", required=True, help="human-readable adventure title")
    args = parser.parse_args()

    if not SLUG_PATTERN.fullmatch(args.slug):
        parser.error("--slug must use lowercase ASCII kebab-case")
    if not args.title.strip():
        parser.error("--title must not be empty")
    if not TEMPLATE.is_dir():
        parser.error(f"template directory not found: {TEMPLATE}")

    target = ADVENTURE
    if target.exists():
        parser.error(
            "this repository already contains an adventure workspace: "
            f"{target}"
        )

    shutil.copytree(TEMPLATE, target)
    values = {
        "ADVENTURE_SLUG": args.slug,
        "ADVENTURE_TITLE": args.title.strip(),
        "DATE": dt.date.today().isoformat(),
    }
    for path in target.rglob("*.md"):
        replace_tokens(path, values)

    print(target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
