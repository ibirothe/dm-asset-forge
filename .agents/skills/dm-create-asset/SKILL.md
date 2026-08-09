---
name: dm-create-asset
description: Create or revise a single structured, system-neutral Dungeon Master asset in an existing adventure, including an NPC, object, information item, encounter, handout, faction, plot thread, or image brief. Use for focused asset work; use the location skill when the request centers on developing a whole place.
---

# Create or revise an asset

1. Read `AGENTS.md`, the normative `docs/asset-katalog.md`, the target adventure overview, the relevant index, and the minimum linked context.
2. Determine the asset type, scope, required relations, and canonical path from the catalog. Do not substitute another type because its generator already exists.
3. For a type currently supported by the asset generator, run:

   ```bash
   python3 scripts/new_asset.py \
     --type <type> \
     --location <location-slug-if-required> \
     --slug <slug> \
     --title "<title>"
   ```

   If the catalog type is not implemented yet, report that gap instead of inventing a conflicting path or borrowing another type's schema.

4. Fill every field that affects table use. Leave an explicit TODO or open question instead of fabricating unsupported canon.
5. Apply the type-specific quality checks:
   - NPC: purpose, recognizable cues, motivation, pressure, leverage, knowledge, behavior, consequences.
   - Object: discoverability, properties, uses, risk, context, consequences.
   - Information: exact statement, truth status, discovery points, prerequisites, consequences if learned or missed.
   - Encounter: trigger, participant intentions, environment, escalation, approaches, consequences.
   - Handout: strictly separate player-facing content from DM-only context.
   - Faction: agenda, reach, resources, methods, internal tensions, relationships, escalation.
   - Plot thread: dramatic question, entry points, pressures, information path, choices, resolutions, neglect.
   - Image brief: canonical facts, composition, style, exclusions, PNG output path, provenance.
6. Add relative links from the parent location and index below `adventure/`. Update related assets only where the relationship must be reciprocal.
7. Update `90-meta/change-log.md`; record assumptions and questions in their respective files.
8. Run the adventure validator and summarize the result.

Do not create system mechanics. Do not duplicate an existing asset merely because it appears in another place.
