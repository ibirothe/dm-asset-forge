# Kanonischer DM-Asset-Katalog v1

Diese Datei ist die normative Quelle für Asset-Typen, technische Bezeichner, kanonische Speicherorte und Typauswahl. Widersprechen Templates, Skripte oder andere Anleitungen diesem Katalog, gilt dieser Katalog. Fachliche Mindestinhalte, Tischgebrauch und Definition of Done stehen im [Autoren- und Tischleitfaden](asset-authoring-guide.md); gemeinsame Metadaten und qualitative Werteskalen in [Metadaten und regelneutrale Werte v1](metadaten-und-werte.md); Ownership, Ortswechsel und Rückverweise in [Beziehungen und ortszentrierte Speicherung v1](beziehungen-und-speicherorte.md).

## Geltungsbereich

- `singleton`: genau einmal pro Abenteuer vorhanden und global gültig
- `global`: nicht im Besitz eines einzelnen Ortes; kann viele Orte betreffen
- `local`: besitzt genau einen kanonischen primären Ort
- `subject-owned`: liegt beim kanonischen Subject-Asset und übernimmt dessen Geltungsbereich

Ein Asset wird nur einmal vollständig gespeichert. Weitere Vorkommen werden durch relative Links dargestellt.

## Typenübersicht

| Type | ID prefix | Scope | Canonical path | Required relation | Visual relationship |
|---|---|---|---|---|---|
| `world` | `world-` | singleton | `adventure/10-world/overview.md` | adventure | optionale `visual`-Assets für Welt, Regionen oder Stil |
| `location` | `loc-` | local | `adventure/30-locations/<location>/location.md` | world; optional parent location | optionale Ansicht, Karte oder Atmosphäre als `visual` |
| `scene` | `scene-` | local | `adventure/30-locations/<location>/scenes/<scene>/scene.md` | primary location | optionales Stimmungs- oder Situationsbild |
| `npc` | `npc-` | local | `adventure/30-locations/<location>/npcs/<npc>/npc.md` | primary location | empfohlenes Identitäts- oder Porträt-`visual` bei wiederkehrenden NPCs |
| `creature` | `cre-` | local | `adventure/30-locations/<location>/creatures/<creature>/creature.md` | primary location | empfohlenes Referenz-`visual` bei wichtigen Arten oder Individuen |
| `faction` | `fac-` | global | `adventure/40-global/factions/<faction>/faction.md` | world | optionales Emblem, Zeichen oder Gruppenbild |
| `object` | `obj-` | local | `adventure/30-locations/<location>/objects/<object>/object.md` | primary location | empfohlen, wenn Aussehen, Zustand oder Erkennung spielrelevant ist |
| `information` | `info-` | local | `adventure/30-locations/<location>/information/<information>/information.md` | primary discovery location | normalerweise kein eigenes Bild; kann durch `handout` oder `visual` vermittelt werden |
| `encounter` | `enc-` | local | `adventure/30-locations/<location>/encounters/<encounter>/encounter.md` | primary location | optionales Lage-, Gegner- oder Atmosphärenbild |
| `plot-thread` | `plot-` | global | `adventure/20-plot/threads/<plot-thread>/plot-thread.md` | world and at least one entry asset | normalerweise kein eigenes Bild; verlinkt beteiligte Visuals |
| `event` | `event-` | global | `adventure/10-world/events/<event>/event.md` | world and affected assets | optionales Bild für sichtbare oder historische Ereignisse |
| `handout` | `hand-` | local | `adventure/30-locations/<location>/handouts/<handout>/handout.md` | primary delivery location | eine PNG-Ausgabe wird als untergeordnetes `visual` geführt |
| `visual` | `vis-` | subject-owned | `<subject-directory>/visuals/<visual>/visual.md` | exactly one subject asset | PNG und `.prompt.md` liegen neben `visual.md` |
| `random-table` | `table-` | global | `adventure/40-global/random-tables/<random-table>/random-table.md` | world and applicable contexts | normalerweise kein eigenes Bild |

`<subject-directory>` bezeichnet den Ordner des kanonischen Subject-Assets. Bei dateibasierten Singletons wie `world` ist es der Ordner, der die kanonische Datei enthält.

## Typdefinitionen

### `world`

Beschreibt die übergreifende Realität des Abenteuers: Prämisse, bestätigte Wahrheiten, Alltagslogik, Kräfte, Themen und Grenzen. `world` ist ein globaler Singleton und kein Sammelcontainer für jede Detailinformation.

Typische Nutzung: Weltprämisse, Naturgesetze, gesellschaftliche Grundannahmen und übergreifende Spannungen. Ortsgebundene Details gehören in `location`; zeitlich abgegrenzte Geschehnisse in `event`.

