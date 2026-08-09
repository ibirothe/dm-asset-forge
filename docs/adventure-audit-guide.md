# Fachlicher Audit-Leitfaden

Dieser Leitfaden definiert die read-only Prüfung eines bestehenden Abenteuers auf Kontinuität, robuste Informationswege, wirksame Spielerentscheidungen und Tischreife. Die technische Prüfung durch [`scripts/validate_adventure.py`](validierung.md) bleibt davon getrennt. Der [Autoren- und Tischleitfaden](asset-authoring-guide.md) liefert die Qualitätskriterien einzelner Assets, der [Leitfaden für Spielerentscheidungen und Abenteuerstruktur](adventure-structure-guide.md) die Kriterien ihres Zusammenspiels.

## Inhalt

- [Audit-Auftrag und Grenzen](#audit-auftrag-und-grenzen)
- [Prüfreihenfolge](#prüfreihenfolge)
- [Technische Basisprüfung](#technische-basisprüfung)
- [Kanon und Kontinuität](#kanon-und-kontinuität)
- [Informationswege](#informationswege)
- [Plot-Threads und Spielerwirksamkeit](#plot-threads-und-spielerwirksamkeit)
- [Tischreife](#tischreife)
- [Schweregrade](#schweregrade)
- [Format eines Findings](#format-eines-findings)
- [Audit-Bericht](#audit-bericht)
- [Fix-Aufträge](#fix-aufträge)
- [Definition of Done](#definition-of-done)

## Audit-Auftrag und Grenzen

Vor der Prüfung werden Umfang und Bezugspunkt benannt: vollständiges Abenteuer, nächste Session, bestimmter Plot-Thread, Ort oder ausgewählte Assets. Fehlt eine Eingrenzung, gilt das aktive Abenteuer als Scope; gelesen wird dennoch schrittweise über Übersicht, Indizes und betroffene Verweise.

Ein Audit:

- bewertet bestehende Aussagen und Verbindungen, erfindet aber keine fehlenden Plotinhalte;
- trennt technische Validator-Diagnosen von fachlichen Findings;
- nennt Unsicherheit, wenn der Kanon keine eindeutige Bewertung erlaubt;
- verändert ohne ausdrücklichen Fix-Auftrag keine Abenteuerdatei, keinen Status, keinen Index und kein Change Log;
- bewertet keine literarische Schönheit, sondern Spielbarkeit, Nachvollziehbarkeit und innere Konsistenz;
- bleibt regelneutral.

## Prüfreihenfolge

1. **Scope festhalten:** Audit-Ziel, betrachteten Spielhorizont und ausdrücklich ausgeschlossene Bereiche nennen.
2. **Orientierung lesen:** `adventure/README.md`, alle fünf Indizes sowie `90-meta/open-questions.md`, `assumptions.md` und `decisions.md` lesen.
3. **Technische Basis prüfen:** Validator ausführen und dessen Ergebnis unverändert als eigenen Berichtsteil behandeln.
4. **Prüfmenge ableiten:** Aktive Plot-Threads, notwendige Schlussfolgerungen, betroffene Locations und direkt verknüpfte Assets bestimmen.
5. **Kanon prüfen:** Widersprüche und unklare Wahrheitsgrenzen bei Ort, Zeit, Ownership, Wissen, Status, Motivation und Beziehungen untersuchen.
6. **Informationswege prüfen:** Notwendigkeit, konkrete Präsentation, unabhängige Entdeckungspfade und Folgen des Verpassens bewerten.
7. **Spielerwirksamkeit prüfen:** Jeden aktiven Plot-Thread auf Einstieg, Druck, Wahl, Folgezustände, Ignorieren und Auflösungen prüfen.
8. **Tischreife prüfen:** Relevante `ready`-Assets gegen ihre Definition of Done und die schnelle Nutzbarkeit am Tisch prüfen.
9. **Findings konsolidieren:** Doppelte Symptome zu einer Ursache bündeln, Schweregrad begründen und kleinste sinnvolle Korrekturrichtung nennen.
10. **Bericht ausgeben:** Technische und fachliche Ergebnisse getrennt, vollständig und ohne Änderungen am Kanon ausgeben.

## Technische Basisprüfung

Zuerst ausführen:

```bash
python3 scripts/validate_adventure.py
```

Der Audit-Bericht übernimmt Exit-Code, Anzahl der Errors und Warnings sowie die betroffenen Pfade. Technische `ERROR`-Diagnosen sind `blocking`, bleiben aber im Abschnitt „Technische Validierung“. Eine `WARNING` wird im Kontext geprüft und nicht automatisch zu einem fachlichen Finding erklärt.

Der fachliche Audit wiederholt keine deterministisch prüfbare Schemaanalyse in Prosa. Er darf jedoch erklären, welche spielerische oder kanonische Auswirkung eine technische Diagnose besitzt.

## Kanon und Kontinuität

Eine Behauptung wird gegen ihre kanonische Quelle und alle für den Scope relevanten Verwendungen geprüft. Ein Widerspruch liegt nur vor, wenn Aussagen gleichzeitig denselben Gegenstand und Zustand betreffen und nicht bewusst als Gerücht, Irrtum, frühere Lage oder offene Frage getrennt sind.

| Bereich | Prüffragen | Typische Quellen |
|---|---|---|
| Ort | Wo befindet sich ein Asset aktuell und redaktionell? Stimmen Auftritte und Zugänge? | Location, `primary_location`, `current_location`, Index, Scene, Event |
| Zeit | In welcher Reihenfolge oder unter welcher Bedingung geschehen Entwicklungen? | Timeline, Event, Plot-Thread, Asset-Status |
| Ownership | Wo liegt die einzige kanonische Beschreibung? Sind Kopien nur Verweise? | kanonischer Pfad, Parent-Location, Index, Beziehungen |
| Wissen | Wer weiß welche Aussage, mit welchem Wahrheitsstatus und seit wann? | Information, NPC, Faction, Handout, Event |
| Status | Ist ein Asset aktiv, verändert, abgeschlossen, verloren oder `retired`? | Frontmatter, Plot-Thread, Event, Change Log |
| Motivation | Passen Ziel, Druck, Verhalten und nächste Handlung eines Akteurs zusammen? | NPC, Faction, Encounter, Plot-Thread |
| Beziehungen | Stimmen Richtung, Gegenseitigkeit und dargestellte Bedeutung überein? | Relationsfelder, relative Links, beteiligte Assets |

Jedes Kontinuitäts-Finding nennt:

- alle Dateien, deren Aussagen sich widersprechen oder eine relevante Lücke bilden;
- die betroffene kanonische Behauptung in knapper Paraphrase;
- warum Wahrheitsstatus, Zeitpunkt oder Perspektive den Unterschied nicht bereits erklären;
- die Auswirkung auf Vorbereitung oder Spiel;
- die kleinste Korrekturrichtung, ohne die richtige Version zu erfinden.

Fehlt eine entscheidende Festlegung, ist eine offene Frage oft richtiger als die Behauptung eines Widerspruchs.

## Informationswege

Zuerst werden notwendige Schlussfolgerungen identifiziert. Notwendig ist eine Schlussfolgerung, wenn ohne sie der zentrale Konflikt oder ein für den betrachteten Spielhorizont erforderlicher Zustandswechsel nicht verständlich oder erreichbar bleibt.

Für jede notwendige Schlussfolgerung prüfen:

1. **Aussage:** Ist klar, was Spieler tatsächlich verstehen können?
2. **Wahrheitsstatus:** Sind Wahrheit, Gerücht, Lüge, Teilwahrheit und Unsicherheit getrennt?
3. **Präsentation:** Existiert pro Pfad mindestens ein konkreter Hinweis, den der DM beschreiben, zeigen oder aussprechen kann?
4. **Zugang:** Sind Voraussetzungen und Fundorte spielbar und nicht selbst von derselben Schlussfolgerung abhängig?
5. **Unabhängigkeit:** Bestehen mindestens zwei Pfade mit unterschiedlichen Quellen oder Zugangsweisen?
6. **Robustheit:** Bleibt Fortschritt möglich, wenn ein Hinweis verpasst, zerstört, abgelehnt oder missverstanden wird?
7. **Konsequenz:** Verändert Lernen, spätes Lernen oder Verpassen die Situation nachvollziehbar?

Eine bloße Wiederholung desselben Hinweises an zwei Stellen ist kein unabhängiger Pfad. Ebenso genügt ein verlinktes `information`-Asset nicht, wenn die beteiligte Scene, der NPC oder Ort keine konkrete Präsentation ermöglicht.

Nicht notwendige Informationen benötigen nicht automatisch zwei Pfade. Sie brauchen jedoch einen verständlichen Zugang und eine erkennbare Tischfunktion, wenn sie als `ready` gelten.

## Plot-Threads und Spielerwirksamkeit

Jeder aktive Plot-Thread wird einzeln erfasst. Die Prüfung darf keinen Thread stillschweigend auslassen.

| Kriterium | Prüffrage |
|---|---|
| Einstieg | Wie können Spieler den Thread wahrnehmen oder betreten, ohne eine vorgeschriebene Motivation? |
| Aktueller Zustand | Welche Lage und dramatische Frage bestehen jetzt? |
| Nächster Druck | Was tun Akteure oder Welt ohne Eingreifen, und woran wird das sichtbar? |
| Wahlmöglichkeiten | Können mindestens zwei plausible Entscheidungen den Zustand unterschiedlich verändern? |
| Vorgehensweisen | Hängt eine zentrale Hürde nicht an genau einer erlaubten Methode? |
| Information | Sind notwendige Schlussfolgerungen robust erreichbar? |
| Scheitern und Rückzug | Entstehen spielbare Folgezustände statt eines Abbruchs? |
| Ignorieren | Verändert sich die Welt nachvollziehbar und bleibt ein späterer Berührungspunkt möglich? |
| Auflösung | Bestehen mehrere plausible Auflösungen oder ein bewusst offener Endzustand? |
| Verbindungen | Erfüllen Plot-, Scene-, Encounter-, Information- und Event-Assets ihre getrennten Rollen? |

Scheinwahl, Pflicht-Scene, einzelner Flaschenhals-Hinweis und folgenloses Ignorieren werden als fachliche Ursache benannt, nicht nur als fehlender Abschnitt. Der Audit beschreibt keine bevorzugte Spielerentscheidung und ergänzt keine neue Lösung.

## Tischreife

Für den Scope relevante Assets mit `status: ready` werden gegen die gemeinsame und typspezifische Definition of Done im Autorenleitfaden geprüft. Besondere Aufmerksamkeit gilt:

- schnell auffindbarer Tischfunktion und unmittelbarem Zustand;
- konkreten präsentierbaren Merkmalen statt reiner Hintergrundprosa;
- klarer Trennung von Spielerwissen und DM-Wissen;
- nutzbaren Auslösern, Zugängen, Hebeln und Konsequenzen;
- konsistenten Verweisen auf die für das Spiel benötigten Assets;
- fehlenden Platzhaltern oder entscheidenden offenen Fragen.

Ein formal vollständiges Asset kann fachlich noch `draft` sein. Ein Detailwunsch ohne Auswirkung auf Tischgebrauch oder Kontinuität ist höchstens `polish`.

## Schweregrade

| Schweregrad | Bedeutung |
|---|---|
| `blocking` | Verhindert einen erforderlichen Spiel- oder Plotfortschritt, erzeugt unauflösbar widersprüchlichen Kanon im betrachteten Scope, verletzt eine technische Muss-Regel oder lässt nicht freigegebenes DM-Wissen in player-facing Inhalt gelangen. |
| `important` | Das Abenteuer bleibt spielbar, aber eine fragile Informationskette, unwirksame Wahl, fehlende Konsequenz, relevante Kontinuitätslücke oder unberechtigter `ready`-Status gefährdet Vorbereitung oder Verlauf deutlich. |
| `polish` | Verbessert Klarheit, Auffindbarkeit oder Darstellung, ohne Spielbarkeit, Kanon oder wesentliche Entscheidungsmöglichkeiten zu gefährden. |

Der Schweregrad folgt aus der Auswirkung, nicht aus der Zahl betroffener Dateien. Unsicherheit wird benannt und nicht vorsorglich als `blocking` eingestuft.

## Format eines Findings

Jedes fachliche Finding verwendet dieses Format:

```markdown
### [important] A-001 – Kurzer Befund

- Bereich: information-path
- Betroffener Kanon: <knappe Behauptung oder erforderlicher Zustand>
- Begründung: <warum dies fachlich problematisch ist>
- Nachweise:
  - `adventure/<path-a>.md` – <betroffene Aussage oder fehlende Funktion>
  - `adventure/<path-b>.md` – <betroffene Aussage oder Abhängigkeit>
- Auswirkung: <konkretes Risiko für Vorbereitung oder Spiel>
- Kleinste Korrekturrichtung: <eng begrenzte Richtung, keine erfundene Lösung>
```

Zulässige Bereiche sind mindestens `continuity`, `information-path`, `player-agency`, `plot-thread`, `truth-boundary` und `table-readiness`. Bei einem Widerspruch werden alle beteiligten Dateien genannt. Ein Finding ohne Begründung, Auswirkung oder Korrekturrichtung ist unvollständig.

## Audit-Bericht

Der Bericht verwendet diese Reihenfolge:

1. **Scope und Lesebasis:** betrachteter Bereich, Spielhorizont, gelesene Übersichten und gezielt verfolgte Assets.
2. **Technische Validierung:** Befehl, Exit-Code, Errors und Warnings; keine Vermischung mit fachlichen Findings.
3. **Fachliche Zusammenfassung:** Anzahl `blocking`, `important` und `polish` sowie das größte Risiko.
4. **Findings:** vollständig im definierten Format, nach Schweregrad sortiert.
5. **Plot-Thread-Abdeckung:** jeder aktive Thread mit Ergebnis für Einstieg, Druck, Wahl, Ignorieren und Auflösung; `ok`, `finding <ID>` oder `not in scope`.
6. **Kritische Informationswege:** jede notwendige Schlussfolgerung mit ihren unabhängigen Pfaden und zugehörigen Finding-IDs.
7. **Offene Fragen und Audit-Grenzen:** fehlende Festlegungen, nicht gelesene Bereiche und Bewertungen, die Bestätigung benötigen.
8. **Empfohlene nächste Aktion:** kleinste priorisierte Korrektur oder Bestätigung, dass im Scope kein Handlungsbedarf besteht.

Sind keine fachlichen Findings vorhanden, wird dies ausdrücklich gesagt. Es werden keine leeren Schweregradabschnitte künstlich gefüllt.

## Fix-Aufträge

Nur wenn der User ausdrücklich Korrekturen verlangt:

1. die ausgewählten Finding-IDs und den betroffenen Dateiumfang vor der Änderung nennen;
2. bei mehrdeutiger kanonischer Wahrheit eine Entscheidung erfragen, statt eine Variante zu wählen;
3. die kleinste kohärente Änderung an kanonischen Assets, Links, Indizes und gegebenenfalls Meta-Dateien durchführen;
4. keine unrelated Findings nebenbei beheben;
5. Validator und betroffene fachliche Prüfschritte erneut ausführen;
6. geschlossene, verbleibende und neu entstandene Findings getrennt berichten.

Ein Audit ohne Fix-Auftrag verändert auch dann nichts, wenn ein `blocking`-Finding vorliegt.

## Definition of Done

Ein fachlicher Audit ist abgeschlossen, wenn:

- [ ] Scope, Spielhorizont und Lesebasis nachvollziehbar sind;
- [ ] technische Validator-Ergebnisse getrennt und vollständig berichtet wurden;
- [ ] relevante Aussagen zu Ort, Zeit, Ownership, Wissen, Status, Motivation und Beziehungen auf Widersprüche geprüft wurden;
- [ ] alle Kontinuitäts-Findings sämtliche beteiligten Dateien und den betroffenen Kanon nennen;
- [ ] jede notwendige Schlussfolgerung auf konkrete Präsentation, mindestens zwei unabhängige Pfade und Folgen des Verpassens geprüft wurde;
- [ ] jeder aktive Plot-Thread auf Einstieg, Druck, Wahl, Scheitern oder Rückzug, Ignorieren und Auflösungen geprüft wurde;
- [ ] Annahmen, Gerüchte, Geheimnisse und etablierte Fakten nicht als gleichwertige Wahrheit behandelt wurden;
- [ ] jedes Finding Schweregrad, Begründung, Nachweise, Auswirkung und kleinste Korrekturrichtung enthält;
- [ ] ohne ausdrücklichen Fix-Auftrag keine Datei verändert wurde;
- [ ] der Bericht eine priorisierte nächste Aktion nennt.
