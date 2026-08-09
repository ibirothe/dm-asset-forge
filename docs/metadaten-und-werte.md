# Gemeinsame Metadaten und regelneutrale Werte v1

Diese Datei ist die normative Quelle für gemeinsame YAML-Schlüssel, kontrollierte Werte und den Umgang mit fehlenden Angaben. Der [DM-Asset-Katalog](asset-katalog.md) definiert Typen, ID-Präfixe und Speicherorte; diese Datei definiert die Metadaten dieser Typen.

## Gemeinsames Metadatenschema

Jedes Asset führt die folgenden Pflichtfelder. Das Abenteuer-Manifest in `adventure/README.md` verwendet dasselbe Schema mit `type: adventure`.

| Key | Format | Bedeutung |
|---|---|---|
| `id` | nicht leerer String | Stabile ID mit dem Präfix aus dem Asset-Katalog; nach der Erstellung nicht ändern. |
| `type` | kontrollierter String | Einer der 14 Katalogtypen; beim Abenteuer-Manifest `adventure`; beim vorläufigen Bildbrief `image-brief`. |
| `title` | nicht leerer String | Anzeigename; darf geändert werden, ohne die ID zu ändern. |
| `status` | kontrollierter String | Bearbeitungsstand gemäß Statuswerten unten. |
| `version` | positive Ganzzahl | Inhaltsversion des Assets; beginnt bei `1` und steigt bei einer inhaltlich relevanten Überarbeitung. |
| `tags` | Liste von Strings | Sachliche Suchbegriffe in englischem `kebab-case`; `[]`, wenn noch keine vergeben sind. |
| `themes` | Liste von Strings | Inhaltliche Themen in englischem `kebab-case`; `[]`, wenn noch keine vergeben sind. |
| `created` | `YYYY-MM-DD` | Datum der erstmaligen Anlage; bleibt unverändert. |
| `updated` | `YYYY-MM-DD` | Datum der letzten inhaltlichen Änderung. |

Gemeinsame optionale Schlüssel:

| Key | Format | Bedeutung |
|---|---|---|
| `aliases` | Liste von Strings | Weitere Namen, unter denen das Asset in der Spielwelt bekannt ist. |
| `provenance` | kontrollierter String | Herkunft der kanonischen Inhalte gemäß Provenienzwerten unten. |
| `source_refs` | Liste relativer Links oder kurzer Bezeichner | Nachvollziehbare Quellen innerhalb des Repositories oder vom User benannte Referenzen. |

YAML-Schlüssel und kontrollierte Werte sind englisch. Freitextinhalte und Benutzeranleitungen sind deutsch.

## Kontrollierte Werte

### `status`

| Value | Bedeutung |
|---|---|
| `draft` | Angelegt oder in Bearbeitung; noch nicht vollständig spielbereit. |
| `ready` | Inhaltlich ausgearbeitet, konsistent verlinkt und am Spieltisch einsetzbar. |
| `retired` | Nicht mehr aktiv, bleibt aber für Kontinuität und Verweise erhalten. |

### `truth_status`

Nur für Aussagen, Informationen und andere Assets, bei denen ein Wahrheitsstatus erforderlich ist.

| Value | Bedeutung |
|---|---|
| `established` | Im Abenteuerkanon als wahr festgelegt. |
| `partial` | Enthält wahre Bestandteile, ist aber unvollständig oder irreführend verkürzt. |
| `false` | Im Abenteuerkanon als falsch festgelegt. |
| `contested` | Mehrere unvereinbare Behauptungen bestehen; der Widerspruch ist selbst kanonisch. |
| `unknown` | Ob die Aussage wahr ist, wurde noch nicht festgelegt. |

`contested` bedeutet nicht, dass der Autor eine Entscheidung vergessen hat. Eine tatsächlich offene Autorenentscheidung wird in `adventure/90-meta/open-questions.md` geführt.

### `provenance`

