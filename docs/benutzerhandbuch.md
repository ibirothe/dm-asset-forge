# Benutzerhandbuch

## Neuen One-Shot beginnen

Starte Codex im Stammverzeichnis dieses Repositories. Beschreibe Welt und Plot zunächst grob. Ein geeigneter Startauftrag ist:

> Erstelle einen neuen regelneutralen One-Shot mit dem Titel „…“. Die Welt ist … Der Ausgangskonflikt ist … Gewünschte ungefähre Spieldauer: … Ton und Themen: … Ausgeschlossen sind: … Lege fehlende Präferenzen als offen ab und bereite den zentralen Konflikt vollständig auflösbar vor.

Codex legt das Abenteuer unter `adventure/` an. Die vollständige ursprüngliche Anfrage bleibt unverändert in `adventure/00-input/original-request.md` erhalten. Welt, Plot und Constraints werden daraus getrennt extrahiert; spätere Antworten stehen datiert in `clarifications.md`.

Ein Repository enthält genau einen abgeschlossenen One-Shot. Existiert `adventure/` bereits, arbeitet Codex mit diesem Stand weiter und initialisiert keinen zweiten One-Shot. Für einen weiteren One-Shot wird eine neue Arbeitskopie aus dem Template erzeugt.

Für den Start genügen eine freie Weltbeschreibung und eine grobe Plot- oder Konfliktidee. Titel, Spielerrolle, gewünschte Spieldauer, Inhaltsdichte, genaue Stimmung und Inhaltsgrenzen sind optional. Codex übernimmt vorhandene Angaben und dokumentiert fehlende Präferenzen ausdrücklich als `open`, statt sie zu erfinden. Es fragt vor dem Erstlauf nur nach, wenn fehlende oder widersprüchliche Angaben den ersten kohärenten Stand wesentlich verändern würden.

Vor der Asset-Erzeugung fasst Codex die spielbare One-Shot-Prämisse zusammen: player-facing Ausgangslage, zentraler Konflikt, mindestens zwei grundsätzlich unterschiedliche Formen der Spieler-Einflussnahme und der innerhalb des One-Shots erforderliche Abschlussrahmen. Diese Angaben werden in den bestehenden Input-, Plot- und Meta-Dateien geführt; es entsteht keine zusätzliche Kanonquelle.

Der vollständige Ablauf und seine Definition of Done stehen in [Geführter Welt- und Plot-Intake](intake-workflow.md).

## Abenteuerstruktur und Spielerentscheidungen

Codex bereitet das Abenteuer als veränderbare Situation vor, nicht als feste Szenenfolge. Der Einstieg erklärt den aktuellen Druck und bietet mehrere Ansatzpunkte, ohne Herkunft, Motivation oder Entscheidung der Spielerfiguren vorzugeben. Notwendige Erkenntnisse bleiben über unabhängige Informationswege erreichbar. Scheitern, Rückzug und Ignorieren verändern Akteure, Orte, Beziehungen oder Druck, statt den Plot zu beenden.

Der [Leitfaden für Spielerentscheidungen und Abenteuerstruktur](adventure-structure-guide.md) enthält die prüfbaren Kriterien für Einstieg, Entscheidungen, Konsequenzen, optionale Scenes, Plot-Threads, mögliche Auflösungen und einen begrenzten One-Shot-Umfang.

Die gewünschte ungefähre Spielzeit und Inhaltsdichte stehen als `Target duration` und `Content density` in `00-input/constraints.md`; fehlende Angaben bleiben `open`. Für die Vorbereitung unterscheidet Codex Inhalte redaktionell als `core`, `supporting` oder `optional`. Der Plot nennt einen minimalen Auflösungszustand, mindestens eine sichere Kürzung und einen vorbereiteten `late pressure`-Zustandswechsel. Diese Angaben helfen beim Verdichten, bilden aber weder einen Zeitplan noch eine feste Szenenfolge.

## Vorbereitung und Tischgebrauch

Beginne in `adventure/README.md`. Die dortige Tischübersicht fasst Ausgangslage, Konflikt, Druck, zentrale Akteure, notwendige Informationen, mögliche Abschlüsse, Folgezustände und den Verweis auf Pacing und sichere Kürzungen knapp zusammen. Zentrale Assets sind direkt verlinkt. Für weitere Locations, NPCs, Objects, Informationen und aktive Plot-Threads führt die Übersicht in genau den passenden Index und von dort in die kanonische Datei.

Die Kurztexte in README und Indizes dienen nur der Orientierung. Vollständiger Kanon, Geheimnisse, Bedingungen und Konsequenzen werden ausschließlich im verlinkten Plot oder Asset gepflegt. Ändert sich dort eine tischrelevante Aussage, lässt du Codex anschließend die betroffene Kurzfassung aktualisieren. Eine Volltextsuche oder ein Durchsehen sämtlicher Ordner sollte für zentrale Inhalte nicht nötig sein.

Ein geeigneter Prüfauftrag ist:

> Prüfe README und die fünf Indizes auf unmittelbare Tischführung. Stelle sicher, dass jedes zentrale Asset direkt oder über genau einen passenden Index erreichbar ist, und aktualisiere nur veraltete Kurzkontexte und Links. Dupliziere keinen vollständigen Kanon.

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

`--overwrite` ist hier nur für die noch unveränderte Platzhalterdatei des Scaffolds vorgesehen. Der Generator aktualisiert vorhandene zuständige Indizes und die eindeutig ableitbaren Links zwischen lokalem Asset und primärem Ort, Parent- und Child-Location sowie Visual und Subject. Wiederholtes Schreiben mit ausdrücklichem `--overwrite` erzeugt dabei keine doppelten Navigationseinträge. Kontextabhängige Beziehungen, inhaltliche Beschreibungen und das Change Log werden anschließend durch Codex gepflegt. Alle Optionen zeigt `python3 scripts/new_asset.py --help`.

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

