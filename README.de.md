# Orca_2_Makerbot_Z18

**Konvertiert Orca Slicer G-Code in MakerBot-`.makerbot` (ZIP) für den MakerBot Replicator Z18.**  
Dieses Repository enthält das Post-Processing-Skript **`Orca_gcode_2_Makerbot_Z18.py`** (v11.5a).

> Ziel: Komplexe Modelle (inkl. Fuzzy Skin) mit Orca 2.3+ auf dem Z18 drucken.

## Funktionen
- Liest Orca-G-Code (absolute/relative E, volumetrisch/nicht volumetrisch).
- Erzeugt `print.jsontoolpath` und `meta.json` **ohne Vorlagen**.
- Zentriert die Koordinaten für den Z18 (±152,5 mm) und berechnet eine korrekte Bounding-Box.
- Erhält **Außenhaut-Perimeter** (Fuzzy Safe). Reduziert Komplexität nur bei Nicht-Surface-Moves.
- Adaptive Vereinfachung, um den Toolpath ggf. vorschaugerecht zu halten.
- Entfernt ausschließlich **Travel**-Mikrobewegungen; Extrusionsmikrogeometrie bleibt erhalten.
- Erstellt eine ZIP-basierte `.makerbot` inkl. Thumbnails (falls in `assets/` vorhanden).

## Schnellstart
1. Python 3.8+ installieren.
2. `src/Orca_gcode_2_Makerbot_Z18.py` kopieren nach:
   - **Linux:** `~/Makerbot_files/Orca_Slicer/`
   - **Windows:** `C:\Users\<USER>\Makerbot_files\Orca_Slicer\`
3. Alle PNG-Thumbnails aus `assets/` in denselben Ordner kopieren.
4. In **Orca Slicer → Printer Settings → Output → Post-processing** hinzufügen:
   - **Linux**  
     `python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
   - **Windows**  
     `python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
5. Slicen → G-Code exportieren → das Skript erzeugt `.makerbot` neben der G-Code-Datei.

## Umgebungsvariablen (optional)
Siehe [`docs/env-vars.de.md`](docs/env-vars.de.md). Wichtige Beispiele:
- `ORCA_MB_MODE=fuzzy|normal` (Standard: `normal`)
- `ORCA_MB_MAX_CMDS=20000` (bei DF-Vorschauproblemen ggf. reduzieren)
- `ORCA_MB_RDP_EPS_BASE=auto`, `ORCA_MB_RDP_EPS_MAX=0.20`
- `ORCA_MB_TRAVEL_MIN_DXY=0.01`

## Hinweise
- Die Digital Factory (DF) kann in der **Vorschau** „**model is too large**“ anzeigen.  
  Der **Druck** funktioniert dennoch; der Z18 führt den Toolpath korrekt aus.
- Z18: **beheizte Kammer**, **kein beheiztes Bett** → Betttemperatur in `meta.json` ist `0`.

## Rechtliches
MakerBot®, Ultimaker® und Digital Factory™ sind Marken ihrer jeweiligen Inhaber.  
Dieses Projekt ist **Community-basiert** und steht in keiner Verbindung zu MakerBot/Ultimaker.

## Lizenz
Siehe [LICENSE](LICENSE).
