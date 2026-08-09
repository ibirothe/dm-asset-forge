# Beziehungen und ortszentrierte Speicherung v1

Diese Datei ist die normative Quelle für Ownership, kanonische Speicherorte und Beziehungen zwischen Assets. Der [Asset-Katalog](asset-katalog.md) bestimmt Typ und Pfad; [Metadaten und Werte](metadaten-und-werte.md) bestimmen zulässige Schlüssel und Werte.

## Inhalt

- [Grundmodell](#grundmodell)
- [Begriffe und Felder](#begriffe-und-felder)
- [Kanonische Datei und Verweise](#kanonische-datei-und-verweise)
- [Erlaubte Beziehungen](#erlaubte-beziehungen)
- [Richtung und Rückverweise](#richtung-und-rückverweise)
- [Mobile NPCs und reisende Kreaturen](#mobile-npcs-und-reisende-kreaturen)
- [Mehrteilige Objekte](#mehrteilige-objekte)
- [Ortsübergreifende Informationen](#ortsübergreifende-informationen)
- [Globale Assets](#globale-assets)
- [Änderungsabläufe](#änderungsabläufe)

## Grundmodell

Ownership und Aufenthaltsort sind zwei verschiedene Sachverhalte:

- `scope` legt fest, wie ein Asset kanonisch eingeordnet und gespeichert wird.
- `primary_location` legt bei lokalen Assets den redaktionell verantwortlichen Ort fest.
- `current_location` beschreibt bei beweglichen Assets den aktuellen Aufenthaltsort in der Fiktion.
- weitere Ortsbeziehungen beschreiben Herkunft, Auftritte, Entdeckung oder thematische Relevanz.

Ein Ortswechsel ändert daher nicht automatisch den kanonischen Speicherort. Eine Datei wird nur dann verschoben, wenn sich ihre redaktionelle Ownership dauerhaft ändert.

## Begriffe und Felder

### `scope`

Jedes Asset führt genau einen Scope aus dem Asset-Katalog:

| Value | Bedeutung |
|---|---|
| `singleton` | Genau einmal pro Abenteuer vorhanden; kein lokaler Besitzer. |
| `global` | Ortsübergreifend kanonisch; verlinkt relevante Orte, gehört aber keinem einzelnen Ort. |
| `local` | Besitzt genau einen kanonischen lokalen Speicherort. |
| `subject-owned` | Liegt beim kanonischen Subject-Asset und übernimmt dessen Geltungsbereich. |

`scope` beschreibt Speicherung, nicht erzählerische Wirkung. Ein lokales Objekt kann `reach: world-spanning` besitzen; ein globaler Plot-Thread kann nur einen einzelnen Ort betreffen.

### Ortsfelder

| Key | Kardinalität | Bedeutung |
|---|---:|---|
| `primary_location` | genau 1 bei lokalen Nicht-Location-Assets | Ort, der die kanonische Datei besitzt; entspricht dem Ordner unter `30-locations/`. |
| `parent_location` | 0 oder 1 bei Locations | Räumlich übergeordnete Location; `null` bei einer Top-Level-Location. |
| `current_location` | 0 oder 1 | Aktueller physischer Aufenthaltsort eines beweglichen Assets; kann vom primären Ort abweichen. |
| `origin_location` | 0 oder 1 | Ort der Herkunft, Entstehung oder ursprünglichen Zugehörigkeit. |
| `appearance_locations` | Liste | Zusätzliche Orte mit geplantem, aktuellem oder wiederkehrendem Auftritt. |
| `discovery_locations` | Liste | Orte, an denen eine Information entdeckt werden kann. |
| `delivery_locations` | Liste | Orte, an denen ein Handout in der Fiktion ausgegeben werden kann. |
| `entry_locations` | Liste | Orte, an denen ein Plot-Thread beginnen oder betreten werden kann. |
| `related_locations` | Liste | Direkte Ortsbezüge eines globalen Assets ohne lokale Ownership. |

Beziehungsfelder enthalten stabile Asset-IDs. `unknown`, `null` und `[]` werden nach der Metadatenspezifikation verwendet. Relative Markdown-Links in den Inhaltsabschnitten machen dieselben Beziehungen für Menschen navigierbar.

### Primärer, aktueller und ursprünglicher Ort

- Der primäre Ort beantwortet: „Welche Location besitzt und pflegt dieses Asset?“
- Der aktuelle Ort beantwortet: „Wo befindet sich das Asset jetzt in der Fiktion?“
- Der Herkunftsort beantwortet: „Woher stammt das Asset?“
- Ein Auftrittsort beantwortet: „Wo wird dieses Asset zusätzlich spielrelevant?“

Nur `primary_location` bestimmt den Dateipfad. Die anderen Felder erzeugen ausschließlich Beziehungen.

## Kanonische Datei und Verweise

1. Jedes lokale Asset wird genau einmal vollständig unter seinem primären Ort gespeichert.
2. Jeder weitere Ort enthält nur einen relativen Markdown-Link und höchstens ortsspezifischen Kontext, niemals eine Kopie des beschreibenden Asset-Inhalts.
3. Strukturierte Metadaten referenzieren stabile IDs, nicht Dateipfade.
4. Markdown-Links verwenden relative Pfade, damit Navigation und Linkprüfung funktionieren.
5. Titel dürfen sich ändern; IDs bleiben stabil. Links und sichtbare Linktexte werden bei Bedarf aktualisiert.
6. Ein Alias, Export, PNG oder Bildbriefing ist keine zweite kanonische Asset-Datei.

Ortspezifischer Kontext darf am auftretenden Ort stehen, etwa „Mara wartet hier nur bei Flut“. Dauerhafte Motivation, Aussehen und Wissen bleiben ausschließlich in Maras kanonischer NPC-Datei.

## Erlaubte Beziehungen

| Key | Source → Target | Zweck |
|---|---|---|
| `primary_location` | lokales Asset → `location` | Kanonische lokale Ownership. |
| `parent_location` | `location` → `location` | Räumliche Hierarchie. |
| `current_location` | bewegliches Asset → `location` | Aktueller Aufenthaltsort. |
| `origin_location` | Asset → `location` | Herkunft oder Entstehung. |
| `appearance_locations` | Asset → `location` | Zusätzliche Auftrittsorte. |
| `discovery_locations` | `information` → `location` | Alternative Fundorte derselben Information. |
| `delivery_locations` | `handout` → `location` | Mögliche Übergabeorte. |
| `entry_locations` | `plot-thread` → `location` | Einstiegspunkte. |
| `related_locations` | globales Asset → `location` | Direkte Ortsrelevanz ohne Ownership. |
| `owner` | `object` → `npc` oder `faction` | Besitz oder Verantwortung in der Fiktion. |
| `factions` | `npc` → `faction` | Mitgliedschaft oder feste Zugehörigkeit. |
| `known_by` | `information` → `npc` oder `faction` | Akteure mit dieser Information. |
| `participants` | `scene`, `encounter` oder `event` → Asset | Beteiligung im jeweiligen Kontext. |
| `reveals` | `handout` → `information` | Kontrolliert offengelegte Information. |
| `related_threads` | Asset → `plot-thread` | Direkte Plot-Relevanz. |
| `related_factions` | Asset → `faction` | Direkte Fraktionsrelevanz. |
| `part_of` | `object` → `object` | Zugehörigkeit eines eigenständig relevanten Teils. |
| `components` | `object` → Liste von `object` | Eigenständig relevante Bestandteile. |
| `subject_asset` | `visual` → Asset | Genau ein dargestelltes Subject-Asset. |

Freie zusätzliche Beziehungen werden im Text mit relativen Links beschrieben. Ein neuer strukturierter Schlüssel wird erst in der Metadatenspezifikation definiert, bevor Templates ihn verwenden.

## Richtung und Rückverweise

Die strukturierte Beziehung wird an der Source geführt. Ein Rückverweis ist ein relativer Markdown-Link am Target; es wird kein zweites Metadatenfeld erfunden, wenn die Tabelle keinen Gegen-Key vorsieht.

| Beziehung | Rückverweis am Target |
|---|---|
| `primary_location` | erforderlich: Location verlinkt das Asset im passenden Abschnitt und Index. |
| `parent_location` | erforderlich: Parent-Location verlinkt die Child-Location. |
| `current_location` | erforderlich, solange der Aufenthalt bekannt und spielrelevant ist. |
| `appearance_locations` | erforderlich: jeder genannte Ort verlinkt den Auftritt. |
| `discovery_locations` | erforderlich: jeder Fundort verlinkt dieselbe Information. |
| `delivery_locations` | erforderlich: jeder Übergabeort verlinkt das Handout. |
| `entry_locations` | erforderlich: jeder Einstieg verlinkt den Plot-Thread. |
| `related_locations` | erforderlich, wenn die Beziehung am Ort spielrelevant ist. |
| `origin_location` | optional; erforderlich, wenn die Herkunft am Ort selbst relevant ist. |
| `part_of` / `components` | erforderlich und beidseitig in Metadaten konsistent. |
| `reveals` | erforderlich: Information verlinkt das offenbarende Handout. |
| `subject_asset` | erforderlich: Subject-Asset verlinkt das Visual. |
| `owner`, `factions`, `known_by` | erforderlich, wenn beide Seiten als Assets existieren und die Beziehung kanonisch ist. |
| `participants`, `related_threads`, `related_factions` | Rückverweis erforderlich, wenn die Beziehung dauerhaft oder für Navigation wesentlich ist; sonst optional. |

Indizes sind Navigationshilfen und keine zweite kanonische Quelle. Sie verlinken Assets, enthalten aber keine vollständigen Beschreibungen.

### Deterministische Navigationspflege

`scripts/new_asset.py` pflegt beim Anlegen eines Assets nur Beziehungen, die ohne fachliche Interpretation feststehen:

- lokale Assets und ihr `primary_location` verlinken sich gegenseitig;
- Parent- und Child-Locations verlinken sich gegenseitig;
- Visual und `subject_asset` verlinken sich gegenseitig;
- Locations, NPCs, Objects, Information, Plot-Threads und Factions erhalten genau eine aktuelle Zeile in ihren vorhandenen zuständigen Indizes.

Die Pflege ist idempotent: Ein ausdrücklich wiederholtes Schreiben aktualisiert die bestehende Zeile oder den vorhandenen Link, statt einen zweiten Eintrag anzulegen. Manuell ergänzte strukturierte Beziehungen benötigen ebenfalls die in der Tabelle definierten Links. `scripts/validate_adventure.py` meldet fehlende Gegenlinks sowie fehlende, doppelte oder anhand der kanonischen Metadaten eindeutig veraltete Indexzeilen. Es verändert keine Datei.

Codex bleibt für die fachliche Auswahl optionaler Beziehungen, ortsspezifischen Kontext, Linktexte mit zusätzlicher Bedeutung und das Change Log verantwortlich.

## Mobile NPCs und reisende Kreaturen

- Die kanonische Datei bleibt unter `primary_location`, auch wenn `current_location` wechselt.
- Der aktuelle Ort verlinkt das Asset und darf ortsspezifischen Auftrittskontext führen.
- Geplante oder wiederkehrende Stationen stehen in `appearance_locations`.
- Eine Reisehistorie wird als `event`, Timeline-Eintrag oder kurzer Verlauf im Asset dokumentiert; sie wird nicht durch Dateikopien abgebildet.
- Bei dauerhaft geänderter redaktioneller Ownership wird die kanonische Datei verschoben, `primary_location` angepasst und jeder eingehende Link aktualisiert.

Reisende Gruppen oder Arten werden als `creature` modelliert, solange kein Individuum eigene Motivation, Beziehungen und Wissen benötigt. Individuen bleiben `npc` und können auf ein Creature-Profil verweisen.

## Mehrteilige Objekte

1. Haben Bestandteile keine eigene Spielrelevanz, bleiben sie Freitext im einzigen Object-Asset.
2. Hat ein Bestandteil eigene Fundorte, Informationen, Besitzer oder Konsequenzen, erhält er ein eigenes Object-Asset.
3. Das Teil setzt `part_of` auf die ID des Gesamtobjekts; das Gesamtobjekt führt die Teil-ID in `components`.
4. Jedes eigenständige Teil besitzt seinen eigenen primären Ort und genau eine kanonische Datei.
5. Das Gesamtobjekt bleibt am redaktionellen Ankerort. Sein `current_location` ist `null`, solange es nicht zusammengesetzt als Ganzes existiert.

## Ortsübergreifende Informationen

Eine Information wird nicht pro Fundort kopiert:

- `primary_location` bestimmt Ablage und redaktionelle Ownership, gewöhnlich am wichtigsten oder zuerst ausgearbeiteten Fundort.
- `discovery_locations` enthält alle tatsächlichen Fundorte, einschließlich des primären Fundorts.
- Jeder Fundort verlinkt dieselbe Information und beschreibt nur die lokale Vermittlung.
- Aussage, `truth_status`, Grenzen und Konsequenzen bleiben in der kanonischen Information-Datei.
- Handouts verweisen über `reveals` auf die Information; sie ersetzen sie nicht.

## Globale Assets

Globale Assets wie Fraktionen und Plot-Threads besitzen `scope: global` und kein `primary_location`. Ihre `related_locations` oder spezialisierten Ortslisten drücken Relevanz aus, aber übertragen keine Ownership.

Ein globales Asset wird nicht lokal, nur weil es derzeit an einem Ort sichtbar ist. Umgekehrt wird ein lokales Asset nicht global, nur weil seine Auswirkungen weit reichen. `scope` folgt der Speicher- und Ownership-Semantik; `reach` folgt der erzählerischen Reichweite.

## Änderungsabläufe

### Temporärer Auftritt

1. Kanonische Datei unverändert lassen.
2. Zielort in `appearance_locations` ergänzen.
3. Am Zielort einen relativen Link mit lokalem Auftrittskontext ergänzen.
4. `updated` und `version` des Assets aktualisieren.

### Aktueller Ortswechsel

1. `current_location` ändern.
2. Alten aktiven Rückverweis entfernen oder als historischen Kontext kennzeichnen.
3. Neuen Ort mit relativem Link ergänzen.
4. Timeline oder Event aktualisieren, wenn der Wechsel kanonisch relevant ist.

### Dauerhafte Änderung der Ownership

1. Kanonische Datei an den neuen Katalogpfad verschieben, nicht kopieren.
2. `primary_location` ändern; ID und `created` beibehalten.
3. Alle relativen Links und betroffenen Indizes aktualisieren.
4. Alten Pfad entfernen und Änderung im Change Log dokumentieren.
5. Abenteuer validieren.