## Handouts für Spieler freigeben

Die kanonische `handout.md` bleibt eine DM-Arbeitsdatei und kann Geheimnisse, Auslieferungskontext sowie interne Beziehungen enthalten. Bitte Codex zunächst um einen vollständigen Entwurf der eigenständigen Spielerfassung:

> Erstelle für das Handout `<name>` einen Safety-geprüften Entwurf für `player.md`. Zeige mir den vollständigen Text, aber schreibe oder ersetze die Datei erst nach meiner ausdrücklichen Freigabe.

Nach der Freigabe liegt `player.md` direkt neben `handout.md`. Sie enthält weder Frontmatter noch DM-only Abschnitte oder interne Repository-Links und ist ohne Projektkontext verständlich. Jede spätere Ersetzung erfordert erneut eine ausdrückliche Freigabe. Eine PNG-Ausgabe ist optional und wird nur auf Wunsch aus der bereits freigegebenen Markdown-Fassung abgeleitet. Sie liegt als reguläres Visual mit Briefing, Freigabe und Provenienz unter `visuals/player/`, niemals direkt neben `handout.md`. Der vollständige Ablauf steht in [Spielerfreigabe für Handouts](player-handout-workflow.md).

## Mit vorhandenen Dateien arbeiten

Codex liest zuerst Übersicht, Indizes und den betroffenen Ort. Es folgt Links nur so weit, wie es für die Aufgabe nötig ist. Dadurch bleiben Änderungen fokussiert und bestehende Inhalte werden nicht unnötig neu formuliert.

Ein Asset besitzt genau einen kanonischen Speicherort. Wenn ein NPC an mehreren Orten auftreten kann, bleibt seine vollständige Datei am primären Ort. Andere Orte verweisen per Link darauf.

Der primäre Ort bestimmt die Ablage, der aktuelle Ort den momentanen Aufenthalt in der Spielwelt. Bei einer Reise ändert Codex `current_location` und die Links am Zielort, kopiert oder verschiebt die NPC-Datei aber nicht. Erst wenn sich die dauerhafte redaktionelle Zuordnung ändert, wird die kanonische Datei einmalig verschoben und werden alle Verweise angepasst. Details stehen in [Beziehungen und ortszentrierte Speicherung](beziehungen-und-speicherorte.md).

## Assets sicher ändern oder ausmustern

Für seltene Änderungen soll Codex vor dem Schreiben zuerst den betroffenen Umfang nennen. Geeignete Aufträge sind:

> Ändere nur den sichtbaren Titel von `<asset>`. Behalte ID, Slug und Pfad bei und aktualisiere Index, Linktexte, Version, Datum und Change Log.

> Verschiebe die redaktionelle Ownership von `<asset>` nach `<location>`. Nenne vorher alle betroffenen Pfade, Links, Beziehungen und Indizes. Behalte die ID bei und stoppe bei Mehrdeutigkeit.

> Setze `<asset>` auf `retired`. Prüfe vorher aktive Abhängigkeiten, behalte die Datei auffindbar und entscheide jeden eingehenden Link bewusst.

Eine Titeländerung verändert niemals automatisch ID, Slug oder Pfad. Ein Ownership-Wechsel verschiebt genau eine kanonische Datei und entfernt den alten Pfad. Ein retired Asset bleibt mit stabilem Pfad und Indexzeile auffindbar; es wird nicht automatisch gelöscht.

Bei einer gewünschten Zusammenführung nennt Codex zuerst beide kanonischen Dateien und alle Konflikte. Der User entscheidet ausdrücklich, welche ID, welcher Pfad und welche Aussagen überleben. Ohne diese Entscheidung werden keine Inhalte zusammengeführt. Der vollständige Preflight und die Checklisten stehen unter [Änderungsabläufe](beziehungen-und-speicherorte.md#änderungsabläufe).

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

Bilddateien werden als PNG gespeichert. Ein Visual-Ordner enthält das kanonische `visual.md`, ein gleichnamiges Bildbriefing mit der Endung `.prompt.md` und optional die PNG-Datei. Die Subject-Datei bleibt Quelle stabiler Identitätsmerkmale; Visual und Prompt trennen diese Merkmale vom dargestellten One-Shot-Zustand sowie von Stil, Perspektive und Licht.

Ein Bildbriefing kann bereits erstellt werden, ohne das Bild zu generieren. Bitte Codex vor einer Erzeugung um das vollständige Briefing und gib die konkrete Visual-Version sowie den Zielpfad ausdrücklich frei. Das gilt erneut, wenn eine vorhandene PNG-Datei ersetzt werden soll. Nach einer Briefing-Änderung bleibt das ältere PNG erhalten, wird aber als `stale` geführt. Codex darf erst dann behaupten, dass ein aktuelles Bild vorhanden ist, wenn die PNG-Datei tatsächlich gespeichert wurde. Details stehen im [Bild-Workflow](bild-workflow.md).

## Vor dem Spielen

Beauftrage Codex mit einer Konsistenzprüfung des vollständigen One-Shots. Der technische Validator und der fachliche Audit werden getrennt berichtet. Der [Fachliche Audit-Leitfaden](adventure-audit-guide.md) verlangt für jedes Finding Begründung, betroffene Dateien, Auswirkung und kleinste sinnvolle Korrekturrichtung. Ohne ausdrücklichen Fix-Auftrag verändert Codex keine Inhalte.

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
