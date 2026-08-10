# Repository instructions

## Purpose

Use this repository to create and maintain exactly one self-contained, system-neutral tabletop role-playing one-shot. The complete central conflict must be playable and resolvable within that one-shot. Keep user-facing guidance in German and technical identifiers, folder names, file names, YAML keys, and IDs in English.

Read `docs/asset-katalog.md` before selecting an asset type or canonical path. Treat it as the normative type source; do not substitute a different type merely because its template or generator already exists.
Read `docs/asset-authoring-guide.md` before drafting or assessing asset content. Use its type-specific minimum content, table-use guidance, anti-patterns, and Definition of Done.
Read `docs/adventure-structure-guide.md` before designing or assessing entry situations, choices, information paths, consequences, plot progression, or resolutions. Prepare state changes rather than a required scene sequence.
Read `docs/adventure-audit-guide.md` before auditing an adventure. Keep validator diagnostics separate from narrative findings and never change content without an explicit fix request.
Read `docs/metadaten-und-werte.md` before creating or changing frontmatter. Treat it as the normative source for shared keys, controlled values, qualitative scales, and missing-value semantics.
Read `docs/beziehungen-und-speicherorte.md` before creating or changing ownership, location relations, appearances, movement, components, or reciprocal links.
Read `docs/validierung.md` before interpreting validator diagnostics or changing validation rules.
Read `docs/player-handout-workflow.md` before creating or replacing a player-facing Handout file. Never infer approval from asset status or an earlier release.
Read `docs/player-character-workflow.md` before creating or replacing a Player Character's player-facing file. Preserve open character decisions and never infer approval from asset status or an earlier release.
Read `docs/bild-workflow.md` before creating or revising a Visual brief or generating or replacing a PNG. Keep the Subject as the identity source and require approval for the exact Visual version before image generation.

## Start a new adventure

1. Read and follow `docs/intake-workflow.md` as the normative first-pass workflow.
2. Begin with the user's free-form world and plot description. Ask only for missing information that materially blocks a coherent first pass.
3. Before interpreting the content, choose a lowercase ASCII kebab-case slug, initialize the scaffold, and preserve the complete original request unchanged in `adventure/00-input/original-request.md`.
4. Treat `adventure/` as the single active adventure workspace. If it already exists, continue there and never initialize a second adventure in this repository.
5. Store clarifications, assumptions, decisions, and open questions in their separate canonical files. Never present an unconfirmed assumption as an established fact.
6. Before creating assets, record a compact one-shot premise in `adventure/20-plot/overview.md`: player-facing starting situation, central conflict, at least two broad forms of player influence, and the resolution boundary. Record target duration, content density, tone, themes, focus, and content boundaries in `adventure/00-input/constraints.md`; use `open` when the user did not specify them.
7. Record session logistics and readiness in `adventure/00-input/session-preflight.md`. Preserve missing answers as `open`; link target duration and content boundaries from `constraints.md` instead of duplicating them.
8. Define qualitative pacing in `adventure/20-plot/overview.md`: distinguish `core`, `supporting`, and `optional` content in prose; preserve a minimum resolution state; name at least one safe cut and a prepared `late pressure` state change. Give every active Plot Thread its own minimum resolution state, must-preserve information, and safe cuts.
9. Create only the locations and assets required for the complete one-shot. Use `scripts/new_asset.py`; it supports all 15 catalog types. Do not copy asset templates manually.
10. Give necessary conclusions independent discovery paths and central situations playable consequences for failure, retreat, or neglect.
11. Turn `adventure/README.md` into the concise table guide and add a short table-use context to every row in the six existing indexes. Link central actors, necessary information, and resolution-relevant assets directly instead of copying their canonical descriptions.
12. Complete `adventure/50-indexes/clue-matrix.md` as the global derived view of conclusion paths. Give every Information asset at least one row and every necessary conclusion at least two rows with different independence groups and source or access paths. Link stable Information, source, discovery-location, and Plot-Thread IDs; never copy truth or truth status from canonical Information assets.
13. Complete `adventure/60-session/dm-cheat-sheet.md` as the compact runtime view. Include only central locations, NPC intent and Voice cues, critical conclusions with independent fallback paths, escalation, safe cuts, minimum resolution, and possible endings; link every entry to its canonical source.
14. Complete `adventure/60-session/run-sheet.md` as the flexible timing and state-control view. Derive optional times from the session preflight, preserve multiple openings and endings, and use movable phases, checkpoints, late pressure, safe cuts, a latest finale trigger, minimum resolution, and live notes without prescribing a Scene order or adding canon.
15. Do not generate images during initialization. Do not create a Player Character's `player.md` during initialization without explicit approval for the exact release draft.

