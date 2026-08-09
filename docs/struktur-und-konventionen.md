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

## Frontmatter

Jedes Asset beginnt mit YAML-Frontmatter. Die gemeinsamen Pflichtfelder sind `id`, `type`, `title`, `status`, `tags`, `themes`, `created` und `updated`. Typspezifische Felder stehen in den Dateien unter `templates/assets/`.

Erlaubte Statuswerte:

- `draft`: angelegt, aber noch nicht spielbereit
- `ready`: spielbereit und konsistent verknüpft
- `retired`: nicht mehr aktiv, bleibt aber aus Kontinuitätsgründen erhalten

## Verknüpfungen

Relative Markdown-Links bilden Beziehungen ab. Freitext darf einen anderen Asset-Titel erwähnen, ersetzt aber nicht den Link in den dafür vorgesehenen Abschnitten. Inhalte werden nicht an mehreren Stellen kopiert.

## Regelneutralität

Werte beschreiben erzählerische Funktion statt Regelmechanik. Geeignete Angaben sind etwa:

- Absicht und Motivation
- Einfluss und Reichweite
- Ressourcen und Druckmittel
- Risiken und mögliche Konsequenzen
- Voraussetzungen für Entdeckung oder Zugang
- erkennbare Schwächen und Ansatzpunkte

Nicht geeignet sind systemspezifische Zahlenwerte, Würfelproben, Schwierigkeitsklassen oder fest benannte Regelzustände.
