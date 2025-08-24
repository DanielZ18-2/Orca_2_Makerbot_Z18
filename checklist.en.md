# Setup & Release Checklist (MakerBot Replicator Z18 · Orca 2.3+)

## A. One-time repo setup
- [ ] `src/Orca_gcode_2_Makerbot_Z18.py` present (v11.5a).
- [ ] `assets/*.png` present (all six thumbnails, exact names).
- [ ] `docs/howto-setup.en.md` / `docs/howto-setup.de.md` added.
- [ ] (Optional) `bundles/Orca_Z18_MasterBundle.zip` via Git LFS.
- [ ] `LICENSE`, `README.md`, `.gitattributes`, `.gitignore`.

## B. Orca Slicer base install
- [ ] Install Orca Slicer 2.3+ from official GitHub.
- [ ] Finish wizard with **Generic Marlin**, nozzle **0.4 mm**.

## C. Z18 printer creation (first pass)
- [ ] Create printer **“MakerBot Replicator Z18”**.
- [ ] Bed: **305 × 305 × 457 mm**, center **152.0 / 152.0 mm** (temporary).
- [ ] Load bed STL: `print_bed_makerbot_replicator_z18.stl`.
- [ ] Heated bed **off**.
- [ ] Set **Start/End G-code** matching your extruder (mk13 / mk13_impla / mk13_experimental).

## D. Post-processing script
- [ ] Copy script + thumbnails to:
  - Linux: `~/Makerbot_files/Orca_Slicer/`
  - Windows: `C:\Users\<USER>\Makerbot_files\Orca_Slicer\`
- [ ] Orca → Printer Settings → Output → Post-processing:
  - Linux: `python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`
  - Windows: `python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"`

## E. Import bundle & finalize
- [ ] File → **Import Configs** → `Orca_Z18_MasterBundle.zip`.
- [ ] In each Z18 profile: bed center **152.5 / 152.5 mm** (final).
- [ ] Verify bed STL still assigned.
- [ ] Verify Start/End G-code per extruder.
- [ ] Save profile.

## F. Smoke test
- [ ] Slice a tiny model → export G-code.
- [ ] `.makerbot` is created next to G-code.
- [ ] Open ZIP → `meta.json` + `print.jsontoolpath` + thumbnails exist.
- [ ] (Optional) Upload to Digital Factory; printing should work even if preview is skipped.

## G. Optional DF preview tuning
- [ ] If preview errors, try env vars:

ORCA_MB_MAX_CMDS=18000
ORCA_MB_RDP_EPS_BASE=0.10
ORCA_MB_RDP_EPS_MAX=0.25
ORCA_MB_TRAVEL_MIN_DXY=0.02