### `location`

Beschreibt einen räumlich stabilen, wiederbesuchbaren Ort oder eine Region mit Zugang, Grenzen, Funktion, Atmosphäre und möglichen Veränderungen. Eine Location kann andere Locations hierarchisch enthalten.

Typische Nutzung: Region, Siedlung, Gebäude, Raum, Wildnisabschnitt oder klar abgegrenzte Ebene. Eine vorübergehende Spielsituation am Ort ist eine `scene`, kein neuer Ort.

### `scene`

Beschreibt eine konkrete spielbare Situation an einem Ort: Ausgangslage, anwesende Assets, unmittelbare Spannung, mögliche Übergänge und Veränderungen nach der Szene. Sie kann ohne Konflikt bestehen.

Typische Nutzung: Audienz, Untersuchung, Reiseabschnitt, Enthüllung oder soziale Zusammenkunft. Erfordert die Situation vor allem Eskalation und Konsequenzen unter Druck, kann zusätzlich ein `encounter` verlinkt werden.

### `npc`

Beschreibt einen individuellen handlungsfähigen Charakter mit Identität, Motivation, Wissen, Beziehungen und wiedererkennbarem Verhalten. Die erzählerische Rolle entscheidet, nicht Spezies oder Erscheinungsform.

Typische Nutzung: benannte Person, individueller Geist, intelligentes Tier oder einzigartiges Wesen. Ein austauschbarer Vertreter einer Art oder ein Artenprofil ist `creature`.

### `creature`

Beschreibt eine Art, einen Archetyp oder eine nicht als vollständiger Charakter ausgearbeitete Kreatur. Fokus sind Verhalten, Lebensraum, erkennbare Merkmale, Bedürfnisse, Risiken und erzählerische Ansatzpunkte.

Typische Nutzung: Tierart, Monsterarchetyp, Schwarm oder anonyme Wächter. Erhält ein Individuum eigene Motivation, Beziehungen und Wissen, wird es als `npc` modelliert und kann auf sein Creature-Profil verweisen.

### `faction`

Beschreibt eine ortsübergreifende organisierte Gruppe mit Agenda, Struktur, Reichweite, Ressourcen, Methoden, inneren Spannungen und Beziehungen. Lokale Niederlassungen werden über Locations und lokale Assets verknüpft.

Typische Nutzung: Gilde, Kult, Haus, Regierung, Geheimbund oder informelles Netzwerk. Eine kurzfristig anwesende Gruppe ohne dauerhafte Organisation ist Teil einer `scene` oder eines `encounter`.

### `object`

Beschreibt einen in der Spielwelt existierenden Gegenstand, dessen Identität, Besitz, Eigenschaften, Nutzung oder Konsequenzen relevant sind. Der kanonische Ort ist der primäre Fund-, Lager- oder Besitzort.

Typische Nutzung: Schlüssel, Dokument in der Fiktion, Relikt, Werkzeug, Waffe oder auffälliges Alltagsobjekt. Die physische oder digitale Ausgabe für Spieler ist ein `handout` und verweist auf das Object.

### `information`

Beschreibt eine konkrete Aussage oder Erkenntnis mit Wahrheitsstatus, Grenzen, Entdeckungspunkten, Voraussetzungen und Konsequenzen. Sie bleibt DM-Kanon, unabhängig davon, wie sie vermittelt wird.

Typische Nutzung: Hinweis, Gerücht, Geheimnis, Schlussfolgerung oder historischer Fakt. Ein spielersichtbarer Brief, Bildausschnitt oder Textzettel ist ein `handout`, das die Information offenbaren kann.

### `encounter`

Beschreibt eine druckvolle Situation mit Trigger, beteiligten Absichten, Eskalation, nutzbarer Umgebung, möglichen Ansätzen und Konsequenzen. Ein Encounter ist nicht automatisch ein Kampf.

Typische Nutzung: Verfolgung, Verhandlung unter Zeitdruck, Hinterhalt, Umweltgefahr oder offener Konflikt. Die räumlich und zeitlich breitere Rahmung kann als `scene` bestehen.

### `plot-thread`

Beschreibt eine fortlaufende dramatische Frage mit Einstiegspunkten, Druck, Informationsweg, Entscheidungen, möglichen Auflösungen und Folgen des Ignorierens. Der Plot-Thread verlinkt Assets, besitzt sie aber nicht.

Typische Nutzung: Quest, Mysterium, Fraktionskonflikt oder drohende Entwicklung. Ein bereits eingetretenes oder terminiertes Geschehen ist ein `event`.

