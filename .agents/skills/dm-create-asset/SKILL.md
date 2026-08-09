---
name: dm-create-asset
description: Create or revise one of the 14 structured, system-neutral Dungeon Master asset types in an existing one-shot. Use for focused asset work; use the location skill when the request centers on developing a whole place.
---

# Create or revise an asset

1. Always read `AGENTS.md`, `docs/asset-katalog.md`, the selected type section of `docs/asset-authoring-guide.md`, the target adventure overview, the relevant index, and the minimum linked context. Do not load unrelated guide sections.
2. Load additional references only when the task requires them: `docs/metadaten-und-werte.md` when changing frontmatter or qualitative values; `docs/beziehungen-und-speicherorte.md` when canonical path, ownership, relations, or lifecycle are involved; `docs/adventure-structure-guide.md` for `scene`, `information`, `encounter`, `plot-thread`, `event`, `npc`, or `faction` work involving choices, consequences, agency, or information paths; `docs/player-handout-workflow.md` before creating or replacing a Handout's `player.md`; and `docs/bild-workflow.md` before Visual-brief or PNG work.
3. Determine the asset type, scope, canonical owner, required relations, reverse-link policy, and canonical path from the loaded normative references. Do not substitute another type because its generator already exists.
   For a title change, ownership move, retire request, or asset combination, use the exact lifecycle workflow in `docs/beziehungen-und-speicherorte.md`. Complete and report its preflight before writing. Preserve stable identity, stop on ambiguity, and require the user's explicit choice of surviving ID, path, and canon before combining assets.
4. Create any of the 14 catalog types with the asset generator:

   ```bash
   python3 scripts/new_asset.py \
     --type <type> \
     --location <location-slug-if-required> \
     --parent-location <parent-slug-if-creating-a-child-location> \
     --subject <existing-asset-id-if-creating-a-visual> \
     --slug <slug> \
     --title "<title>"
   ```

   Pass only the type-specific options shown by `python3 scripts/new_asset.py --help`. Never use `--overwrite` unless the user explicitly intends to replace the canonical target; the World placeholder during initial adventure creation is the documented exception.

5. Fill only content that supports preparation, play, or continuity. Apply the matching section of `docs/asset-authoring-guide.md`: minimum content, guiding questions, table-use summary, visibility boundary, Visual decision, anti-patterns, and Definition of Done.
6. For `scene`, `information`, `encounter`, `plot-thread`, `event`, `npc`, or `faction`, apply the relevant state, choice, information-path, consequence, and actor-agency rules from `docs/adventure-structure-guide.md`. Do not prescribe a player action or mandatory scene.
7. Use only documented keys and controlled values. Represent unknown, inapplicable, empty-list, and open values according to the metadata specification instead of fabricating unsupported canon.
8. Keep `status: draft` while a shared or type-specific Definition of Done criterion is missing. Set `ready` only after checking every criterion; template completeness alone is insufficient.
   For a player-facing Handout file, present the complete proposed `player.md`, run the documented Safety-Check, and obtain the user's explicit approval before writing. Never treat an earlier approval as permission to replace an existing player file.
   For a Visual, keep the canonical Subject as identity source, separate stable anchors from depicted state and style, and report conflicts before writing. Present the exact Visual version, prompt, and output path and obtain explicit approval before any PNG generation or replacement. Do not mark a PNG `current` unless the file was successfully stored.
9. Keep the full asset in exactly one canonical file. Inspect the navigation files reported by `scripts/new_asset.py`: it maintains the applicable index and deterministic owner, parent, or Subject links without duplicates. Add only missing contextual links for appearance locations and other structured relationships, and update related assets wherever the relationship model requires a reciprocal link. Never add a second row or link for a target already present.
10. Update `90-meta/change-log.md`; record assumptions and questions in their respective files.
11. Run the adventure validator and summarize the result.

Do not create system mechanics. Do not duplicate an existing asset merely because it appears in another place.
