# Bild-Workflow

## Dateipaar

Ein visuelles Asset besteht aus:

- `<name>.prompt.md`: reproduzierbares Bildbriefing
- `<name>.png`: tatsächlich erzeugtes Ergebnis

Das Briefing entsteht zuerst. Die PNG-Datei wird nur bei einer ausdrücklichen Bildanforderung erzeugt oder ersetzt.

## Inhalt des Briefings

Das Template `templates/assets/image-brief.md` führt:

- Zweck und Motiv
- Komposition und Blickwinkel
- sichtbare Merkmale und erzählerische Hinweise
- Stil, Farbwelt und Licht
- auszuschließende Elemente
- gewünschte Auflösung beziehungsweise Seitenrelation
- Ausgabepfad
- Provenienz und Änderungsnotizen

## Konsistenz

Wiederkehrende Figuren und Orte verweisen auf ihre kanonischen Beschreibungen. Das Briefing nennt stabile Erkennungsmerkmale ausdrücklich. Neue visuelle Details dürfen bestehenden Fakten nicht widersprechen.

## Karten und Handouts

Präzise Karten, Diagramme oder textreiche Handouts sollten nicht als freie Illustration erzeugt werden. Dafür wird zuerst eine strukturierte Vorlage in Markdown erstellt; ein PNG kann anschließend als Ausgabe oder Vorschau ergänzt werden.
