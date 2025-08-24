
---

## 📄 `docs/howto-setup.de.md`

```markdown
# MakerBot Replicator Z18 – Einrichtungsanleitung (Orca Slicer 2.3+)

Diese Anleitung zeigt:
1) Download von Orca Slicer
2) Abschluss des Orca-Assistenten (generischer Marlin-Drucker, 0,4-mm-Düse)
3) Anlage eines neuen „MakerBot Replicator Z18“ in Orca (mit allen Parametern)
4) Import von `Orca_Z18_MasterBundle.zip` und letzte Anpassungen

> Hinweise
> - Z18 hat **beheizte Kammer**, **kein beheiztes Bett**. Betttemperatur muss `0` bleiben.
> - Die Koordinaten sind auf dem Z18 **zentriert**. Bei der ersten Druckeranlage erlaubt Orca nur **152,0 mm** als Bettmittelpunkt. Nach dem Bundle-Import wird der Wert in jedem Profil auf **152,5 mm** korrigiert.
> - Verwende das Bett-Modell **`print_bed_makerbot_replicator_z18.stl`** (im Video früher `makerbot_replicator_z18.stl`).

---

## 1) Orca Slicer herunterladen

- Offizielles GitHub: https://github.com/SoftFever/OrcaSlicer  
- Installer für dein OS herunterladen und Orca 2.3+ installieren.

---

## 2) Orca-Assistent (Basiseinrichtung)

1. Orca starten → der Einrichtungsassistent öffnet sich.
2. **Generischen Marlin-Drucker** mit **0,4-mm-Düse** hinzufügen.
3. Assistent beenden.  
   Damit gibt es ein Basis-Profil; als Nächstes legen wir den Z18 an.

---

## 3) Neuen Drucker anlegen: „MakerBot Replicator Z18“

In Orca: **Printer Settings → Machine → Add new printer** und eintragen:

### 3.1 Identität
- **Name:** `MakerBot Replicator Z18`
- **G-code flavor:** `Marlin` (Z18 versteht Marlin-ähnlichen G-Code)
- **Extruderanzahl:** `1`

### 3.2 Bauraum & Bettmodell
- **Bettform:** Rechteck  
  **Größe (X × Y):** `305 × 305 mm`  
  **Z-Höhe:** `457 mm`
- **Mittelpunkt:** **X = 152,0 mm, Y = 152,0 mm** *(Orca limitiert hier auf 152,0)*  
  **Nach dem Bundle-Import auf 152,5 mm korrigieren.**
- **Beheiztes Bett:** **Deaktiviert** (Z18 hat kein beheiztes Bett)
- **Eigenes Bettmodell:** **`print_bed_makerbot_replicator_z18.stl`** laden  
  (Menü: *Printer Settings → Machine → Bed model → Load STL*)

### 3.3 Düse
- **Standard-Düsendurchmesser:** `0,4 mm` (weitere Düsen später per Profil)

### 3.4 Start- & End-G-Code (Copy & Paste)

> Ort zum Einfügen: **Printer Settings → Custom G-code → Start G-code / End G-code**  
> Wähle den Block passend zu deinem Extruder.  
> Die Sequenzen sind Z18-minimal: metrisch, absolut, Home, sichere Z-Höhe, kein Heizbett.

**Smart Extruder+** (Tool-Tag `mk13`)
```gcode
; makerbot_tool_type = mk13
G21                      ; metrisch
G90                      ; absolute XYZ
M82                      ; absolute E
M107                     ; Lüfter aus
G28 X0 Y0 Z0             ; Home alle Achsen
G92 E0                   ; Extruder zurücksetzen
G1 Z35 F9000             ; sichere Z-Höhe
G1 X152.5 Y152.5 F15000  ; zum Bettzentrum (305x305 -> 152,5/152,5)
; Optional: Prime-Linie (deaktiviert)
; G1 X40 Y10 Z0.30 F9000
; G1 X260 Y10 E8.0 F900

**Tough Smart Extruder+** (Tool-Tag mk13_impla)

; makerbot_tool_type = mk13_impla
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optional Prime-Linie (deaktiviert)


**LABS Extruder** (Tool-Tag mk13_experimental)

; makerbot_tool_type = mk13_experimental
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optional Prime-Linie (deaktiviert)

**Gemeinsamer End-G-Code** (alle Extruder)

; --- End ---
M104 S0                  ; Hotend aus
M107                     ; Lüfter aus
G91                      ; relativ
G1 Z10 F3000             ; anheben
G90                      ; absolut
G92 E0
G1 E-2 F1800             ; kleine Retract
M84                      ; Motoren aus


Die Kammerheizung wird hier nicht gesteuert; bei Bedarf am Z18-Panel einstellen.

Speichere den Drucker.

### 4) Bundle importieren und Profile finalisieren

In Orca: File → Import Configs… und Orca_Z18_MasterBundle.zip wählen.
Orca importiert Drucker-/Prozess-/Material-Presets.

Öffne dein Z18-Druckerprofil und passe an:

Bettmittelpunkt: X = 152,0 → 152,5 mm, Y = 152,0 → 152,5 mm

Bettmodell: ggf. print_bed_makerbot_replicator_z18.stl erneut laden

Custom G-code: sicherstellen, dass Start/End zum Extruder passen

Post-Processing: Python-Skript eintragen

Linux
python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

Windows
python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

Profil speichern.

Modell slicen und G-Code exportieren → das Skript erzeugt die .makerbot neben dem G-Code.

Tipp: Falls die Digital-Factory-Vorschau „model is too large“ meldet, kannst du später über Umgebungsvariablen die Nicht-Surface-Komplexität reduzieren (siehe Projektdokumentation). Der Druck selbst funktioniert auch ohne Vorschau.


---

### So kannst du sie einchecken

- Lege im Repo einen Ordner `docs/` an und speichere beide Dateien:
  - `docs/howto-setup.en.md`
  - `docs/howto-setup.de.md`
- Verlinke sie in deiner `README.md`, z. B.:
