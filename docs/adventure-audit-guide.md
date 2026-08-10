# Fachlicher Audit-Leitfaden

Dieser Leitfaden definiert die read-only Prüfung eines vollständigen One-Shots auf Kontinuität, robuste Informationswege, wirksame Spielerentscheidungen, erreichbare Auflösungen und Tischreife. Die technische Prüfung durch [`scripts/validate_adventure.py`](validierung.md) bleibt davon getrennt. Der [Autoren- und Tischleitfaden](asset-authoring-guide.md) liefert die Qualitätskriterien einzelner Assets, der [Leitfaden für Spielerentscheidungen und Abenteuerstruktur](adventure-structure-guide.md) die Kriterien ihres Zusammenspiels.

## Inhalt

- [Audit-Auftrag und Grenzen](#audit-auftrag-und-grenzen)
- [Prüfreihenfolge](#prüfreihenfolge)
- [Technische Basisprüfung](#technische-basisprüfung)
- [Kanon und Kontinuität](#kanon-und-kontinuität)
- [Informationswege](#informationswege)
- [Spielerausgaben und Visuals](#spielerausgaben-und-visuals)
- [Plot-Threads und Spielerwirksamkeit](#plot-threads-und-spielerwirksamkeit)
- [Pacing und sichere Kürzbarkeit](#pacing-und-sichere-kürzbarkeit)
- [Übersichten und Navigationswege](#übersichten-und-navigationswege)
- [Tischreife](#tischreife)
- [Schweregrade](#schweregrade)
- [Format eines Findings](#format-eines-findings)
- [Audit-Bericht](#audit-bericht)
- [Fix-Aufträge](#fix-aufträge)
- [Definition of Done](#definition-of-done)

## Audit-Auftrag und Grenzen

Vor der Prüfung werden Umfang und Bezugspunkt benannt: vollständiger One-Shot, bestimmter Plot-Thread, Ort oder ausgewählte Assets. Fehlt eine Eingrenzung, gilt der vollständige One-Shot als Scope; gelesen wird dennoch schrittweise über Übersicht, Indizes und betroffene Verweise.

Ein Audit:

- bewertet bestehende Aussagen und Verbindungen, erfindet aber keine fehlenden Plotinhalte;
- trennt technische Validator-Diagnosen von fachlichen Findings;
- nennt Unsicherheit, wenn der Kanon keine eindeutige Bewertung erlaubt;
- verändert ohne ausdrücklichen Fix-Auftrag keine Abenteuerdatei, keinen Status, keinen Index und kein Change Log;
- bewertet keine literarische Schönheit, sondern Spielbarkeit, Nachvollziehbarkeit und innere Konsistenz;
- bleibt regelneutral.

## Prüfreihenfolge

1. **Scope festhalten:** Audit-Ziel und ausdrücklich ausgeschlossene Bereiche nennen.
2. **Orientierung lesen:** `adventure/README.md`, `50-indexes/clue-matrix.md`, `60-session/dm-cheat-sheet.md`, `60-session/run-sheet.md`, `60-session/readiness-report.md`, alle sechs Asset-Indizes sowie `90-meta/open-questions.md`, `assumptions.md` und `decisions.md` lesen.
3. **Technische Basis prüfen:** Validator ausführen und dessen Ergebnis unverändert als eigenen Berichtsteil behandeln.
4. **Prüfmenge ableiten:** Aktive Plot-Threads, notwendige Schlussfolgerungen, betroffene Locations und direkt verknüpfte Assets bestimmen.
5. **Kanon prüfen:** Widersprüche und unklare Wahrheitsgrenzen bei Ort, Zeit, Ownership, Wissen, Status, Motivation und Beziehungen untersuchen.
6. **Informationswege prüfen:** Aus der globalen Clue Matrix alle notwendigen Schlussfolgerungen und behaupteten Pfade ableiten; Notwendigkeit, konkrete Präsentation, echte Quellen- oder Zugangs-Unabhängigkeit und Folgen des Verpassens anschließend in den kanonischen Information-, Quellen- und Fundort-Assets bewerten.
7. **Spielerausgaben prüfen:** Vorhandene `player.md`-Dateien gegen Freigabequelle, `reveals`, Wahrheitsstatus und Auslieferungssituation prüfen.
8. **Visuals prüfen:** Visual, Subject, Prompt und vorhandene PNG auf Identität, dargestellten Zustand, Sichtbarkeit und Ausschlüsse abgleichen.
9. **Spielerwirksamkeit prüfen:** Jeden aktiven Plot-Thread auf Einstieg, Druck, Wahl, Folgezustände, Ignorieren und Auflösungen prüfen.
10. **One-Shot-Abschluss prüfen:** Sicherstellen, dass der zentrale Konflikt innerhalb des vorbereiteten Umfangs erreichbar aufgelöst werden kann und keine Pflichtentwicklung vertagt ist.
11. **Pacing prüfen:** Zielrahmen, Session Run Sheet, minimalen Auflösungszustand, Inhaltsrollen, Checkpoints, sichere Kürzungen, `late pressure` und Finale-Trigger auf praktische Leitbarkeit und erhaltene Spielerwirksamkeit prüfen.
12. **Navigation prüfen:** README, globale Clue Matrix, DM-Spickzettel, Session Run Sheet und sechs Asset-Indizes auf tischrelevante Kurzkontexte, direkte kanonische Links und einen Suchweg ohne Volltextsuche oder blindes Ordnerscannen prüfen.
13. **Tischreife prüfen:** Relevante `ready`-Assets gegen ihre Definition of Done und die schnelle Nutzbarkeit am Tisch prüfen.
14. **Findings konsolidieren:** Doppelte Symptome zu einer Ursache bündeln, Schweregrad begründen und kleinste sinnvolle Korrekturrichtung nennen.
15. **Bericht ausgeben:** Technische und fachliche Ergebnisse getrennt, vollständig und ohne Änderungen am Kanon ausgeben. Zusätzlich melden, ob der vorhandene Readiness-Status zu Preflight, Validator und Audit-Ergebnis passt; den Readiness-Bericht ohne ausdrücklichen Schreibauftrag nicht aktualisieren.

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

Zuerst werden notwendige Schlussfolgerungen identifiziert. Notwendig ist eine Schlussfolgerung, wenn ohne sie der zentrale Konflikt oder ein für die Auflösung erforderlicher Zustandswechsel nicht verständlich oder erreichbar bleibt.

Für jede notwendige Schlussfolgerung prüfen:

1. **Aussage:** Ist klar, was Spieler tatsächlich verstehen können?
2. **Wahrheitsstatus:** Sind Wahrheit, Gerücht, Lüge, Teilwahrheit und Unsicherheit getrennt?
3. **Präsentation:** Existiert pro Pfad mindestens ein konkreter Hinweis, den der DM beschreiben, zeigen oder aussprechen kann?
4. **Zugang:** Sind Voraussetzungen und Fundorte spielbar und nicht selbst von derselben Schlussfolgerung abhängig?
5. **Unabhängigkeit:** Bestehen mindestens zwei Pfade mit unterschiedlichen Quellen oder Zugangsweisen?
6. **Robustheit:** Bleibt Fortschritt möglich, wenn ein Hinweis verpasst, zerstört, abgelehnt oder missverstanden wird?
7. **Konsequenz:** Verändert Lernen, spätes Lernen oder Verpassen die Situation nachvollziehbar?

Eine bloße Wiederholung desselben Hinweises an zwei Stellen ist kein unabhängiger Pfad. Ebenso genügt ein verlinktes `information`-Asset nicht, wenn die beteiligte Scene, der NPC oder Ort keine konkrete Präsentation ermöglicht.

Die globale Clue Matrix dient dabei als Coverage-Landkarte, nicht als Beweis. Der Audit gleicht jeden `Conclusion key`, jede Einstufung als `necessary`, jede `Independence group`, jeden Fundort, Fail-forward-Pfad, jede Folge und jeden Plot-Thread mit den verlinkten kanonischen Assets ab. Aussagen oder Wahrheitsstatus, die nur in der Matrix vorkommen, sind abgeleiteter Drift; zwei Matrixzeilen mit gleicher Quelle und Zugangsweise bleiben trotz verschiedener Gruppennamen derselbe Pfad.

Nicht notwendige Informationen benötigen nicht automatisch zwei Pfade. Sie brauchen jedoch einen verständlichen Zugang und eine erkennbare Tischfunktion, wenn sie als `ready` gelten.

## Spielerausgaben und Visuals

Diese Prüfung ergänzt den technischen Validator um semantische Grenzen. Bei einem vollständigen One-Shot-Audit umfasst sie alle vorhandenen `player.md`-Dateien sowie alle Visuals mit vorhandener PNG-Datei oder geplanter Spieler-Sichtbarkeit. Bei engerem Scope werden nur Ausgaben der betrachteten Subject-Assets geprüft. Existiert keine entsprechende Ausgabe, wird dies im Bericht festgehalten und es entsteht kein Finding allein wegen ihres Fehlens.

Für jede `player.md` prüfen:

1. **Freigabequelle:** Verweist das zugehörige `handout.md` oder `player-character.md` auf genau diese Spielerdatei und die freigegebene Quellversion?
2. **Erlaubter Inhalt:** Stammt jede Aussage beim Handout aus `Player-facing content` oder bewusst offenbarten Informationen und beim Player Character ausschließlich aus freigabefähigem Konzept, Ausgangslage, Hintergrund, offenen Entscheidungen, Stärken, Grenzen, Startwissen und Beziehungen?
3. **Wahrheitsgrenze:** Bleiben Gerücht, Lüge, Teilwahrheit und Unsicherheit in derselben Bedeutung erhalten?
4. **Auslieferung:** Verrät die Datei nur, was Spieler in der dokumentierten Auslieferungs- oder Character-Ausgangssituation tatsächlich erhalten?
5. **Geheimnisschutz und Entscheidungsfreiheit:** Fehlen DM-Kontext, verdeckte Ursachen, Lösungen, zukünftige Ereignisse, interne IDs, Statuswerte und Repository-Navigation, und bleiben unbestätigte Motivation, Loyalität und Entscheidungen offen?

Für jedes relevante Visual prüfen:

1. **Subject-Identität:** Sind `Identity source` und `Stable identity anchors` durch das kanonische Subject oder bei einer Handout-Bildfassung durch die freigegebene `player.md` gedeckt?
2. **One-Shot-Zustand:** Kommt der unter `Depicted state` beschriebene Zustand im vorbereiteten One-Shot tatsächlich vor, ohne spätere Abenteuerentwicklung vorwegzunehmen?
3. **Briefing-Konsistenz:** Stimmen Visual und Prompt bei Identitätsankern, Zustand, Variation, Komposition, Sichtbarkeit, Ausschlüssen und Zielpfad überein?
4. **PNG-Konsistenz:** Wenn eine PNG existiert, entsprechen ihre erkennbaren Inhalte der freigegebenen Visual-Version und dem Prompt? Kann die Datei im verfügbaren Audit-Werkzeug nicht visuell geprüft werden, wird sie als Audit-Grenze statt als verifiziert gemeldet.
5. **Spieler-Sicherheit:** Zeigen Text, Symbole, Komposition oder Hintergrund keine Geheimnisse, die zum vorgesehenen Anzeigezeitpunkt noch nicht bekannt sind?

Ein tatsächlich player-facing Geheimnisleck ist `blocking`. Ein Widerspruch zwischen Subject, Visual, Prompt und PNG ist nach seiner Auswirkung einzustufen; er ist mindestens `important`, wenn Wiedererkennung, Kanonverständnis oder eine spielrelevante Information betroffen sind. Rein technische Status-, Pfad- und Provenienzfehler bleiben im getrennten Validator-Abschnitt, können aber als Nachweis für ihre fachliche Auswirkung dienen.

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

## Pacing und sichere Kürzbarkeit

Der Audit vergleicht `Target duration` und `Content density` aus `00-input/constraints.md` mit dem tatsächlich als erforderlich beschriebenen Umfang. Sind die Werte `open`, wird keine konkrete Laufzeit behauptet; geprüft wird dennoch, ob der One-Shot einen kompakten minimalen Auflösungszustand und sichere Kürzungen besitzt.

Prüfen:

1. **Minimum resolution state:** Bleiben zentraler Konflikt, notwendige Schlussfolgerungen, handlungsfähige Akteure und erreichbare Auflösungen im kleinsten vorbereiteten Umfang erhalten?
2. **Content roles:** Sind `core`, `supporting` und `optional` nachvollziehbar unterschieden, ohne Pflichtinhalt als optional zu tarnen?
3. **Safe cuts:** Nennt der One-Shot mindestens eine konkrete Kürzung samt Auswirkung, die unabhängige Informationswege, Spieler-Einfluss und Auflösungen erhält?
4. **Thread coverage:** Besitzt jeder aktive Plot-Thread einen eigenen minimalen Auflösungszustand, unverzichtbare Informationen und sichere Kürzungen?
5. **Late pressure:** Entsteht die Verdichtung aus etablierten Akteuren oder Zuständen und bleiben mehrere plausible Spielerreaktionen möglich?
6. **Overload:** Verlangt der minimale Auflösungszustand nahezu alle vorbereiteten Locations, Threads oder `supporting` Inhalte, obwohl der Zielrahmen kleiner ist?
7. **Run Sheet:** Sind Zeiten optional aus dem Preflight übernommen, Phasen als bewegliche Zustandsziele statt Scene-Reihenfolge formuliert und Checkpoints, Druck, Kürzungen sowie Finale-Trigger durch kanonische Zustände gedeckt?

Ein Zielrahmen ohne realistisch erreichbaren minimalen Auflösungszustand oder ohne sichere Kürzung ist mindestens `important`. Ein als sicher bezeichneter Cut ist `blocking`, wenn er den einzigen verbleibenden Fortschritt oder jede Auflösung entfernt. Der Audit berechnet keine fehlenden Minuten und erfindet keinen Ablaufplan. Vorhandene Zeitangaben und Run-Sheet-Trigger werden jedoch auf Widerspruchsfreiheit, praktische Reihenfolge und erhaltene Spielerwahl geprüft.

## Übersichten und Navigationswege

Die README wird als abgeleitete Tischübersicht geprüft, nicht als zweite Kanonquelle. Sie muss Ausgangslage, zentralen Konflikt, aktuellen Druck, zentrale Akteure, notwendige Informationen, mögliche Abschlüsse und relevante Folgezustände knapp sichtbar machen. Pacing und sichere Kürzungen werden nur aus dem Plot zusammengefasst und dorthin verlinkt.

Der DM-Spickzettel wird als noch stärker verdichtete Laufzeitansicht geprüft. Einstieg und Druck, zentrale Orte, NPC-Absichten und Voice Cues, notwendige Schlussfolgerungen und unabhängige Ersatzpfade, Eskalation, sichere Kürzungen, Mindestauflösung und mögliche Endzustände müssen schnell scannbar sein. Jede Aussage verweist auf ihre kanonische Plot-, Index- oder Asset-Quelle; ein Widerspruch oder neuer Kanon im Spickzettel ist nach seiner Tischwirkung einzustufen.

Das Session Run Sheet wird als operative Laufzeitansicht geprüft. Es muss aus Preflight, Plot, Threads, Informationen und Spickzettel ableiten, mehrere Opening- und Abschlussoptionen erhalten und flexible Zustandsphasen statt Pflicht-Scenes verwenden. Checkpoints, `late pressure`, Kürzungen und Finale-Trigger dürfen weder einen einzelnen Lösungsweg erzwingen noch die letzten unabhängigen Informationspfade oder den minimalen Auflösungszustand entfernen.

Die globale Clue Matrix wird als abgeleitete Abdeckungsansicht geprüft. Sie muss jedes Information-Asset und seine kanonischen Fundorte relativ über stabile IDs verlinken, notwendige von optionalen oder offenen Schlussfolgerungen unterscheiden und konkrete Präsentation, Zugang, Unabhängigkeitsgruppe, Voraussetzungen, Fail-forward, Folgen und betroffene Plot-Threads sichtbar machen. Wahrheit, Wahrheitsstatus und vollständige Entdeckungslogik werden nur in den kanonischen Information-Assets bewertet.

Für jedes zentrale Asset prüfen:

1. **Direkter Weg:** Ist es aus der README direkt oder über genau einen passenden der sechs Indizes erreichbar?
2. **Tischkontext:** Erklärt der Link oder die Indexzeile knapp, warum das Asset jetzt relevant ist?
3. **Kanonisches Ziel:** Führt der Weg zur einzigen vollständigen Beschreibung statt zu einer Kopie oder weiteren Übersichtsdatei?
4. **Aktualität:** Stimmen Kurzkontext, Status und Link mit dem kanonischen Plot oder Asset überein?
5. **Abdeckung:** Sind insbesondere zentrale Factions und Events direkt in der README verlinkt, da für sie keiner der fünf Tischindizes existiert?

Die sechs Asset-Indizes werden nach ihrer jeweiligen Tischfunktion bewertet: aktueller Ortsdruck, unmittelbare NPC-Absicht, One-Shot-Rolle und freiwilliger Hook eines Player Characters, Object-Einsatz, Bedeutung und unabhängige Fundwege einer Information sowie nächster Druck, minimaler Auflösungszustand und sichere Kürzung eines aktiven Threads. Kurzkontexte bleiben knapp und enthalten keinen vollständigen Kanon. Die Clue Matrix ersetzt den Information-Index nicht, sondern verbindet dessen kanonische Ziele abenteuerweit nach Schlussfolgerung und Pfad.

Für jeden zentralen NPC wird geprüft, ob der Spickzettel unmittelbare Absicht und einen aus dem kanonischen NPC ableitbaren Voice Cue enthält. Für jede notwendige Schlussfolgerung wird geprüft, ob robuste Ersatzpfade sichtbar sind. Sichere Kürzungen dürfen weder den minimalen Auflösungszustand noch den letzten unabhängigen Informationsweg entfernen.

Ein zentrales Asset, das nur durch Volltextsuche oder blindes Durchsuchen von Ordnern erreichbar ist, ist mindestens `important`. Ein veralteter Kurzkontext ist nach seiner Auswirkung einzustufen und `blocking`, wenn er den DM zum falschen einzigen Informationsweg oder zu einer unerreichbaren Auflösung führt.

## Tischreife

Für den Scope relevante Assets mit `status: ready` werden gegen die gemeinsame und typspezifische Definition of Done im Autorenleitfaden geprüft. Besondere Aufmerksamkeit gilt:

- schnell auffindbarer Tischfunktion und unmittelbarem Zustand;
- konkreten präsentierbaren Merkmalen statt reiner Hintergrundprosa;
- klarer Trennung von Spielerwissen und DM-Wissen;
- nutzbaren Auslösern, Zugängen, Hebeln und Konsequenzen;
- konsistenten Verweisen auf die für das Spiel benötigten Assets;
- fehlenden Platzhaltern oder entscheidenden offenen Fragen.

Ein formal vollständiges Asset kann fachlich noch `draft` sein. Ein Detailwunsch ohne Auswirkung auf Tischgebrauch oder Kontinuität ist höchstens `polish`.

Der Readiness-Bericht ist nur eine abgeleitete Statussicht. Der Audit prüft, ob seine drei Ergebniszeilen, verbleibenden Blocker und die priorisierte nächste Aktion mit den gelesenen Quellen übereinstimmen. Ein Audit-Finding wird dort nicht wiederholt; nach einem reinen Audit bleibt die Datei unverändert.

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

Zulässige Bereiche sind mindestens `continuity`, `information-path`, `player-output`, `visual-consistency`, `player-agency`, `plot-thread`, `pacing`, `navigation`, `truth-boundary`, `one-shot-scope` und `table-readiness`. Bei einem Widerspruch werden alle beteiligten Dateien genannt. Ein Finding ohne Begründung, Auswirkung oder Korrekturrichtung ist unvollständig.

## Audit-Bericht

Der Bericht verwendet diese Reihenfolge:

1. **Scope und Lesebasis:** betrachteter Bereich, gelesene Übersichten und gezielt verfolgte Assets.
2. **Technische Validierung:** Befehl, Exit-Code, Errors und Warnings; keine Vermischung mit fachlichen Findings.
3. **Fachliche Zusammenfassung:** Anzahl `blocking`, `important` und `polish` sowie das größte Risiko.
4. **Findings:** vollständig im definierten Format, nach Schweregrad sortiert.
5. **Plot-Thread-Abdeckung:** jeder aktive Thread mit Ergebnis für Einstieg, Druck, Wahl, Ignorieren und Auflösung; `ok`, `finding <ID>` oder `not in scope`.
6. **Kritische Informationswege:** jede notwendige Schlussfolgerung mit ihren unabhängigen Pfaden und zugehörigen Finding-IDs.
7. **Spielerausgaben und Visuals:** jede geprüfte `player.md` und jedes relevante Visual mit `ok`, `finding <ID>` oder `not visually inspected`; wenn keine existieren, dies ausdrücklich nennen.
8. **Pacing und Kürzbarkeit:** Zielrahmen, Session Run Sheet, Checkpoints, `late pressure`, Finale-Trigger, minimaler Auflösungszustand und jede deklarierte sichere Kürzung mit `ok`, `finding <ID>` oder `target frame open`.
9. **Übersichten und Navigation:** README-Kernfragen, globale Clue Matrix, DM-Spickzettel, Session Run Sheet, sechs Asset-Indizes und der direkte Pfad zu jedem zentralen Asset mit `ok` oder `finding <ID>`.
10. **Readiness-Abgleich:** vorhandener Gesamtstatus gegen Preflight, technische Validierung, fachliches Ergebnis und Blocker; `ok` oder `finding <ID>`.
11. **Offene Fragen und Audit-Grenzen:** fehlende Festlegungen, nicht gelesene Bereiche und Bewertungen, die Bestätigung benötigen.
12. **Empfohlene nächste Aktion:** kleinste priorisierte Korrektur oder Bestätigung, dass im Scope kein Handlungsbedarf besteht.

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

- [ ] Scope und Lesebasis nachvollziehbar sind;
- [ ] technische Validator-Ergebnisse getrennt und vollständig berichtet wurden;
- [ ] relevante Aussagen zu Ort, Zeit, Ownership, Wissen, Status, Motivation und Beziehungen auf Widersprüche geprüft wurden;
- [ ] alle Kontinuitäts-Findings sämtliche beteiligten Dateien und den betroffenen Kanon nennen;
- [ ] jede notwendige Schlussfolgerung auf konkrete Präsentation, mindestens zwei unabhängige Pfade und Folgen des Verpassens geprüft wurde;
- [ ] die globale Clue Matrix vollständig gegen alle Information-Assets, Fundorte und zugehörigen Plot-Threads abgeglichen wurde und bloße Hinweiswiederholung nicht als Unabhängigkeit zählt;
- [ ] jeder aktive Plot-Thread auf Einstieg, Druck, Wahl, Scheitern oder Rückzug, Ignorieren und Auflösungen geprüft wurde;
- [ ] der zentrale Konflikt innerhalb des One-Shots vollständig erreichbar und auflösbar ist;
- [ ] Annahmen, Gerüchte, Geheimnisse und etablierte Fakten nicht als gleichwertige Wahrheit behandelt wurden;
- [ ] jede vorhandene `player.md` im Scope gegen Freigabequelle, `reveals`, Wahrheitsstatus, Auslieferung und DM-Wissen geprüft wurde;
- [ ] jedes relevante Visual im Scope gegen Subject-Identität, One-Shot-Zustand, Prompt, Sichtbarkeit, Ausschlüsse und eine vorhandene PNG geprüft oder die fehlende visuelle Prüfbarkeit als Grenze benannt wurde;
- [ ] Zielrahmen, Session Run Sheet, minimaler Auflösungszustand, Inhaltsrollen, Checkpoints, sichere Kürzungen, `late pressure` und Finale-Trigger fachlich geprüft wurden;
- [ ] jede sichere Kürzung notwendige Informationswege, mehrere Formen der Spieler-Einflussnahme und erreichbare Auflösungen erhält;
- [ ] README, globale Clue Matrix, DM-Spickzettel, Session Run Sheet und sechs Asset-Indizes knappe tischrelevante Kurzkontexte besitzen, ohne vollständigen Kanon zu duplizieren;
- [ ] der DM-Spickzettel zentrale NPCs mit unmittelbarer Absicht und Voice Cue, notwendige Schlussfolgerungen mit Ersatzpfaden sowie Mindestauflösung, sichere Kürzungen und mögliche Endzustände aus kanonischen Quellen verdichtet;
- [ ] das Session Run Sheet optionale Zeitangaben aus dem Preflight, mehrere Einstiege und Abschlüsse sowie flexible Checkpoints, Druck-, Kürzungs- und Finale-Trigger ohne feste Scene-Reihenfolge oder neue Plotlogik führt;
- [ ] der Readiness-Status mit Preflight, Validator, fachlichem Ergebnis und verbleibenden Blockern abgeglichen wurde, ohne Findings in den Bericht zu kopieren oder ihn ohne Schreibauftrag zu ändern;
- [ ] jedes zentrale Asset direkt oder über genau einen passenden Index ohne Volltextsuche erreichbar ist;
- [ ] jedes Finding Schweregrad, Begründung, Nachweise, Auswirkung und kleinste Korrekturrichtung enthält;
- [ ] ohne ausdrücklichen Fix-Auftrag keine Datei verändert wurde;
- [ ] der Bericht eine priorisierte nächste Aktion nennt.
