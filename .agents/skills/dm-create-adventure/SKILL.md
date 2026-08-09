---
name: dm-create-adventure
description: Create and initialize a new system-neutral tabletop RPG adventure in this repository from a user's rough world and plot description. Use when starting a new adventure, campaign, scenario, or module; do not use for editing a single asset in an existing adventure.
---

# Create an adventure

1. Read the repository `AGENTS.md` and `docs/struktur-und-konventionen.md`.
2. Capture the requested title plus the user's rough world and plot descriptions. Ask only about missing facts that would materially change the first structure; record non-blocking uncertainties instead.
3. Derive a lowercase ASCII kebab-case slug. Confirm no folder with that slug exists below `adventures/`.
4. Run:

   ```bash
   python3 scripts/init_adventure.py --slug <slug> --title "<title>"
   ```

5. Preserve the user's original wording in:
   - `00-input/world.md`
   - `00-input/plot.md`
   - `00-input/constraints.md` when constraints were supplied
6. Build a restrained first pass in `10-world/` and `20-plot/`. Distinguish facts, interpretations, assumptions, and unknowns.
7. Create only locations and assets supported by the brief. Use `scripts/new_asset.py` for each supported asset type.
8. Link every created asset from the relevant local file and `50-indexes/`. Do not duplicate descriptive bodies.
9. Record impactful assumptions in `90-meta/decisions.md`, unresolved user choices in `90-meta/open-questions.md`, and the work in `90-meta/change-log.md`.
10. Run `python3 scripts/validate_adventure.py adventures/<slug>` and fix structural errors.
11. Return a concise summary of the created structure, assumptions, open questions, and validation result.

Do not introduce system-specific rules, statistics, difficulty values, or named mechanics. Do not create an example adventure when the user has not supplied a world and plot brief.
