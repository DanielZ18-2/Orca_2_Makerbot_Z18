# Fehlersuche / Troubleshooting (MakerBot Replicator Z18 · Orca 2.3+)

## Skript startet nicht aus Orca
- Python-Pfad in **Post-processing** prüfen (voller Pfad in Anführungszeichen).
- Windows: `python` vs. `py` testen; sicherstellen, dass Python in PATH ist.
- Dateirechte (Linux): Leserechte genügen; `chmod +x` optional.
- Skript wartet ~1,5 s; bei sehr langsamen Datenträgern ggf. mehr Zeit nötig.

## „No gcode file found“
- Orca hat `[output_filepath]` nicht übergeben oder Skript manuell ohne Datei gestartet.
- Befehl exakt wie in der Doku eintragen.

## Falscher Ausgabename
- Name wird aus `; printing object …` im G-Code-Header übernommen.
- Falls Orca diese Zeile nicht schreibt, wird auf den Dateinamen-Stamm zurückgegriffen.

## Digital Factory: „model is too large“
- Bezieht sich auf **Toolpath-Komplexität**, nicht auf Abmessungen.
- Upload/Druck funktionieren trotzdem; nur die Vorschau kann abbrechen.
- Env-Variablen testen, um Nicht-Surface zu reduzieren:

ORCA_MB_MAX_CMDS=18000
ORCA_MB_RDP_EPS_BASE=0.10
ORCA_MB_RDP_EPS_MAX=0.25
ORCA_MB_TRAVEL_MIN_DXY=0.02

- **Surface** (Außenhaut) bleibt unangetastet; Fuzzy wird nicht zerstört.

## Thumbnails fehlen in `.makerbot`
- Die sechs PNGs müssen im selben Ordner wie das Skript liegen:
- `isometric_thumbnail_120x120.png`
- `isometric_thumbnail_320x320.png`
- `isometric_thumbnail_640x640.png`
- `thumbnail_55x40.png`
- `thumbnail_110x80.png`
- `thumbnail_320x200.png`

## Material / Extruder wird in DF nicht angezeigt
- In `meta.json` müssen vorhanden sein:
- `material` und `materials` (z. B. `"pla"`, `["pla"]`)
- `tool_type` und `tool_types` (z. B. `"mk13"`, `["mk13"]`)
- Minimaler `miracle_config`-Block mit `_bot:"z18_6"`, `_extruders:["mk13"]`, `_materials:["pla"]`
- Das Skript setzt diese Felder automatisch; bei Hand-Edits unbedingt beibehalten.

## Bettmittelpunkt 152,0 vs. 152,5 mm
- Orca erlaubt bei der ersten Anlage nur **152,0**.
- Nach dem Bundle-Import in jedem Z18-Profil auf **152,5 / 152,5 mm** korrigieren.

## Einheiten / Volumetrik
- Skript unterstützt volumetrisch (`M200 D…`) und normale E-Angaben.
- Bei eigenem Filamentdurchmesser sicherstellen, dass Orca den Wert im Header schreibt.

## `.makerbot` prüfen
- `.makerbot` ist ein ZIP – mit ZIP-Tool öffnen.
- Enthalten: `meta.json`, `print.jsontoolpath`, sowie die PNG-Thumbnails.