| Value | Bedeutung |
|---|---|
| `user-authored` | Der User hat den kanonischen Inhalt direkt vorgegeben. |
| `agent-inferred` | Der Agent hat den Inhalt nachvollziehbar aus vorhandenen Fakten abgeleitet. |
| `agent-generated` | Der Agent hat den Inhalt als neue Ausgestaltung erzeugt. |
| `imported` | Der Inhalt stammt aus einer ausdrücklich benannten externen Quelle. |
| `mixed` | Mehrere der genannten Ursprünge tragen wesentlich zum Inhalt bei. |
| `unknown` | Die Herkunft wurde noch nicht nachvollziehbar erfasst. |

Provenienz beschreibt Herkunft, nicht Wahrheit. Externe Quellen werden nur als Referenz genannt; längere geschützte Inhalte werden nicht kopiert.

## Regelneutrale qualitative Skalen

Die Werte beschreiben erzählerische Bedeutung, nicht Würfel, Zielzahlen, Stufen oder andere Regelmechanik. `unknown` ist bei jeder Skala zulässig und bedeutet, dass die Skala anwendbar, der Wert aber noch nicht bekannt ist.

### `danger`

| Value | Bedeutung |
|---|---|
| `none` | Verursacht unter normalen Umständen keinen relevanten Schaden oder Verlust. |
| `limited` | Folgen bleiben gewöhnlich lokal, kurzfristig oder leicht umkehrbar. |
| `significant` | Kann wichtige Ziele, Personen oder Ressourcen ernsthaft beeinträchtigen. |
| `severe` | Kann dauerhafte Verluste oder weitreichende Schäden verursachen. |
| `existential` | Bedroht den Fortbestand einer Gemeinschaft, Region, Welt oder zentralen Realität. |
| `unknown` | Gefahr ist relevant, aber noch nicht zuverlässig einzuschätzen. |

### `influence`

| Value | Bedeutung |
|---|---|
| `none` | Kann Entscheidungen anderer nicht nennenswert verändern. |
| `limited` | Wirkt auf wenige Personen oder nur unter günstigen Bedingungen. |
| `notable` | Kann regelmäßig relevante Entscheidungen oder Ressourcen beeinflussen. |
| `strong` | Prägt Entscheidungen und Entwicklungen auch gegen Widerstand. |
| `dominant` | Bestimmt den betrachteten Kontext weitgehend und kann Alternativen verdrängen. |
| `unknown` | Einfluss ist anwendbar, aber noch nicht zuverlässig bekannt. |

### `reach`

| Value | Bedeutung |
|---|---|
| `personal` | Betrifft eine Person oder einen sehr kleinen unmittelbaren Kreis. |
| `local` | Betrifft einen Ort oder eine eng verbundene Gemeinschaft. |
| `regional` | Betrifft mehrere Orte oder eine klar abgegrenzte Region. |
| `widespread` | Betrifft große Teile der bekannten Welt oder mehrere Regionen. |
| `world-spanning` | Kann die gesamte Spielwelt oder ihre grundlegende Ordnung betreffen. |
| `unknown` | Reichweite ist anwendbar, aber noch nicht absehbar. |

### `rarity`

| Value | Bedeutung |
|---|---|
| `common` | Im passenden Kontext regelmäßig anzutreffen oder zu beschaffen. |
| `uncommon` | Nicht alltäglich, aber mit vertretbarem Aufwand auffindbar. |
| `rare` | Nur an wenigen Orten, bei wenigen Akteuren oder unter besonderen Umständen vorhanden. |
| `unique` | Im Abenteuerkanon existiert genau ein Exemplar oder Vorkommen. |
| `unknown` | Seltenheit ist anwendbar, aber noch nicht bekannt. |

### `accessibility`

| Value | Bedeutung |
|---|---|
| `open` | Ohne besondere Voraussetzung zugänglich. |
| `limited` | Mit gewöhnlichem Aufwand, Zeit oder einer naheliegenden Voraussetzung zugänglich. |
| `restricted` | Erfordert Erlaubnis, besondere Beziehungen, Ressourcen oder gezielte Vorbereitung. |
| `hidden` | Der Zugang oder das Vorhandensein muss zunächst entdeckt werden. |
| `sealed` | Bewusst verschlossen; Öffnung erfordert eine außergewöhnliche Veränderung der Situation. |
| `unknown` | Zugänglichkeit ist relevant, aber noch nicht bekannt. |

