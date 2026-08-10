---
name: dm-create-adventure
description: Create and initialize one complete system-neutral tabletop RPG one-shot in this repository from a user's rough world and plot description. Use when starting a new one-shot; do not use for editing a single asset in an existing adventure.
---

# Create an adventure

1. Always read `AGENTS.md`, `docs/intake-workflow.md`, and `docs/adventure-structure-guide.md`. Do not load every normative guide up front.
2. Load references when their decisions become active: `docs/asset-katalog.md` before selecting asset types; only the selected type sections of `docs/asset-authoring-guide.md` before drafting those assets; `docs/metadaten-und-werte.md` before assigning frontmatter or qualitative values; `docs/beziehungen-und-speicherorte.md` before assigning ownership or relations; and `docs/player-character-workflow.md` before drafting a Player Character release.
3. Treat the user's free-form world description and plot or conflict description as the required inputs. Accept an optional title, target duration, content density, player role, tone, themes, focus, content boundaries, group details, schedule, Safety tools, accessibility needs, play mode, and technical requirements. Do not turn optional fields into a questionnaire. Ask only the minimum blocking questions defined by the intake workflow and record non-blocking missing preferences as `open`.
4. Confirm that `adventure/` does not exist. Derive a provisional title when needed and a lowercase ASCII kebab-case slug; record an agent-proposed title as an assumption after initialization.
5. Run:

   ```bash
   python3 scripts/init_adventure.py --slug <slug> --title "<title>"
   ```

6. While `adventure/10-world/overview.md` is still the untouched scaffold placeholder, replace it with the canonical World template:

   ```bash
   python3 scripts/new_asset.py --type world --slug <slug> --title "<title>" --overwrite
   ```

   Do not use `--overwrite` if the file already contains authored material.
7. Preserve the complete original request unchanged in `00-input/original-request.md`. Extract only explicit world, plot, and constraint statements into their dedicated input files; store later user answers in `00-input/clarifications.md`.
8. Classify derived work as established fact, clarification, assumption, decision, or open question. Store each category in the file required by the intake workflow and never present a proposed assumption as established canon.
9. Before creating assets, record the compact one-shot premise in `20-plot/overview.md`: player-facing starting situation, central conflict, at least two broad forms of player influence, and the resolution boundary. Record target duration, content density, player role, tone, themes, focus, and content boundaries in `00-input/constraints.md`; record session logistics and readiness in `00-input/session-preflight.md`. Preserve missing answers as `open`, link target duration and content boundaries from the preflight to `constraints.md`, and link material uncertainty to assumptions or open questions.
10. Define qualitative pacing in `20-plot/overview.md`: minimum resolution state; `core`, `supporting`, and `optional` content; at least one safe cut with its impact; and `late pressure` as an established state change that preserves player choice. Give every active Plot Thread a minimum resolution state, must-preserve information, and safe cuts. Treat the three content labels as prose, never metadata. Do not calculate runtime or prescribe a Scene order.
11. Build the restrained world and plot overviews as states rather than a required scene sequence. Provide a clear entry without prescribing player-character motivation, independent paths to every necessary conclusion, playable consequences for failure or neglect, and multiple possible resolutions. Create only the plot threads, locations, and assets necessary for the complete one-shot. Do not defer required parts of the central conflict. Use `scripts/new_asset.py` for all catalog types and keep them `draft` until they meet their type-specific Definition of Done.
12. Assign canonical ownership and add required links. Inspect the navigation files reported by `scripts/new_asset.py`, which maintains applicable indexes and deterministic owner, Parent, or Subject links without duplicates. Give every row in the six existing indexes one short table-use context and one canonical link. Complete `adventure/README.md` as the concise table guide: starting situation, central conflict, current pressure, central actors, necessary information, possible resolutions, relevant consequence states, and a short link to pacing and safe cuts. Link every central asset directly or through one matching index; never copy its full description into navigation. Complete contextual reciprocal links and the change log without repeating existing navigation entries.
13. Complete `50-indexes/clue-matrix.md` after creating the Information assets. Use one row per concrete discovery path, reuse one lowercase kebab-case conclusion key across its alternatives, and classify it as `necessary`, `optional`, or `open`. Every necessary conclusion needs at least two different independence groups and distinct source or access paths. Link stable Information, source, discovery-location, and related Plot-Thread IDs. Keep statement, truth status, limits, and full discovery logic only in canonical Information assets.
14. Complete `60-session/dm-cheat-sheet.md` as the compact runtime view. Include only the immediately necessary opening, pressure, locations, NPC intent and Voice cues, critical conclusions with independent fallback paths, escalation, safe cuts, minimum resolution, and possible endings. Link every row to Plot, index, clue matrix, or canonical Asset and introduce no new canon.
15. Complete `60-session/run-sheet.md` as the flexible timing and state-control view. Carry over optional time anchors from `00-input/session-preflight.md`; preserve multiple openings and endings; and derive movable phases, checkpoints, late pressure, safe cuts, the latest finale trigger, minimum resolution, and live-note prompts from the canonical Plot and indexes. Do not prescribe a Scene order, single clue path, or new Plot logic.
16. Do not generate images during initialization. A requested Player Character may be created as a canonical draft, but do not create its `player.md` without presenting and obtaining approval for the exact release draft.
17. Check every item in the intake Definition of Done. Run `python3 scripts/validate_adventure.py` and fix structural errors.
18. Return the German completion summary in the exact content order defined by the intake workflow: created state, confirmed basis, assumptions, open questions, validation, and prioritized next steps.

Do not introduce system-specific rules, statistics, difficulty values, or named mechanics. Do not create an example adventure when the user has not supplied a world and plot brief. If `adventure/` already exists, stop initialization and offer to continue editing the existing adventure.
