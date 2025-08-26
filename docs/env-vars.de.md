
# Umgebungsvariablen

| Name                     | Standard | Bedeutung |
|--------------------------|----------|-----------|
| `ORCA_MB_MODE`           | `normal` | `normal` = minimale Vereinfachung der Außenhaut; `fuzzy` = keinerlei Vereinfachung der Außenhaut |
| `ORCA_MB_MAX_CMDS`       | `20000`  | Ziel-Obergrenze der Gesamtbefehle (adaptive Vereinfachung) |
| `ORCA_MB_RDP_EPS_BASE`   | `auto`   | Start-Epsilon für Nicht-Surface-RDP: `auto` = `max(0.05, 0.2*nozzle)` |
| `ORCA_MB_RDP_EPS_MAX`    | `0.20`   | Obergrenze für adaptives Epsilon |
| `ORCA_MB_FEED_TOL`       | `1.0`    | Erlaubte Feed-Änderung vor Polyline-Splitting (mm/s) |
| `ORCA_MB_TRAVEL_MIN_DXY` | `0.01`   | Schwelle für Travel-Mikrobewegungen (mm) |
| `ORCA_MB_BED_X`          | `305`    | Bettgröße X (mm) |
| `ORCA_MB_BED_Y`          | `305`    | Bettgröße Y (mm) |

**Tipp:** Falls Ultimaker Digital Factory weiterhin „model is too large“ meldet:
ORCA_MB_MAX_CMDS=18000 ORCA_MB_RDP_EPS_BASE=0.10 ORCA_MB_RDP_EPS_MAX=0.25 ORCA_MB_TRAVEL_MIN_DXY=0.02
