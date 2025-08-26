
README (macOS) — docs/mac-install.en.md
# macOS Install & Configuration — Orca_2_Makerbot_Z18 (v11.5a)

This guide covers:
- Installing Python on macOS
- Placing the script & thumbnails
- Configuring Orca Slicer to call the script (stable on Apple Silicon & Intel)
- Optional performance/preview tuning
- Troubleshooting

---

## 1) Install Python 3 (Homebrew)

**Apple Silicon (M-series):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11
/opt/homebrew/bin/python3 --version
```

**Intel Mac:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11
/usr/local/bin/python3 --version
```

We will reference the full interpreter path in Orca to avoid PATH issues.

## 2) Script & thumbnails

Create the folder and copy files:
```bash
mkdir -p "$HOME/Makerbot_files/Orca_Slicer"
cp src/Orca_gcode_2_Makerbot_Z18.py "$HOME/Makerbot_files/Orca_Slicer/"
# Place the six PNGs (thumbnails) into the same folder:
# isometric_thumbnail_120x120.png
# isometric_thumbnail_320x320.png
# isometric_thumbnail_640x640.png
# thumbnail_55x40.png
# thumbnail_110x80.png
# thumbnail_320x200.png
```

**Remove macOS quarantine** (if needed):
```bash
xattr -dr com.apple.quarantine "$HOME/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py"
```
## 3) Orca Slicer: base setup

Install Orca Slicer 2.3+ from the official GitHub release page.

Run the first-run wizard with Generic Marlin and 0.4 mm nozzle.

## 4) Add the MakerBot Replicator Z18 printer

**Printer Settings → Machine → Add new printer**

Name: MakerBot Replicator Z18

G-code flavor: Marlin

Extruders: 1

Bed: 305 × 305 mm (Z) 457 mm

Bed center (temporary): X=152.0 mm, Y=152.0 mm (Orca limits to 152.0 here; later set 152.5)

Heated bed: Disabled (Z18 has no heated bed)

Bed model: load print_bed_makerbot_replicator_z18.stl

Default nozzle: 0.4 mm

**Custom G-code: Paste the Start/End blocks that match your extruder (see project README).
(Smart Extruder+ = mk13, Tough Smart Extruder+ = mk13_impla, LABS = mk13_experimental)**

## 5) Configure Post-Processing (macOS)

Open Printer Settings → Output → Post-processing scripts and add:

**Apple Silicon:**
```bash
/opt/homebrew/bin/python3 "/Users/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"
/opt/homebrew/bin/python3 "/Users/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[tmp_output_filepath]"
```

**Intel Mac:**
```bash
/usr/local/bin/python3 "/Users/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"
/usr/local/bin/python3 "/Users/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[tmp_output_filepath]"
```

Why two lines?
Some Orca builds pass a temporary file path while slicing. The first line handles normal exports; the second line handles temp paths. The script is robust either way.

Optional (most stable): In Orca → Preferences → Output, set Default export folder to ~/Makerbot_files/Orca_Slicer/ and enable Export G-code after slicing. Then keep only the [output_filepath] line.

## 6) Import the Z18 bundle & finalize

**File → Import Configs… → select Orca_Z18_MasterBundle.zip.**

**In each Z18 profile:**

Set bed center to X=152.5 / Y=152.5 mm (final value).

**Ensure the bed STL is assigned.**

**Verify Start/End G-code match your extruder.**

Save profile.

## 7) Environment variables (optional tuning)

If you want to make DF preview more likely to succeed (printing works regardless), reduce non-surface complexity:
```bash
export ORCA_MB_MAX_CMDS=18000
export ORCA_MB_RDP_EPS_BASE=0.10
export ORCA_MB_RDP_EPS_MAX=0.25
export ORCA_MB_TRAVEL_MIN_DXY=0.02
```

Then re-launch Orca from the same terminal so it inherits these variables.

## 8) Smoke test

Slice a small model; export G-code.

The script waits until the file is fully written and then produces a .makerbot in the same folder.

Open the .makerbot (ZIP) and check: meta.json, print.jsontoolpath, and all thumbnails.

## 9) Troubleshooting

**“script can’t access the temp gcode located in Orca”**

Ensure you used full interpreter paths and kept both lines ([output_filepath] and [tmp_output_filepath]) with quotes.

If your G-code file is very large, the script now waits up to 10 seconds for the file to finish writing (size + mtime stabilization).

If Orca writes .gcode.gz, the script automatically decompresses it.

**Permission/quarantine**
```bash
Run: xattr -dr com.apple.quarantine ~/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py
```
Preview says “model is too large”

**Upload/printing still works. For preview, reduce non-surface complexity with the environment variables above.**

## 10) Notes

**The Z18 has a heated chamber but no heated bed → platform temperature is 0 in meta.json.**

The script preserves surface perimeters 1:1 (Fuzzy-safe), and simplifies only non-surface moves.

Output filename is derived from the G-code header line ; printing object …. If missing, it falls back to the G-code filename stem.


---
