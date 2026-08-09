# Benutzerhandbuch

## Neues Abenteuer beginnen

Starte Codex im Stammverzeichnis dieses Repositories. Beschreibe Welt und Plot zunächst grob. Ein geeigneter Startauftrag ist:

> Erstelle ein neues regelneutrales Abenteuer mit dem Titel „…“. Die Welt ist … Der Ausgangskonflikt ist … Die Spielerfiguren sollen … erleben. Lege Unklarheiten als offene Fragen ab.

Codex legt das Abenteuer unter `adventure/` an. Die vollständige ursprüngliche Anfrage bleibt unverändert in `adventure/00-input/original-request.md` erhalten. Welt, Plot und Constraints werden daraus getrennt extrahiert; spätere Antworten stehen datiert in `clarifications.md`.

Ein Repository enthält genau ein Abenteuer. Existiert `adventure/` bereits, arbeitet Codex mit diesem Stand weiter und initialisiert kein zweites Abenteuer. Für ein weiteres Abenteuer wird eine neue Arbeitskopie aus dem Template erzeugt.

Für den Start genügen eine freie Weltbeschreibung und eine grobe Plot- oder Konfliktidee. Titel, Spielerrolle, Umfang und genaue Stimmung dürfen später ergänzt werden. Codex fragt vor dem Erstlauf nur nach, wenn fehlende oder widersprüchliche Angaben den ersten kohärenten Stand wesentlich verändern würden.

Der vollständige Ablauf und seine Definition of Done stehen in [Geführter Welt- und Plot-Intake](intake-workflow.md).

## Abenteuerstruktur und Spielerentscheidungen

Codex bereitet das Abenteuer als veränderbare Situation vor, nicht als feste Szenenfolge. Der Einstieg erklärt den aktuellen Druck und bietet mehrere Ansatzpunkte, ohne Herkunft, Motivation oder Entscheidung der Spielerfiguren vorzugeben. Notwendige Erkenntnisse bleiben über unabhängige Informationswege erreichbar. Scheitern, Rückzug und Ignorieren verändern Akteure, Orte, Beziehungen oder Druck, statt den Plot zu beenden.

Der [Leitfaden für Spielerentscheidungen und Abenteuerstruktur](adventure-structure-guide.md) enthält die prüfbaren Kriterien für Einstieg, Entscheidungen, Konsequenzen, optionale Scenes, Plot-Threads, mögliche Auflösungen und die Skalierung vom One-Shot bis zum längeren Abenteuer.

## Sinnvolle Folgeaufträge

- „Arbeite den Ort `<name>` aus und lege alle dort verankerten NPCs, Objekte und Hinweise am Ort ab.“
- „Erstelle einen NPC namens `<name>` für `<location>` mit Motivation, Konflikt, Wissen und Spielhinweisen.“
- „Ergänze drei auffindbare Hinweise, die den Plotfaden `<thread>` voranbringen.“
- „Erstelle Bildbriefings für die wichtigsten Orte; noch keine Bilder erzeugen.“
- „Prüfe das Abenteuer auf Widersprüche, tote Hinweise und nicht verknüpfte Assets.“

## Assets anlegen

Der Generator unterstützt alle 14 Typen des [Asset-Katalogs](asset-katalog.md). Beispiele:

```bash
python3 scripts/new_asset.py --type location --slug alter-hafen --title "Alter Hafen"
python3 scripts/new_asset.py --type npc --location alter-hafen --slug mara-veen --title "Mara Veen"
python3 scripts/new_asset.py --type faction --slug graue-laterne --title "Graue Laterne"
python3 scripts/new_asset.py --type visual --subject npc-mara-veen --slug portrait --title "Porträt von Mara Veen"
```

Lokale Assets benötigen `--location`; ein Visual benötigt mit `--subject` die ID eines bestehenden Assets. Eine Location kann mit `--parent-location` hierarchisch eingeordnet werden. Der Generator prüft Argumente, Beziehungen, IDs und Zielpfade vor dem Schreiben. Bestehende Dateien werden nur mit dem ausdrücklich gesetzten `--overwrite` ersetzt.

Nach der Initialisierung wird der World-Singleton einmalig aus seinem Asset-Template erzeugt:

```bash
python3 scripts/new_asset.py --type world --slug <adventure-slug> --title "<title>" --overwrite
```

`--overwrite` ist hier nur für die noch unveränderte Platzhalterdatei des Scaffolds vorgesehen. Der Generator aktualisiert keine Indizes, Rückverweise oder Inhalte automatisch; diese werden anschließend durch Codex gepflegt. Alle Optionen zeigt `python3 scripts/new_asset.py --help`.

## Assets fachlich ausarbeiten

Das Template legt Abschnitte und Metadaten an, erzeugt aber noch keinen spielbereiten Inhalt. Der [Autoren- und Tischleitfaden für DM-Assets](asset-authoring-guide.md) beschreibt für jeden der 14 Typen:

- Einsatz und Abgrenzung zu ähnlichen Typen;
- fachlichen Mindestinhalt und hilfreiche Leitfragen;
- Informationen, die der DM am Tisch schnell benötigt;
- Trennung von Spielerwissen, DM-Wissen und Geheimnissen;
- sinnvollen, optionalen oder unnötigen Einsatz eines Visuals;
- typische Anti-Patterns;
- eine typspezifische Definition of Done.

