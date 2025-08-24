# Setup- & Release-Checkliste (MakerBot Replicator Z18 · Orca 2.3+)

## A. Einmalige Repo-Einrichtung
- [ ] `src/Orca_gcode_2_Makerbot_Z18.py` vorhanden (v11.5a).
- [ ] `assets/*.png` vorhanden (alle sechs Thumbnails, exakt benannt).
- [ ] `docs/howto-setup.en.md` / `docs/howto-setup.de.md` hinzugefügt.
- [ ] (Optional) `bundles/Orca_Z18_MasterBundle.zip` via Git LFS.
- [ ] `LICENSE`, `README.md`, `.gitattributes`, `.gitignore`.

## B. Orca Slicer Basis
- [ ] Orca Slicer 2.3+ installieren.
- [ ] Assistent abschließen: **Generic Marlin**, Düse **0,4 mm**.

## C. Z18-Drucker (erste Anlage)
- [ ] Drucker **„MakerBot Replicator Z18“** anlegen.
- [ ] Bett: **305 × 305 × 457 mm**, Mittelpunkt **152,0 / 152,0 mm** (temporär).
- [ ] Bett-STL laden: `print_bed_makerbot_replicator_z18.stl`.
- [ ] Beheiztes Bett **aus**.
- [ ] **Start/End-G-Code** je Extruder setzen (mk13 / mk13_impla / mk13_experimental).

## D. Post-Processing-Skript
- [ ] Script + Thumbnails kopieren nach:
  - Linux: `~/Makerbot_files/Orca_Slicer/`
  - Windows: `C:\Users\<USER>\Makerbot_files\Orca_Slicer\`
- [ ] Orca → Printer Settings → Output → Post-processing:
  - Linux: `python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
  - Windows: `python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`

## E. Bundle importieren & finalisieren
- [ ] Datei → **Import Configs** → `Orca_Z18_MasterBundle.zip`.
- [ ] In jedem Z18-Profil: Bettmittelpunkt **152,5 / 152,5 mm** (final).
- [ ] Bett-STL prüfen.
- [ ] Start/End-G-Code je Extruder prüfen.
- [ ] Profil speichern.

## F. Smoke-Test
- [ ] Kleines Modell slicen → G-Code exportieren.
- [ ] `.makerbot` wird neben dem G-Code erstellt.
- [ ] ZIP öffnen → `meta.json` + `print.jsontoolpath` + Thumbnails vorhanden.
- [ ] (Optional) Upload in die Digital Factory; Druck funktioniert auch ohne Vorschau.

## G. Optionale DF-Vorschau-Optimierung
- [ ] Bei Preview-Fehlern folgende Env-Variablen testen:

ORCA_MB_MAX_CMDS=18000
ORCA_MB_RDP_EPS_BASE=0.10
ORCA_MB_RDP_EPS_MAX=0.25
ORCA_MB_TRAVEL_MIN_DXY=0.02
