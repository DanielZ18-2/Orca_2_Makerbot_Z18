## Orca_2_Makerbot_Z18

**Convert Orca Slicer G-code to MakerBot `.makerbot` (ZIP) for the MakerBot Replicator Z18.**  
This repository contains the post-processing script **`Orca_gcode_2_Makerbot_Z18.py`** (v11.5a).

> Goal: print complex models (incl. Fuzzy Skin) on a Z18 while using a modern slicer (Orca 2.3+).

## Features
- Parses Orca G-code (absolute/relative E, volumetric/non-volumetric).
- Builds `print.jsontoolpath` and `meta.json` from scratch—no templates.
- Centers coordinates for Z18 (±152.5 mm) and computes a correct bounding box.
- Keeps **surface perimeters** intact (Fuzzy Safe). Reduces complexity on non-surface moves.
- Adaptive simplification to keep toolpath preview-friendly if needed.
- Drops only micro **travel** moves; extrusion micro-geometry remains for surface fidelity.
- Generates a ZIP-based `.makerbot` with thumbnails (if present in `assets/`).

## Quick start
1. Install Python 3.8+.
2. Copy `src/Orca_gcode_2_Makerbot_Z18.py` to:
   - **Linux:** `~/Makerbot_files/Orca_Slicer/`
   - **Windows:** `C:\Users\<USER>\Makerbot_files\Orca_Slicer\`
3. Copy all PNG thumbnails from `assets/` into the same folder.
4. In **Orca Slicer → Printer Settings → Output → Post-processing** add:
   - **Linux**  
     `python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
   - **Windows**  
     `python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
5. Slice → export G-code → the script writes a `.makerbot` next to the G-code.

## Environment variables (optional)
See [`docs/env-vars.en.md`](docs/env-vars.en.md) for exhaustive details. The useful ones:
- `ORCA_MB_MODE=fuzzy|normal` (default: `normal`)
- `ORCA_MB_MAX_CMDS=20000` (reduce if DF preview still bails)
- `ORCA_MB_RDP_EPS_BASE=auto` and `ORCA_MB_RDP_EPS_MAX=0.20`
- `ORCA_MB_TRAVEL_MIN_DXY=0.01` (travel micro-filter)

## Known behavior
- Ultimaker Digital Factory (DF) **preview** may show **“model is too large”** for highly complex paths.  
  Upload/print still works; the printer executes the toolpath correctly.
- Z18 has **heated chamber**, **no heated bed**. Bed temp in `meta.json` is set to `0`.

## Legal
MakerBot®, Ultimaker®, and Digital Factory™ are trademarks of their respective owners.  
This project is **community-made** and not affiliated with MakerBot/Ultimaker.

## License
See [LICENSE](LICENSE).
