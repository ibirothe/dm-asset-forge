# Spielerfreigabe für Handouts

Dieser Leitfaden definiert die sichere Markdown-Ausgabe eines Handouts für Spieler. Er gilt ausschließlich für den einen One-Shot im Repository und erzeugt weder einen allgemeinen Exportbestand noch ein Rendering-System.

## Dateimodell

- `handout.md` bleibt die einzige kanonische DM-Datei. Sie enthält Frontmatter, Auslieferungskontext, offenbarte Informationen und DM-only Wissen.
- `player.md` ist eine optionale, abgeleitete Spielerdatei im selben Handout-Ordner.
- `player.md` enthält kein YAML-Frontmatter, keine Arbeitsnotizen und keine Repository-Navigation.
- Eine optionale PNG-Fassung wird als reguläres Visual des Handouts geführt. Sie darf erst aus der freigegebenen `player.md` entstehen; Markdown bleibt die maßgebliche Spielerfassung.
- Player-Dateien werden nicht außerhalb des zugehörigen Handout-Ordners gesammelt oder für andere Abenteuer wiederverwendet.

Beispiel:

```text
adventure/30-locations/old-harbor/handouts/harbor-letter/
├── handout.md
├── player.md                    (optional, ausdrücklich freigegeben)
└── visuals/player/              (optionale Bildfassung)
    ├── visual.md
    ├── player.prompt.md
    └── player.png
```

## Freigabestatus in der Quelle

Jedes `handout.md` führt den Abschnitt `## Player release` mit genau diesen Angaben:

```markdown
## Player release

- Status: not-approved
- Player file: none
- Approved source version: none
- Approval: none
```

Nach einer ausdrücklichen Freigabe werden `Status: approved`, ein relativer Link auf `player.md`, die aktuelle `version` des Handouts und ein kurzer Freigabevermerk eingetragen. Der Vermerk dokumentiert die Freigabe, ersetzt aber keine erneute Zustimmung für einen späteren Ersatz.

Jede inhaltliche Änderung an `handout.md` erhöht dessen `version`. Eine vorhandene Freigabe gilt dadurch nicht mehr für die neue Quellversion; vor dem Ersetzen von `player.md` ist erneut die ausdrückliche Zustimmung des Users erforderlich.

## Freigabeworkflow

1. `handout.md` und alle über `reveals` referenzierten Information-Assets lesen. Nur direkt betroffene Kanonquellen ergänzend öffnen.
2. Einen vollständigen Entwurf für `player.md` vorlegen, ohne die Datei anzulegen oder eine vorhandene Datei zu ersetzen.
3. Den Safety-Check durchführen und jedes Problem vor der Freigabe korrigieren. Erkannte Leaks blockieren die Ausgabe.
4. Den User ausdrücklich um Freigabe genau dieses Entwurfs bitten. Schweigen, eine frühere Freigabe oder `status: ready` gelten nicht als Zustimmung.
5. Erst nach Zustimmung die aktuelle Handout-Version, `Player release` und den Change Log aktualisieren. Danach `player.md` aus `templates/player-handout.md` schreiben.
6. `python3 scripts/validate_adventure.py` ausführen. Fehler blockieren den Abschluss.
7. Geänderte Dateien, freigegebene Quellversion und Validierung berichten.

Existiert `player.md` bereits, gilt derselbe Ablauf. Codex zeigt den vollständigen Ersatzentwurf oder eine eindeutige Änderungsvorschau und überschreibt die Datei erst nach neuer ausdrücklicher Freigabe.

## Safety-Check

Vor jeder Erstellung oder Ersetzung müssen alle Punkte erfüllt sein:

- Der Text stammt ausschließlich aus `Player-facing content` und bewusst offenbarten Aussagen der über `reveals` verknüpften Information-Assets.
- Gerüchte, Teilwahrheiten und falsche Aussagen werden nicht versehentlich als bestätigte Wahrheit umformuliert.
- Der Text enthält keine Inhalte aus `DM-only context`, keine verdeckten Ursachen, unentdeckten Konsequenzen, Lösungswege oder zukünftigen Ereignisse.
- YAML-Frontmatter, Asset-IDs, interne Statuswerte, Arbeitsnotizen, Kommentare und Repository-Pfade fehlen vollständig.
- Relative Links zu internen Dateien und Überschriften wie `DM-only context`, `Delivery`, `Reveals and consequences`, `Rendered output` oder `Player release` fehlen.
- Der Text besitzt eine verständliche Überschrift und erklärt sich ohne Repository-Kontext selbst.
- Die Ausgabe verrät nur Informationen, die das Handout in der vorgesehenen Auslieferungssituation tatsächlich vermittelt.

Kann ein möglicher Spoiler nicht sicher bewertet werden, bleibt die Ausgabe blockiert und die konkrete Frage wird dem User vorgelegt.

## Optionale PNG-Ausgabe

Eine PNG-Ausgabe ist keine Voraussetzung für ein nutzbares Handout. Nach Freigabe von `player.md` darf Codex auf ausdrücklichen Wunsch ein Visual mit dem Handout als Subject anlegen:

```bash
python3 scripts/new_asset.py \
  --type visual \
  --subject <handout-id> \
  --slug player \
  --title "<title> – Spielerfassung"
```

Die Bildfassung liegt ausschließlich unter `visuals/player/`; eine direkte `player.png` neben `handout.md` ist unzulässig. `visual.md` nennt die freigegebene `player.md` als konkrete Identitäts- und Inhaltsquelle. Das Prompt-Briefing darf nur deren player-facing Aussagen übernehmen. Inhaltliche Aussagen dürfen sich nicht ändern; Layout, Schrift, Symbole und Illustration müssen den Handout-Safety-Check und den vollständigen [Bild-Workflow](bild-workflow.md) bestehen.

## Definition of Done

- `player.md` ist ausdrücklich für die aktuelle Handout-Version freigegeben;
- die Quelle verlinkt die Spielerdatei und dokumentiert Freigabe sowie Quellversion;
- die Spielerdatei ist ohne Repository-Kontext verständlich;
- Safety-Check und technische Validierung sind ohne blockierenden Befund abgeschlossen;
- keine allgemeine Exportstruktur wurde erzeugt.
