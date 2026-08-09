# Struktur und Konventionen

## Abenteuerverzeichnis

```text
adventure/
├── README.md
├── 00-input/
│   ├── world.md
│   ├── plot.md
│   └── constraints.md
├── 10-world/
│   ├── overview.md
│   ├── themes.md
│   └── timeline.md
├── 20-plot/
│   ├── overview.md
│   └── threads/<thread>/plot-thread.md
├── 30-locations/<location>/
│   ├── location.md
│   ├── npcs/<npc>/npc.md
│   ├── objects/<object>/object.md
│   ├── information/<information>/information.md
│   ├── encounters/<encounter>/encounter.md
│   ├── handouts/<handout>/handout.md
│   └── images/
├── 40-global/factions/<faction>/faction.md
├── 50-indexes/
└── 90-meta/
```

Das Verzeichnis `adventure/` entsteht bei der einmaligen Initialisierung. Titel und Slug werden als stabile Metadaten im Abenteuer-Frontmatter geführt, nicht als zusätzliche Verzeichnisebene.

## Benennung

- Ordner, Dateien, IDs und YAML-Schlüssel: englisch
- Erläuternder Inhalt und Nutzeranleitungen: deutsch
- Slugs: ASCII, kleingeschrieben, mit Bindestrichen
- IDs: stabiler Präfix plus Slug, beispielsweise `loc-old-harbor` oder `npc-mara-veen`
- Bilder: PNG; Briefing: gleicher Basisname plus `.prompt.md`

## Asset-Typen

Der [kanonische DM-Asset-Katalog v1](asset-katalog.md) ist die verbindliche Quelle für alle 14 Typen, Präfixe, Geltungsbereiche, Speicherorte, Pflichtbeziehungen und Auswahlregeln. Diese Datei wiederholt die Typentabelle bewusst nicht, damit keine zweite Quelle abweichende Definitionen entwickelt.

Kurzregel:

- lokale Assets besitzen genau einen primären Ort;
- globale Assets werden nicht in einem Ortsordner dupliziert;
- Visuals liegen bei ihrem kanonischen Subject-Asset;
- weitere Vorkommen werden ausschließlich verlinkt.

Die vollständigen Regeln für primären, aktuellen und ursprünglichen Ort, Auftritte, Rückverweise und dauerhafte Umzüge stehen in [Beziehungen und ortszentrierte Speicherung v1](beziehungen-und-speicherorte.md).

## Frontmatter

Jedes Asset beginnt mit YAML-Frontmatter. [Gemeinsame Metadaten und regelneutrale Werte v1](metadaten-und-werte.md) ist die verbindliche Quelle für Pflichtfelder, zulässige typspezifische Schlüssel, kontrollierte Werte und die Unterscheidung zwischen `unknown`, `null`, `[]` und offenen Entscheidungen. Die Dateien unter `templates/assets/` setzen dieses Schema um.

## Verknüpfungen

Strukturierte Metadaten führen Beziehungen über stabile IDs; relative Markdown-Links machen sie navigierbar. Freitext darf einen anderen Asset-Titel erwähnen, ersetzt aber nicht den Link in den dafür vorgesehenen Abschnitten. Inhalte werden nicht an mehreren Stellen kopiert. Richtung und erforderliche Rückverweise folgen dem [Beziehungsmodell](beziehungen-und-speicherorte.md).

## Regelneutralität

Werte beschreiben erzählerische Funktion statt Regelmechanik. Geeignete Angaben sind etwa:

- Absicht und Motivation
- Einfluss und Reichweite
- Ressourcen und Druckmittel
- Risiken und mögliche Konsequenzen
- Voraussetzungen für Entdeckung oder Zugang
- erkennbare Schwächen und Ansatzpunkte

Nicht geeignet sind systemspezifische Zahlenwerte, Würfelproben, Schwierigkeitsklassen oder fest benannte Regelzustände.
