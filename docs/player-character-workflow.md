# Spielerfreigabe für Player Characters

Dieser Leitfaden definiert die regelneutrale Vorbereitung und sichere Markdown-Ausgabe eines optionalen Player Characters für genau einen One-Shot. Er erzeugt weder ein Regelsystem-Charakterblatt noch Material für spätere Sessions.

## Dateimodell

- `player-character.md` ist die einzige kanonische DM-Datei. Sie enthält Frontmatter, interne Beziehungen, freigegebenes Startwissen und mögliche verdeckte One-Shot-Verknüpfungen.
- `player.md` ist eine optionale, abgeleitete Spielerdatei im selben Character-Ordner.
- `player.md` enthält kein YAML-Frontmatter, keine internen Links, keine Arbeitsnotizen und keine DM-only Inhalte.
- Die Vorlage für die Spielerfassung liegt in `templates/player-character-player.md`; sie wird erst nach ausdrücklicher Freigabe geschrieben.
- Ein Portrait oder anderes Character-Bild wird als reguläres Subject-owned `visual` unterhalb des Player Characters geführt.

Beispiel:

```text
adventure/40-global/player-characters/ira-veen/
├── player-character.md
├── player.md                    (optional, ausdrücklich freigegeben)
└── visuals/portrait/            (optional)
    ├── visual.md
    ├── portrait.prompt.md
    └── portrait.png
```

## Fachliche Grenzen

Ein Player Character beschreibt eine spielbare Ausgangslage, keine vorgeschriebene Darstellung. Ohne ausdrückliche User-Vorgabe bleiben Herkunft, Motivation, Moral, Loyalität, Beziehungen und Entscheidungen offen oder werden als wählbare Angebote formuliert.

Regelneutrale Stärken und Grenzen beschreiben Erfahrungen, erkennbare Fähigkeiten, Ressourcen, Risiken und geeignete Herangehensweisen in Prosa. Trefferpunkte, Klassen, Stufen, Würfelwerte, Schwierigkeitsklassen und andere systemspezifische Mechaniken sind unzulässig.

Persönliche Hooks verbinden die Figur mit dem One-Shot, ohne eine Reaktion zu erzwingen. Jeder Hook nennt eine wahrnehmbare Gelegenheit, Beziehung, Verpflichtung oder Frage und lässt mehrere Haltungen oder Vorgehensweisen zu. Notwendiger Plotfortschritt darf nicht von der Motivation genau dieses Characters abhängen.

## Freigabestatus in der Quelle

Jedes `player-character.md` führt den Abschnitt `## Player release` mit genau diesen Angaben:

```markdown
## Player release

- Status: not-approved
- Player file: none
- Approved source version: none
- Approval: none
```

Nach ausdrücklicher Freigabe werden `Status: approved`, ein relativer Link auf `player.md`, die aktuelle `version` und ein konkreter Freigabevermerk eingetragen. Jede inhaltliche Änderung der kanonischen Quelle erhöht ihre Version und macht vor einem Ersatz von `player.md` eine neue Freigabe erforderlich.

## Freigabeworkflow

1. `player-character.md` und nur die direkt verknüpften Assets lesen, die Startwissen, Beziehungen oder Hooks begründen.
2. Etablierte Angaben von offenen Spielerentscheidungen und DM-only Verknüpfungen trennen.
3. Einen vollständigen Entwurf für `player.md` aus den freigabefähigen Abschnitten vorlegen, ohne die Datei anzulegen oder zu ersetzen.
4. Den Safety-Check durchführen und erkannte Leaks vor der Freigabe korrigieren.
5. Den User ausdrücklich um Freigabe genau dieses Entwurfs bitten. Eine frühere Freigabe oder `status: ready` genügt nicht.
6. Erst nach Zustimmung Quellversion, `Player release` und Change Log aktualisieren und `player.md` schreiben.
7. `python3 scripts/validate_adventure.py` ausführen; Fehler blockieren den Abschluss.

## Safety-Check

- Der Text enthält nur den bewusst spielersichtbaren Character-Inhalt und ausdrücklich freigegebenes Startwissen.
- `DM-only connections`, verdeckte Ursachen, nicht freigegebene Wahrheiten, Lösungen und zukünftige Ereignisse fehlen.
- Gerüchte, Teilwahrheiten und falsche Annahmen werden nicht als bestätigte Wahrheit umformuliert.
- Offene Entscheidungen bleiben als Optionen erkennbar; der Text behauptet keine unbestätigte Motivation, Loyalität oder Reaktion.
- YAML-Frontmatter, Asset-IDs, Repository-Pfade, interne Statuswerte, Kommentare und Arbeitsnotizen fehlen.
- Relative Links und technische Abschnittsnamen fehlen; notwendiger Kontext wird eigenständig und spoilerfrei formuliert.
- Die Ausgabe besitzt eine verständliche Überschrift und ist ohne Repository-Kontext nutzbar.

Kann ein möglicher Spoiler oder eine vorgegebene Charakterentscheidung nicht sicher bewertet werden, bleibt die Ausgabe blockiert und die konkrete Frage wird dem User vorgelegt.

## Visuals

Ein Player Character kann wie jedes andere kanonische Subject ein `visual` erhalten. Identitätsanker stammen aus der kanonischen Quelle; dargestellter Zustand, Stil, Freigabe und PNG-Provenienz folgen vollständig dem [Bild-Workflow](bild-workflow.md). Ein Portrait ersetzt weder `player-character.md` noch `player.md` und darf keine DM-only Verbindung sichtbar machen.

## Definition of Done

- One-Shot-Rolle, freiwillige Hooks, Startwissen, narrative Stärken und Grenzen sind unmittelbar nutzbar;
- offene Entscheidungen sind klar von etabliertem Hintergrund getrennt;
- notwendiger Plotfortschritt hängt nicht von einer vorgeschriebenen Motivation oder Handlung dieser Figur ab;
- Beziehungen verweisen auf kanonische Assets, ohne deren Inhalt zu duplizieren;
- eine vorhandene `player.md` ist für die aktuelle Quellversion ausdrücklich freigegeben und besteht den Safety-Check;
- alle Inhalte bleiben regelneutral und auf den einen One-Shot begrenzt;
- technische Validierung und zuständiger Index sind aktuell.
