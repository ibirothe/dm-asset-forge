---
name: dm-develop-location
description: Develop or revise one location in an existing system-neutral tabletop RPG one-shot, grouping its scenes, NPCs, creatures, objects, information, encounters, handouts, and visuals under that location. Use for location design, scene hubs, settlements, rooms, regions, and location-centered content; do not use to initialize a new one-shot.
---

# Develop a location

1. Always read the root `AGENTS.md`, the `location` section of `docs/asset-katalog.md` and `docs/asset-authoring-guide.md`, `adventure/README.md`, `adventure/50-indexes/locations.md`, and the target location if it exists. When the scope creates or changes Information assets, also read `adventure/50-indexes/clue-matrix.md`. Do not load unrelated guide sections.
2. Load additional references only when the task requires them: `docs/adventure-structure-guide.md` for local choices, states, information paths, or relevant scene-like assets; `docs/metadaten-und-werte.md` when changing frontmatter or qualitative values; and `docs/beziehungen-und-speicherorte.md` when parentage, ownership, appearances, movement, or cross-links are involved.
3. Read only directly related plot threads, world facts, and linked assets needed to maintain continuity.
4. If the location is new, create it with:

   ```bash
   python3 scripts/new_asset.py --type location --slug <slug> --title "<title>"
   ```

5. Apply the `location` section of the authoring guide. Give the location a table purpose, immediate impression, sensory identity, access boundaries, usable areas, pressures, and possible change over time. Set qualitative metadata only with documented values.
6. Classify local assets according to the catalog. Before drafting another asset type, load only its catalog row and authoring-guide section. Create it only when it serves the location or an established plot need. Use `scripts/new_asset.py` for every selected type and pass `--location <location-slug>` for scenes, NPCs, creatures, objects, information, encounters, and handouts.
7. Keep each owned asset canonical under this location. Link visiting, mobile, or otherwise externally owned assets and record only location-specific appearance context instead of copying them.
8. Apply the matching authoring-guide section to every local asset and the adventure-structure guide to local Scenes, Encounters, Information, Events, NPCs, and Factions. Provide multiple approaches and transitions as changed states; do not turn the location into a required scene sequence. Keep assets `draft` until their Definition of Done is met.
9. Inspect the navigation files reported by `scripts/new_asset.py`. Preserve its idempotent Location index and deterministic owner or Parent links; give the Location and every indexed local asset one short action-relevant table context with a single canonical link. For every new or changed Information asset, replace its `open` clue-matrix starter row with concrete source- and discovery-location-linked paths; necessary conclusions need two genuine independence groups and distinct source or access paths. If the Location or one of its assets is central, update its direct README route or confirm the route through one matching index. Add only missing contextual cross-links and never duplicate an existing target. Update metadata logs and any other affected indexes.
10. Run the adventure validator and report changed files plus unresolved continuity questions.

Keep all descriptions system-neutral and table-usable. Do not invent a complete cast or exhaustive room list unless the user requests that scope.
