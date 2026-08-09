# Repository instructions

## Purpose

Use this repository to create and maintain system-neutral tabletop role-playing adventure material. Keep user-facing guidance in German and technical identifiers, folder names, file names, YAML keys, and IDs in English.

Read `docs/asset-katalog.md` before selecting an asset type or canonical path. Treat it as the normative type source; do not substitute a different type merely because its template or generator already exists.

## Start a new adventure

1. Begin with the user's rough world and plot description. Ask only for missing information that blocks a coherent first pass.
2. Choose a lowercase ASCII kebab-case adventure slug and run `python3 scripts/init_adventure.py --slug <slug> --title "<title>"`.
3. Treat `adventure/` as the single active adventure workspace. If it already exists, continue there and never initialize a second adventure in this repository.
4. Preserve the user's original wording in `adventure/00-input/world.md` and `adventure/00-input/plot.md` before interpreting it.
5. Derive only supported facts. Record assumptions in `adventure/90-meta/decisions.md` and unresolved choices in `adventure/90-meta/open-questions.md`.
6. Create locations and assets with `scripts/new_asset.py`; do not copy template files manually when the script supports the asset type.

## Read before editing

For an existing adventure, read in this order:

1. `adventure/README.md`;
2. relevant files in `adventure/50-indexes/` and `adventure/90-meta/open-questions.md`;
3. the target location's `location.md` below `adventure/30-locations/`;
4. only the linked assets required for the task.

Do not scan every asset by default. Expand the read set only when relationships or continuity require it.

## Canonical storage

- Store a local asset exactly once under its primary location:
  - `adventure/30-locations/<location>/npcs/<npc>/npc.md`
  - `adventure/30-locations/<location>/objects/<object>/object.md`
  - `adventure/30-locations/<location>/information/<information>/information.md`
  - `adventure/30-locations/<location>/encounters/<encounter>/encounter.md`
  - `adventure/30-locations/<location>/handouts/<handout>/handout.md`
- Store factions under `adventure/40-global/factions/` and plot threads under `adventure/20-plot/threads/`.
- Represent appearances elsewhere with relative Markdown links. Never duplicate the descriptive body.
- Keep all IDs unique and stable after creation. Rename titles without changing IDs.
- Update the relevant files in `adventure/50-indexes/` whenever an asset is added, moved, renamed, or retired.

## Content rules

- Remain system-neutral. Do not introduce armor class, hit points, challenge ratings, difficulty classes, spell slots, named rules, dice formulas, or system-specific stat blocks.
- Express challenge and capability narratively with context, risks, leverage, and consequences.
- Separate established facts, rumors, secrets, assumptions, and unresolved questions.
- Give every usable asset a purpose at the table, discoverability, and consequences.
- Preserve user-authored facts. Make small, targeted edits and never silently rewrite unrelated files.
- Use YAML frontmatter from the matching template in `templates/assets/`.
- Use ISO dates (`YYYY-MM-DD`) and relative Markdown links.

## Images

- Store final visual assets as `.png`.
- Store a neighboring `.prompt.md` image brief containing subject, composition, style, exclusions, output path, and provenance.
- Do not claim an image exists until the PNG file exists.
- Do not generate or replace images unless the user requests it or approves a proposed image pass.

## Finish work

1. Resolve or record affected links and contradictions.
2. Update indexes and `adventure/90-meta/change-log.md`.
3. Run `python3 scripts/validate_adventure.py`.
4. Report created or changed files, unresolved questions, and validation results.

Do not create example adventures in this template repository.
