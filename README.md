# DM Asset Forge

Ein regelneutrales Codex-Template zum strukturierten Erstellen und Pflegen von Pen-&-Paper-Abenteuern. Inhalte werden als Markdown geführt, visuelle Ergebnisse als PNG. Ortsgebundene Figuren, Objekte, Hinweise, Begegnungen und Handouts liegen direkt am zugehörigen Ort.

## Schnellstart

1. Repository klonen und Codex im Repository-Stamm starten.
2. Codex mit einer groben Beschreibung von Welt und Plot beauftragen, zum Beispiel:

   > Erstelle ein neues Abenteuer namens „Nebel über Arken“. Die Welt besteht aus ... Der grobe Plot ist ...

3. Codex legt das einzige Abenteuer dieses Repositories unter `adventure/` an, strukturiert den Ausgangstext und nennt offene Entscheidungen.
4. Danach Orte oder einzelne Assets gezielt ausarbeiten lassen.
5. Vor einer Spielrunde eine Konsistenzprüfung anfordern.

Die vollständige Anleitung steht in [docs/benutzerhandbuch.md](docs/benutzerhandbuch.md).

## Grundprinzipien

- vollständig regelneutral; keine systemgebundenen Werte oder Begriffe
- englische technische Bezeichner und Dateinamen, deutsche Benutzeranleitungen
- ein kanonischer Speicherort pro Information oder Asset
- lokale Inhalte werden unter ihrem primären Ort gruppiert
- Querverweise statt inhaltlicher Duplikate
- kleine, nachvollziehbare Änderungen an vorhandenen Dateien
- Bildbriefing neben jedem erzeugten PNG

## Repository-Struktur

```text
.agents/skills/       Repository-lokale Codex-Skills
adventure/            Von Codex erzeugtes Abenteuer; entsteht bei Initialisierung
docs/                 Deutsche Benutzer- und Strukturhinweise
scripts/              Initialisierung und Validierung
templates/adventure/  Grundgerüst eines Abenteuers
templates/assets/     Einheitliche Asset-Schemata
```

## Enthaltene Skills

- `dm-create-adventure`: initialisiert ein Abenteuer aus Welt- und Plotbeschreibung
- `dm-develop-location`: entwickelt einen Ort samt lokal gruppierter Assets
- `dm-create-asset`: erzeugt oder überarbeitet ein einzelnes DM-Asset
- `dm-audit-adventure`: prüft Struktur, Links und erzählerische Konsistenz

## Lokale Werkzeuge

```bash
python3 scripts/init_adventure.py --slug nebel-ueber-arken --title "Nebel über Arken"
python3 scripts/new_asset.py --type location --slug hafenviertel --title "Hafenviertel"
python3 scripts/validate_adventure.py
```

Die Skripte verwenden ausschließlich die Python-Standardbibliothek.

Jede aus diesem Template erzeugte Arbeitskopie enthält genau ein Abenteuer. Eine zweite Initialisierung wird abgelehnt; für ein weiteres Abenteuer wird ein neues Repository aus dem Template erzeugt.
