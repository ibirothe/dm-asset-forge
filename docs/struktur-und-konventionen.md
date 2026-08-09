# Struktur und Konventionen

## Abenteuerverzeichnis

```text
adventures/<adventure-slug>/
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

## Benennung

- Ordner, Dateien, IDs und YAML-Schlüssel: englisch
- Erläuternder Inhalt und Nutzeranleitungen: deutsch
- Slugs: ASCII, kleingeschrieben, mit Bindestrichen
- IDs: stabiler Präfix plus Slug, beispielsweise `loc-old-harbor` oder `npc-mara-veen`
- Bilder: PNG; Briefing: gleicher Basisname plus `.prompt.md`

## Asset-Typen

| Typ | Präfix | Kanonischer Speicherort |
|---|---:|---|
| location | `loc-` | `30-locations/<location>/location.md` |
| npc | `npc-` | `<location>/npcs/<npc>/npc.md` |
| object | `obj-` | `<location>/objects/<object>/object.md` |
| information | `info-` | `<location>/information/<information>/information.md` |
| encounter | `enc-` | `<location>/encounters/<encounter>/encounter.md` |
| handout | `hand-` | `<location>/handouts/<handout>/handout.md` |
| faction | `fac-` | `40-global/factions/<faction>/faction.md` |
| plot-thread | `plot-` | `20-plot/threads/<thread>/plot-thread.md` |

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
