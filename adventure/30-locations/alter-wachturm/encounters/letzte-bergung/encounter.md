---
id: enc-letzte-bergung
type: encounter
title: "Letzte Bergung"
status: draft
version: 10
scope: local
primary_location: "loc-alter-wachturm"
participants: ["fac-gefallene-von-der-glocke", "obj-goldene-glocke", "npc-baron-von-dornfels", "npc-waechter-der-glocke", "cre-wiedererweckter-bergungsmann", "cre-gefallene-bergungsleute", "obj-bergungsgestell-des-barons"]
related_threads: ["plot-fluch-oder-gier"]
danger: severe
tags: [tower-pressure, final-choice, configurable-encounter]
themes: [greed, guardianship, reckoning]
created: 2026-08-14
updated: 2026-08-29
---

# Letzte Bergung

## Table purpose

Der Encounter setzt genau eine von drei Endkonfigurationen auf demselben Schlachtfeld um. Die Entscheidung der Gruppe bestimmt Gegner, Verbündete und Ziel; ein Rückzug unterbricht die Auseinandersetzung, bildet aber kein viertes Ende.

## Trigger

Die Gruppe erreicht [Glockenraum und Siegelkammer](../../scenes/glockenraum-und-siegelkammer/scene.md). Der Encounter beginnt, sobald sie die Glocke für eigenen Gewinn löst oder auf Barons offene Bergungsforderung antwortet. Der Baron erscheint nach wirklichem Läuten sofort; bei einer sichtbar gewordenen schweigenden Sicherung oder längeren Schutzwache setzt er sein vorbereitetes Gerät verzögert auch ohne Sicherheitssignal in Marsch.

## Situation

Glocke und Siegelring bilden den umkämpften Mittelpunkt. Frühere Entscheidungen bestimmen, welche Gebeine noch gebunden sind und welche Beweise gegen den Baron bereitliegen; die finale Seitenwahl bestimmt jedoch die Konfiguration. Ordne sie beim ersten unumkehrbaren Schritt zu:

| Auslöser | Konfiguration | Partei der Gruppe | Gegenseite |
|---|---|---|---|
| Die Gruppe beginnt ohne den Baron, Joch oder Glocke für den eigenen Goldgewinn zu lösen. | 1: Die neuen Plünderer | Gruppe | Wächter, sämtliche noch gebundenen Bergungstoten und der feindselige Turm |
| Der Baron trifft nach Glockenschlag oder sichtbar gewordener schweigender Sicherung ein; die Gruppe unterstützt seinen Bergungsanspruch. | 2: Im Dienst des Barons | Gruppe, Baron, Wachen und Arbeiter | Wächter, sämtliche noch gebundenen Bergungstoten und der feindselige Turm |
| Der Baron trifft nach Glockenschlag oder sichtbar gewordener schweigender Sicherung ein; die Gruppe verweigert ihm die Bergung und verteidigt den Verbleib der Glocke. | 3: Verteidiger der Glocke | Gruppe, Wächter und Gefallene des geplünderten Dorfes | Baron, Wachen, Arbeiter und Bergungsgestell |

## Participants and intentions

- Der [Wächter](../../npcs/waechter-der-glocke/npc.md) verhindert den Abtransport der Glocke und gibt die jüngeren Opfer nur frei, wenn die Gruppe ihren Verbleib verteidigt.
- Die [Gefallenen Bergungsleute](../../creatures/gefallene-bergungsleute/creature.md) greifen unter seinem Zwang jede bergende Partei an; zuvor gelöste Körper bleiben liegen.
- Die [Gefallenen von der Glocke](../../../../40-global/factions/gefallene-von-der-glocke/faction.md) weisen erneuten Raub zurück und helfen nur den Verteidigern des Verbleibs.
- Der [Baron](../../../dornfels/npcs/baron-von-dornfels/npc.md) will den Goldwert mit seinem [Bergungsgestell](../../objects/bergungsgestell-des-barons/object.md) sichern; Wachen schützen seinen Anspruch, Arbeiter wollen Auftrag und Kampf überleben.
- Die Gruppe entscheidet, ob sie die [Goldene Glocke](../../objects/goldene-glocke/object.md) selbst raubt, dem Baron überlässt oder im Turm verteidigt.

## Environment and leverage

