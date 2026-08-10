# Validierung

`scripts/validate_adventure.py` prüft ein initialisiertes Abenteuer deterministisch und ausschließlich lesend. Der Validator repariert keine Dateien und bewertet keine erzählerische Qualität.

## Ausführung

Im Repository-Stamm:

```bash
python3 scripts/validate_adventure.py
```

Ein anderes Abenteuerverzeichnis kann ausdrücklich angegeben werden:

```bash
python3 scripts/validate_adventure.py /path/to/adventure
```

Exit-Code `0` bedeutet: keine blockierenden Fehler. Exit-Code `1` bedeutet: mindestens ein Fehler. Warnungen allein führen nicht zum Fehlschlag.

## Geprüfte Regeln

| Bereich | Prüfung |
|---|---|
| Struktur | Pflichtordner und Pflichtdateien des Abenteuer-Scaffolds |
| Session-Preflight | Pflichtabschnitte, Status `open`, `blocked` oder `ready` und Verweis auf die kanonischen Constraints |
| Frontmatter | gemeinsame Pflichtfelder, unbekannte Schlüssel, Listenformat, leere Strings, Versionen und ISO-Daten |
| Typen | alle 15 Katalogtypen, ID-Präfix, Scope, typspezifische Schlüssel und Pflichtfelder |
| Werte | `status`, `truth_status`, `provenance` und alle regelneutralen qualitativen Skalen |
| Pfade | kanonischer Pfad aus Typ, ID, primärem Ort oder Visual-Subject |
| Inhalt | ausschließlich die funktional erforderlichen `##`-Abschnitte des passenden Asset-Templates; optionale Navigation erst bei tatsächlichem Bedarf |
| Beziehungen | existierende Ziel-ID und erlaubter Zieltyp für strukturierte Relationsfelder |
| Navigation | vollständige, eindeutige und aktuelle Indexzeilen sowie relative Links und verpflichtende Gegenlinks strukturierter Beziehungen |
| Referenzen | doppelte IDs, defekte relative Markdown-Links und verwaiste Visual-Prompts |
| Bilder | ausschließlich PNG-Dateien und PNG-Verweise; passender strukturierter Prompt, Identitätsquelle, Zustandsvariante, Ausgabepfad, Freigabe, Dateistatus und Provenienz für jedes Visual |
| Hygiene | verbliebene Template-Platzhalter und mögliche systemspezifische Begriffe |

Die normativen Grundlagen bleiben der [Asset-Katalog](asset-katalog.md), die [Metadaten und Werte](metadaten-und-werte.md) sowie das [Beziehungsmodell](beziehungen-und-speicherorte.md). Die anschließende fachliche Prüfung und ihr getrenntes Berichtsformat definiert der [Fachliche Audit-Leitfaden](adventure-audit-guide.md).

Zusätzliche Überschriften aus älteren Template-Ständen bleiben zulässig. Werden funktionslose Pflichtaufforderungen aus einem Template entfernt, bleiben bestehende Abenteuer daher valide; der Validator verlangt sie lediglich bei neu erzeugten oder überarbeiteten Assets nicht mehr.

## Ausgabe verstehen

Jede Meldung enthält:

```text
SEVERITY: path [RULE_CODE]: problem Fix: concrete correction.
```

Beispiel:

```text
ERROR: 30-locations/hafen/npcs/mara/npc.md [FM_ENUM]: invalid 'reach' value 'galactic'. Fix: Use one of: local, personal, regional, unknown, widespread, world-spanning.
```

- `ERROR` kennzeichnet eine verletzte Struktur-, Schema-, Pfad- oder Integritätsregel und blockiert den erfolgreichen Abschluss.
- `WARNING` kennzeichnet einen prüfbedürftigen Fund, der nicht zweifelsfrei falsch ist. Systemspezifische Begriffe sind Warnungen, weil sie auch in Zitaten oder bewussten Erläuterungen vorkommen können.
- `RULE_CODE` bezeichnet die stabile technische Regel, etwa `FM_UNKNOWN_KEY`, `ASSET_PATH`, `REL_TARGET_TYPE`, `REL_LINK_MISSING`, `BACKLINK_MISSING`, `INDEX_MISSING`, `INDEX_DUPLICATE`, `INDEX_STALE`, `SECTION_REQUIRED`, `PREFLIGHT_SECTION`, `PREFLIGHT_STATUS`, `PREFLIGHT_CONSTRAINTS_LINK`, `VISUAL_PNG_STATE`, `VISUAL_APPROVED_VERSION`, `PNG_ORPHAN` oder `LINK_BROKEN`.
- `Fix` nennt die kleinste typische Korrektur. Vor einer Änderung bleibt der fachliche Kontext zu prüfen.

## Grenzen

Der Validator prüft keine Dramaturgie, Originalität, Spielbarkeit, Hinweisredundanz oder inhaltliche Plausibilität. Kontinuität, Informationswege, Spielerwirksamkeit und Tischreife bearbeitet der Skill `dm-audit-adventure` nach dem [Fachlichen Audit-Leitfaden](adventure-audit-guide.md) getrennt. Der Validator erzeugt keine Assets, aktualisiert keine Indizes und führt keine automatische Reparatur durch. Er erkennt nur deterministische Navigationslücken; ob eine optionale Freitextbeziehung dauerhaft oder spielrelevant genug für einen Gegenlink ist, bleibt eine fachliche Entscheidung.

## Regressionstests

Änderungen an Templates, Schema oder Validator werden mit der Standardbibliothek geprüft:

```bash
python3 -m unittest discover -s tests -v
```

Die Tests erzeugen temporäre Abenteuer, prüfen alle 15 Typen sowie gezielte Fehlerszenarien und vergleichen vor und nach der Validierung die Dateihashes.
