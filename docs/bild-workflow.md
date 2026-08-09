# Bild-Workflow

Dieser Leitfaden definiert reproduzierbare Visual-Briefings und optionale PNG-Ausgaben für den einen One-Shot im Repository. Er baut keine Bildanbieter-, Rendering- oder Exportplattform auf.

## Dateimodell

Ein Visual besteht aus:

- `visual.md`: kanonisches Visual-Asset mit Subject-Beziehung, Zustandsvariante, Freigabe und Provenienz;
- `<slug>.prompt.md`: reproduzierbares Bildbriefing;
- optional `<slug>.png`: tatsächlich erzeugtes Ergebnis.

Alle Dateien liegen in `<subject-directory>/visuals/<slug>/`. Visual und Prompt entstehen mit:

```bash
python3 scripts/new_asset.py \
  --type visual \
  --subject <asset-id> \
  --slug <slug> \
  --title "<title>"
```

Der Generator erzeugt keine PNG-Datei.

## Kanonische Identitätsquelle

Die kanonische Subject-Datei bleibt die einzige Quelle für stabile visuelle Tatsachen. Bei mehreren Darstellungen desselben NPCs, Ortes, Wesens oder Objekts verweisen alle Visuals auf dieses eine Subject.

Vor einem Briefing:

1. das kanonische Subject und nur die für die Darstellung relevanten verlinkten Assets lesen;
2. die exakten Subject-Abschnitte unter `Identity source` verlinken oder benennen;
3. fehlende stabile Merkmale zuerst im Subject ergänzen und dessen Version, Datum und Change Log pflegen;
4. diese Merkmale unter `Stable identity anchors` knapp für das Briefing extrahieren, ohne eine zweite Kanonquelle zu erzeugen.

Stabile Anker sind beispielsweise Körperform, prägende Gesichtszüge, dauerhafte Zeichen, Material, Grundform, Architekturmerkmale oder wiederkehrende Symbole. Stil, Perspektive, Licht, Wetter, Pose und Bildausschnitt sind keine Identitätsmerkmale.

## Zustandsvarianten im One-Shot

`Depicted state` beschreibt genau den im Bild sichtbaren Zustand und seine kanonische Grundlage. Eine Abweichung vom Grundzustand wird nur aufgenommen, wenn sie im vorbereiteten One-Shot vorkommt, etwa Verletzung, Verfall, Verkleidung, Tageszeit oder eine durch Spielerhandlungen mögliche Veränderung.

`Allowed variation` grenzt frei veränderbare Darstellungsmittel von stabilen Ankern ab. Neue Visuals dürfen keine zukünftigen Formen, Kampagnenzustände oder Varianten für andere Abenteuer vorausplanen.

## Reproduzierbares Briefing

Das Prompt-Briefing übernimmt aus `visual.md`:

- Identitätsanker und dargestellten Zustand;
- erlaubte Variation;
- Komposition und Blickwinkel;
- Stil, Palette und Licht;
- narrative, sichtbar kanonische Details;
- Player-Sichtbarkeit und Ausschlüsse;
- Seitenverhältnis, Auflösung und relativen PNG-Pfad.

Bei einem Konflikt zwischen Subject, Visual und Prompt wird kein PNG erzeugt. Codex benennt die widersprüchlichen Aussagen und betroffenen Dateien; Kanon wird nicht stillschweigend im Prompt entschieden.

## PNG-Status

`visual.md` führt unter `Generation approval`:

```markdown
- Status: not-approved
- PNG state: not-created
- Approved visual version: none
- Approval: none
```

Zulässige Zustände:

| PNG state | Bedeutung |
|---|---|
| `not-created` | Es existiert keine PNG-Datei. |
| `current` | Die PNG-Datei entspricht der aktuell freigegebenen Visual-Version. |
| `stale` | Eine ältere PNG-Datei bleibt erhalten, entspricht aber nicht mehr der aktuellen Visual- oder Prompt-Fassung. |

Nach jeder inhaltlichen Änderung an Visual oder Prompt wird die Visual-Version erhöht. Existiert bereits ein PNG, wird es bis zur erneuten Freigabe als `stale` geführt; es wird weder gelöscht noch als aktuell ausgegeben.

## Freigabe und Erzeugung

1. Visual und Prompt vollständig ausarbeiten und gegeneinander sowie gegen das Subject prüfen.
2. Den vollständigen Prompt, den relativen Ausgabepfad und die beabsichtigte Erzeugung oder Ersetzung nennen.
3. Den User ausdrücklich um Freigabe genau dieser Visual-Version bitten. Eine frühere Freigabe, ein vorhandenes PNG oder `status: ready` gilt nicht als Zustimmung zum Ersatz.
4. Erst nach Freigabe die verfügbare Codex-Bildgenerierung auf konkreten Auftrag verwenden.
5. Nur ein tatsächlich erfolgreich gespeichertes PNG als `current` markieren. `Status` wird `approved`, `Approved visual version` entspricht der aktuellen `version`, und `Approval` dokumentiert die konkrete Zustimmung.
6. `provenance` und `Provenance and revisions` an die tatsächliche Herkunft und Änderung anpassen.
7. `python3 scripts/validate_adventure.py` ausführen und Ergebnis sowie geänderte Dateien berichten.

Wird die Bildgenerierung abgebrochen oder liefert sie keine gespeicherte PNG-Datei, bleibt der Zustand `not-created` beziehungsweise `stale`. Codex behauptet nicht, dass ein Bild vorhanden oder ersetzt ist.

## Karten und Handouts

Präzise Karten, Diagramme oder textreiche Handouts werden nicht als freie Illustration entworfen. Struktur und Text entstehen zuerst in Markdown. Eine Handout-Bildfassung ist ein reguläres Visual mit dem Handout als Subject und liegt unter dessen `visuals/<slug>/`; eine PNG direkt neben `handout.md` ist unzulässig. `Identity source` verweist auf die freigegebene `player.md`. Zusätzlich gilt deren Freigabe- und Safety-Workflow aus [Spielerfreigabe für Handouts](player-handout-workflow.md).

## Definition of Done

- Subject und exakte Identitätsquelle sind eindeutig;
- stabile Anker, dargestellter One-Shot-Zustand und freie Variation sind getrennt;
- Visual und Prompt stimmen in Inhalt, Ausschlüssen und relativem Ausgabepfad überein;
- ein vorhandenes PNG besitzt den korrekten Status, eine passende Freigabe und nachvollziehbare Provenienz;
- Konflikte wurden vor einer Erzeugung geklärt;
- keine externe Plattform oder Planung für weitere Abenteuer wurde ergänzt.
