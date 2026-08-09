# Geführter One-Shot-Intake v1

Diese Datei definiert den reproduzierbaren Erstlauf, mit dem Codex aus einem freien Welt- und Plottext einen belastbaren, in sich abgeschlossenen One-Shot erzeugt. Sie ist die normative Quelle für Eingaben, Rückfragen, Annahmen, Ablage und Definition of Done. Die fachlichen Regeln für Entscheidungen, Informationswege und Folgezustände stehen im [Leitfaden für Spielerentscheidungen und Abenteuerstruktur](adventure-structure-guide.md).

## Inhalt

- [Ziel und Ergebnis](#ziel-und-ergebnis)
- [One-Shot-Prämisse](#one-shot-prämisse)
- [Minimale Eingaben](#minimale-eingaben)
- [Optionale Vertiefung](#optionale-vertiefung)
- [Rückfragen und Annahmen](#rückfragen-und-annahmen)
- [Ablage und Trennung](#ablage-und-trennung)
- [Workflow](#workflow)
- [Definition of Done](#definition-of-done)
- [Erwartete Abschlussmeldung](#erwartete-abschlussmeldung)
- [Deutsche Nutzerprompts](#deutsche-nutzerprompts)

## Ziel und Ergebnis

Der Erstlauf erzeugt keinen ausgeschriebenen Abenteuerband. Er schafft jedoch bereits die vollständige, auflösbare Struktur des One-Shots, von der aus Orte und Assets gezielt vertieft werden können.

Nach dem Erstlauf existieren:

- die unveränderte Originalanfrage;
- getrennte Welt-, Plot- und Constraint-Extrakte;
- eine Weltübersicht und eine Plotübersicht;
- nur die für Einstieg, Kernkonflikt und mögliche Auflösungen notwendigen Locations und Assets;
- aktuelle Indizes;
- getrennte Klarstellungen, Annahmen, Entscheidungen und offene Fragen;
- eine Abschlussmeldung mit Ergebnis, Unsicherheiten, Validierung und nächsten Schritten.

## One-Shot-Prämisse

Vor der Asset-Erzeugung leitet Codex aus den bestätigten Angaben eine kompakte, spielbare One-Shot-Prämisse ab. Sie ist kein zusätzlicher Dateityp und keine zweite Kanonquelle. Ihre Plotbestandteile werden in `adventure/20-plot/overview.md`, ihre Nutzerpräferenzen in `adventure/00-input/constraints.md` geführt.

Die Prämisse beantwortet:

1. **Player-facing starting situation:** Welche Lage, Gelegenheit oder Bedrohung können die Spieler zu Beginn wahrnehmen?
2. **Central conflict:** Welche zentrale dramatische Frage kann innerhalb dieses One-Shots beantwortet werden?
3. **Player influence:** Über welche mindestens zwei grundsätzlich unterschiedlichen Arten können Spieler die Lage beeinflussen, ohne dass ihre konkrete Entscheidung vorweggenommen wird?
4. **Resolution boundary:** Welcher Konflikt muss im One-Shot auflösbar sein und welche Nebenfragen dürfen bewusst offen bleiben?
5. **Target frame:** Welche ungefähre Spieldauer und Inhaltsdichte wünscht der User?
6. **Tone and boundaries:** Welche Stimmung, Themen, Schwerpunkte und Inhaltsgrenzen wurden genannt?

Fehlt eine nicht blockierende Präferenz, wird sie als `open` dokumentiert. Codex erfindet weder Spielerrollen noch Präferenzen. Eine Rückfrage ist nur nötig, wenn unterschiedliche Antworten den ersten Asset-Umfang, die zentrale Konfliktstruktur oder eine ausdrückliche Inhaltsgrenze materiell verändern würden.

## Minimale Eingaben

Der User darf in freiem Text schreiben. Eine feste Formularsprache ist nicht erforderlich.

| Input | Erforderlich | Regel |
|---|---:|---|
| Weltbeschreibung | ja | Mindestens Prämisse, Umgebung oder erkennbare Weltlogik, aus der ein erster Kontext ableitbar ist. |
| Plotbeschreibung | ja | Mindestens Ausgangskonflikt, drohende Entwicklung oder dramatische Frage. |
| Titel | nein | Codex darf einen ausdrücklich vorläufigen Arbeitstitel vorschlagen und als Annahme dokumentieren. |
| Startort | nein | Wird aus dem Plot abgeleitet; nur bei strukturell gleichwertigen, stark unterschiedlichen Optionen nachfragen. |
| Spielerrolle | nein | Wird nur übernommen, wenn der User sie vorgibt; andernfalls bleibt der Einstieg rollen- und motivationsneutral. |
| Zielspielzeit und Inhaltsdichte | nein | Eine Nutzerangabe wird übernommen; fehlt sie, werden beide Werte im Intake ausdrücklich als `open` dokumentiert. |
| Ton, Themen, Schwerpunkte und Inhaltsgrenzen | nein | Ausdrückliche Angaben werden übernommen; fehlende Präferenzen bleiben `open` und werden nicht stillschweigend festgelegt. |
| Regelsystem | nein | Das Repository bleibt unabhängig von der Antwort regelneutral. |

Fehlt Welt- oder Plottext vollständig, beginnt Codex nicht mit der Initialisierung. Es bittet gezielt um die fehlende minimale Eingabe.

## Optionale Vertiefung

Die folgenden Fragen verbessern den Entwurf, blockieren ihn aber normalerweise nicht:

- Welche Stimmung und welche zentralen Themen sind gewünscht?
- Welche Inhalte oder Themen sollen ausgeschlossen werden?
- Soll der One-Shot eher Erkundung, soziale Spannung, Mysterium, Reise oder offenen Konflikt betonen?
- Welche Rolle oder Ausgangslage haben die Spielerfiguren?
- Welche ungefähre Spieldauer und inhaltliche Dichte sind vorgesehen?
- Gibt es unverzichtbare Orte, Fraktionen, Figuren, Gegenstände oder Enthüllungen?
- Wie offen oder zielgerichtet sollen mögliche Verläufe sein?

Codex übernimmt bereits enthaltene Antworten in `constraints.md` und dokumentiert fehlende Präferenzen als `open`. Es stellt nicht automatisch den vollständigen Fragenkatalog, sondern fragt nur, wenn eine Antwort den ersten kohärenten Stand materiell verändert.

## Rückfragen und Annahmen

### Blockierende Rückfragen

Vor der Initialisierung wird nur gefragt, wenn mindestens eine Bedingung erfüllt ist:

1. Welt- oder Plotbeschreibung fehlt vollständig.
2. Zwei Aussagen widersprechen sich in einer Weise, die Kernprämisse, Startort oder zentralen Konflikt unterschiedlich strukturieren würde.
3. Mehrere gleich plausible Interpretationen würden zu deutlich verschiedenen ersten Locations oder Plot-Threads führen.
4. Eine ausdrückliche Nutzergrenze ist so unklar, dass ihre falsche Auslegung den gewünschten Inhalt verletzen könnte.
5. Eine player-facing Ausgangslage lässt sich nur ableiten, indem Codex Herkunft, Motivation, Loyalität oder Entscheidung der Spielerfiguren erfinden müsste.

Rückfragen werden in einem kompakten Block gestellt. Nur die kleinste Zahl von Fragen verwenden, die den Erstlauf freigibt; in der Regel höchstens drei.

### Dokumentierbare Annahmen

Eine Annahme darf den Erstlauf nicht als bestätigten Kanon verändern. Sie ist zulässig, wenn sie:

- leicht umkehrbar ist;
- keine Nutzerangabe überschreibt;
- keine neue zentrale Wahrheit, Auflösung oder Spielerrolle festlegt;
- nur Arbeitsorganisation, vorläufige Benennung oder eine neutrale Verbindung unterstützt.

Beispiele sind ein vorläufiger Titel, ein technischer Slug oder die Reihenfolge, in der bereits genannte Orte ausgearbeitet werden.

Jede Annahme wird in `adventure/90-meta/assumptions.md` als `proposed` gespeichert. Abgeleitete Dateien kennzeichnen sie als Arbeitsannahme und verlinken den Eintrag. Erst nach Bestätigung wird sie in `decisions.md` übernommen oder als bestätigte Wahrheit eingearbeitet.

### Nicht zulässige stille Annahmen

Codex darf insbesondere nicht ungefragt festlegen:

- die wahre Auflösung eines zentralen Mysteriums;
- Motive oder Schuld wichtiger Akteure;
- die Rolle, Herkunft oder Ziele der Spielerfiguren;
- ausgeschlossene oder sensible Inhalte;
- eine verpflichtende Reihenfolge von Spielerentscheidungen;
- systemspezifische Werte oder Mechaniken.

Solche Punkte bleiben offene Fragen oder werden vorab geklärt, wenn sie den ersten kohärenten Stand blockieren.

## Ablage und Trennung

| Inhalt | Kanonische Datei | Pflege |
|---|---|---|
| vollständige ursprüngliche Nutzeranfrage | `00-input/original-request.md` | Nach dem ersten Speichern nicht umformulieren oder überschreiben. |
| extrahierte Weltangaben | `00-input/world.md` | Mit Quelle zur Originalanfrage; keine neuen Fakten ergänzen. |
| extrahierte Plotangaben | `00-input/plot.md` | Mit Quelle zur Originalanfrage; keine neue Auflösung ergänzen. |
| extrahierte Grenzen und Präferenzen | `00-input/constraints.md` | Zielspielzeit, Inhaltsdichte, Ton, Themen, Schwerpunkt und Grenzen führen; fehlende Werte als `open` markieren. |
| abgeleitete One-Shot-Prämisse | `20-plot/overview.md` | Ausgangslage, zentralen Konflikt, Spieler-Einfluss und Abschlussrahmen aus bestätigten Angaben ableiten; Unsicherheit verlinken. |
| spätere Antworten und Präzisierungen | `00-input/clarifications.md` | Datiert, wortgetreu und mit betroffener Frage speichern. |
| unbestätigte Arbeitsannahmen | `90-meta/assumptions.md` | Status `proposed`, `confirmed`, `rejected` oder `superseded`. |
| getroffene Entscheidungen | `90-meta/decisions.md` | Entscheidung, Begründung und Autorität getrennt führen. |
| noch offene Entscheidungen | `90-meta/open-questions.md` | Priorität, Auswirkung, verantwortliche Person und Status führen. |
| durchgeführte Änderungen | `90-meta/change-log.md` | Dateien und Grund nachvollziehbar festhalten. |

Originaltext, Klarstellung, Annahme und Entscheidung dürfen nicht in derselben Tabelle vermischt werden. Eine spätere Klarstellung ergänzt die Originalanfrage, verändert sie aber nicht rückwirkend.

## Workflow

### 1. Preflight

1. Prüfen, ob `adventure/` bereits existiert.
2. Bei vorhandenem Abenteuer keine zweite Initialisierung durchführen; stattdessen den bestehenden Stand fortsetzen.
3. Welt- und Plottext auf minimale Vollständigkeit prüfen.
4. Nur blockierende Rückfragen stellen.
5. Titel übernehmen oder einen vorläufigen Arbeitstitel als Annahme kennzeichnen.

### 2. Scaffold und Originaleingabe

1. Einen stabilen Slug ableiten.
2. `python3 scripts/init_adventure.py --slug <slug> --title "<title>"` ausführen.
3. Den World-Singleton mit `python3 scripts/new_asset.py --type world --slug <slug> --title "<title>" --overwrite` aus dem Asset-Template erzeugen. `--overwrite` nur verwenden, solange `10-world/overview.md` noch die unveränderte Scaffold-Platzhalterdatei ist; sonst stoppen und den bestehenden Inhalt erhalten.
4. Die vollständige Nutzeranfrage unverändert in `00-input/original-request.md` einfügen.
5. Welt-, Plot- und Constraint-Angaben in die jeweiligen Input-Dateien extrahieren und zur Originalanfrage verlinken.
6. Noch keine Bilder erzeugen oder Bilddateien behaupten.

### 3. Aussagen klassifizieren

Jede relevante Aussage genau einer Arbeitskategorie zuordnen:

- `established`: ausdrücklich vom User vorgegeben oder später bestätigt;
- `clarification`: datierte Präzisierung einer vorherigen Aussage;
- `assumption`: umkehrbare, noch unbestätigte Arbeitsannahme;
- `decision`: bewusst getroffene und begründete Festlegung;
- `open`: ausstehende Entscheidung oder Wissenslücke.

Nicht bestätigte Annahmen erscheinen nie unter „Established truths“ oder als feststehende Plotauflösung.

### 4. One-Shot-Prämisse prüfen

1. Eine player-facing Ausgangslage formulieren, ohne Hintergrund, Motivation, Loyalität oder Entscheidung der Spielerfiguren festzulegen.
2. Den zentralen Konflikt als innerhalb des One-Shots beantwortbare dramatische Frage abgrenzen.
3. Mindestens zwei grundsätzlich unterschiedliche Formen der Spieler-Einflussnahme benennen, ohne eine Methode oder Reihenfolge vorzuschreiben.
4. Den Abschlussrahmen festhalten: Was muss auflösbar sein, was darf als bewusste Nebenfrage offen bleiben?
5. Zielspielzeit, Inhaltsdichte, Ton, Themen, Schwerpunkt und Inhaltsgrenzen aus den Eingaben übernehmen oder jeweils als `open` dokumentieren.
6. Jede unbestätigte Interpretation in `assumptions.md` oder `open-questions.md` ablegen und aus der Prämisse darauf verweisen.

Erst nach diesem Check wird entschieden, welche Locations und Assets wirklich notwendig sind.

### 5. Erster strukturierter Stand

1. `10-world/overview.md` mit Prämisse, bestätigten Wahrheiten, Alltag, Kräften und Unknowns füllen.
2. `10-world/themes.md` nur mit belegten Themen und Guardrails füllen; fehlende Angaben offenlassen.
3. `10-world/timeline.md` nur mit ausdrücklich etablierten oder klar als unbekannt markierten Ereignissen ergänzen.
4. `20-plot/overview.md` mit player-facing Ausgangslage, flexiblen Spieler-Hooks, zentralem Konflikt, mindestens zwei Formen der Spieler-Einflussnahme, Stakes, möglichen Zielen, Entscheidungsraum, Informationswegen, Abschlussrahmen, Folgen von Scheitern oder Ignorieren und mehreren möglichen Ergebnissen füllen. Im Abschnitt `One-shot scope and pacing` den minimalen Auflösungszustand, `core`, `supporting` und `optional` Inhalte, mindestens eine sichere Kürzung und einen vorbereiteten `late pressure`-Zustandswechsel festhalten.
5. Nur Plot-Threads anlegen, die für den Kernkonflikt und seine möglichen Auflösungen erforderlich sind. Jeder aktive Thread benennt seinen minimalen Auflösungszustand, unverzichtbare Informationen, sichere Kürzungen und die Auswirkung dieser Kürzungen.
6. Genau die Locations anlegen, die für Einstieg, zentrale Entscheidungen, Verständnis oder Auflösung des Kernkonflikts notwendig sind.
7. Nur Assets anlegen, die für den vollständigen One-Shot oder die logische Verbindung des Plots benötigt werden.
8. Ownership, Metadaten und Beziehungen nach den normativen Referenzen setzen.

Nicht jeden erwähnten Ort, NPC oder Gegenstand ausarbeiten. Ein Name oder Link genügt, wenn das Asset noch keine eigenständige Tischfunktion benötigt.

### 6. Navigation und Nachweis

1. Alle erzeugten Assets aus den passenden Locations und Indizes verlinken. In den sechs Indizes je einen kurzen tischrelevanten Kontext ergänzen; vollständige Beschreibungen bleiben im kanonischen Asset.
2. Annahmen, Entscheidungen und offene Fragen in ihren getrennten Dateien erfassen.
3. Den Erstlauf in `90-meta/change-log.md` dokumentieren.
4. `adventure/README.md` mit Kurzfassung, Arbeitsstand, wichtigster offener Frage und nächsten Schritten aktualisieren. Die Tischübersicht muss Ausgangslage, zentralen Konflikt, aktuellen Druck, zentrale Akteure, notwendige Informationen, mögliche Abschlüsse und relevante Folgezustände knapp beantworten; Pacing und sichere Kürzungen nur zusammenfassen und zum Plot verlinken.
5. `python3 scripts/validate_adventure.py` ausführen und strukturelle Fehler beheben.

## Definition of Done

Der Erstlauf ist abgeschlossen, wenn alle folgenden Punkte erfüllt sind:

- [ ] `00-input/original-request.md` enthält die unveränderte ursprüngliche Anfrage.
- [ ] Welt, Plot und Constraints sind extrahiert und auf die Originalanfrage zurückführbar.
- [ ] Klarstellungen, Annahmen, Entscheidungen und offene Fragen sind getrennt gespeichert.
- [ ] Die One-Shot-Prämisse benennt player-facing Ausgangslage, zentralen Konflikt, mindestens zwei Formen der Spieler-Einflussnahme und den Abschlussrahmen.
- [ ] Zielspielzeit, Inhaltsdichte, Ton, Themen, Schwerpunkt und Inhaltsgrenzen sind als Nutzerangabe oder ausdrücklich als `open` dokumentiert.
- [ ] Der Plot unterscheidet `core`, `supporting` und `optional` Inhalte in Prosa und benennt mindestens eine sichere Kürzung.
- [ ] Der minimale Auflösungszustand bleibt nach jeder vorgesehenen Kürzung erreichbar; notwendige Schlussfolgerungen behalten ihre unabhängigen Entdeckungspfade.
- [ ] Ein vorbereiteter `late pressure`-Zustandswechsel verdichtet den One-Shot, ohne eine Spielerentscheidung oder feste Szenenfolge zu erzwingen.
- [ ] `10-world/overview.md` trennt bestätigte Wahrheiten von Unknowns und Arbeitsannahmen.
- [ ] `20-plot/overview.md` enthält Ausgangslage, zentralen Konflikt, Stakes und mehrere mögliche Auflösungen des vollständigen One-Shots.
- [ ] Der Einstieg bietet mindestens zwei erkennbare Ansatzpunkte, ohne Motivation oder Entscheidung der Spielerfiguren vorzugeben.
- [ ] Notwendige Schlussfolgerungen besitzen mindestens zwei unabhängige Entdeckungspfade; keine Pflichtentwicklung hängt an einer einzelnen Scene.
- [ ] Zentrale Entscheidungen sowie Scheitern, Rückzug oder Ignorieren führen zu spielbaren Folgezuständen.
- [ ] Der zentrale Konflikt besitzt mindestens zwei plausible Auflösungen oder eine Auflösung plus einen bewusst offenen Endzustand.
- [ ] Alle für Einstieg und Kernkonflikt notwendigen Locations existieren; optionale Orte wurden nicht vorsorglich ausgebaut.
- [ ] Notwendige Plot-Threads und Assets besitzen kanonische Pfade, Metadaten und Links.
- [ ] Alle sechs Indizes spiegeln den erzeugten Stand wider.
- [ ] Jeder Indexeintrag besitzt einen kurzen tischrelevanten Kontext und genau einen Link zur einzigen kanonischen Beschreibung.
- [ ] Jedes zentrale Asset ist direkt aus der README oder über genau einen passenden Index ohne Volltextsuche erreichbar.
- [ ] `adventure/README.md` nennt Arbeitsstand, wichtigste offene Frage und nächste Schritte und beantwortet die für die Tischübersicht geforderten Kernfragen.
- [ ] Es wurden keine PNGs oder automatischen Bilder erzeugt.
- [ ] `python3 scripts/validate_adventure.py` endet ohne Fehler.
- [ ] Der User erhält die definierte Abschlussmeldung.

## Erwartete Abschlussmeldung

Codex antwortet nach dem Erstlauf auf Deutsch und in dieser Reihenfolge:

1. **Erzeugter Stand:** Titel, player-facing Ausgangslage, zentraler Konflikt, Formen der Spieler-Einflussnahme und wichtigste angelegte Bereiche.
2. **Bestätigte Grundlage:** die wesentlichen Nutzerfakten, ohne Annahmen beizumischen.
3. **Annahmen:** Anzahl und wichtigste noch unbestätigte Arbeitsannahmen mit Dateiverweis.
4. **Offene Fragen:** blockierende oder besonders wirkungsvolle Fragen mit Dateiverweis.
5. **Validierung:** exaktes Ergebnis des Validators.
6. **Nächste Schritte:** zwei bis vier konkrete, priorisierte Folgeaufträge.

Keine Datei oder kein Bild als erzeugt melden, wenn sie beziehungsweise es nicht tatsächlich existiert.

## Deutsche Nutzerprompts

### Minimaler Start

> Erstelle einen neuen regelneutralen One-Shot. Die Welt ist: … Der Ausgangskonflikt ist: … Bewahre meinen Originaltext, dokumentiere Annahmen getrennt und erstelle nur den notwendigen vollständigen Stand.

### Start mit Leitplanken

> Erstelle einen One-Shot mit dem Titel „…“. Welt: … Plot: … Gewünschte Stimmung: … Ausgeschlossen sind: … Frage nur nach Punkten, die den ersten kohärenten Stand wesentlich verändern. Erzeuge noch keine Bilder.

### Stark freier Start

> Ich habe eine grobe Idee für einen One-Shot: … Strukturiere daraus Welt und Plot, markiere alles Unbestätigte als Annahme oder offene Frage und nenne mir danach die sinnvollsten nächsten Ausarbeitungsschritte.
