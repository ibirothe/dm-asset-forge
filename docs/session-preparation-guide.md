# Leitfaden für Session-Vorbereitung

Dieser Leitfaden beschreibt, wie Codex aus dem kanonischen Abenteuer eine kompakte Markdown-Arbeitsmappe für einen konkreten Spielabend erstellt. Die Arbeitsmappe ist eine abgeleitete Tischansicht, keine zweite Wahrheit. Bei jedem Widerspruch gelten die verlinkten kanonischen Assets.

## Inhalt

- [Zweck und Grenzen](#zweck-und-grenzen)
- [Speicherort und Dateiname](#speicherort-und-dateiname)
- [Eingaben](#eingaben)
- [Leseumfang bestimmen](#leseumfang-bestimmen)
- [Arbeitsmappe erstellen](#arbeitsmappe-erstellen)
- [Player-safe und DM-only](#player-safe-und-dm-only)
- [Startsituation und Übergänge](#startsituation-und-übergänge)
- [NPC-Kurzprofile](#npc-kurzprofile)
- [Informationen und Handouts](#informationen-und-handouts)
- [Folgezustände](#folgezustände)
- [Improvisationsanker](#improvisationsanker)
- [Quellenregister und Aktualität](#quellenregister-und-aktualität)
- [Pflegegrenzen](#pflegegrenzen)
- [Definition of Done](#definition-of-done)

## Zweck und Grenzen

Eine Session-Arbeitsmappe verdichtet nur Inhalte, die für den gewählten Spielhorizont wahrscheinlich relevant oder als Ausweichmaterial unmittelbar nützlich sind. Sie soll während des Spiels schnelles Erfassen ermöglichen und unerwartete Spielerentscheidungen unterstützen.

Sie ist ausdrücklich:

- kein kanonisches Asset und verwendet deshalb kein Asset-Frontmatter;
- keine vollständige Kopie beteiligter Assets;
- keine Vorhersage einer Szenenreihenfolge oder Spielerentscheidung;
- kein Ersatz für Plot-, Location-, NPC-, Information-, Encounter- oder Handout-Dateien;
- keine player-facing Ausgabe; die gesamte Datei gilt als DM-only;
- kein Generator-, PDF-, Build- oder Release-Ergebnis.

Komprimierte Aussagen tragen immer einen relativen Link zu ihrer kanonischen Quelle. Neue Ideen und Improvisationsanker werden als `provisional` markiert und gelten nicht als etablierter Kanon.

## Speicherort und Dateiname

Session-Arbeitsmappen liegen unter:

```text
adventure/60-sessions/<YYYY-MM-DD>-<session-slug>.md
```

Das Datum ist das geplante Session-Datum; ist es noch unbekannt, wird das Erstellungsdatum verwendet und dies unter „Session metadata“ vermerkt. Der Slug ist lowercase ASCII kebab-case. Eine bestehende Arbeitsmappe wird nicht still ersetzt. Bei gleichem Datum erhält sie einen unterscheidbaren Fokus-Slug.

Als Grundlage dient `templates/session-prep.md`. Das Verzeichnis `adventure/60-sessions/` wird bei Bedarf angelegt. Die Datei bleibt Markdown und enthält keine generierten Bilder.

## Eingaben

| Eingabe | Erforderlich | Umgang mit fehlender Angabe |
|---|---:|---|
| Session-Ziel oder Fokus | ja | Aus bestehendem Arbeitsstand vorschlagen, aber vor der endgültigen Auswahl bestätigen lassen, wenn mehrere deutlich verschiedene Fokusse plausibel sind. |
| Geplantes Session-Datum | nein | Erstellungsdatum verwenden und als Planungsannahme kennzeichnen. |
| Erwartete Locations | nein | Aus Startzustand und Fokus ableiten; Alternativorte nur aufnehmen, wenn sie plausibel erreichbar sind. |
| Aktive Plot-Threads | nein | Aus Open-threads-Index und Fokus auswählen. |
| Beteiligte Assets | nein | Aus Locations, Threads und direkten Beziehungen ableiten. |
| Gewünschte Dauer oder Umfang | nein | Eine kompakte Session ohne feste Scene-Zahl vorbereiten. |
| Bekannte letzte Spielsituation | bedingt | Bei fortlaufendem Abenteuer erforderlich, wenn der aktuelle Startzustand nicht eindeutig dokumentiert ist. |

Nur Fragen stellen, deren Antwort Startsituation, relevanten Lesescope oder zentrale Vorbereitung wesentlich verändert. Fehlende Kanonentscheidungen nicht in der Arbeitsmappe lösen, sondern als offene Frage verlinken.

## Leseumfang bestimmen

1. `adventure/README.md`, die fünf Indizes und relevante Meta-Dateien lesen.
2. Session-Fokus, unmittelbaren Startzustand und betrachteten Spielhorizont festhalten.
3. Erwartete Locations und aktive Plot-Threads auswählen.
4. Von dort nur direkt benötigte NPCs, Informationen, Encounters, Events, Handouts, Objekte, Fraktionen und Random Tables verfolgen.
5. Einen kleinen Ausweichring ergänzen: unmittelbar benachbarte Locations, ein plausibler alternativer Akteur oder ein offener Thread, den Spieler unerwartet aufgreifen könnten.
6. Alles ausschließen, was weder Fokus, Startzustand, erwartbare Übergänge noch Improvisation unterstützt.

Die Arbeitsmappe soll am Tisch schneller sein als das Durchsuchen des gesamten Abenteuers. Vollständige Biografien, Weltgeschichte und entfernte Plotäste gehören nicht hinein.

## Arbeitsmappe erstellen

Die Abschnitte des Templates werden in dieser Reihenfolge gefüllt:

1. **Session metadata:** Erstellungsdatum, Session-Datum, Fokus, Spielhorizont und Aktualitätsstatus.
2. **Scope:** Ziel, erwartete Locations, aktive Plot-Threads und beteiligte Assets als Links.
3. **Immediate starting state:** Wahrnehmbare Lage, aktueller Druck, anwesende Akteure und offene Ansatzpunkte.
4. **Possible transitions:** Auslöser, veränderter Zustand und kanonische Quelle; keine Pflichtreihenfolge.
5. **NPC quick reference:** nur unmittelbar relevante Darstellung und Reaktionen.
6. **Information and handouts:** player-safe Bekanntes getrennt von DM-only Hinweisen, Geheimnissen und Auslieferungspunkten.
7. **Active pressure and consequences:** laufende Akteurspläne, Eskalationen und offene Konsequenzen.
8. **Outcome states:** Erfolg, Teilerfolg, Scheitern, Rückzug und Ignorieren als mögliche veränderte Zustände.
9. **Improvisation anchors:** provisional Namen, Gerüchte, Umgebungsdetails und alternative Reaktionen.
10. **Source register:** alle verwendeten Quellen mit aufgezeichnetem Versionsstand.
11. **Pre-session review:** Aktualität, Links, Sichtbarkeit und Tischreife prüfen.

Abschnitte werden knapp gehalten. Ein Link allein genügt nicht, wenn der DM die Information unmittelbar am Tisch braucht; eine komprimierte Aussage ohne Quellenlink ist ebenfalls unzulässig.

## Player-safe und DM-only

Die Arbeitsmappe als Ganzes ist DM-only. Innerhalb der Datei werden Inhalte trotzdem getrennt:

- **Player-safe known facts:** bereits bekannte oder unmittelbar sichtbare Tatsachen, die der DM offen wiedergeben kann;
- **DM-only clues and secrets:** verborgene Wahrheit, Motive, geplante Entwicklungen, noch nicht offenbarte Hinweise und Konsequenzen;
- **Handouts:** nur Auslieferungssituation und Link zum kanonischen Handout; die Arbeitsmappe ersetzt keine freigegebene Spielerdatei.

Player-safe Abschnitte enthalten keine YAML-Metadaten, internen IDs ohne Erklärung, unveröffentlichten Wahrheitsstatus oder unbeabsichtigte Hinweise auf Geheimnisse. Inhalte werden nicht aus der Arbeitsmappe an Spieler weitergegeben, solange sie nicht über einen eigenen Handout-Workflow freigegeben wurden.

## Startsituation und Übergänge

Die Startsituation beantwortet auf einen Blick:

- Was können die Spieler jetzt wahrnehmen oder wissen?
- Wo befinden sich die relevanten Akteure?
- Welcher Druck ist bereits aktiv?
- Welche mindestens zwei Ansatzpunkte sind sichtbar oder leicht erreichbar?
- Was geschieht zunächst ohne Eingreifen?

Übergänge sind mögliche Zustandsänderungen, keine Scenes in fester Reihenfolge. Jeder vorbereitete Übergang nennt Auslöser, sichtbare Veränderung, betroffene Assets und Quelle. Unerwartete Ansätze werden anhand etablierter Interessen und Umstände beurteilt; die Tabelle begrenzt keine zulässigen Handlungen.

## NPC-Kurzprofile

Nur NPCs aufnehmen, die im Startzustand, in einem erwarteten Übergang oder als plausibler Ausweichkontakt relevant sind. Pro NPC knapp festhalten:

- Name, Rolle und Quellenlink;
- ein erkennbares Merkmal und ein Hinweis für Stimme oder Ausdruck;
- aktuelles Ziel oder Motivation;
- unmittelbar nutzbares Wissen, getrennt nach Wahrheit und Irrtum;
- wahrscheinliche Reaktion auf Hilfe, Druck, Täuschung und Ignorieren, soweit relevant;
- aktuelle Beziehung oder Konsequenz, die sich in dieser Session verändern kann.

Die Kurzfassung überschreibt das NPC-Asset nicht. Ändert sich die kanonische Quelle, wird das Profil geprüft und nicht automatisch als neue Wahrheit zurückgeschrieben.

## Informationen und Handouts

Für notwendige Schlussfolgerungen werden die unabhängigen Entdeckungspfade zusammen sichtbar gemacht. Jeder Eintrag nennt:

- die konkrete Information oder Schlussfolgerung;
- präsentierbare Hinweise und jeweilige Zugänge;
- bekannten Wahrheitsstatus nur im DM-only Bereich;
- Folgen von Lernen, spätem Lernen oder Verpassen;
- Links zu `information`, beteiligten Assets und gegebenenfalls `handout`.

Ein Handout-Eintrag nennt Auslieferungsbedingung, Freigabestatus und kanonische Quelle. Die Session-Arbeitsmappe enthält keine neu formulierte Spielerfassung und ersetzt keine Handout-Datei.

## Folgezustände

Für zentrale Drucksituationen werden mindestens diese Ergebnisarten bedacht, soweit sie plausibel sind:

| Ergebnisart | Vorbereitungsfrage |
|---|---|
| Erfolg | Welcher Zustand verändert sich zugunsten der Spieler, und welcher neue Druck bleibt? |
| Teilerfolg oder Preis | Was wird erreicht, und welche Kosten, Verpflichtungen oder Risiken entstehen? |
| Scheitern | Was verschlechtert oder verlagert sich, und welcher Ansatz bleibt offen? |
| Rückzug | Was bleibt erhalten, was schreitet fort, und unter welchen Bedingungen ist Rückkehr möglich? |
| Ignorieren | Wer handelt stattdessen, welche Zeichen werden sichtbar, und wo berührt die Entwicklung das Spiel erneut? |

Die Arbeitsmappe bereitet Zustände vor, keine festgelegten Ergebnisse. Fehlt für eine zentrale Situation ein spielbarer Folgezustand, wird dies als Vorbereitungslücke markiert und nicht durch erfundenen Kanon verdeckt.

## Improvisationsanker

Improvisationsanker helfen bei nicht erwarteten Entscheidungen, ohne sie vorherzusagen. Geeignet sind:

- kurze Namen für beiläufige Personen;
- Gerüchte mit ausdrücklich markiertem Wahrheitsstatus `provisional`;
- sensorische Umgebungsdetails ohne neue Plotbehauptung;
- alternative Reaktionen bereits etablierter Akteure, aus ihren Motiven abgeleitet;
- neutrale Komplikationen, die bestehenden Druck sichtbar machen;
- passende Einträge aus kanonischen Random Tables.

Jeder nicht bereits kanonische Anker wird sichtbar als `provisional` markiert. Wird er im Spiel relevant, muss er nach der Session bewusst bestätigt, verworfen oder als offene Frage behandelt werden. Die Vorbereitung allein macht ihn nicht zum Kanon.

## Quellenregister und Aktualität

Jede komprimierte Quelle erscheint im Quellenregister mit:

- relativem Markdown-Link;
- Funktion in der Session;
- beim Erstellen gelesener `version`;
- beim Erstellen gelesenen `updated`-Datum;
- Prüfstatus `current`, `changed`, `missing` oder `not-checked`.

Für Dateien ohne Asset-Frontmatter wird statt Version `n/a` und das beim Erstellen geprüfte Datum eingetragen.

Vor der Session wird jede Quelle erneut geöffnet:

- `current`: Pfad existiert und aufgezeichnete Version sowie `updated` stimmen überein;
- `changed`: Quelle existiert, aber Version oder `updated` weicht ab;
- `missing`: Link oder Datei ist nicht mehr erreichbar;
- `not-checked`: Vergleich wurde noch nicht durchgeführt.

Bei `changed` wird die betroffene Kurzfassung manuell gegen die Quelle geprüft. Der Status wird erst danach auf `current` gesetzt und die aufgezeichneten Werte werden aktualisiert. Bei `missing` wird die Quelle nicht still ersetzt. Der technische Validator erkennt gebrochene relative Links; der fachliche Audit vergleicht Quellenstände und abgeleitete Aussagen.

## Pflegegrenzen

- Änderungen an der Arbeitsmappe ändern niemals automatisch kanonische Assets.
- Entdeckte Widersprüche werden als Audit-Finding oder offene Frage berichtet, nicht in der Arbeitsmappe entschieden.
- Eine kanonische Änderung kann die Arbeitsmappe veralten lassen; das Quellenregister macht dies sichtbar.
- Sitzungsentscheidungen und improvisierte Fakten werden nach dem Spiel nicht ausschließlich in der Arbeitsmappe belassen.
- Eine neue Session erhält eine neue Datei. Frühere Arbeitsmappen bleiben als zeitgebundene Vorbereitung erhalten und werden nicht zur aktuellen Kanonquelle umgedeutet.
- Erstellung oder Aktualisierung wird knapp in `90-meta/change-log.md` dokumentiert, ohne die komprimierten Inhalte dort zu duplizieren.

## Definition of Done

Eine Session-Arbeitsmappe ist tischbereit, wenn:

- [ ] Session-Fokus, Datum, Spielhorizont und Scope klar sind;
- [ ] nur relevante Locations, Plot-Threads und Assets aufgenommen wurden;
- [ ] die unmittelbare Startsituation und mindestens zwei plausible Ansatzpunkte schnell erfassbar sind;
- [ ] mögliche Übergänge als Zustandsänderungen statt als Pflichtreihenfolge beschrieben sind;
- [ ] relevante NPC-Kurzprofile Motivation, Wissen, Stimme und wahrscheinliches Verhalten enthalten;
- [ ] player-safe bekannte Fakten und DM-only Hinweise oder Geheimnisse eindeutig getrennt sind;
- [ ] notwendige Schlussfolgerungen samt unabhängigen Entdeckungspfaden, Präsentation und Konsequenzen gebündelt sind;
- [ ] Handouts nur über kanonische Quellen und klare Auslieferungsbedingungen geführt werden;
- [ ] Erfolg, Teilerfolg, Scheitern, Rückzug und Ignorieren für zentrale Situationen spielbare Folgezustände besitzen;
- [ ] Improvisationsanker nützlich, knapp und nicht-kanonisch als `provisional` markiert sind;
- [ ] jede komprimierte Aussage einen relativen Link zur kanonischen Quelle besitzt;
- [ ] das Quellenregister Version, `updated` und aktuellen Prüfstatus jeder Quelle zeigt;
- [ ] `changed`- oder `missing`-Quellen sichtbar sind und nicht still überschrieben wurden;
- [ ] Validator und fokussierter Audit keine blockierenden Befunde für die Session melden.
