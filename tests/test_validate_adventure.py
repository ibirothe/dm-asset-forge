#!/usr/bin/env python3
"""Regression tests for type-aware adventure validation."""

from __future__ import annotations

import hashlib
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_adventure.py"
MODULE_SPEC = importlib.util.spec_from_file_location("validate_adventure", VALIDATOR_PATH)
assert MODULE_SPEC and MODULE_SPEC.loader
VALIDATOR = importlib.util.module_from_spec(MODULE_SPEC)
sys.modules[MODULE_SPEC.name] = VALIDATOR
MODULE_SPEC.loader.exec_module(VALIDATOR)


class AdventureValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="dm-asset-forge-test-", dir=ROOT.parent
        )
        self.repo = Path(self.temporary.name) / "repo"
        shutil.copytree(
            ROOT,
            self.repo,
            ignore=self.copy_ignore,
        )
        self.run_script("init_adventure.py", "--slug", "schema-test", "--title", "Schema-Test")
        self.create("world", "schema-test", "Schema-Test", "--overwrite")
        self.create("location", "hafen", "Hafen")
        self.create("npc", "mara", "Mara", "--location", "hafen")
        self.create("information", "route", "Route", "--location", "hafen")
        self.create("faction", "laterne", "Laterne")
        self.create("visual", "portrait", "Portrait", "--subject", "npc-mara")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @property
    def adventure(self) -> Path:
        return self.repo / "adventure"

    @staticmethod
    def copy_ignore(directory: str, names: list[str]) -> set[str]:
        ignored = {"__pycache__"} if "__pycache__" in names else set()
        if Path(directory).resolve() == ROOT and "adventure" in names:
            ignored.add("adventure")
        return ignored

    def run_script(self, name: str, *arguments: str) -> None:
        subprocess.run(
            ["python3", str(self.repo / "scripts" / name), *arguments],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )

    def create(self, asset_type: str, slug: str, title: str, *arguments: str) -> None:
        self.run_script(
            "new_asset.py",
            "--type",
            asset_type,
            "--slug",
            slug,
            "--title",
            title,
            *arguments,
        )

    def validate(self) -> tuple[list[str], list[str]]:
        return VALIDATOR.validate(self.adventure)

    def test_all_fourteen_types_pass_at_canonical_paths(self) -> None:
        self.create("scene", "ankunft", "Ankunft", "--location", "hafen")
        self.create("creature", "nebelvogel", "Nebelvogel", "--location", "hafen")
        self.create("object", "schluessel", "Schlüssel", "--location", "hafen")
        self.create("encounter", "kontrolle", "Kontrolle", "--location", "hafen")
        self.create("handout", "brief", "Brief", "--location", "hafen")
        self.create("plot-thread", "fracht", "Fracht")
        self.create("event", "nebel", "Nebel")
        self.create("random-table", "geruechte", "Gerüchte")

        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(
            set(VALIDATOR.ASSET_SPECS),
            {
                "world", "location", "scene", "npc", "creature", "faction",
                "object", "information", "encounter", "plot-thread", "event",
                "handout", "visual", "random-table",
            },
        )

    def test_unknown_key_and_invalid_enum_are_errors_with_hints(self) -> None:
        npc = self.adventure / "30-locations/hafen/npcs/mara/npc.md"
        content = npc.read_text(encoding="utf-8")
        content = content.replace("reach: unknown", "reach: galactic\nunsupported_rating: 12")
        npc.write_text(content, encoding="utf-8")

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[FM_ENUM]", rendered)
        self.assertIn("[FM_UNKNOWN_KEY]", rendered)
        self.assertIn("30-locations/hafen/npcs/mara/npc.md", rendered)
        self.assertIn("Fix:", rendered)

    def test_sections_paths_and_relation_types_are_checked(self) -> None:
        npc = self.adventure / "30-locations/hafen/npcs/mara/npc.md"
        npc.write_text(
            npc.read_text(encoding="utf-8").replace("## Motivation\n", ""),
            encoding="utf-8",
        )
        information = self.adventure / "30-locations/hafen/information/route/information.md"
        information.write_text(
            information.read_text(encoding="utf-8").replace(
                "known_by: []", 'known_by: ["loc-hafen"]'
            ),
            encoding="utf-8",
        )
        wrong = self.adventure / "30-locations/hafen/npcs/wrong/npc.md"
        wrong.parent.mkdir(parents=True)
        shutil.copy2(npc, wrong)
        npc.unlink()

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[SECTION_REQUIRED]", rendered)
        self.assertIn("[ASSET_PATH]", rendered)
        self.assertIn("[REL_TARGET_TYPE]", rendered)

    def test_links_images_placeholders_and_warnings_are_separate(self) -> None:
        faction = self.adventure / "40-global/factions/laterne/faction.md"
        faction.write_text(
            faction.read_text(encoding="utf-8")
            + "\nArmor Class {{UNRESOLVED}} ![Bild](missing.jpg) [Link](missing.md)\n",
            encoding="utf-8",
        )

        errors, warnings = self.validate()
        error_text = "\n".join(errors)
        warning_text = "\n".join(warnings)

        self.assertIn("[CONTENT_PLACEHOLDER]", error_text)
        self.assertIn("[IMAGE_LINK_FORMAT]", error_text)
        self.assertIn("[LINK_BROKEN]", error_text)
        self.assertIn("[CONTENT_SYSTEM_SPECIFIC]", warning_text)
        self.assertNotIn("[CONTENT_SYSTEM_SPECIFIC]", error_text)

    def test_validation_is_read_only(self) -> None:
        before = self.file_hashes()
        self.validate()
        after = self.file_hashes()
        self.assertEqual(before, after)

    def file_hashes(self) -> dict[Path, str]:
        return {
            path.relative_to(self.adventure): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.adventure.rglob("*")
            if path.is_file()
        }


if __name__ == "__main__":
    unittest.main()
