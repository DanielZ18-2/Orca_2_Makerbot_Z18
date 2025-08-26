
# Setup Guide (Linux & Windows)

## 1) Install Python 3.8+
- **Linux**: Use your package manager (e.g. `sudo apt install python3`).
- **Windows**: Download from python.org, check “Add Python to PATH”.

## 2) Place the script and thumbnails
- Create folder:
  - **Linux**: `~/Makerbot_files/Orca_Slicer/`
  - **Windows**: `C:\Users\<USER>\Makerbot_files\Orca_Slicer\`
- Copy `src/Orca_gcode_2_Makerbot_Z18.py` there.
- Copy all PNGs from `/assets` into the same folder.

## 3) Configure Orca Slicer 2.3+
`Printer Settings → Output → Post-processing scripts`
- **Linux**  
  `python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
- **Windows**  
  `python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`

## 4) (Optional) Environment tuning
Set env vars before launching Orca (Linux) or via PowerShell (Windows).  
See `docs/env-vars.en.md` for details.

## 5) Run a smoke test
- Open `examples/minimal.gcode`.
- Export G-code → the script should create `minimal.makerbot` next to the G-code.
- Zip content should include: `meta.json`, `print.jsontoolpath`, and all thumbnails.
