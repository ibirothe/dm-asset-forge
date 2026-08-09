---
name: dm-prepare-session
description: Create or refresh a compact, source-linked, system-neutral Markdown preparation package for one tabletop RPG session. Use when preparing a game night, assembling a DM session sheet, reviewing changed session sources, or gathering likely locations, plot threads, NPCs, clues, handouts, consequences, and improvisation anchors without changing canonical assets.
---

# Prepare a session

1. Read `AGENTS.md`, `docs/session-preparation-guide.md`, `docs/adventure-structure-guide.md`, `docs/adventure-audit-guide.md`, `docs/asset-katalog.md`, `docs/asset-authoring-guide.md`, `docs/metadaten-und-werte.md`, `docs/beziehungen-und-speicherorte.md`, and `docs/validierung.md`.
2. Confirm that `adventure/` exists. Determine the session focus and play horizon. Ask only when multiple plausible foci or an undocumented current state would materially change the preparation.
3. Read `adventure/README.md`, all five indexes, relevant meta files, expected locations, active plot threads, and only their directly needed assets. Add a small fallback ring for plausible unexpected choices; do not scan or copy the whole adventure.
4. Create `adventure/60-sessions/<YYYY-MM-DD>-<session-slug>.md` from `templates/session-prep.md`. Do not overwrite an existing package silently.
5. Summarize the immediate state, open approaches, possible transitions, relevant NPCs, information, handouts, active pressure, and outcome states. Keep player-safe known facts separate from DM-only clues and secrets.
6. Link every compressed statement to a canonical source. Record each source's current `version`, `updated`, and review status. For refreshes, mark changed or missing sources before revising summaries; never push package edits back into canonical assets automatically.
7. Add only useful improvisation anchors and mark every non-canonical name, rumor, detail, or reaction as `provisional`.
8. Check the guide's Definition of Done. Run `python3 scripts/validate_adventure.py`, then apply the focused session checks from `docs/adventure-audit-guide.md`.
9. Record creation or refresh in `adventure/90-meta/change-log.md`. Report the package path, scope, changed or missing sources, blocking findings, and remaining preparation questions.

Do not create a generator, PDF, player export, fixed scene sequence, or second canonical description.
