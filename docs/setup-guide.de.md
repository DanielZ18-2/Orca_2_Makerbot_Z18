
# Einrichtungsanleitung (Linux & Windows)

## 1) Python 3.8+ installieren
- **Linux**: Paketverwaltung (z. B. `sudo apt install python3`).
- **Windows**: Von python.org, Haken „Add Python to PATH“ setzen.

## 2) Script und Thumbnails platzieren
- Ordner anlegen:
  - **Linux**: `~/Makerbot_files/Orca_Slicer/`
  - **Windows**: `C:\Users\<USER>\Makerbot_files\Orca_Slicer\`
- `src/Orca_gcode_2_Makerbot_Z18.py` dorthin kopieren.
- Alle PNGs aus `/assets` in denselben Ordner kopieren.

## 3) Orca Slicer 2.3+ konfigurieren
`Printer Settings → Output → Post-processing scripts`
- **Linux**  
  `python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
- **Windows**  
  `python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`

## 4) (Optional) Umgebungsvariablen
Vor dem Start von Orca setzen (Linux) oder via PowerShell (Windows).  
Details: `docs/env-vars.de.md`.

## 5) Smoke-Test
- `examples/minimal.gcode` in Orca laden.
- G-Code exportieren → `.makerbot` wird neben der G-Code-Datei erzeugt.
- ZIP-Inhalt prüfen: `meta.json`, `print.jsontoolpath`, Thumbnails.
