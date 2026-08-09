---
name: dm-develop-location
description: Develop or revise one location in an existing system-neutral tabletop RPG adventure, grouping its scenes, NPCs, creatures, objects, information, encounters, handouts, and visuals under that location. Use for location design, scene hubs, settlements, rooms, regions, and location-centered content; do not use to initialize a new adventure.
---

# Develop a location

1. Read the root `AGENTS.md`, the normative `docs/asset-katalog.md`, `docs/metadaten-und-werte.md`, and `docs/beziehungen-und-speicherorte.md`, `adventure/README.md`, `adventure/50-indexes/locations.md`, and the target location if it exists.
2. Read only directly related plot threads, world facts, and linked assets needed to maintain continuity.
3. If the location is new, create it with:

   ```bash
   python3 scripts/new_asset.py --type location --slug <slug> --title "<title>"
   ```

4. Give the location a table purpose, immediate impression, sensory identity, access boundaries, usable areas, pressures, and possible change over time. Set qualitative metadata only with documented values.
5. Classify local assets according to the catalog. Create them only when they serve the location or an established plot need. Use `scripts/new_asset.py` for every selected type and pass `--location <location-slug>` for scenes, NPCs, creatures, objects, information, encounters, and handouts.
6. Keep each owned asset canonical under this location. Link visiting, mobile, or otherwise externally owned assets and record only location-specific appearance context instead of copying them.
7. Ensure information has a discovery path and consequence; encounters have a trigger, intentions, leverage, escalation, and outcomes; NPCs have motivation and actionable knowledge.
8. Update the location body, relevant `50-indexes/` files, metadata logs, and cross-links.
9. Run the adventure validator and report changed files plus unresolved continuity questions.

Keep all descriptions system-neutral and table-usable. Do not invent a complete cast or exhaustive room list unless the user requests that scope.
