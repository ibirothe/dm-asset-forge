---
name: dm-create-asset
description: Create or revise one of the 14 structured, system-neutral Dungeon Master asset types in an existing one-shot. Use for focused asset work; use the location skill when the request centers on developing a whole place.
---

# Create or revise an asset

1. Read `AGENTS.md`, the normative `docs/asset-katalog.md`, `docs/asset-authoring-guide.md`, `docs/adventure-structure-guide.md`, `docs/metadaten-und-werte.md`, and `docs/beziehungen-und-speicherorte.md`, the target adventure overview, the relevant index, and the minimum linked context.
2. Determine the asset type, scope, canonical owner, required relations, reverse-link policy, and canonical path from the normative references. Do not substitute another type because its generator already exists.
3. Create any of the 14 catalog types with the asset generator:

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

4. Fill only content that supports preparation, play, or continuity. Apply the matching section of `docs/asset-authoring-guide.md`: minimum content, guiding questions, table-use summary, visibility boundary, Visual decision, anti-patterns, and Definition of Done.
5. For `scene`, `information`, `encounter`, `plot-thread`, `event`, `npc`, or `faction`, apply the relevant state, choice, information-path, consequence, and actor-agency rules from `docs/adventure-structure-guide.md`. Do not prescribe a player action or mandatory scene.
6. Use only documented keys and controlled values. Represent unknown, inapplicable, empty-list, and open values according to the metadata specification instead of fabricating unsupported canon.
7. Keep `status: draft` while a shared or type-specific Definition of Done criterion is missing. Set `ready` only after checking every criterion; template completeness alone is insufficient.
8. Keep the full asset in exactly one canonical file. Inspect the navigation files reported by `scripts/new_asset.py`: it maintains the applicable index and deterministic owner, parent, or Subject links without duplicates. Add only missing contextual links for appearance locations and other structured relationships, and update related assets wherever the relationship model requires a reciprocal link. Never add a second row or link for a target already present.
9. Update `90-meta/change-log.md`; record assumptions and questions in their respective files.
10. Run the adventure validator and summarize the result.

Do not create system mechanics. Do not duplicate an existing asset merely because it appears in another place.
