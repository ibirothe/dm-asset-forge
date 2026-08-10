# Autoren- und Tischleitfaden für DM-Assets

Dieser Leitfaden beschreibt, wie aus den 15 technischen Asset-Grundgerüsten fachlich belastbare, regelneutrale und am Spieltisch nutzbare Inhalte werden. Der [Asset-Katalog](asset-katalog.md) bestimmt Typ und Speicherort, [Metadaten und Werte](metadaten-und-werte.md) bestimmen Frontmatter und kontrollierte Werte, das [Beziehungsmodell](beziehungen-und-speicherorte.md) bestimmt Ownership und Verweise. Das zustandsbasierte Zusammenspiel von Plot, Scenes, Encounters und Informationen regelt der [Leitfaden für Spielerentscheidungen und Abenteuerstruktur](adventure-structure-guide.md).

## Inhalt

- [Gemeinsame Qualitätsregeln](#gemeinsame-qualitätsregeln)
- [`world`](#world)
- [`location`](#location)
- [`scene`](#scene)
- [`npc`](#npc)
- [`player-character`](#player-character)
- [`creature`](#creature)
- [`faction`](#faction)
- [`object`](#object)
- [`information`](#information)
- [`encounter`](#encounter)
- [`plot-thread`](#plot-thread)
- [`event`](#event)
- [`handout`](#handout)
- [`visual`](#visual)
- [`random-table`](#random-table)

## Gemeinsame Qualitätsregeln

### Tiefe nach Tischfunktion

Ein Asset wird nur so weit ausgearbeitet, wie es eine erkennbare Funktion für Vorbereitung, Spiel oder Kontinuität besitzt. Namen ohne eigene Tischfunktion bleiben Erwähnungen oder Links. Leere Ausschmückung, wiederholte Zusammenfassungen und vorsorgliche Detailfülle machen ein Asset nicht spielbereiter.

Jedes `ready`-Asset erfüllt mindestens:

- eine klare Tischfunktion;
- konkrete, schnell erfassbare Merkmale;
- relevante Beziehungen als IDs und relative Links;
- mindestens einen nutzbaren Zugang, Auslöser oder Anwendungskontext;
- erkennbare Folgen, wenn die Spieler damit interagieren oder es ignorieren;
- eine Trennung zwischen etablierten Fakten, unsicheren Aussagen und offenen Autorenfragen;
- alle typspezifischen Kriterien seines Abschnitts.

`status: draft` bleibt richtig, solange zentrale Voraussetzungen, Beziehungen oder Konsequenzen fehlen. Ein formal vollständiges Template ist nicht automatisch `ready`.

### Abschnittsfunktion und Redundanz

Jeder ausgefüllte Abschnitt erfüllt mindestens eine klar erkennbare Rolle:

- **Tischfunktion:** liefert unmittelbar beschreibbare Merkmale, Entscheidungslage, Reaktion, Druck, Ansatz oder Folgezustand;
- **Kanonfunktion:** hält genau die Aussage, Identität, Zuständigkeit oder Wahrheitsgrenze, für die dieser Asset-Typ verantwortlich ist;
- **Navigationsfunktion:** verlinkt kanonische Assets und ergänzt nur den für dieses Asset spezifischen Kurzkontext.

Navigationsabschnitte wiederholen weder Erscheinung, Motivation, Aussage noch Konsequenzen des Ziel-Assets vollständig. Eine optionale Beziehung erhält erst dann einen eigenen Abschnitt, wenn sie existiert und nützlich ist. Insbesondere legt `new_asset.py` bei einem tatsächlich erzeugten Visual am Subject den Abschnitt `Visuals` an; leere `Visual reference`-Platzhalter gehören nicht zum Mindestgerüst.

Typspezifische Kernabschnitte ersetzen ein pauschales Universal-Feld: `Core premise` trägt die Tischfunktion der World, `Statement` die der Information, `Dramatic question` die des Plot-Threads und `Player-facing content` die des Handouts. Diese Unterschiede sind beabsichtigt.

### Sichtbarkeit

- Spielerwissen umfasst nur unmittelbar Wahrnehmbares, allgemein Bekanntes oder bewusst Offenbartes.
- DM-Wissen umfasst Motive, Wahrheitsstatus, verborgene Beziehungen, zukünftige Entwicklungen und nicht offenbarte Konsequenzen.
- Geheimnisse werden nicht versehentlich in player-facing Abschnitte oder Handout-Ausgaben kopiert.
- Ein Asset darf unterschiedliche Wissensstände beschreiben, ohne für jeden Wissensstand dupliziert zu werden.

### Visuals

Ein `visual` ist sinnvoll, wenn Wiedererkennung, räumliche Orientierung, Zustand, Symbolik oder Atmosphäre am Tisch wesentlich davon profitieren. Es ist optional, wenn Text dieselbe Funktion schneller erfüllt, und unnötig, wenn es nur dekoriert oder neue unbestätigte Fakten einführen würde.

### Pflege

Bei einer inhaltlichen Änderung die betroffenen Beziehungen und Konsequenzen mitprüfen. `version` und `updated` nur bei tatsächlicher inhaltlicher Änderung aktualisieren. Indizes, Rückverweise und Change Log nach den Repository-Anweisungen pflegen.

Ändert sich eine Aussage, die für die unmittelbare Tischführung verdichtet wurde, auch `60-session/dm-cheat-sheet.md` aktualisieren. Der Spickzettel enthält nur einen kurzen, handlungsrelevanten Kontext und einen relativen Link zur kanonischen Quelle. Insbesondere stammen NPC-Absicht und Voice Cue aus dem NPC, unabhängige Ersatzpfade aus den Information- und Plot-Assets sowie Mindestauflösung, sichere Kürzungen und Endzustände aus dem Plot.

Ändert sich ein pacing- oder auflösungsrelevanter Zustand, zusätzlich `60-session/run-sheet.md` prüfen. Checkpoints, `late pressure`, Kürzungen und Finale-Trigger leiten sich aus Preflight, Plot, Threads, Informationen und betroffenen Assets ab. Sie dürfen keine feste Scene-Reihenfolge, neue Plotlogik oder einen einzelnen verpflichtenden Informationsweg etablieren.

## `world`

**Einsatz:** Übergreifende Realität, Alltagslogik und Kräfte festlegen, die mehrere Orte oder Plot-Threads prägen. Einzelne Ortsdetails oder konkrete Geschehnisse gehören nicht hierher.

**Mindestinhalt:** Kernprämisse, bestätigte Grundwahrheiten, Alltag, wirksame Mächte oder Spannungen, Arbeitsannahmen und offene Weltfragen.

**Leitfragen:** Was unterscheidet diese Welt im Spiel? Was gilt überall oder in großen Teilen? Welche Kräfte erzeugen wiederkehrenden Druck? Was ist ausdrücklich noch nicht entschieden?

**Am Spieltisch:** Eine kurze Prämisse, zwei bis fünf relevante Weltregeln und die aktuell wirksamen Spannungen müssen schnell auffindbar sein.

**Sichtbarkeit und Visual:** Allgemeines Weltwissen darf spielersichtbar sein; Autorenannahmen und ungelöste Wahrheiten bleiben DM-Wissen. Ein Visual lohnt sich für Gesamtästhetik, Regionalkarte oder ein prägendes Weltphänomen.

**Anti-Patterns:** Enzyklopädischer Weltenbau ohne Abenteuerbezug; lokale Fakten duplizieren; Arbeitsannahmen als Kanon ausgeben; jedes Geheimnis vorab auflösen.

**Definition of Done:** Prämisse und Grundwahrheiten erklären den Abenteuerkontext; Alltag und Spannungen erzeugen konkrete Spielansätze; Annahmen und Unknowns sind sauber getrennt.

## `location`

**Einsatz:** Einen stabilen, wiederbesuchbaren räumlichen Kontext beschreiben. Eine einmalige Situation ist eine `scene`; unmittelbarer Druck mit Eskalation ein `encounter`.

**Mindestinhalt:** Tischfunktion, erster Eindruck, mehrere Sinneseindrücke, Zugang und Grenzen, nutzbare Bereiche, relevante Bewohner, Informationen, Druck, Verbindungen und mögliche Veränderungen.

**Leitfragen:** Warum kommen Spieler hierher? Was erkennen sie sofort? Was können sie untersuchen, beeinflussen oder übersehen? Wie verändert sich der Ort nach wichtigen Entscheidungen?

**Am Spieltisch:** Erster Eindruck, Zugänge, drei bis sieben spielrelevante Bereiche, anwesende Akteure und aktuelle Spannungen müssen überblickbar sein.

**Sichtbarkeit und Visual:** Wahrnehmbare Merkmale sind spielersichtbar; verborgene Bereiche, Ursachen und Konsequenzen bleiben DM-Wissen. Karten oder Ansichten sind hilfreich, wenn räumliche Entscheidungen oder Wiedererkennung wichtig sind.

**Anti-Patterns:** Raumlisten ohne Funktion; Prosa ohne Interaktionsmöglichkeiten; alle möglichen Bewohner vorsorglich ausarbeiten; lokale Assets im Ortsdokument vollständig duplizieren.

**Definition of Done:** Der Ort kann beschrieben, betreten und bespielt werden; relevante Assets sind verlinkt; mindestens ein Druck oder Veränderungspotenzial ist erkennbar.

## `scene`

**Einsatz:** Eine konkrete spielbare Situation mit Ausgangszustand, Beteiligten und möglichen Übergängen rahmen. Eine Scene ist kein vorgeschriebenes Drehbuch.

**Mindestinhalt:** Einstiegssituation, Teilnehmer und Absichten, unmittelbare Spannung, nutzbare Umgebung, entdeckbare Informationen sowie mehrere mögliche Übergänge mit ihren Zustandsänderungen.

**Leitfragen:** Was ist beim Eintritt bereits in Bewegung? Was wollen die Beteiligten jetzt? Welche Entscheidungen verändern die Situation? Wohin kann die Scene plausibel führen?

**Am Spieltisch:** Ausgangszustand, Absichten, Druck, verfügbare Informationen und zwei oder mehr Übergänge müssen auf einen Blick erfassbar sein.

**Sichtbarkeit und Visual:** Ausgangslage und wahrnehmbare Umgebung sind spielersichtbar; Absichten, verdeckte Informationen und Folgezustände bleiben DM-Wissen. Ein Situationsbild ist nur hilfreich, wenn Position, Stimmung oder sichtbare Details spielrelevant sind.

**Anti-Patterns:** Dialog oder Ergebnis vorschreiben; nur einen gültigen Übergang zulassen; Scene und Location doppelt beschreiben; Konsequenzen aus Spielerentscheidungen ignorieren.

**Definition of Done:** Die Scene kann aus unterschiedlichen Spielerhandlungen weiterlaufen; Teilnehmer handeln aus nachvollziehbaren Absichten; Zustandsänderungen und Folgezustände sind vorbereitet. Sie ist kein verpflichtender Knoten einer festen Szenenfolge.

## `npc`

**Einsatz:** Ein individuelles Wesen mit eigener Motivation, Wissen, Beziehungen und wiedererkennbarem Verhalten führen. Austauschbare Arten oder Archetypen sind `creature`.

**Mindestinhalt:** Tischfunktion, erster Eindruck, erkennbare Merkmale, Stimme oder Ausdruck, öffentliche Rolle, Motivation, Druck oder Furcht, Ressourcen, Wissen, Beziehungen und wahrscheinliches Verhalten.

**Leitfragen:** Was will der NPC jetzt? Woran erkennen und erinnern die Spieler ihn? Was weiß er wirklich, was glaubt er nur? Wie reagiert er auf Hilfe, Druck und Ignorieren?

**Am Spieltisch:** Name, Rolle, ein Erkennungsmerkmal, ein Sprachhinweis, aktuelles Ziel, verfügbare Information und Reaktionsmuster müssen schnell auffindbar sein.

**Sichtbarkeit und Visual:** Erscheinung, Auftreten und öffentliche Rolle sind spielersichtbar; Motive, Ängste, Geheimnisse und falsche Annahmen bleiben DM-Wissen. Ein Porträt lohnt sich bei wiederkehrenden oder leicht verwechselbaren NPCs.

**Anti-Patterns:** Biografie ohne Spielbezug; Motivation mit Plotfunktion verwechseln; Wissen nicht nach Wahrheit trennen; starres Verhalten unabhängig von Spielerhandlungen.

**Definition of Done:** Der NPC ist wiedererkennbar, kann eigenständig reagieren und besitzt mindestens einen konkreten Bezug zu Ort, Information, Fraktion oder Plot.

## `player-character`

**Einsatz:** Eine optionale vorgefertigte oder teilweise vorbereitete Spielerfigur für den einen One-Shot bereitstellen. Vom DM geführte Figuren sind `npc`; ein Regelsystem-Charakterbogen gehört nicht in dieses Asset.

**Mindestinhalt:** One-Shot-Rolle, player-facing Konzept, Ausgangslage, freiwillige persönliche Hooks, etablierter Hintergrund, offene Entscheidungen, narrative Stärken und Herangehensweisen, Grenzen und Komplikationen, freigegebenes Startwissen, Beziehungen, DM-only Verknüpfungen und Player-Release-Status.

**Leitfragen:** Was macht die Figur sofort spielbar? Welche unterschiedlichen Handlungsweisen unterstützt sie? Welche Verbindungen laden zur Beteiligung ein, ohne Motivation oder Loyalität vorzuschreiben? Was darf der Spieler zu Beginn wissen, und welche Entscheidungen bleiben ausdrücklich bei ihm?

**Am Spieltisch:** Konzept, unmittelbare Rolle, zwei oder mehr geeignete Herangehensweisen, relevante Grenzen, Startwissen und freiwillige Hooks müssen schnell erfassbar sein. Offene Entscheidungen dürfen nicht wie festgelegter Kanon klingen.

**Sichtbarkeit und Visual:** Die freigegebene Spielerfassung entsteht ausschließlich nach [Spielerfreigabe für Player Characters](player-character-workflow.md). DM-only Verknüpfungen, verdeckte Wahrheiten und mögliche Konsequenzen bleiben in `player-character.md`. Ein Portrait ist optional und folgt als reguläres Subject-Visual dem Bild-Workflow.

**Anti-Patterns:** Motivation oder Reaktion vorschreiben; eine Figur zur einzigen Quelle notwendigen Wissens machen; Systemeigenschaften oder Zahlenwerte verstecken; `npc` und `player-character` vermischen; interne Links oder Spoiler in `player.md` übernehmen.

**Definition of Done:** Die Figur ist regelneutral und sofort spielbar; Hooks bieten Wahl statt Zwang; etablierter Hintergrund und offene Entscheidungen sind getrennt; notwendiger Fortschritt hängt nicht von einer vorgeschriebenen Charakterhandlung ab; Startwissen und Beziehungen sind kanonisch verlinkt; eine vorhandene `player.md` ist für die aktuelle Version ausdrücklich freigegeben.

## `creature`

**Einsatz:** Eine Art, einen Archetyp, einen Schwarm oder ein austauschbares Wesen über Verhalten und Umweltbezug beschreiben. Ein eigenständiges Individuum mit Motivation und Beziehungen ist `npc`.

**Mindestinhalt:** Tischfunktion, erster Eindruck, erkennbare Merkmale, Habitat, Bedürfnisse, Verhalten, Spuren, Risiken sowie Schwächen oder Ansatzpunkte. Varianten werden nur ergänzt, wenn sie Wiedererkennung, Verhalten, Risiko oder mögliche Ansätze verändern.

**Leitfragen:** Woran wird die Kreatur erkannt, bevor sie erscheint? Was braucht oder verteidigt sie? Wie reagiert sie auf Annäherung, Bedrohung oder Veränderung ihrer Umwelt? Welche nicht-konfrontativen Ansatzpunkte bestehen?

**Am Spieltisch:** Zeichen, Verhalten, unmittelbares Risiko, Eskalationsmuster und nutzbare Schwäche müssen schnell erfassbar sein.

**Sichtbarkeit und Visual:** Erscheinung, Spuren und beobachtbares Verhalten sind spielersichtbar; verborgene Bedürfnisse oder Ursachen bleiben DM-Wissen. Ein Referenzbild ist bei ungewohnter Anatomie oder wiederkehrender Art hilfreich.

**Anti-Patterns:** Verdeckter regelgebundener Statblock; Kreatur nur als Kampfziel behandeln; Habitat und Bedürfnisse ignorieren; Individuen und Artprofil vermischen.

**Definition of Done:** Die Kreatur kann ohne systemspezifische Werte glaubwürdig dargestellt werden; Risiko, Verhalten und mindestens ein alternativer Umgang sind beschrieben.

## `faction`

**Einsatz:** Eine dauerhafte organisierte Gruppe mit ortsübergreifender Agenda, Ressourcen und inneren Spannungen führen.

**Mindestinhalt:** Öffentliche Identität, Agenda, Struktur und Reichweite, relevante Orte, Ressourcen, Methoden, innere Konflikte, Beziehungen, aktueller Druck und mögliche Eskalation.

**Leitfragen:** Was will die Fraktion verändern oder bewahren? Wie setzt sie Einfluss ein? Wo ist sie sichtbar? Welche inneren Widersprüche können Spieler nutzen oder verschärfen?

**Am Spieltisch:** Agenda, erkennbare Vertreter oder Zeichen, aktuelle Handlung, Ressourcen, Beziehungen und nächste Eskalation müssen schnell auffindbar sein.

**Sichtbarkeit und Visual:** Ruf, Symbole und öffentliche Ziele können spielersichtbar sein; interne Konflikte, verdeckte Methoden und tatsächliche Reichweite bleiben DM-Wissen. Emblem oder Kleidungscode helfen bei schneller Zuordnung.

**Anti-Patterns:** Fraktion als einheitliche Meinung darstellen; nur Organisationsgeschichte schreiben; lokale Präsenz duplizieren; Ressourcen ohne konkrete Anwendung nennen.

**Definition of Done:** Die Fraktion verfolgt eine aktive Agenda, kann auf Spielerhandlungen reagieren und besitzt mindestens eine nutzbare interne oder externe Spannung.

## `object`

**Einsatz:** Einen Gegenstand mit eigener Identität, Nutzung, Besitzlage, Information oder Konsequenz beschreiben. Eine reine Spieler-Ausgabe ist `handout`.

**Mindestinhalt:** Erscheinung, Kontext, Fund- oder Besitzlage, Entdeckbarkeit, Eigenschaften, mögliche Nutzungen, Risiken oder Kosten, verbundene Informationen und Konsequenzen.

**Leitfragen:** Warum ist der Gegenstand ein eigenes Asset? Wie wird er gefunden oder erkannt? Was ermöglicht er? Wer reagiert auf Besitz, Nutzung, Verlust oder Zerstörung?

**Am Spieltisch:** Erscheinung, Fundkontext, unmittelbare Nutzung, Risiko und betroffene Akteure müssen schnell erfassbar sein.

**Sichtbarkeit und Visual:** Sichtbare Merkmale und offensichtliche Nutzung sind spielersichtbar; Herkunft, verborgene Eigenschaften und Folgen bleiben DM-Wissen. Ein Visual lohnt sich bei Erkennung, Zustand, Symbolen oder räumlichen Details.

**Anti-Patterns:** Gewöhnliche Requisiten ohne Tischfunktion als Asset anlegen; properties als Regelwerte verstecken; Besitzer und Komponenten ohne Verweise führen; Konsequenzen der Nutzung auslassen.

**Definition of Done:** Der Gegenstand ist auffindbar, nutzbar und mit mindestens einer relevanten Information, Person, Fraktion oder Konsequenz verbunden.

## `information`

**Einsatz:** Eine konkrete Aussage, Erkenntnis, ein Gerücht oder Geheimnis mit Wahrheitsstatus und Entdeckungspfaden kanonisch führen.

**Mindestinhalt:** Präzise Aussage, Wahrheitsstatus und Grenzen, primärer und alternative Entdeckungspunkte, Voraussetzungen, präsentierbare Hinweise, Fehlinterpretationsrisiken sowie Folgen des Lernens und Verpassens.

**Leitfragen:** Was genau können Spieler erfahren? Wie wahr und vollständig ist es? Über welche unterschiedlichen Wege ist es erreichbar? Was verändert sich, wenn es erkannt, missverstanden oder verpasst wird?

**Am Spieltisch:** Aussage, Fundorte, konkrete Präsentationshinweise, bekannte Träger und Konsequenz müssen schnell auffindbar sein.

**Sichtbarkeit und Visual:** Die Information wird erst durch einen beschriebenen Entdeckungspunkt spielersichtbar; Wahrheitsstatus und Grenzen bleiben DM-Wissen. Ein eigenes Visual ist selten nötig, kann aber über Handout oder Subject-Visual vermittelt werden.

**Anti-Patterns:** Vage Themen statt konkreter Aussage; genau ein fragiler Fundweg; Hinweis und Schlussfolgerung verwechseln; keine Folge bei Verpassen; Gerücht als bestätigte Wahrheit schreiben.

**Definition of Done:** Aussage und Wahrheitsstatus sind eindeutig; für eine notwendige Schlussfolgerung bestehen mindestens zwei unabhängige Entdeckungspfade, andernfalls mindestens ein belastbarer Pfad; Folgen von Lernen und Verpassen sind bekannt.

## `encounter`

**Einsatz:** Eine Situation unter Druck mit Trigger, widerstreitenden Absichten, Eskalation und Konsequenzen beschreiben. Ein Encounter ist nicht automatisch ein Kampf.

**Mindestinhalt:** Trigger, Ausgangssituation, Beteiligte und Absichten, nutzbare Umgebung, Eskalationsstufen, mehrere Ansätze sowie Folgen für Erfolg, Preis, Scheitern, Rückzug und Ignorieren.

**Leitfragen:** Warum entsteht jetzt Druck? Was wollen die Beteiligten? Welche Hebel bietet die Umgebung? Wie verändert sich die Lage, statt lediglich zu enden?

**Am Spieltisch:** Trigger, Absichten, sichtbarer Druck, zwei oder mehr Ansätze, Eskalation und Folgezustände müssen sofort verfügbar sein.

**Sichtbarkeit und Visual:** Wahrnehmbare Situation und Gefahren sind spielersichtbar; verdeckte Absichten und spätere Folgen bleiben DM-Wissen. Ein Visual hilft bei räumlicher Lage oder klar erkennbaren Gefahren, nicht als Ersatz für Handlungsoptionen.

**Anti-Patterns:** Encounter mit Kampf gleichsetzen; eine vorgesehene Lösung; binäres Erfolg-Scheitern ohne Folgezustand; systemspezifische Schwierigkeit statt erzählerischem Druck.

**Definition of Done:** Der Encounter kann über mehrere Ansätze gespielt werden; Eskalation ist nachvollziehbar; jedes wesentliche Ergebnis führt zu einer spielbaren Konsequenz.

## `plot-thread`

**Einsatz:** Eine fortlaufende dramatische Frage mit Druck, Informationswegen, Entscheidungen und möglichen Auflösungen führen.

**Mindestinhalt:** Dramatische Frage, Einstiegspunkte, aktueller Zustand, fortschreitender Druck, Informationsweg, beteiligte Assets, bedeutungsvolle Spielerentscheidungen, mehrere mögliche Auflösungen, minimaler Auflösungszustand, sichere Kürzungen und Folgen des Ignorierens.

**Leitfragen:** Welche offene Frage treibt diesen Thread? Wie können Spieler einsteigen oder aussteigen? Was geschieht ohne ihr Eingreifen? Welche unterschiedlichen Entscheidungen können den Zustand verändern?

**Am Spieltisch:** Aktueller Zustand, nächster Druck, verfügbare Einstiegspunkte, bekannte Informationen, minimaler Auflösungszustand, sichere Kürzungen und mögliche Folgezustände müssen schnell erfassbar sein. Unter `Involved assets` werden Inhalte in Prosa als `core`, `supporting` oder `optional` eingeordnet; diese Labels sind keine Metadatenwerte.

**Sichtbarkeit und Visual:** Spieler sehen nur bekannte Ziele, Zeichen und Konsequenzen; tatsächliche Ursachen, verdeckte Beteiligte und mögliche Auflösungen bleiben DM-Wissen. Eigene Visuals sind selten nötig und sollten auf beteiligte Assets verweisen.

**Anti-Patterns:** Vorgegebene Szenenfolge; nur eine gültige Auflösung; passiver Thread ohne Druck; zentrale Information nur einmal platzieren; Ignorieren folgenlos lassen.

**Definition of Done:** Einstieg, Druck, bedeutungsvolle Wahlmöglichkeiten, robuste Informationswege und mindestens zwei plausible Folgezustände sind vorhanden; der Thread beschreibt nächsten Druck, `Late pressure`, minimalen Auflösungszustand, must-preserve Informationen, sichere Kürzungen und Folgen des Ignorierens; beteiligte Assets sind verlinkt. Jede Kürzung erhält die für den zentralen Konflikt notwendigen Informationswege und Auflösungen.

## `event`

**Einsatz:** Ein vergangenes, laufendes, geplantes oder mögliches Geschehen mit zeitlicher Einordnung und Folgen festhalten.

**Mindestinhalt:** Zeit und Status, Trigger oder Ursachen, Beteiligte, Ablauf, sichtbare Zeichen, unmittelbare und langfristige Konsequenzen sowie Möglichkeiten zur Verhinderung oder Veränderung.

**Leitfragen:** Wann und unter welchen Bedingungen tritt das Event ein? Wer handelt oder ist betroffen? Was können Spieler vorher erkennen? Welche Teile lassen sich verhindern, umlenken oder nur noch bewältigen?

**Am Spieltisch:** Auslöser, sichtbare Vorzeichen, aktueller Stand, betroffene Assets und nächste Konsequenz müssen schnell auffindbar sein.

**Sichtbarkeit und Visual:** Beobachtete Ereignisse und sichtbare Folgen sind spielersichtbar; Ursachen, Zeitplan und vermeidbare Bedingungen können DM-Wissen bleiben. Ein Visual hilft bei historischen Schlüsselmomenten oder deutlich verändertem Zustand.

**Anti-Patterns:** Offenen Plot-Thread als festes Event behandeln; Ursache und Konsequenz verwechseln; unvermeidliches Ereignis ohne Handlungsspielraum behaupten; Timeline und Asset widersprechen lassen.

**Definition of Done:** Status und zeitliche Einordnung sind klar; sichtbare Zeichen und Folgen sind beschrieben; Veränderbarkeit oder Unvermeidbarkeit ist bewusst festgelegt.

## `handout`

**Einsatz:** Ein kontrolliert spielersichtbares Artefakt mit eigener Ausgabe und eindeutig getrenntem DM-Kontext bereitstellen.

**Mindestinhalt:** Player-facing Inhalt, Auslieferungssituation, DM-only Kontext, offenbarte Information und Player-Release-Status. `Player release` verweist auf eine vorhandene freigegebene `player.md`; eine PNG-Fassung wird ausschließlich als verlinktes Visual geführt.

**Leitfragen:** Was erhalten Spieler tatsächlich? Wann und unter welchen Bedingungen? Welche Information wird dadurch bestätigt oder angedeutet? Welche internen Hinweise dürfen keinesfalls in die Ausgabe gelangen?

**Am Spieltisch:** Freigegebener Inhalt, Übergabepunkt und betroffene Information müssen sofort auffindbar sein; DM-Kontext muss optisch eindeutig getrennt bleiben.

**Sichtbarkeit und Visual:** Nur der freigegebene Abschnitt ist spielersichtbar. Eine eigenständige `player.md` entsteht ausschließlich nach dem Safety- und Freigabeworkflow in [Spielerfreigabe für Handouts](player-handout-workflow.md). Ein PNG ist optional und lohnt sich bei Layout, Handschrift, Symbolen oder Illustration; die freigegebene Markdown-Fassung bleibt die maßgebliche Spielerquelle.

**Anti-Patterns:** DM-Notizen in Spielertext kopieren; interne Links oder Frontmatter exportieren; Information und Handout doppelt kanonisch beschreiben; Ausgabe ohne Freigabe erzeugen.

**Definition of Done:** Player-facing Inhalt ist eigenständig verständlich; DM-only Wissen ist sicher getrennt; Auslieferung und `reveals`-Beziehungen sind klar. Wenn eine Spielerdatei existiert, verweist die Quelle nachvollziehbar auf die ausdrücklich freigegebene Quellversion und der Safety-Check ist bestanden.

## `visual`

**Einsatz:** Eine reproduzierbare visuelle Darstellung genau eines kanonischen Subject-Assets beschreiben.

**Mindestinhalt:** Tischfunktion, Subject-Beziehung und exakte Identitätsquelle, stabile visuelle Anker, dargestellter One-Shot-Zustand, erlaubte Variation, Spieler-Sichtbarkeit, PNG-Freigabestatus, gewünschte Ausgabe, Prompt-Verweis, Provenienz und Revisionskontext.

**Leitfragen:** Welche Tischfunktion erfüllt das Bild? Welche Subject-Abschnitte begründen die Identität? Welche Merkmale müssen unverändert bleiben? Welcher innerhalb des One-Shots mögliche Zustand wird gezeigt? Welche Aspekte sind freie Stil- oder Perspektivvariation? Was darf das Bild nicht zeigen oder neu erfinden?

**Am Spieltisch:** Subject, sichtbare Schlüsseldetails, Freigabestatus und vorhandene Ausgabe müssen eindeutig sein. Eine PNG-Datei gilt nur als vorhanden, wenn sie tatsächlich gespeichert ist.

**Sichtbarkeit und Visual:** Das Visual selbst definiert, ob und wann seine Ausgabe Spielern gezeigt wird. Geheimnisse dürfen weder Komposition noch Hintergrund unbeabsichtigt verraten. Vor jeder ersten PNG-Erzeugung und jedem Ersatz gilt der Freigabeweg aus dem [Bild-Workflow](bild-workflow.md).

**Anti-Patterns:** Neue kanonische Fakten im Prompt erfinden; mehrere Subjects vermischen; Stil als Identitätsmerkmal behandeln; PNG ohne Prompt oder Provenienz; vorhandene Ausgabe still ersetzen.

**Definition of Done:** Subject und kanonische Identitätsquelle sind eindeutig; stabile Anker, dargestellter Zustand und freie Variation sind getrennt; Prompt und Ausgabepfad stimmen überein; Sichtbarkeit und Ausschlüsse verhindern Widersprüche oder Spoiler. Ein vorhandenes PNG entspricht seinem dokumentierten Status, der freigegebenen Visual-Version und der Provenienz.

## `random-table`

**Einsatz:** Eine begrenzte Auswahlmenge für regelneutrale, kontextgebundene Improvisation bereitstellen.

**Mindestinhalt:** Tischfunktion, Einsatzkontexte, Auswahlweise, unterscheidbare Einträge, Einschränkungen und Regel zur Kanonisierung dauerhaft relevanter Ergebnisse.

**Leitfragen:** Welche Vorbereitungslücke füllt die Tabelle? Wann passt sie und wann nicht? Verändert jeder Eintrag die Situation sinnvoll? Welche Ergebnisse benötigen anschließend ein eigenes Asset?

**Am Spieltisch:** Kontext, schnelle Auswahlmethode und kurze direkt nutzbare Einträge müssen ohne weitere Vorbereitung verständlich sein.

**Sichtbarkeit und Visual:** Einträge können DM-Impulse oder player-facing Ergebnisse sein; dies muss im Zweck klar sein. Ein eigenes Visual ist gewöhnlich unnötig.

**Anti-Patterns:** Beliebige Füllinhalte; versteckte Würfelabhängigkeit; Einträge ohne Konsequenz oder Kontext; dauerhaft etabliertes Ergebnis nur in der Tabelle belassen.

**Definition of Done:** Alle Einträge passen zum definierten Kontext, sind unterscheidbar und direkt nutzbar; die Kanonisierungsregel verhindert, dass relevante Ergebnisse verloren gehen.
