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
        self.create("player-character", "ira", "Ira")
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

    def test_all_fifteen_types_pass_at_canonical_paths(self) -> None:
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
        preflight = self.adventure / "00-input/session-preflight.md"
        self.assertTrue(preflight.is_file())
        self.assertIn("- Preflight status: open", preflight.read_text(encoding="utf-8"))

        trimmed_sections = {
            self.adventure / "30-locations/hafen/location.md": ("## DM notes",),
            self.adventure / "30-locations/hafen/scenes/ankunft/scene.md": ("## Changes after the scene",),
            self.adventure / "30-locations/hafen/npcs/mara/npc.md": ("## Visual reference",),
            self.adventure / "30-locations/hafen/creatures/nebelvogel/creature.md": ("## Variations", "## Visual reference"),
            self.adventure / "30-locations/hafen/objects/schluessel/object.md": ("## Visual reference",),
            self.adventure / "30-locations/hafen/handouts/brief/handout.md": ("## Rendered output",),
        }
        for path, removed in trimmed_sections.items():
            content = path.read_text(encoding="utf-8")
            for heading in removed:
                self.assertNotIn(heading, content)
        self.assertIn("## Visuals", (self.adventure / "30-locations/hafen/npcs/mara/npc.md").read_text(encoding="utf-8"))
        self.assertEqual(
            set(VALIDATOR.ASSET_SPECS),
            {
                "world", "location", "scene", "npc", "player-character", "creature", "faction",
                "object", "information", "encounter", "plot-thread", "event",
                "handout", "visual", "random-table",
            },
        )
        self.assertIn("player-character", VALIDATOR.RELATION_RULES["owner"][1])
        self.assertIn("player-character", VALIDATOR.RELATION_RULES["known_by"][1])

    def test_session_preflight_structure_status_and_constraints_link_are_checked(self) -> None:
        preflight = self.adventure / "00-input/session-preflight.md"
        content = preflight.read_text(encoding="utf-8")
        content = content.replace("## Schedule\n", "")
        content = content.replace("- Preflight status: open", "- Preflight status: pending")
        content = content.replace("(constraints.md", "(clarifications.md")
        preflight.write_text(content, encoding="utf-8")

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[PREFLIGHT_SECTION]", rendered)
        self.assertIn("[PREFLIGHT_STATUS]", rendered)
        self.assertIn("[PREFLIGHT_CONSTRAINTS_LINK]", rendered)

    def test_missing_session_preflight_is_a_structural_error(self) -> None:
        (self.adventure / "00-input/session-preflight.md").unlink()

        errors, _ = self.validate()

        self.assertIn("[STRUCT_FILE]", "\n".join(errors))

    def test_player_character_is_global_indexed_and_can_own_a_visual(self) -> None:
        character = self.adventure / "40-global/player-characters/ira/player-character.md"
        index = self.adventure / "50-indexes/player-characters.md"

        self.assertTrue(character.is_file())
        self.assertEqual(index.read_text(encoding="utf-8").count("pc-ira"), 1)

        self.create("visual", "ira-portrait", "Ira-Porträt", "--subject", "pc-ira")
        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        visual = character.parent / "visuals/ira-portrait/visual.md"
        self.assertTrue(visual.is_file())
        self.assertIn("[Ira-Porträt]", character.read_text(encoding="utf-8"))

    def test_approved_player_character_release_is_standalone_and_traceable(self) -> None:
        character = self.adventure / "40-global/player-characters/ira/player-character.md"
        player = character.parent / "player.md"
        source = character.read_text(encoding="utf-8")
        source = source.replace("- Status: not-approved", "- Status: approved")
        source = source.replace("- Player file: none", "- Player file: [player.md](player.md)")
        source = source.replace("- Approved source version: none", "- Approved source version: 1")
        source = source.replace("- Approval: none", "- Approval: User approved this exact character draft")
        character.write_text(source, encoding="utf-8")
        player.write_text(
            "# Ira\n\n## Konzept\n\nEine aufmerksame Reisende.\n\n"
            "## Offene Entscheidungen\n\nDu entscheidest, wem Ira vertraut.\n",
            encoding="utf-8",
        )

        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_player_character_release_blocks_dm_content_and_unapproved_file(self) -> None:
        character = self.adventure / "40-global/player-characters/ira/player-character.md"
        player = character.parent / "player.md"
        player.write_text(
            "---\nsource: internal\n---\n\n# Ira\n\n"
            "## DM-only connections\n\n[Interne Quelle](player-character.md)\n",
            encoding="utf-8",
        )

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[PLAYER_RELEASE_BLOCKED]", rendered)
        self.assertIn("[PLAYER_FRONTMATTER]", rendered)
        self.assertIn("[PLAYER_DM_SECTION]", rendered)
        self.assertIn("[PLAYER_INTERNAL_LINK]", rendered)

    def test_player_character_relationship_types_are_checked(self) -> None:
        character = self.adventure / "40-global/player-characters/ira/player-character.md"
        source = character.read_text(encoding="utf-8")
        character.write_text(
            source.replace("related_factions: []", "related_factions: [loc-hafen]"),
            encoding="utf-8",
        )

        errors, _ = self.validate()

        self.assertIn("[REL_TARGET_TYPE]", "\n".join(errors))

    def test_legacy_optional_sections_remain_compatible(self) -> None:
        self.create("scene", "ankunft", "Ankunft", "--location", "hafen")
        self.create("creature", "nebelvogel", "Nebelvogel", "--location", "hafen")
        self.create("object", "schluessel", "Schlüssel", "--location", "hafen")
        self.create("handout", "brief", "Brief", "--location", "hafen")

        legacy_sections = {
            self.adventure / "30-locations/hafen/location.md": ("DM notes",),
            self.adventure / "30-locations/hafen/scenes/ankunft/scene.md": ("Changes after the scene",),
            self.adventure / "30-locations/hafen/npcs/mara/npc.md": ("Visual reference",),
            self.adventure / "30-locations/hafen/creatures/nebelvogel/creature.md": ("Variations", "Visual reference"),
            self.adventure / "30-locations/hafen/objects/schluessel/object.md": ("Visual reference",),
            self.adventure / "30-locations/hafen/handouts/brief/handout.md": ("Rendered output",),
        }
        for path, headings in legacy_sections.items():
            content = path.read_text(encoding="utf-8").rstrip()
            content += "\n\n" + "\n\n".join(f"## {heading}\n\nLegacy content." for heading in headings) + "\n"
            path.write_text(content, encoding="utf-8")

        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

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

    def test_current_visual_png_has_matching_approval_and_provenance(self) -> None:
        visual = self.adventure / "30-locations/hafen/npcs/mara/visuals/portrait/visual.md"
        png = visual.parent / "portrait.png"
        source = visual.read_text(encoding="utf-8")
        source = source.replace("provenance: unknown", "provenance: agent-generated")
        source = source.replace("- Status: not-approved", "- Status: approved")
        source = source.replace("- PNG state: not-created", "- PNG state: current")
        source = source.replace("- Approved visual version: none", "- Approved visual version: 1")
        source = source.replace("- Approval: none", "- Approval: User approved version 1 and its exact prompt")
        visual.write_text(source, encoding="utf-8")
        png.write_bytes(b"\x89PNG\r\n\x1a\n")

        errors, warnings = self.validate()

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_visual_prompt_drift_and_unapproved_png_are_blocking(self) -> None:
        visual = self.adventure / "30-locations/hafen/npcs/mara/visuals/portrait/visual.md"
        prompt = visual.parent / "portrait.prompt.md"
        png = visual.parent / "portrait.png"
        prompt.write_text(
            prompt.read_text(encoding="utf-8")
            .replace("## Identity anchors\n", "")
            .replace("`portrait.png`", "`wrong.png`"),
            encoding="utf-8",
        )
        png.write_bytes(b"\x89PNG\r\n\x1a\n")

        errors, _ = self.validate()
        rendered = "\n".join(errors)

        self.assertIn("[VISUAL_PROMPT_SECTION]", rendered)
        self.assertIn("[VISUAL_PROMPT_OUTPUT]", rendered)
        self.assertIn("[VISUAL_PNG_STATE]", rendered)
        self.assertIn("[VISUAL_PNG_APPROVAL]", rendered)

    def test_handout_png_requires_a_regular_visual_asset(self) -> None:
        self.create("handout", "brief", "Brief", "--location", "hafen")
        handout = self.adventure / "30-locations/hafen/handouts/brief/handout.md"
        player = handout.parent / "player.md"
        source = handout.read_text(encoding="utf-8")
        source = source.replace("- Status: not-approved", "- Status: approved")
        source = source.replace("- Player file: none", "- Player file: [player.md](player.md)")
        source = source.replace("- Approved source version: none", "- Approved source version: 1")
        source = source.replace("- Approval: none", "- Approval: User approved this exact player draft")
        handout.write_text(source, encoding="utf-8")
        player.write_text("# Brief\n\nTrefft mich am alten Kai.\n", encoding="utf-8")
        (handout.parent / "player.png").write_bytes(b"\x89PNG\r\n\x1a\n")

        errors, _ = self.validate()
        self.assertIn("[PNG_ORPHAN]", "\n".join(errors))

        (handout.parent / "player.png").unlink()
        self.create("visual", "player", "Brief – Spielerfassung", "--subject", "hand-brief")
        visual = handout.parent / "visuals/player/visual.md"
        visual_source = visual.read_text(encoding="utf-8")
        visual_source = visual_source.replace("provenance: unknown", "provenance: agent-generated")
        visual_source = visual_source.replace("- Status: not-approved", "- Status: approved")
        visual_source = visual_source.replace("- PNG state: not-created", "- PNG state: current")
        visual_source = visual_source.replace("- Approved visual version: none", "- Approved visual version: 1")
        visual_source = visual_source.replace("- Approval: none", "- Approval: User approved the Handout Visual")
        visual.write_text(visual_source, encoding="utf-8")
        (visual.parent / "player.png").write_bytes(b"\x89PNG\r\n\x1a\n")

        errors, warnings = self.validate()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

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

        self.assertIn("| Current pressure | Link |", (self.adventure / "50-indexes/locations.md").read_text(encoding="utf-8"))
        self.assertIn("| Immediate intent | Link |", npc_index.read_text(encoding="utf-8"))
        self.assertIn("| Table relevance | Discovery paths | Link |", information_index.read_text(encoding="utf-8"))

        npc_index.write_text(
            npc_index.read_text(encoding="utf-8").replace(
                "| npc-mara | Mara | draft | loc-hafen | — |",
                "| npc-mara | Mara | draft | loc-hafen | Sucht sofort die gestohlene Fracht. |",
            ),
            encoding="utf-8",
        )

        self.create("location", "kai", "Kai", "--parent-location", "hafen")
        child = self.adventure / "30-locations/kai/location.md"
        self.assertEqual(self.link_count(location, child), 1)
        self.assertEqual(self.link_count(child, location), 1)

        self.create("npc", "mara", "Mara Neu", "--location", "hafen", "--overwrite")
        self.assertEqual(self.link_count(location, npc), 1)
        self.assertEqual(self.link_count(npc, location), 1)
        self.assertEqual(npc_index.read_text(encoding="utf-8").count("npcs/mara/npc.md"), 1)
        self.assertIn("| npc-mara | Mara Neu | draft | loc-hafen |", npc_index.read_text(encoding="utf-8"))
        self.assertIn("Sucht sofort die gestohlene Fracht.", npc_index.read_text(encoding="utf-8"))
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
                "| npc-mara | Mara | draft | loc-hafen | — | [Mara]",
                "| npc-mara | Mara Veen | retired | loc-hafen | — | [Mara Veen]",
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
