---
name: dm-create-adventure
description: Create and initialize a new system-neutral tabletop RPG adventure in this repository from a user's rough world and plot description. Use when starting a new adventure, campaign, scenario, or module; do not use for editing a single asset in an existing adventure.
---

# Create an adventure

1. Read `AGENTS.md` and the normative `docs/intake-workflow.md`, `docs/asset-katalog.md`, `docs/asset-authoring-guide.md`, `docs/adventure-structure-guide.md`, `docs/metadaten-und-werte.md`, and `docs/beziehungen-und-speicherorte.md` before creating assets.
2. Treat the user's free-form world description and plot or conflict description as the required inputs. Accept an optional title and constraints. Ask only the minimum blocking questions defined by the intake workflow.
3. Confirm that `adventure/` does not exist. Derive a provisional title when needed and a lowercase ASCII kebab-case slug; record an agent-proposed title as an assumption after initialization.
4. Run:

   ```bash
   python3 scripts/init_adventure.py --slug <slug> --title "<title>"
   ```

5. While `adventure/10-world/overview.md` is still the untouched scaffold placeholder, replace it with the canonical World template:

   ```bash
   python3 scripts/new_asset.py --type world --slug <slug> --title "<title>" --overwrite
   ```

   Do not use `--overwrite` if the file already contains authored material.
6. Preserve the complete original request unchanged in `00-input/original-request.md`. Extract only explicit world, plot, and constraint statements into their dedicated input files; store later user answers in `00-input/clarifications.md`.
7. Classify derived work as established fact, clarification, assumption, decision, or open question. Store each category in the file required by the intake workflow and never present a proposed assumption as established canon.
8. Build the restrained world and plot overviews as states rather than a required scene sequence. Provide a clear entry without prescribing player-character motivation, at least two plausible approaches, independent paths to every necessary conclusion, playable consequences for failure or neglect, and multiple possible resolutions. Create only the plot threads, locations, and assets necessary for the entry situation and central conflict, using `scripts/new_asset.py` for all catalog types. Keep them `draft` until they meet their type-specific Definition of Done.
9. Assign canonical ownership and add required links. Update all five indexes, the adventure README, and the change log.
10. Do not generate images during initialization.
11. Check every item in the intake Definition of Done. Run `python3 scripts/validate_adventure.py` and fix structural errors.
12. Return the German completion summary in the exact content order defined by the intake workflow: created state, confirmed basis, assumptions, open questions, validation, and prioritized next steps.

Do not introduce system-specific rules, statistics, difficulty values, or named mechanics. Do not create an example adventure when the user has not supplied a world and plot brief. If `adventure/` already exists, stop initialization and offer to continue editing the existing adventure.
