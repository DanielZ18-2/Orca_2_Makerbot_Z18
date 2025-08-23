# Orca Post-Processing – Befehl und Hinweise

**Befehl (Linux):**
python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

**Befehl (Windows):**
python "C:\Users<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"

**Hinweise**
- Das Skript wartet ~1,5 s, damit der G-Code vollständig geschrieben ist.
- Liegt kein G-Code vor, meldet das Skript „No gcode file found“.
- Der Ausgabename wird aus der Header-Zeile `; printing object ...` abgeleitet.
- Thumbnails sind optional, aber empfohlen; sie müssen im selben Ordner liegen.