### `event`

Beschreibt ein eindeutig geschehenes, geplantes oder mögliches Ereignis mit zeitlicher Einordnung, Ursache, Beteiligten und Folgen. Events bilden die kanonische Timeline und können Plot-Threads verändern.

Typische Nutzung: historischer Umbruch, bevorstehendes Ritual, Frist, Katastrophe oder eine bereits eingetretene Konsequenz. Ein Event ist kein offener Handlungsbogen.

### `handout`

Beschreibt ein kontrolliert spielersichtbares Artefakt mit Auslieferungskontext, offenbarten Informationen und strikt getrennten DM-Hinweisen. Markdown ist die Quelle; eine optionale PNG-Fassung wird als Subject-owned `visual` des Handouts geführt.

Typische Nutzung: Brief, Aushang, Tagebuchseite, Symbolblatt oder Bild für Spieler. Ein Handout darf keine kanonischen Geheimnisse enthalten, die nicht bewusst offengelegt werden.

### `visual`

Beschreibt die reproduzierbare visuelle Darstellung genau eines Subject-Assets. Das Subject bleibt Quelle stabiler Identitätsmerkmale; das Visual trennt deren Extrakt von dargestelltem One-Shot-Zustand, freier Variation, Komposition, Stil, Ausschlüssen, Ausgabe, Freigabe, Provenienz und Revisionen.

Typische Nutzung: Porträt, Ortsansicht, Karte, Gegenstandsbild, Emblem oder Stimmungsbild. Das `visual`-Asset ist die Metadatenquelle; PNG und Prompt sind zugehörige Dateien, keine separaten kanonischen Assets.

### `random-table`

Beschreibt eine wiederverwendbare Auswahlmenge für kontrollierte Improvisation. Sie definiert Zweck, Einsatzkontext, Einträge, Auswahlweise und Einschränkungen, ohne ein bestimmtes Würfelsystem vorauszusetzen.

Typische Nutzung: Gerüchte, Begegnungsimpulse, Wetter, Fundstücke, Namen oder Komplikationen. Ein feststehender Sachverhalt wird als passender kanonischer Asset-Typ gespeichert, nicht als Tabelleneintrag allein.

## Auswahlregeln bei Überschneidungen

| Entscheidung | Verwende A, wenn … | Verwende B, wenn … |
|---|---|---|
| `location` oder `scene` | der räumliche Kontext stabil und wiederbesuchbar ist | die konkrete Situation, Besetzung oder Spannung zeitlich begrenzt ist |
| `scene` oder `encounter` | der spielbare Rahmen auch ohne Konflikt funktioniert | Absichten, Druck, Eskalation und Konsequenzen im Zentrum stehen |
| `npc` oder `creature` | ein individuelles Wesen Motivation, Wissen und Beziehungen besitzt | Art, Archetyp oder austauschbares Verhalten beschrieben wird |
| `object` oder `handout` | der Gegenstand in der Fiktion existiert | die spielersichtbare Ausgabe am Tisch gemeint ist |
| `information` oder `handout` | Wahrheit, Gerücht oder Erkenntnis als Kanon geführt wird | die kontrollierte Vermittlungsform für Spieler gemeint ist |
| `plot-thread` oder `event` | eine offene dramatische Frage fortschreitet | ein zeitlich bestimmtes Geschehen festgehalten wird |
| `visual` oder `handout` | eine reproduzierbare Darstellung eines Subject-Assets benötigt wird | das Ergebnis gezielt an Spieler ausgegeben wird |
| `random-table` oder festes Asset | mehrere kontextgebundene Optionen zur Improvisation benötigt werden | ein Ergebnis als etablierter Kanon fortbesteht |

## Implementierungsstatus

`scripts/new_asset.py` unterstützt alle 14 Typen aus diesem Katalog. Der Generator wählt Template, ID-Präfix und kanonischen Pfad anhand von `--type`, prüft erforderliche Beziehungen vor dem Schreiben und überschreibt bestehende Dateien nur mit `--overwrite`.

Bei `world` ersetzt der Generator mit explizitem `--overwrite` die noch unbefüllte Overview-Datei des initialisierten Scaffolds. Bei `visual` entstehen `visual.md` und das zugehörige `<slug>.prompt.md`; eine PNG-Datei wird nicht automatisch erzeugt. Der Generator pflegt die vorhandenen zuständigen Indizes sowie eindeutig aus Ownership, Location-Hierarchie und Visual-Subject ableitbare relative Gegenlinks. Freie oder kontextabhängige Beziehungen und das Change Log werden weiterhin bewusst durch Codex gepflegt.
