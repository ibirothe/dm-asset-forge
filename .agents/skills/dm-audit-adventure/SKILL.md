---
name: dm-audit-adventure
description: Audit an existing system-neutral tabletop RPG one-shot for technical integrity, canon continuity, robust clue paths, player agency, plot-thread reachability, truth boundaries, complete resolution paths, and table readiness. Use for reviews and final readiness checks; report only unless the user explicitly requests selected fixes.
---

# Audit an adventure

1. Read the root `AGENTS.md` and `docs/adventure-audit-guide.md`. Follow its scope, read order, severity definitions, finding format, report order, and read-only boundary. Read `docs/asset-katalog.md`, `docs/asset-authoring-guide.md`, `docs/adventure-structure-guide.md`, `docs/metadaten-und-werte.md`, `docs/beziehungen-und-speicherorte.md`, and `docs/validierung.md` as required by the audit scope.
2. Read `adventure/README.md`, all `adventure/50-indexes/`, and `adventure/90-meta/open-questions.md`, `assumptions.md`, and `decisions.md`. Derive the narrow set of active plot threads, necessary conclusions, locations, and directly linked assets to inspect.
3. Run:

   ```bash
   python3 scripts/validate_adventure.py
   ```

4. Keep technical diagnostics separate. Treat validator errors as blocking technical results; review warnings in context rather than automatically promoting them to findings.
5. Apply the guide's sequence: canon and continuity; necessary information paths; every active plot thread; complete one-shot resolution paths; and table readiness. For contradictions, inspect every file that asserts the affected canon. Do not infer one correct version when the sources are ambiguous.
6. Record each narrative finding as `blocking`, `important`, or `polish` with area, affected canon, rationale, every evidence path, impact, and smallest useful correction direction.
7. Report in the guide's order, including coverage for every active plot thread and every necessary conclusion. If no finding exists, say so explicitly.
8. Do not modify any file unless the user explicitly requests fixes. For a fix request, name selected finding IDs and affected files first, make the smallest coherent edits, update required indexes and change log, then rerun technical and affected narrative checks.

Do not create system mechanics, fill missing story content, or judge literary quality during an audit.