- Glockenjoch und Arbeitssteg: Das Joch kann gesichert, gelöst oder blockiert werden. Ein Sturz in den Schacht ist eine sichtbare Gefahr, kein überraschender Sofortverlust.
- Durchtrenntes Seil und Hebel: Der reparierte Zug kann die Glocke läuten, trägt aber nicht ihr Gewicht. Im Kampf lässt er sich als Schwunglinie, Fessel oder Ablenkung nutzen.
- Siegelring: Solange die Glocke innerhalb des Rings hängt, kann der Wächter Turm und Gebeine lenken. Wird sie darüber hinausgehoben, bricht die Bindung unkontrolliert auf.
- Wandketten und Balken: Ketten schlagen oder würgen nur im Radius ihres Ankers; Balkenstürze werden durch Staub, Knarren und das Geisterbild angekündigt.
- Mauernischen, Eingangswinkel und Spalten am Siegelring: Von hier kommen die [Gefallenen Bergungsleute](../../creatures/gefallene-bergungsleute/creature.md). Befreite oder würdevoll gebettete Tote bleiben liegen.
- Bergungsgestell: In Konfiguration 2 und 3 steht das [Bergungsgestell des Barons](../../objects/bergungsgestell-des-barons/object.md) über dem Schacht. Es ist Ziel, Deckung und Gefahrenquelle zugleich.

## Konfiguration 1: Die neuen Plünderer

Die Gruppe versucht, die Glocke selbst als Goldschatz zu bergen. Der Wächter verriegelt den Rückweg, zieht schwarze Siegellinien zu allen noch gebundenen Leibern und orchestriert ihren Angriff. Dazu gehören der [Wiedererweckte Bergungsmann](../../creatures/wiedererweckter-bergungsmann/creature.md), falls seine Bindung im Aufstieg nicht gelöst wurde, und die weiteren Gefallenen aus Nischen, Spalten und Eingangswinkeln.

Ziel der Gruppe ist, die Glocke aus dem Siegelring zu schaffen. Ziel des Wächters ist nicht ihr Tod, sondern die Aufgabe der Bergung: Er trennt Hände von Werkzeugen, Körper vom Joch und Beute vom Ausgang. Wer die Bergung sichtbar aufgibt, einen Gefährdeten rettet oder die Glocke wieder sichert, kann auch während des Kampfes kapitulieren.

## Konfiguration 2: Im Dienst des Barons

Nach dem Glockenschlag oder dem verzögerten Zugriff auf eine sichtbar gewordene schweigende Sicherung erscheint der Baron mit wenigen Wachen, Arbeitern und vorbereitetem Gestell. Er erklärt offen, dass sein Haus den Goldwert der Glocke beansprucht, und ordnet ihre Bergung an. Unterstützt die Gruppe ihn, erhebt der Wächter dieselben noch gebundenen Bergungstoten wie in Konfiguration 1.

Die Arbeiter bedienen Winde, Gurte und Keile; die Wachen schützen sie und die Gruppe hält Turmverteidigung und Tote fern. Der Baron kämpft nicht heldenhaft: Er gibt Befehle, nutzt Deckung und zieht sich nur so weit zurück, dass sein Anspruch bestehen bleibt. Fällt das Gestell aus, geraten Arbeiter in Gefahr oder wird seine Lüge vor seinen Leuten bewiesen, muss die Gruppe zwischen Rettung, Reparatur und fortgesetzter Goldbergung wählen.

## Konfiguration 3: Verteidiger der Glocke

Nach seiner sofortigen oder verzögerten Ankunft fordert der Baron Übergabe und Mithilfe. Verweigert die Gruppe den Abtransport, lässt der Wächter die jüngeren Bergungsopfer zur Ruhe sinken: Sie sollen nicht ein weiteres Mal für fremde Gier kämpfen. Stattdessen treten die [Gefallenen von der Glocke](../../../../40-global/factions/gefallene-von-der-glocke/faction.md) als jenseitige Verbündete hervor.

