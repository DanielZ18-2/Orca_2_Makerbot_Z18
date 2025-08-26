
# Environment variables

| Name                     | Default  | Meaning |
|--------------------------|----------|---------|
| `ORCA_MB_MODE`           | `normal` | `normal` = minimal surface simplification; `fuzzy` = no surface simplification at all |
| `ORCA_MB_MAX_CMDS`       | `20000`  | Target maximum for total commands (adaptive simplification) |
| `ORCA_MB_RDP_EPS_BASE`   | `auto`   | Base epsilon for non-surface RDP: `auto` = `max(0.05, 0.2*nozzle)` |
| `ORCA_MB_RDP_EPS_MAX`    | `0.20`   | Upper bound for adaptive epsilon |
| `ORCA_MB_FEED_TOL`       | `1.0`    | Allowed feedrate delta before splitting polylines (mm/s) |
| `ORCA_MB_TRAVEL_MIN_DXY` | `0.01`   | Travel micro-move filter threshold (mm) |
| `ORCA_MB_BED_X`          | `305`    | Bed size X (mm) |
| `ORCA_MB_BED_Y`          | `305`    | Bed size Y (mm) |

**Tip:** If Ultimaker Digital Factory preview still says “model is too large”, try:
ORCA_MB_MAX_CMDS=18000 ORCA_MB_RDP_EPS_BASE=0.10 ORCA_MB_RDP_EPS_MAX=0.25 ORCA_MB_TRAVEL_MIN_DXY=0.02