## Read before editing

For an existing adventure, read in this order:

1. `adventure/README.md`;
2. relevant files in `adventure/50-indexes/` and `adventure/90-meta/open-questions.md`;
3. `adventure/90-meta/assumptions.md` when unconfirmed canon can affect the task;
4. the target location's `location.md` below `adventure/30-locations/`;
5. only the linked assets required for the task.

Do not scan every asset by default. Expand the read set only when relationships or continuity require it.

For preparation and table use, navigate from `adventure/README.md` either directly to a central asset or through exactly one matching index. Treat README and index prose as short derived orientation only; resolve details and canon conflicts in the linked canonical asset.
During play, use `adventure/60-session/dm-cheat-sheet.md` for compact content recall, `adventure/60-session/run-sheet.md` for flexible timing, checkpoints, and state changes, and `adventure/50-indexes/clue-matrix.md` to recover independent clue paths. Treat all three as derived navigation, keep each entry short, and update them whenever a linked source changes materially.

## Canonical storage

- Store a local asset exactly once under its primary location:
  - `adventure/30-locations/<location>/scenes/<scene>/scene.md`
  - `adventure/30-locations/<location>/npcs/<npc>/npc.md`
  - `adventure/30-locations/<location>/creatures/<creature>/creature.md`
  - `adventure/30-locations/<location>/objects/<object>/object.md`
  - `adventure/30-locations/<location>/information/<information>/information.md`
  - `adventure/30-locations/<location>/encounters/<encounter>/encounter.md`
  - `adventure/30-locations/<location>/handouts/<handout>/handout.md`
- Store factions, Player Characters, and random tables under their catalog paths in `adventure/40-global/`, plot threads under `adventure/20-plot/threads/`, and events under `adventure/10-world/events/`.
- Store each visual under `<subject-directory>/visuals/<visual>/visual.md` with its matching prompt file.
- Represent appearances elsewhere with relative Markdown links. Never duplicate the descriptive body.
- Keep `primary_location` stable when only `current_location` or a temporary appearance changes. Move the canonical file only when editorial ownership changes permanently.
- Store relationship targets as stable IDs in frontmatter and add relative Markdown links plus required back-references according to `docs/beziehungen-und-speicherorte.md`.
- Keep an optional player-facing Handout as `player.md` beside its canonical `handout.md`. It has no frontmatter, internal links, or DM-only content and requires explicit approval before creation or replacement.
- Keep an optional player-facing Character file as `player.md` beside its canonical `player-character.md`. It has no frontmatter, internal links, or DM-only content, preserves open player decisions, and requires explicit approval before creation or replacement.
- Represent every Handout PNG as a regular Visual under the Handout's `visuals/<slug>/` directory. Never store `player.png` directly beside `handout.md`.
- Keep all IDs unique and stable after creation. Rename titles without changing IDs.
- Update the relevant files in `adventure/50-indexes/` whenever an asset is added, moved, renamed, retired, or changes its immediate table function. Keep each context cell to one short, action-relevant summary and the final link pointed at the only canonical description.

## Asset lifecycle changes

