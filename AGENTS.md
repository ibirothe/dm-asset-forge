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

## Start a new adventure

1. Read and follow `docs/intake-workflow.md` as the normative first-pass workflow.
2. Begin with the user's free-form world and plot description. Ask only for missing information that materially blocks a coherent first pass.
3. Before interpreting the content, choose a lowercase ASCII kebab-case slug, initialize the scaffold, and preserve the complete original request unchanged in `adventure/00-input/original-request.md`.
4. Treat `adventure/` as the single active adventure workspace. If it already exists, continue there and never initialize a second adventure in this repository.
5. Store clarifications, assumptions, decisions, and open questions in their separate canonical files. Never present an unconfirmed assumption as an established fact.
6. Create only the locations and assets required for the complete one-shot. Use `scripts/new_asset.py`; it supports all 14 catalog types. Do not copy asset templates manually.
7. Give necessary conclusions independent discovery paths and central situations playable consequences for failure, retreat, or neglect.
8. Do not generate images during initialization.

## Read before editing

For an existing adventure, read in this order:

1. `adventure/README.md`;
2. relevant files in `adventure/50-indexes/` and `adventure/90-meta/open-questions.md`;
3. `adventure/90-meta/assumptions.md` when unconfirmed canon can affect the task;
4. the target location's `location.md` below `adventure/30-locations/`;
5. only the linked assets required for the task.

Do not scan every asset by default. Expand the read set only when relationships or continuity require it.

## Canonical storage

- Store a local asset exactly once under its primary location:
  - `adventure/30-locations/<location>/scenes/<scene>/scene.md`
  - `adventure/30-locations/<location>/npcs/<npc>/npc.md`
  - `adventure/30-locations/<location>/creatures/<creature>/creature.md`
  - `adventure/30-locations/<location>/objects/<object>/object.md`
  - `adventure/30-locations/<location>/information/<information>/information.md`
  - `adventure/30-locations/<location>/encounters/<encounter>/encounter.md`
  - `adventure/30-locations/<location>/handouts/<handout>/handout.md`
- Store factions and random tables under their catalog paths in `adventure/40-global/`, plot threads under `adventure/20-plot/threads/`, and events under `adventure/10-world/events/`.
- Store each visual under `<subject-directory>/visuals/<visual>/visual.md` with its matching prompt file.
- Represent appearances elsewhere with relative Markdown links. Never duplicate the descriptive body.
- Keep `primary_location` stable when only `current_location` or a temporary appearance changes. Move the canonical file only when editorial ownership changes permanently.
- Store relationship targets as stable IDs in frontmatter and add relative Markdown links plus required back-references according to `docs/beziehungen-und-speicherorte.md`.
- Keep all IDs unique and stable after creation. Rename titles without changing IDs.
- Update the relevant files in `adventure/50-indexes/` whenever an asset is added, moved, renamed, or retired.

## Content rules

- Remain system-neutral. Do not introduce armor class, hit points, challenge ratings, difficulty classes, spell slots, named rules, dice formulas, or system-specific stat blocks.
- Keep the scope to one complete one-shot. Do not defer any required part of the central conflict or its possible resolutions to later play.
- Express challenge and capability narratively with context, risks, leverage, and consequences.
- Separate established facts, rumors, secrets, assumptions, and unresolved questions.
- Give every usable asset a purpose at the table, discoverability, and consequences.
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
- Do not claim an image exists until the PNG file exists.
- Do not generate or replace images unless the user requests it or approves a proposed image pass.

## Finish adventure work

1. Resolve or record affected links and contradictions.
2. Update indexes and `adventure/90-meta/change-log.md` when adventure content changed.
3. Run `python3 scripts/validate_adventure.py`.
4. Treat errors as blocking and warnings as findings that require contextual review. Do not suppress or automatically repair a diagnostic without checking its rule and target file.
5. Report created or changed files, unresolved questions, and validation results.

Do not create example adventures in this template repository.
