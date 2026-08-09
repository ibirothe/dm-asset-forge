---
name: dm-audit-adventure
description: Audit an existing system-neutral tabletop RPG one-shot for technical integrity, canon continuity, robust clue paths, player-output safety, visual consistency, qualitative pacing, safe cuts, direct table navigation, player agency, plot-thread reachability, truth boundaries, complete resolution paths, and table readiness. Use for reviews and final readiness checks; report only unless the user explicitly requests selected fixes.
---

# Audit an adventure

1. Always read the root `AGENTS.md`, `docs/adventure-audit-guide.md`, and `docs/validierung.md`. Follow the audit guide's scope, read order, severity definitions, finding format, report order, and read-only boundary. Do not load every normative guide up front.
2. Load additional references only for the affected audit area: `docs/asset-katalog.md` for type or canonical-path questions; the relevant type section of `docs/asset-authoring-guide.md` for table readiness; `docs/adventure-structure-guide.md` for player agency, information paths, plot threads, resolutions, pacing, or safe cuts; `docs/metadaten-und-werte.md` for metadata or controlled values; `docs/beziehungen-und-speicherorte.md` for ownership, movement, reciprocity, or continuity; `docs/player-handout-workflow.md` when a scoped Handout has a `player.md` or player-facing Visual; and `docs/bild-workflow.md` when a scoped Visual, prompt, or PNG exists.
3. Read `adventure/README.md`, all `adventure/50-indexes/`, and `adventure/90-meta/open-questions.md`, `assumptions.md`, and `decisions.md`. Derive the narrow set of active plot threads, necessary conclusions, locations, and directly linked assets to inspect. Record whether every central asset is reachable directly from the README or through exactly one matching index without full-text search or blind directory scanning.
4. Run:

   ```bash
   python3 scripts/validate_adventure.py
   ```

5. Keep technical diagnostics separate. Treat validator errors as blocking technical results; review warnings in context rather than automatically promoting them to findings.
6. Apply the guide's sequence: canon and continuity; necessary information paths; player outputs and relevant Visuals; every active plot thread; complete one-shot resolution paths; qualitative pacing and safe cuts; README and index navigation; and table readiness. Check the target frame, minimum resolution state, prose content roles, each declared safe cut, and `late pressure` without calculating runtime or inventing a Scene order. Verify that README and index contexts are short, current, action-relevant, and linked to the only canonical source rather than duplicating it. Compare each scoped `player.md` with its Handout, `reveals`, truth boundaries, and delivery context. Compare each relevant Visual and prompt with its Subject identity, depicted One-Shot state, visibility, exclusions, and any existing PNG. If the PNG cannot be inspected visually with available tools, report that limit instead of treating it as verified. For contradictions, inspect every file that asserts the affected canon. Do not infer one correct version when the sources are ambiguous.
7. Record each narrative finding as `blocking`, `important`, or `polish` with area, affected canon, rationale, every evidence path, impact, and smallest useful correction direction.
8. Report in the guide's order, including coverage for every active plot thread, every necessary conclusion, each scoped `player.md`, each relevant Visual, every declared safe cut, all five indexes, and the navigation path to every central asset. If no finding exists, say so explicitly.
9. Do not modify any file unless the user explicitly requests fixes. For a fix request, name selected finding IDs and affected files first, make the smallest coherent edits, update required indexes and change log, then rerun technical and affected narrative checks.

Do not create system mechanics, fill missing story content, or judge literary quality during an audit.
