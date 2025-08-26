
# MakerBot Replicator Z18 – Einrichtungsanleitung (Orca Slicer 2.3+)

Diese Anleitung umfasst:

1. Download von Orca Slicer über GitHub  
2. Abschluss des Ersteinrichtungs-Assistenten (Generischer Marlin, 0,4 mm)  
3. Anlage eines neuen **MakerBot Replicator Z18**-Druckers (alle erforderlichen Parameter)  
4. Import von **`Orca_Z18_MasterBundle.zip`** und finale Anpassungen (Bettmittelpunkt 152,5 mm, Bett-STL, Start/End-G-Code je Extruder, Post-Processing-Skript)

> **Hinweise**
>
> - Der Z18 hat eine **beheizte Kammer**, aber **kein beheiztes Bett** → Betttemperatur auf **0**.  
> - Der Z18 nutzt ein **zentriertes Koordinatensystem**. Bei der ersten Druckeranlage erlaubt Orca nur **152,0 mm** als Bettmittelpunkt. Nach dem Bundle-Import muss in jedem Z18-Profil auf **152,5 mm** korrigiert werden.  
> - Verwende das Bettmodell **`print_bed_makerbot_replicator_z18.stl`** (im älteren Video `makerbot_replicator_z18.stl`).

---

## 1) Orca Slicer herunterladen

- Offizielles Repository: <https://github.com/SoftFever/OrcaSlicer>  
- **Orca Slicer 2.3+** für dein Betriebssystem herunterladen und installieren.

---

## 2) Ersteinrichtung in Orca (Basiskonfiguration)

1. Orca Slicer starten → der Einrichtungs-Assistent öffnet sich.  
2. Einen **Generischen Marlin**-Drucker mit **0,4 mm** Düse hinzufügen.  
3. Assistent beenden.

Damit existiert ein Basisprofil; als Nächstes legst du den Z18 als eigenen Drucker an.

---

## 3) Neuen Drucker anlegen: „MakerBot Replicator Z18“

In Orca: **Printer Settings → Machine → Add new printer** und eintragen:

### 3.1 Identität
- **Name:** `MakerBot Replicator Z18`  
- **G-Code-Flavor:** `Marlin` (der Z18 versteht Marlin-ähnlichen G-Code)  
- **Extruderanzahl:** `1`

### 3.2 Bauraum & Bettmodell
- **Bettform:** Rechteck  
  **Größe (X × Y):** `305 × 305 mm`  
  **Z-Höhe:** `457 mm`
- **Bettmittelpunkt (temporär):** `X = 152,0 mm`, `Y = 152,0 mm`  
  *(Orca erlaubt hier nur 152,0 mm; die Korrektur auf **152,5 mm** erfolgt später in Schritt 4.)*
- **Beheiztes Bett:** **Deaktiviert** (Z18 hat kein beheiztes Bett)
- **Eigenes Bettmodell:** **`print_bed_makerbot_replicator_z18.stl`** laden  
  *(Printer Settings → Machine → Bed model → Load STL)*

### 3.3 Düse
- **Standard-Düsendurchmesser:** `0,4 mm`  
  (Weitere Düsen später über Profile.)

### 3.4 Start- & End-G-Code (Copy & Paste)

Füge **einen** der folgenden **Start-G-Code**-Blöcke passend zu deinem Extruder sowie den **gemeinsamen End-G-Code** ein.

**Ablageort:** **Printer Settings → Custom G-code → Start G-code / End G-code**

**Smart Extruder+** (Tool-Tag `mk13`)
```gcode
; makerbot_tool_type = mk13
G21                      ; metrisch
G90                      ; absolute XYZ
M82                      ; absolutes E
M107                     ; Lüfter aus
G28 X0 Y0 Z0             ; alle Achsen homen
G92 E0                   ; Extruder zurücksetzen
G1 Z35 F9000             ; sichere Z-Höhe
G1 X152.5 Y152.5 F15000  ; zum Bettzentrum (305x305 -> 152,5/152,5)
; Optionale Prime-Linie (deaktiviert):
; G1 X40 Y10 Z0.30 F9000
; G1 X260 Y10 E8.0 F900

```

**Tough Smart Extruder+** (Tool-Tag mk13_impla)
```gcode
; makerbot_tool_type = mk13_impla
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optionale Prime-Linie (deaktiviert)

```

**LABS Extruder** (Tool-Tag mk13_experimental)
```gcode
; makerbot_tool_type = mk13_experimental
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optionale Prime-Linie (deaktiviert)

```
**Gemeinsamer End-G-Code** (alle Extruder)
```gcode
; --- End ---
M104 S0                  ; Hotend aus
M107                     ; Lüfter aus
G91                      ; relativ
G1 Z10 F3000             ; Z anheben
G90                      ; absolut
G92 E0
G1 E-2 F1800             ; kleiner Retract
M84                      ; Motoren aus

```
Die Kammerheizung wird hier nicht gesteuert; bei Bedarf am Z18-Panel einstellen.

Speichere den Drucker.

### 4) Bundle importieren und Profile finalisieren

In Orca: File → Import Configs… und Orca_Z18_MasterBundle.zip wählen.
Dadurch werden Drucker-/Prozess-/Material-Presets für alle Extruder-/Düsen-Varianten importiert.

Öffne deine Z18-Profile und passe an:

Bettmittelpunkt: X = 152,0 → 152,5 mm, Y = 152,0 → 152,5 mm

Bettmodell: bei Bedarf print_bed_makerbot_replicator_z18.stl erneut laden

Custom G-Code: sicherstellen, dass Start/End zum Extruder passen

Post-Processing (Python-Skript):

Linux:
```bash
python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

```
Windows:
```bash
python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

```

Profile speichern.

Modell slicen und G-Code exportieren → das Skript erzeugt eine .makerbot-Datei neben dem G-Code.

Wenn die Digital-Factory-Vorschau „model is too large“ meldet, kannst du dennoch hochladen und drucken.
Für eine vorschaugerechte Pfadkomplexität lassen sich Nicht-Surface-Moves über Umgebungsvariablen reduzieren (siehe Projektdoku).

```makefile
::contentReference[oaicite:0]{index=0}