Die Gefallenen sind keine zusätzlichen gewöhnlichen Kämpfer. Sie löschen Fackeln, zeigen Angreifern Erinnerungsbilder der Plünderung, halten einmal einen stürzenden Balken auf oder öffnen der Gruppe eine kurze sichere Linie. Der Wächter lenkt Türen, Ketten und Joch gegen Bergungsgestell und Arbeiter. Ziel der Gruppe ist, die Bergung zu stoppen: Gestell unbrauchbar machen, Arbeiter und Wachen zum Aufgeben bringen oder den Baron zum Rückzug zwingen. Wer Wehrlose rettet oder die Toten als einzelne Menschen bezeugt, verstärkt die Hilfe der Gefallenen; dafür genügen Miras letzte Worte und Vorschussmünze, Gurt- und Werkzeugzeichen, persönliche Gegenstände, eine würdige Bettung oder eine öffentliche Anerkennung. Ein verfügbarer Name kann verwendet werden, ist aber nicht erforderlich. Wahllose Gewalt schwächt die Hilfe.

## Escalation

1. Position beziehen: Der Wächter zeigt den Siegelring; der Baron zeigt in Konfiguration 2 oder 3 seinen Eigentumsbefehl und das Gestell.
2. Bewegung erzwingen: Kettenradien, Arbeitssteg und erste Bergungstote trennen die Beteiligten von ihrem Ziel.
3. Preis sichtbar machen: Ein Balken bedroht einen Menschen, das Joch reißt oder das Gestell kippt. Die Gruppe kann Vorteil sichern oder jemanden retten.
4. Entscheidung vollenden: Glocke und Siegelring beginnen sich zu trennen, das Gestell fällt aus oder der Baron verliert die Kontrolle über seine Leute. Die gegnerische Seite fordert ein letztes Mal Aufgabe oder Übergabe.

## Approaches

- Kettenanker, Joch, Hebel oder Gestell als konkrete Ziele sichern, blockieren, sabotieren oder übernehmen.
- Tote durch persönliche Zeugnisse, zugeordnete Gegenstände, würdige Bettung, Trennung ihrer Bergungszeichen oder Aufgabe des Raubs aus der Bindung lösen; ein genauer Name ist keine Voraussetzung.
- Beweise gegen den Baron seinen Wachen und Arbeitern zeigen, damit sie Befehle verweigern oder den Raum verlassen.
- Den Wächter durch eine klare Schutzhandlung stärken oder durch erneute Plünderung schwächen.
- Gegner zurückdrängen und die jeweilige Kernaufgabe unter Zeitdruck vollenden, statt alle Beteiligten besiegen zu müssen.
- Einen gefährdeten Arbeiter, eine Wache oder ein Gruppenmitglied retten und damit einen Seitenwechsel oder eine Kampfpause erzwingen.

## Consequences

### Ende 1: Gold unter einem Fluch

Gelingt der eigene Diebstahl, besitzt die Gruppe die Glocke oder einen geborgenen Teil ihres Goldes. Der Wächter bleibt an den geraubten Wert gebunden, die Gefallenen finden keine Ruhe und der Turm wird als aufgebrochener Bannort zurückgelassen. Scheitert die Gruppe oder gibt sie die Bergung auf, bleibt die Glocke im Turm; dieses Ende tritt erst ein, wenn sie den Raub dennoch vollendet.

### Ende 2: Der Preis des Auftrags

Baron und Gruppe bergen die Glocke gemeinsam. Er erfüllt den vereinbarten Lohn nur unter Berufung auf die Eigentumsklausel und beansprucht Glocke sowie Turmfunde. Die gebundenen Toten werden niedergerungen, aber nicht erlöst; mit der Glocke tragen Baron und Helfer die fortbestehende Schuld aus dem Turm.

### Ende 3: Die Glocke bleibt

Barons Bergung scheitert, sein Gerät wird aufgegeben und er zieht sich mit überlebenden Leuten zurück oder wird gestellt. Die Glocke bleibt im Siegelring. Die alten Gefallenen bezeugen die Entscheidung, der Wächter entlässt die jüngeren Bergungstoten aus seinem Zwang und der Turm wird zum Mahnmal statt zum Schatzlager.

### Unterbrechung

Ein Rückzug oder eine Kampfpause erhält Beweise, Verletzungen und beschädigtes Gerät. Bei einer Rückkehr besteht dieselbe Grundentscheidung fort; erst der vollendete Umgang mit der Glocke legt eines der drei Enden fest.

## Follow-up links

- Primary location: [Alter Wachturm](../../location.md)
- Entscheidungsszene: [Glockenraum und Siegelkammer](../../scenes/glockenraum-und-siegelkammer/scene.md)
- Related thread: [Fluch oder Gier](../../../../20-plot/threads/fluch-oder-gier/plot-thread.md)
