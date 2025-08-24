# Troubleshooting (MakerBot Replicator Z18 · Orca 2.3+)

## Script doesn’t run from Orca
- Check Python path in **Post-processing** (quotes + full path).
- Windows: try `python` vs. `py`; ensure Python is on PATH.
- File permissions (Linux): `chmod +x Orca_gcode_2_Makerbot_Z18.py` not required, but readable.
- The script waits ~1.5 s; very slow disks can need a bit more time.

## “No gcode file found”
- Orca didn’t pass `[output_filepath]` or you triggered the script manually without a file.
- Ensure you used the exact Post-processing command from the docs.

## Output name is wrong
- The script derives the name from `; printing object …` in the G-code header.
- Ensure Orca writes this header; otherwise we fall back to the G-code file name stem.

## Digital Factory: “model is too large”
- This refers to **toolpath complexity**, not dimensions.
- Upload/printing still works; only preview may fail.
- Try environment variables to reduce non-surface complexity:
- 
ORCA_MB_MAX_CMDS=18000
ORCA_MB_RDP_EPS_BASE=0.10
ORCA_MB_RDP_EPS_MAX=0.25
ORCA_MB_TRAVEL_MIN_DXY=0.02

- Keep **surface** (outer perimeters) intact for Fuzzy; the script already does that.

## Missing thumbnails in .makerbot
- Put the six PNGs in the same folder as the script:
- `isometric_thumbnail_120x120.png`
- `isometric_thumbnail_320x320.png`
- `isometric_thumbnail_640x640.png`
- `thumbnail_55x40.png`
- `thumbnail_110x80.png`
- `thumbnail_320x200.png`

## Material / Extruder not shown in DF
- Ensure `meta.json` has:
- `material` and `materials` (e.g., `"pla"`, `["pla"]`)
- `tool_type` and `tool_types` (e.g., `"mk13"`, `["mk13"]`)
- Minimal `miracle_config` block with `_bot:"z18_6"`, `_extruders:["mk13"]`, `_materials:["pla"]`
- The script fills these automatically; if you hand-edit, keep the keys.

## Bed center 152.0 vs. 152.5 mm
- Orca only allows **152.0** during first creation.
- After importing the bundle, change to **152.5 / 152.5 mm** in each Z18 profile.

## Units / Volumetric
- Script supports volumetric (`M200 D…`) and normal E.
- If filament diameter is custom, ensure Orca writes it in the header.

## Verify .makerbot contents
- `.makerbot` is a ZIP. Open with a ZIP tool.
- You should see `meta.json`, `print.jsontoolpath`, and the PNGs.