Ein Asset bleibt `status: draft`, solange zentrale Beziehungen, Zugänge, Handlungsmöglichkeiten oder Konsequenzen fehlen. Erst wenn es die gemeinsamen und typspezifischen Kriterien erfüllt, darf Codex es als `ready` markieren. Dabei soll nicht jeder Abschnitt möglichst lang, sondern jede Information für Vorbereitung, Spiel oder Kontinuität nützlich sein.

## Mit vorhandenen Dateien arbeiten

Codex liest zuerst Übersicht, Indizes und den betroffenen Ort. Es folgt Links nur so weit, wie es für die Aufgabe nötig ist. Dadurch bleiben Änderungen fokussiert und bestehende Inhalte werden nicht unnötig neu formuliert.

Ein Asset besitzt genau einen kanonischen Speicherort. Wenn ein NPC an mehreren Orten auftreten kann, bleibt seine vollständige Datei am primären Ort. Andere Orte verweisen per Link darauf.

Der primäre Ort bestimmt die Ablage, der aktuelle Ort den momentanen Aufenthalt in der Spielwelt. Bei einer Reise ändert Codex `current_location` und die Links am Zielort, kopiert oder verschiebt die NPC-Datei aber nicht. Erst wenn sich die dauerhafte redaktionelle Zuordnung ändert, wird die kanonische Datei einmalig verschoben und werden alle Verweise angepasst. Details stehen in [Beziehungen und ortszentrierte Speicherung](beziehungen-und-speicherorte.md).

## Offene Fragen und Annahmen

- `90-meta/open-questions.md` enthält Entscheidungen, die noch vom User benötigt werden.
- `90-meta/assumptions.md` enthält unbestätigte, umkehrbare Arbeitsannahmen.
- `90-meta/decisions.md` dokumentiert getroffene Entscheidungen und ihre Begründung.
- `00-input/clarifications.md` bewahrt spätere Nutzerantworten möglichst wortgetreu.
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

Bilddateien werden als PNG gespeichert. Ein Visual-Ordner enthält das kanonische `visual.md`, ein gleichnamiges Bildbriefing mit der Endung `.prompt.md` und optional die PNG-Datei. So kann das Motiv später reproduziert oder gezielt überarbeitet werden.

Ein Bildbriefing kann bereits erstellt werden, ohne das Bild zu generieren. Codex darf erst dann behaupten, dass ein Bild vorhanden ist, wenn die PNG-Datei tatsächlich im Projekt liegt.

## Vor einer Spielrunde

Für einen konkreten Spielabend kann Codex eine kompakte Arbeitsmappe anlegen:

> Bereite die nächste Session mit dem Fokus „…“ vor. Erwartete Orte sind …, aktive Plotfäden sind …. Bündele nur relevante Inhalte, verlinke jede kanonische Quelle und markiere Improvisationsideen als vorläufig.

Die Arbeitsmappe liegt unter `adventure/60-sessions/` und fasst Startsituation, mögliche Übergänge, NPC-Kurzprofile, Hinweise, Handouts, laufenden Druck, Folgezustände und Improvisationsanker zusammen. Sie ist vollständig DM-only und keine zweite kanonische Beschreibung. Ein Quellenregister zeigt für jede verwendete Datei die aufgezeichnete Version, das `updated`-Datum und den Prüfstatus `current`, `changed`, `missing` oder `not-checked`.

Der [Leitfaden für Session-Vorbereitung](session-preparation-guide.md) beschreibt Eingaben, Speicherort, Sichtbarkeit, Quellenpflege und Definition of Done. Änderungen an der Arbeitsmappe verändern kanonische Assets niemals automatisch.

Beauftrage Codex mit einer Konsistenzprüfung. Der technische Validator und der fachliche Audit werden getrennt berichtet. Der [Fachliche Audit-Leitfaden](adventure-audit-guide.md) verlangt für jedes Finding Begründung, betroffene Dateien, Auswirkung und kleinste sinnvolle Korrekturrichtung. Ohne ausdrücklichen Fix-Auftrag verändert Codex keine Inhalte.

Die Prüfung kontrolliert unter anderem:

- fehlende Pflichtverzeichnisse und Metadaten
- doppelte IDs
- defekte relative Markdown-Links
- verbliebene Template-Platzhalter
- systemgebundene Begriffe
- Hinweise ohne Fundort oder Konsequenz
- notwendige Schlussfolgerungen mit nur einem fragilen Entdeckungspfad
- jeden aktiven Plotfaden auf Einstieg, Druck, Wahl, Ignorieren und mögliche Auflösung
- Widersprüche bei Ort, Zeit, Ownership, Wissen, Status, Motivation und Beziehungen

Das technische Prüfsystem kann auch direkt ausgeführt werden:

```bash
python3 scripts/validate_adventure.py
```

Fehler enthalten den betroffenen Pfad, einen stabilen technischen Regelcode und einen konkreten Korrekturhinweis. Fehler blockieren den erfolgreichen Abschluss; Warnungen markieren prüfbedürftige, aber nicht zwingend falsche Inhalte. Der Validator verändert keine Abenteuerdateien und nimmt keine automatischen Reparaturen vor. Die vollständige Referenz steht in [Validierung](validierung.md).
