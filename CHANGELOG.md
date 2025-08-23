# Changelog

## 1.0.0 – Orca_2_Makerbot_Z18 v1.0
- First public release.
- Full parsing from Orca G-code → `print.jsontoolpath` + `meta.json` (no templates).
- Fuzzy-skin friendly: no simplification on surface perimeters; adaptive RDP on non-surface moves.
- Centered Z18 coordinate system; correct bounding box from extrusions.
- Thumbnails packaged if present; `.makerbot` output next to the G-code.
