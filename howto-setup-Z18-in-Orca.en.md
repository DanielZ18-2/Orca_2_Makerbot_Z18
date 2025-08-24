# MakerBot Replicator Z18 – How-to Setup (Orca Slicer 2.3+)

This guide shows how to:
1) Download Orca Slicer
2) Complete the initial Orca wizard (generic Marlin, 0.4 mm nozzle)
3) Create a new “MakerBot Replicator Z18” printer in Orca (with all parameters)
4) Import `Orca_Z18_MasterBundle.zip` and finish the final tweaks

> Notes
> - Z18 has a **heated chamber** but **no heated bed**. Bed temperature must remain `0`.
> - Coordinates are **centered** on Z18. During the first printer creation Orca only allows **152.0 mm** for the bed center. After importing the bundle, correct it to **152.5 mm** in each printer profile.
> - Use the bed model **`print_bed_makerbot_replicator_z18.stl`** (in older videos named `makerbot_replicator_z18.stl`).

---

## 1) Download Orca Slicer

- Official GitHub: https://github.com/SoftFever/OrcaSlicer  
- Download the installer for your OS and install Orca Slicer 2.3+.

---

## 2) Run the Orca first-run wizard (base setup)

1. Start Orca Slicer → the setup wizard opens.
2. Add a **Generic Marlin** printer with a **0.4 mm** nozzle.
3. Finish the wizard.  
   This creates a baseline profile; we’ll add the Z18 as a new printer next.

---

## 3) Create a new printer: “MakerBot Replicator Z18”

In Orca: **Printer Settings → Machine → Add new printer** and fill in:

### 3.1 Identification
- **Name:** `MakerBot Replicator Z18`
- **G-code flavor:** `Marlin` (Z18 accepts standard Marlin-style G-code)
- **Number of extruders:** `1`

### 3.2 Build volume & bed model
- **Bed shape:** Rectangular  
  **Size (X × Y):** `305 × 305 mm`  
  **Z height:** `457 mm`
- **Origin / Center:** set **X = 152.0 mm, Y = 152.0 mm** *(Orca limits to 152.0 here)*  
  You will **correct this to 152.5 mm** later after importing the bundle.
- **Heated bed:** **Disabled** (Z18 has no heated bed)
- **Custom bed model:** load **`print_bed_makerbot_replicator_z18.stl`**  
  (Menu: *Printer Settings → Machine → Bed model → Load STL*)

### 3.3 Nozzle
- **Default nozzle diameter:** `0.4 mm` (you can add other nozzles later via profiles)

### 3.4 Start & End G-code (copy & paste)

> Where to paste: **Printer Settings → Custom G-code → Start G-code / End G-code**  
> Choose the block that matches your extruder.  
> These sequences keep things simple for the Z18: absolute units, home, safe Z, and no bed heat.

**Smart Extruder+** (tool tag `mk13`)
```gcode
; makerbot_tool_type = mk13
G21                      ; metric
G90                      ; absolute XYZ
M82                      ; absolute E
M107                     ; fan off
G28 X0 Y0 Z0             ; home all
G92 E0                   ; reset extruder
G1 Z35 F9000             ; lift to safe Z
G1 X152.5 Y152.5 F15000  ; move to bed center (305x305 -> 152.5,152.5)
; Optional: prime line near front (uncomment if desired)

**Tough Smart Extruder+** (tool tag mk13_impla)
```gcode
; makerbot_tool_type = mk13_impla
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optional prime line (disabled by default)

**LABS Extruder** (tool tag mk13_experimental)
```gcode
; makerbot_tool_type = mk13_experimental
G21
G90
M82
M107
G28 X0 Y0 Z0
G92 E0
G1 Z35 F9000
G1 X152.5 Y152.5 F15000
; Optional prime line (disabled by default)

**Common End G-code** (all extruders)
```gcode
; --- End ---
M104 S0                  ; cool down hotend
M107                     ; fan off
G91                      ; relative
G1 Z10 F3000             ; lift
G90                      ; absolute
G92 E0
G1 E-2 F1800             ; small retract
M84                      ; motors off

Chamber heating is not controlled here; if you want it, set it on the Z18 panel.

Click Save to store the new printer.

; G1 X40 Y10 Z0.30 F9000
; G1 X260 Y10 E8.0 F900
