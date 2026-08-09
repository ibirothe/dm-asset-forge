# Benutzerhandbuch

## Neues Abenteuer beginnen

Starte Codex im Stammverzeichnis dieses Repositories. Beschreibe Welt und Plot zunächst grob. Ein geeigneter Startauftrag ist:

> Erstelle ein neues regelneutrales Abenteuer mit dem Titel „…“. Die Welt ist … Der Ausgangskonflikt ist … Die Spielerfiguren sollen … erleben. Lege Unklarheiten als offene Fragen ab.

Codex legt das Abenteuer unter `adventure/` an. Der ursprüngliche Welt- und Plottext bleibt in `adventure/00-input/` erhalten. Daraus entstehen strukturierte Welt-, Plot- und Ortsdateien.

Ein Repository enthält genau ein Abenteuer. Existiert `adventure/` bereits, arbeitet Codex mit diesem Stand weiter und initialisiert kein zweites Abenteuer. Für ein weiteres Abenteuer wird eine neue Arbeitskopie aus dem Template erzeugt.

## Sinnvolle Folgeaufträge

- „Arbeite den Ort `<name>` aus und lege alle dort verankerten NPCs, Objekte und Hinweise am Ort ab.“
- „Erstelle einen NPC namens `<name>` für `<location>` mit Motivation, Konflikt, Wissen und Spielhinweisen.“
- „Ergänze drei auffindbare Hinweise, die den Plotfaden `<thread>` voranbringen.“
- „Erstelle Bildbriefings für die wichtigsten Orte; noch keine Bilder erzeugen.“
- „Prüfe das Abenteuer auf Widersprüche, tote Hinweise und nicht verknüpfte Assets.“

## Mit vorhandenen Dateien arbeiten

Codex liest zuerst Übersicht, Indizes und den betroffenen Ort. Es folgt Links nur so weit, wie es für die Aufgabe nötig ist. Dadurch bleiben Änderungen fokussiert und bestehende Inhalte werden nicht unnötig neu formuliert.

Ein Asset besitzt genau einen kanonischen Speicherort. Wenn ein NPC an mehreren Orten auftreten kann, bleibt seine vollständige Datei am primären Ort. Andere Orte verweisen per Link darauf.

## Offene Fragen und Annahmen

- `90-meta/open-questions.md` enthält Entscheidungen, die noch vom User benötigt werden.
- `90-meta/decisions.md` dokumentiert getroffene Annahmen und ihre Begründung.
- `90-meta/change-log.md` macht inhaltliche Änderungen nachvollziehbar.

Bitte Codex ausdrücklich, Annahmen nicht als Fakten auszugeben. Unkritische Annahmen dürfen dokumentiert werden; Entscheidungen mit großem Einfluss auf Ton, Plot oder Weltlogik sollen als offene Frage stehen bleiben.

## Metadaten und qualitative Werte

Assets verwenden gemeinsame Metadaten und feste englische Werte für Gefahr, Einfluss, Reichweite, Seltenheit, Zugänglichkeit und Informationssicherheit. Die Bedeutungen sind regelneutral und in [Metadaten und regelneutrale Werte v1](metadaten-und-werte.md) festgelegt.

- `unknown`: Die Angabe ist relevant, aber noch nicht bekannt.
- `null`: Ein einzelnes Feld ist bewusst nicht anwendbar oder besitzt kein Ziel.
- `[]`: Eine Liste ist anwendbar, enthält aber aktuell keine Einträge.
- Offene Entscheidungen: stehen zusätzlich in `90-meta/open-questions.md`.

Leere Zeichenketten werden nicht als Platzhalter verwendet. Dadurch kann Codex offene Fragen von bewusst nicht anwendbaren Angaben unterscheiden.

## Bilder

Bilddateien werden als PNG gespeichert. Neben jedem Bild liegt ein gleichnamiges Bildbriefing mit der Endung `.prompt.md`. So kann das Motiv später reproduziert oder gezielt überarbeitet werden.

Ein Bildbriefing kann bereits erstellt werden, ohne das Bild zu generieren. Codex darf erst dann behaupten, dass ein Bild vorhanden ist, wenn die PNG-Datei tatsächlich im Projekt liegt.

## Vor einer Spielrunde

Beauftrage Codex mit einer Konsistenzprüfung. Die Prüfung kontrolliert unter anderem:

- fehlende Pflichtverzeichnisse und Metadaten
- doppelte IDs
- defekte relative Markdown-Links
- verbliebene Template-Platzhalter
- systemgebundene Begriffe
- Hinweise ohne Fundort oder Konsequenz
- Plotfäden ohne Einstieg, Fortschritt oder möglichen Abschluss

Das technische Prüfsystem kann auch direkt ausgeführt werden:

```bash
python3 scripts/validate_adventure.py
```
