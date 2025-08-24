MakerBot Replicator Z18 – Setup Guide (Orca Slicer 2.3+)

This guide covers:

Downloading Orca Slicer from GitHub

Completing the first-run wizard (Generic Marlin, 0.4 mm)

Creating a new MakerBot Replicator Z18 printer (all required parameters)

Importing Orca_Z18_MasterBundle.zip and final tweaks (bed center 152.5 mm, bed STL, G-code per extruder, post-processing script)

Notes

The Z18 features a heated chamber, but no heated bed → set bed temperature to 0.

The Z18 uses a centered coordinate system. During initial printer creation, Orca only allows 152.0 mm as the bed center. After importing the bundle, change to 152.5 mm in each printer profile.

Use the bed model print_bed_makerbot_replicator_z18.stl (older video name: makerbot_replicator_z18.stl).

1) Download Orca Slicer

Official repository: https://github.com/SoftFever/OrcaSlicer

Download and install Orca Slicer 2.3+ for your OS.

2) Complete Orca’s first-run wizard (base setup)

Launch Orca Slicer → the setup wizard opens.

Add a Generic Marlin printer with a 0.4 mm nozzle.

Finish the wizard.
You now have a baseline profile. Next, we’ll add the Z18 as a dedicated printer.

3) Create a new printer: “MakerBot Replicator Z18”

In Orca, go to Printer Settings → Machine → Add new printer and enter:

3.1 Identification

Name: MakerBot Replicator Z18

G-code flavor: Marlin (the Z18 accepts Marlin-style G-code)

Number of extruders: 1

3.2 Build volume & bed model

Bed shape: Rectangular
Size (X × Y): 305 × 305 mm
Z height: 457 mm

Bed center (temporary): X = 152.0 mm, Y = 152.0 mm
(Orca’s UI limits this to 152.0 mm at creation time; you will correct it to 152.5 mm later in step 4.)

Heated bed: Disabled (Z18 has no heated bed)

Custom bed model: load print_bed_makerbot_replicator_z18.stl
(Printer Settings → Machine → Bed model → Load STL)

3.3 Nozzle

Default nozzle diameter: 0.4 mm
(You can use other nozzle diameters later via profiles.)

3.4 Start & End G-code (copy/paste)

Paste one of the following Start G-code blocks depending on your extruder, and the common End G-code.
Location: Printer Settings → Custom G-code → Start G-code / End G-code.

Smart Extruder+ (tool tag mk13)

; makerbot_tool_type = mk13
G21                      ; metric units
G90                      ; absolute XYZ
M82                      ; absolute E
M107                     ; fan off
G28 X0 Y0 Z0             ; home all axes
G92 E0                   ; reset extruder
G1 Z35 F9000             ; lift to safe Z
G1 X152.5 Y152.5 F15000  ; move to bed center (305x305 -> 152.5,152.5)
; Optional prime line (disabled):
; G1 X40 Y10 Z0.30 F9000
; G1 X260 Y10 E8.0 F900


Tough Smart Extruder+ (tool tag mk13_impla)

; makerbot_tool_type = mk13_impla
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optional prime line (disabled)


LABS Extruder (tool tag mk13_experimental)

; makerbot_tool_type = mk13_experimental
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optional prime line (disabled)


Common End G-code (all extruders)

; --- End ---
M104 S0                  ; cool down hotend
M107                     ; fan off
G91                      ; relative
G1 Z10 F3000             ; lift Z
G90                      ; absolute
G92 E0
G1 E-2 F1800             ; small retract
M84                      ; motors off


Chamber temperature is not controlled here; adjust on the Z18 panel if needed.

Click Save to store the printer.

4) Import the Z18 bundle and finalize the profiles

In Orca: File → Import Configs… and choose Orca_Z18_MasterBundle.zip.
This imports printer/process/material presets for all extruder/nozzle variants.

Open your Z18 printer profile(s) and adjust:

Bed center: change X = 152.0 → 152.5 mm and Y = 152.0 → 152.5 mm.

Bed model: (re)load print_bed_makerbot_replicator_z18.stl if needed.

Custom G-code: ensure the Start/End blocks match your extruder type.

Post-processing (Python script):

Linux

python3 "/home/<USER>/Makerbot_files/Orca_Slicer/Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"


Windows

python "C:\Users\<USER>\Makerbot_files\Orca_Slicer\Orca_gcode_2_Makerbot_Z18.py" "[output_filepath]"


Save your profiles.

Slice a model and export G-code → the script will create a .makerbot file next to the G-code.

If Digital Factory preview says “model is too large”, you can still upload and print.
For preview friendliness, reduce non-surface complexity via environment variables (see project docs).
