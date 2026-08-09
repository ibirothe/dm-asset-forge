---
name: dm-develop-location
description: Develop or revise one location in an existing system-neutral tabletop RPG adventure, grouping its NPCs, objects, information, encounters, handouts, and visual briefs under that location. Use for location design, scene hubs, settlements, rooms, regions, and location-centered content; do not use to initialize a new adventure.
---

# Develop a location

1. Read the root `AGENTS.md`, the target adventure `README.md`, `50-indexes/locations.md`, and the target location if it exists.
2. Read only directly related plot threads, world facts, and linked assets needed to maintain continuity.
3. If the location is new, create it with:

   ```bash
   python3 scripts/new_asset.py --adventure <adventure-slug> --type location --slug <slug> --title "<title>"
   ```

4. Give the location a table purpose, immediate impression, sensory identity, access boundaries, usable areas, pressures, and possible change over time.
5. Create local assets only when they serve the location or an established plot need. Use `scripts/new_asset.py` and pass `--location <location-slug>`.
6. Keep each asset canonical under this location. Link existing external assets instead of copying them.
7. Ensure information has a discovery path and consequence; encounters have a trigger, intentions, leverage, escalation, and outcomes; NPCs have motivation and actionable knowledge.
8. Update the location body, relevant `50-indexes/` files, metadata logs, and cross-links.
9. Run the adventure validator and report changed files plus unresolved continuity questions.

Keep all descriptions system-neutral and table-usable. Do not invent a complete cast or exhaustive room list unless the user requests that scope.
