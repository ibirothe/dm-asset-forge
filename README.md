# DM Asset Forge

Ein regelneutrales Codex-Template zum strukturierten Erstellen und Pflegen eines abgeschlossenen Pen-&-Paper-One-Shots. Inhalte werden als Markdown geführt, visuelle Ergebnisse als PNG. Ortsgebundene Figuren, Objekte, Hinweise, Begegnungen und Handouts liegen direkt am zugehörigen Ort.

## Schnellstart

1. Repository klonen und Codex im Repository-Stamm starten.
2. Codex mit einer groben Beschreibung von Welt und Plot beauftragen, zum Beispiel:

   > Erstelle einen neuen One-Shot namens „Nebel über Arken“. Die Welt besteht aus ... Der grobe Plot ist ...

3. Codex legt das einzige Abenteuer dieses Repositories unter `adventure/` an, strukturiert den Ausgangstext und nennt offene Entscheidungen.
4. Danach Orte oder einzelne Assets gezielt ausarbeiten lassen.
5. Vor dem Spielen eine Konsistenzprüfung des vollständigen One-Shots anfordern.

Die vollständige Anleitung steht in [docs/benutzerhandbuch.md](docs/benutzerhandbuch.md).
Der verbindliche v1-Typenkatalog steht in [docs/asset-katalog.md](docs/asset-katalog.md).
Die fachlichen Mindestinhalte und Definition of Done jedes Typs stehen in [docs/asset-authoring-guide.md](docs/asset-authoring-guide.md).
Der zustandsbasierte Abenteueraufbau mit echten Entscheidungen und robusten Informationswegen steht in [docs/adventure-structure-guide.md](docs/adventure-structure-guide.md).
Die getrennte fachliche Prüfung von Kontinuität, Informationswegen und Spielerwirksamkeit steht in [docs/adventure-audit-guide.md](docs/adventure-audit-guide.md).
Das gemeinsame Metadatenschema und alle regelneutralen Werteskalen stehen in [docs/metadaten-und-werte.md](docs/metadaten-und-werte.md).
Das verbindliche Ownership- und Beziehungsmodell steht in [docs/beziehungen-und-speicherorte.md](docs/beziehungen-und-speicherorte.md).
Der geführte Erstlauf von freiem Welt- und Plottext zum strukturierten Abenteuer steht in [docs/intake-workflow.md](docs/intake-workflow.md).
Regeln, Fehlercodes und Grenzen der technischen Prüfung stehen in [docs/validierung.md](docs/validierung.md).

## Grundprinzipien

- vollständig regelneutral; keine systemgebundenen Werte oder Begriffe
- ausschließlich ein in sich abgeschlossener One-Shot pro Repository
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

- `dm-create-adventure`: initialisiert einen One-Shot aus Welt- und Plotbeschreibung
- `dm-develop-location`: entwickelt einen Ort samt lokal gruppierter Assets
- `dm-create-asset`: erzeugt oder überarbeitet ein einzelnes DM-Asset
- `dm-audit-adventure`: prüft Struktur, Links und erzählerische Konsistenz

## Lokale Werkzeuge

```bash
python3 scripts/init_adventure.py --slug nebel-ueber-arken --title "Nebel über Arken"
python3 scripts/new_asset.py --type world --slug nebel-ueber-arken --title "Nebel über Arken" --overwrite
python3 scripts/new_asset.py --type location --slug hafenviertel --title "Hafenviertel"
python3 scripts/new_asset.py --type npc --location hafenviertel --slug mara-veen --title "Mara Veen"
python3 scripts/new_asset.py --type visual --subject npc-mara-veen --slug portrait --title "Porträt von Mara Veen"
python3 scripts/validate_adventure.py
python3 -m unittest discover -s tests -v
```

`new_asset.py` unterstützt alle 14 Typen des Asset-Katalogs. `python3 scripts/new_asset.py --help` zeigt typspezifische Optionen und Beispiele. Es überschreibt keine bestehende Datei ohne `--overwrite` und pflegt Indizes oder Rückverweise nicht automatisch.

Die Skripte verwenden ausschließlich die Python-Standardbibliothek.

Jede aus diesem Template erzeugte Arbeitskopie enthält genau einen abgeschlossenen One-Shot. Eine zweite Initialisierung wird abgelehnt; für einen weiteren One-Shot wird ein neues Repository aus dem Template erzeugt.
