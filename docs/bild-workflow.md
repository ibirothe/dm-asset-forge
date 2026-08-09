# Bild-Workflow

## Asset-Dateien

Ein visuelles Asset besteht aus:

- `visual.md`: kanonische Metadaten, sichtbare Fakten und Subject-Beziehung
- `<name>.prompt.md`: reproduzierbares Bildbriefing
- optional `<name>.png`: tatsächlich erzeugtes Ergebnis

Das Visual und sein Briefing entstehen zuerst. Die PNG-Datei wird nur bei einer ausdrücklichen Bildanforderung erzeugt oder ersetzt. Alle drei Dateien liegen in `<subject-directory>/visuals/<name>/`.

```bash
python3 scripts/new_asset.py \
  --type visual \
  --subject <asset-id> \
  --slug <name> \
  --title "<title>"
```

## Inhalt des Briefings

Die Templates `templates/assets/visual.md` und `templates/visual-prompt.md` führen:

- Zweck und Motiv
- Komposition und Blickwinkel
- sichtbare Merkmale und erzählerische Hinweise
- Stil, Farbwelt und Licht
- auszuschließende Elemente
- gewünschte Auflösung beziehungsweise Seitenrelation
- Ausgabepfad
- Provenienz und Änderungsnotizen im kanonischen Visual

## Konsistenz

Wiederkehrende Figuren und Orte verweisen auf ihre kanonischen Beschreibungen. Das Briefing nennt stabile Erkennungsmerkmale ausdrücklich. Neue visuelle Details dürfen bestehenden Fakten nicht widersprechen.

## Karten und Handouts

Präzise Karten, Diagramme oder textreiche Handouts sollten nicht als freie Illustration erzeugt werden. Dafür wird zuerst eine strukturierte Vorlage in Markdown erstellt; ein PNG kann anschließend als Ausgabe oder Vorschau ergänzt werden.