### `confidence`

Die Skala bewertet die Absicherung einer Information, nicht ihren `truth_status`.

| Value | Bedeutung |
|---|---|
| `unverified` | Behauptung ohne belastbare Stütze. |
| `weak` | Einzelne oder indirekte Anhaltspunkte stützen die Behauptung. |
| `supported` | Mindestens eine belastbare Quelle oder klare Indizien stützen sie. |
| `corroborated` | Mehrere voneinander unabhängige Quellen oder Indizien stimmen überein. |
| `confirmed` | Im betrachteten Kontext direkt und zuverlässig belegt. |
| `unknown` | Informationssicherheit ist relevant, aber noch nicht bewertet. |

## Zulässige typspezifische Schlüssel

Templates dürfen neben den gemeinsamen Schlüsseln nur die hier für ihren Typ aufgeführten Schlüssel verwenden. Ein Schlüssel wird nur aufgenommen, wenn er für das konkrete Asset sinnvoll ist.

| Type | Zusätzliche Keys |
|---|---|
| `location` | `parent_location`, `function`, `danger`, `accessibility` |
| `npc` | `primary_location`, `factions`, `influence`, `reach` |
| `object` | `primary_location`, `owner`, `danger`, `rarity`, `accessibility` |
| `information` | `truth_status`, `confidence`, `accessibility`, `primary_location`, `known_by`, `related_threads` |
| `encounter` | `primary_location`, `participants`, `related_threads`, `danger` |
| `handout` | `primary_location`, `reveals`, `accessibility` |
| `faction` | `scope`, `locations`, `influence`, `reach` |
| `plot-thread` | `entry_locations`, `related_factions`, `danger`, `reach` |
| `image-brief` | `subject_asset`, `output_file` |

`image-brief` bleibt bis zur vollständigen Implementierung des Katalogtyps `visual` ein vorläufiger technischer Dokumenttyp. Er darf nicht anstelle eines anderen Assets verwendet werden.

## Fehlende, leere und offene Angaben

| Darstellung | Verwenden, wenn … | Beispiel |
|---|---|---|
| `unknown` | ein skalares Feld anwendbar ist, sein Wert aber noch nicht bekannt ist | `danger: unknown` |
| `null` | ein skalares oder einzelnes Beziehungsfeld bewusst nicht anwendbar ist oder kein Ziel besitzt | `parent_location: null` |
| `[]` | ein Listenfeld anwendbar ist, aktuell aber keine Einträge besitzt | `factions: []` |
| Schlüssel fehlt | der Schlüssel für diesen Typ optional und für das konkrete Asset nicht sinnvoll ist | kein `rarity` bei einem NPC |
| Eintrag in `open-questions.md` | eine Autoren- oder Userentscheidung noch aussteht | „Ist die Maske einzigartig?“ |

Leere Strings wie `""` sind nicht zulässig. Ein offener Entscheid darf weder als leere Zeichenkette noch als `null` verborgen werden. Bis zur Klärung erhält ein anwendbares skalares Feld `unknown`; die eigentliche Frage steht zusätzlich in `adventure/90-meta/open-questions.md`.

## Pflege

- Bei jeder inhaltlich relevanten Änderung `updated` aktualisieren und `version` um eins erhöhen.
- `created` und `id` nicht ändern.
- Nach einer Umbenennung nur `title`, Links und gegebenenfalls `aliases` anpassen.
- Neue Schlüssel oder Werte zuerst in dieser Datei definieren, danach Templates und Skills angleichen.
- Regelmechanische Zahlen, Würfelnotationen, Schwierigkeitsklassen und systemspezifische Zustände nicht in qualitative Skalen übertragen.
