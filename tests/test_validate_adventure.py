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

    @staticmethod
    def link_count(source: Path, target: Path) -> int:
        return sum(
            1
            for raw_target in VALIDATOR.LINK.findall(source.read_text(encoding="utf-8"))
            if VALIDATOR.resolve_link(source, raw_target) == target.resolve()
        )

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

    def test_approved_player_handout_is_standalone_and_traceable(self) -> None:
        self.create("handout", "brief", "Brief", "--location", "hafen")
        handout = self.adventure / "30-locations/hafen/handouts/brief/handout.md"
        player = handout.parent / "player.md"
        source = handout.read_text(encoding="utf-8")
        source = source.replace("- Status: not-approved", "- Status: approved")
        source = source.replace("- Player file: none", "- Player file: [player.md](player.md)")
        source = source.replace("- Approved source version: none", "- Approved source version: 1")
        source = source.replace("- Approval: none", "- Approval: User approval for this exact draft")
        handout.write_text(source, encoding="utf-8")
        player.write_text("# Brief\n\nTrefft mich bei Sonnenuntergang am alten Kai.\n", encoding="utf-8")

        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_player_handout_leaks_and_missing_approval_are_blocking(self) -> None:
        self.create("handout", "brief", "Brief", "--location", "hafen")
        handout = self.adventure / "30-locations/hafen/handouts/brief/handout.md"
        player = handout.parent / "player.md"
        player.write_text(
            "---\nsource: internal\n---\n\n# Brief\n\n"
            "## DM-only context\n\n[Interne Quelle](handout.md)\n",
            encoding="utf-8",
        )

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[PLAYER_RELEASE_BLOCKED]", rendered)
        self.assertIn("[PLAYER_FRONTMATTER]", rendered)
        self.assertIn("[PLAYER_DM_SECTION]", rendered)
        self.assertIn("[PLAYER_INTERNAL_LINK]", rendered)

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

    def test_generator_keeps_indexes_and_backlinks_idempotent(self) -> None:
        location = self.adventure / "30-locations/hafen/location.md"
        npc = self.adventure / "30-locations/hafen/npcs/mara/npc.md"
        information = self.adventure / "30-locations/hafen/information/route/information.md"
        visual = npc.parent / "visuals/portrait/visual.md"
        npc_index = self.adventure / "50-indexes/npcs.md"
        information_index = self.adventure / "50-indexes/information.md"
        faction_index = self.adventure / "40-global/factions/index.md"

        self.assertEqual(self.link_count(location, npc), 1)
        self.assertEqual(self.link_count(npc, location), 1)
        self.assertEqual(self.link_count(location, information), 1)
        self.assertEqual(self.link_count(information, location), 1)
        self.assertEqual(self.link_count(npc, visual), 1)
        self.assertEqual(self.link_count(visual, npc), 1)
        self.assertIn("| npc-mara | Mara | draft | loc-hafen |", npc_index.read_text(encoding="utf-8"))
        self.assertIn("| info-route | Route | established | loc-hafen |", information_index.read_text(encoding="utf-8"))
        self.assertIn("| fac-laterne | Laterne | draft |", faction_index.read_text(encoding="utf-8"))

        self.create("location", "kai", "Kai", "--parent-location", "hafen")
        child = self.adventure / "30-locations/kai/location.md"
        self.assertEqual(self.link_count(location, child), 1)
        self.assertEqual(self.link_count(child, location), 1)

        self.create("npc", "mara", "Mara Neu", "--location", "hafen", "--overwrite")
        self.assertEqual(self.link_count(location, npc), 1)
        self.assertEqual(self.link_count(npc, location), 1)
        self.assertEqual(npc_index.read_text(encoding="utf-8").count("npcs/mara/npc.md"), 1)
        self.assertIn("| npc-mara | Mara Neu | draft | loc-hafen |", npc_index.read_text(encoding="utf-8"))
        self.assertIn("[Mara Neu](npcs/mara/npc.md)", location.read_text(encoding="utf-8"))

    def test_validator_detects_navigation_drift(self) -> None:
        location = self.adventure / "30-locations/hafen/location.md"
        npc_index = self.adventure / "50-indexes/npcs.md"
        information_index = self.adventure / "50-indexes/information.md"
        faction_index = self.adventure / "40-global/factions/index.md"

        npc_index.write_text(
            npc_index.read_text(encoding="utf-8").replace(
                "| npc-mara | Mara | draft | loc-hafen |",
                "| npc-mara | Alte Mara | ready | loc-hafen |",
            ),
            encoding="utf-8",
        )
        faction_index.write_text(
            "\n".join(
                line
                for line in faction_index.read_text(encoding="utf-8").splitlines()
                if "laterne/faction.md" not in line
            )
            + "\n",
            encoding="utf-8",
        )
        information_row = next(
            line
            for line in information_index.read_text(encoding="utf-8").splitlines()
            if "information/route/information.md" in line
        )
        information_index.write_text(
            information_index.read_text(encoding="utf-8").rstrip()
            + "\n"
            + information_row
            + "\n",
            encoding="utf-8",
        )
        location.write_text(
            "\n".join(
                line
                for line in location.read_text(encoding="utf-8").splitlines()
                if "npcs/mara/npc.md" not in line
            )
            + "\n",
            encoding="utf-8",
        )

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[INDEX_STALE]", rendered)
        self.assertIn("[INDEX_MISSING]", rendered)
        self.assertIn("[INDEX_DUPLICATE]", rendered)
        self.assertIn("[BACKLINK_MISSING]", rendered)

    def test_renamed_retired_asset_keeps_stable_identity_and_index(self) -> None:
        npc = self.adventure / "30-locations/hafen/npcs/mara/npc.md"
        npc.write_text(
            npc.read_text(encoding="utf-8")
            .replace('title: "Mara"', 'title: "Mara Veen"')
            .replace("status: draft", "status: retired", 1)
            .replace("version: 1", "version: 2", 1)
            .replace("# Mara\n", "# Mara Veen\n", 1),
            encoding="utf-8",
        )
        index = self.adventure / "50-indexes/npcs.md"
        index.write_text(
            index.read_text(encoding="utf-8").replace(
                "| npc-mara | Mara | draft | loc-hafen | [Mara]",
                "| npc-mara | Mara Veen | retired | loc-hafen | [Mara Veen]",
            ),
            encoding="utf-8",
        )

        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertIn("id: npc-mara", npc.read_text(encoding="utf-8"))
        self.assertEqual(npc.parent.name, "mara")

    def file_hashes(self) -> dict[Path, str]:
        return {
            path.relative_to(self.adventure): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.adventure.rglob("*")
            if path.is_file()
        }


if __name__ == "__main__":
    unittest.main()
