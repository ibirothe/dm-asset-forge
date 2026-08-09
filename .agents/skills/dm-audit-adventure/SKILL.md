---
name: dm-audit-adventure
description: Audit an existing system-neutral tabletop RPG adventure for structural integrity, broken links, duplicate IDs, unresolved placeholders, system-specific leakage, orphaned assets, dead clues, plot continuity, and table readiness. Use for reviews and pre-session checks; do not expand or rewrite content unless the user asks for fixes.
---

# Audit an adventure

1. Read the root `AGENTS.md`, the normative `docs/asset-katalog.md`, `docs/asset-authoring-guide.md`, `docs/metadaten-und-werte.md`, `docs/beziehungen-und-speicherorte.md`, and `docs/validierung.md`, then `adventure/README.md`, all `adventure/50-indexes/`, and `adventure/90-meta/` files.
2. Run:

   ```bash
   python3 scripts/validate_adventure.py
   ```

3. Treat validator errors as blocking structural findings. Review warnings in context before classifying them; a warning is not automatically a defect. Use rule codes and paths to select a narrow read set. Inspect implicated locations, assets, and their direct links.
4. Check narrative quality separately from structural validation:
   - every asset uses the catalog type and canonical path that match its purpose;
   - every asset uses only defined metadata keys, controlled values, and missing-value semantics;
   - every local asset has one canonical owner location, appearances are links rather than copies, and required reciprocal links exist;
   - unconfirmed assumptions remain in `90-meta/assumptions.md` and are not presented as established truths;
   - every active plot thread has an entry point, pressure, player choice, and possible outcome;
   - important information has at least one discoverable path and meaningful consequence;
   - no required conclusion depends on a single fragile clue;
   - NPC knowledge and motivations do not contradict established facts;
   - timelines, locations, ownership, and relationships agree;
   - every asset marked `ready` meets the shared and type-specific Definition of Done in the authoring guide;
   - system-specific mechanics have not entered the content;
   - generated PNGs have matching Visual assets, prompt companions, and declared provenance.
5. Classify findings as `blocking`, `important`, or `polish`. Cite exact relative file paths.
6. If the user requested fixes, make the smallest coherent edits, update indexes and change log, then rerun validation. Otherwise, do not edit files.
7. Report validation output, narrative findings, open questions, and the recommended next action.
