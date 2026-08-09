---
name: dm-create-asset
description: Create or revise one of the 14 structured, system-neutral Dungeon Master asset types in an existing adventure. Use for focused asset work; use the location skill when the request centers on developing a whole place.
---

# Create or revise an asset

1. Read `AGENTS.md`, the normative `docs/asset-katalog.md`, `docs/metadaten-und-werte.md`, and `docs/beziehungen-und-speicherorte.md`, the target adventure overview, the relevant index, and the minimum linked context.
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

4. Fill every field that affects table use. Use only documented keys and controlled values. Represent unknown, inapplicable, empty-list, and open values according to the metadata specification instead of fabricating unsupported canon.
5. Apply the type-specific quality checks:
   - World: premise, established truths, assumptions, everyday logic, powers, tensions, unknowns.
   - Location: table purpose, sensory identity, access, areas, inhabitants, pressures, connections, change.
   - Scene: entry state, participants, tension, opportunities, discoveries, transitions, aftermath.
   - NPC: purpose, recognizable cues, motivation, pressure, leverage, knowledge, behavior, consequences.
   - Creature: recognizable signs, habitat, needs, behavior, risk, leverage, variations.
   - Object: discoverability, properties, uses, risk, context, consequences.
   - Information: exact statement, truth status, discovery points, prerequisites, consequences if learned or missed.
   - Encounter: trigger, participant intentions, environment, escalation, approaches, consequences.
   - Handout: strictly separate player-facing content from DM-only context.
   - Faction: agenda, reach, resources, methods, internal tensions, relationships, escalation.
   - Plot thread: dramatic question, entry points, pressures, information path, choices, resolutions, neglect.
   - Event: timing, trigger, participants, sequence, visible signs, consequences, possible alteration.
   - Visual: subject relation, canonical visual facts, player visibility, PNG output path, prompt, provenance.
   - Random table: purpose, context, selection method, bounded entries, consequences, canonicalization rule.
6. Keep the full asset in exactly one canonical file. Add relative links from its owner, appearance locations, and index below `adventure/`. Update related assets wherever the relationship model requires a reciprocal link.
7. Update `90-meta/change-log.md`; record assumptions and questions in their respective files.
8. Run the adventure validator and summarize the result.

Do not create system mechanics. Do not duplicate an existing asset merely because it appears in another place.