- Before changing a title, canonical owner, status to `retired`, or combining assets, follow the preflight and exact workflow in `docs/beziehungen-und-speicherorte.md`. Report the canonical target, stable ID, current and proposed paths, affected indexes, incoming links, reciprocal relations, and meta files before writing.
- Preserve ID and `created` for title changes and ownership moves. A title change does not rename the technical slug or path.
- Stop without modifying files when ownership, successor identity, or merged canon is ambiguous. Combining assets requires an explicit user decision about the surviving ID, path, and content.
- Keep retired assets at their canonical path and indexed with `status: retired` unless the user explicitly authorizes deletion after impact review.
- After an approved lifecycle change, update version, date, links, indexes, reciprocal relations, and change log, then run the adventure validator.

## Content rules

- Remain system-neutral. Do not introduce armor class, hit points, challenge ratings, difficulty classes, spell slots, named rules, dice formulas, or system-specific stat blocks.
- Keep the scope to one complete one-shot. Do not defer any required part of the central conflict or its possible resolutions to later play.
- Express challenge and capability narratively with context, risks, leverage, and consequences.
- Separate established facts, rumors, secrets, assumptions, and unresolved questions.
- Give every usable asset a purpose at the table, discoverability, and consequences.
- Keep `adventure/README.md`, `adventure/50-indexes/clue-matrix.md`, `adventure/60-session/dm-cheat-sheet.md`, `adventure/60-session/run-sheet.md`, and index summaries concise and derived. Never introduce canon there that is absent from the linked plot or asset source, and never copy a full canonical description into navigation.
- Never make required progress depend on one prescribed player action, one fragile clue, or one mandatory Scene. Express prerequisites as reachable states.
- Treat player-character background, motivation, loyalty, and decisions as open unless the user explicitly establishes them.
- Keep `status: draft` until the asset meets the shared and type-specific Definition of Done in `docs/asset-authoring-guide.md`; template completeness alone is insufficient.
- Preserve user-authored facts. Make small, targeted edits and never silently rewrite unrelated files.
- Use YAML frontmatter from the matching template in `templates/assets/`.
- Use only keys and controlled values defined in `docs/metadaten-und-werte.md`. Never use an empty string for an unknown, inapplicable, or open value.
- Use ISO dates (`YYYY-MM-DD`) and relative Markdown links.

## Images

- Store final visual assets as `.png`.
- Store visual metadata in `visual.md` and a neighboring `<slug>.prompt.md` brief containing composition, style, exclusions, and output path.
- Separate stable Subject identity, depicted One-Shot state, and allowed stylistic variation. Resolve conflicts before generating an image.
- Do not claim an image exists until the PNG file exists.
- Do not generate or replace images until the user explicitly approves the exact Visual version, prompt, and target path. Keep an older PNG as `stale` after briefing changes until replacement is approved.

## Finish work

Choose exactly one completion path according to the work performed.

### Template or repository work

1. Do not create or update adventure indexes, adventure meta files, or an `adventure/` workspace solely to validate repository changes.
2. Run `python3 scripts/validate_repository.py`.
3. Run `python3 -m unittest discover -s tests -v`.
4. Run any focused check required by a changed script, template, or repository-local skill.
5. Report changed repository files and every validation result.

### Adventure content changes

1. Resolve or record affected links and contradictions.
2. Update the relevant indexes and `adventure/90-meta/change-log.md`.
3. Run `python3 scripts/validate_adventure.py`.
4. Treat errors as blocking and warnings as findings that require contextual review. Do not suppress or automatically repair a diagnostic without checking its rule and target file.
5. Report created or changed adventure files, unresolved questions, and validation results.

### Read-only audit

1. Do not modify adventure content, indexes, meta files, statuses, or repository guidance without an explicit fix request.
2. If `adventure/` exists, run `python3 scripts/validate_adventure.py` as the separate technical basis. If it does not exist, report that the adventure validation is not applicable; do not initialize an adventure for the audit.
3. Apply `docs/adventure-audit-guide.md` and keep technical diagnostics separate from narrative findings.
4. Report the inspected scope, validation availability, findings, and unresolved questions. State explicitly that no files were changed.

Do not create example adventures in this template repository.
