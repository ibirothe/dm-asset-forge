---
name: dm-audit-adventure
description: Audit an existing system-neutral tabletop RPG adventure for structural integrity, broken links, duplicate IDs, unresolved placeholders, system-specific leakage, orphaned assets, dead clues, plot continuity, and table readiness. Use for reviews and pre-session checks; do not expand or rewrite content unless the user asks for fixes.
---

# Audit an adventure

1. Read the root `AGENTS.md`, adventure `README.md`, all `50-indexes/`, and `90-meta/` files.
2. Run:

   ```bash
   python3 scripts/validate_adventure.py adventures/<adventure-slug>
   ```

3. Use validator results to select a narrow read set. Inspect implicated locations, assets, and their direct links.
4. Check narrative quality separately from structural validation:
   - every active plot thread has an entry point, pressure, player choice, and possible outcome;
   - important information has at least one discoverable path and meaningful consequence;
   - no required conclusion depends on a single fragile clue;
   - NPC knowledge and motivations do not contradict established facts;
   - timelines, locations, ownership, and relationships agree;
   - assets marked `ready` are usable at the table;
   - system-specific mechanics have not entered the content;
   - generated PNGs have matching image briefs and declared provenance.
5. Classify findings as `blocking`, `important`, or `polish`. Cite exact relative file paths.
6. If the user requested fixes, make the smallest coherent edits, update indexes and change log, then rerun validation. Otherwise, do not edit files.
7. Report validation output, narrative findings, open questions, and the recommended next action.
