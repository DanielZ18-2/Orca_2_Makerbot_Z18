#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Orca_gcode_2_Makerbot_Z18.py — v11.5a

Env-Tuning:
  ORCA_MB_MODE=fuzzy|normal
  ORCA_MB_MAX_CMDS=20000
  ORCA_MB_RDP_EPS_BASE=auto
  ORCA_MB_RDP_EPS_MAX=0.20
  ORCA_MB_FEED_TOL=1.0
  ORCA_MB_TRAVEL_MIN_DXY=0.01
  ORCA_MB_BED_X=305
  ORCA_MB_BED_Y=305
"""

import os, re, sys, time, math, json, zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple, Union

# ---------- Pfade & Wartezeiten ----------
WATCH_DIR = (Path(os.environ.get("USERPROFILE","")) / "Makerbot_files" / "Orca_Slicer") if os.name=="nt" else (Path.home()/ "Makerbot_files" / "Orca_Slicer")
WAIT_AFTER_WRITE_S = 1.5
NO_GCODE_MSG_DELAY_S = 3.0

# ---------- Bett & RDP/Filter ----------
BED_X = float(os.environ.get("ORCA_MB_BED_X", 305.0))
BED_Y = float(os.environ.get("ORCA_MB_BED_Y", 305.0))
FEED_TOL = float(os.environ.get("ORCA_MB_FEED_TOL", 1.0))
TRAVEL_MIN_DXY = float(os.environ.get("ORCA_MB_TRAVEL_MIN_DXY", 0.01))
MAX_COMMANDS_TARGET = int(os.environ.get("ORCA_MB_MAX_CMDS", 20000))
RDP_EPS_MAX = float(os.environ.get("ORCA_MB_RDP_EPS_MAX", 0.20))
MODE = os.environ.get("ORCA_MB_MODE", "normal").strip().lower()  # 'normal' | 'fuzzy'

# ---------- Rundungen ----------
ROUND_XY = 3; ROUND_Z = 3; ROUND_E = 5

# ---------- Thumbnails ----------
THUMBS = [
    "isometric_thumbnail_120x120.png",
    "isometric_thumbnail_320x320.png",
    "isometric_thumbnail_640x640.png",
    "thumbnail_55x40.png",
    "thumbnail_110x80.png",
    "thumbnail_320x200.png",
]

# ---------- Materialien ----------
DENSITY = {"pla":1.24,"abs":1.04,"asa":1.07,"petg":1.27,"tpu":1.21,"nylon":1.14,"pc":1.20,"pva":1.19}
DEFAULT_MATERIAL = "pla"
DEFAULT_TOOLTYPE = "mk13"  # Smart Extruder+
MB_PREF_BOUNDS = [152.5, 187.5, -152.5, -187.5]

FLOAT_RE = r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))"

# ---------- Helpers ----------
def _norm_float(tok: str) -> float:
    tok = tok.strip()
    if tok.startswith("."): tok = "0"+tok
    elif tok.startswith("+.") and len(tok)>1: tok = "+0"+tok[1:]
    elif tok.startswith("-.") and len(tok)>2: tok = "-0"+tok[1:]
    return float(tok)

def _parse_time_s(human: str) -> float:
    d=h=m=s=0
    mo=re.search(r"(\d+)\s*d", human); d=int(mo.group(1)) if mo else 0
    mo=re.search(r"(\d+)\s*h", human); h=int(mo.group(1)) if mo else 0
    mo=re.search(r"(\d+)\s*m", human); m=int(mo.group(1)) if mo else 0
    mo=re.search(r"(\d+)\s*s", human); s=int(mo.group(1)) if mo else 0
    return d*86400+h*3600+m*60+s

def _latest_gcode(dirpath: Path):
    files = sorted([p for p in dirpath.glob("*.gcode") if p.is_file() and not p.name.startswith(".")], key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

def _sleep_stable(p: Path, secs: float):
    t0 = p.stat().st_mtime
    time.sleep(secs)
    if p.stat().st_mtime != t0:
        time.sleep(secs)

# ---------- RDP ----------
def _point_line_distance_xy(p, a, b) -> float:
    (px,py) = (p[0], p[1]); (ax,ay) = (a[0], a[1]); (bx,by) = (b[0], b[1])
    vx = bx-ax; vy = by-ay
    wx = px-ax; wy = py-ay
    v2 = vx*vx + vy*vy
    if v2 <= 1e-18: return math.hypot(px-ax, py-ay)
    t = max(0.0, min(1.0, (wx*vx + wy*vy)/v2))
    cx = ax + t*vx; cy = ay + t*vy
    return math.hypot(px-cx, py-cy)

def _rdp_xy(points, eps):
    if len(points) <= 2: return points[:]
    idx_max=-1; dmax=-1.0
    a=points[0]; b=points[-1]
    for i in range(1,len(points)-1):
        d=_point_line_distance_xy(points[i],a,b)
        if d>dmax: idx_max=i; dmax=d
    if dmax>eps:
        left=_rdp_xy(points[:idx_max+1],eps)
        right=_rdp_xy(points[idx_max:],eps)
        return left[:-1]+right
    return [a,b]

# ---------- Datenstrukturen ----------
@dataclass
class Header:
    duration_s: float = 0.0
    total_layers: Optional[int] = None
    max_z: float = 0.0
    min_z: float = 0.0
    material: str = DEFAULT_MATERIAL
    filament_diam: float = 1.75
    volumetric: bool = False
    tool_type: str = DEFAULT_TOOLTYPE
    object_name: Optional[str] = None
    extruder_temp: Optional[int] = None
    base_layer: str = "none"  # "none" | "raft"
    nozzle_diam: float = 0.4

# EX: ("EX", (feature, [ (x,y,z,a,f), ... ]))
# TR: ("TR", (x,y,z,f))
Segment = Union[
    Tuple[str, Tuple[str, List[Tuple[float,float,float,float,Optional[float]]]]],
    Tuple[str, Tuple[Optional[float],Optional[float],Optional[float],Optional[float]]]
]

@dataclass
class Parsed:
    segments: List[Segment]
    header: Header
    bbox_raw_xy: Tuple[Optional[float],Optional[float],Optional[float],Optional[float]]

# Feature-Mapping (Orca Kommentare)
SURFACE_TYPES = {"WALL-OUTER", "SKIN", "TOP", "BOTTOM", "WALL-OUTER SKIN"}

# ---------- Parser ----------
def parse_gcode(gpath: Path) -> Parsed:
    H=Header()
    # Header regex
    re_time = re.compile(r";\s*estimated printing time.*=\s*(.+)", re.I)
    re_layers = re.compile(r";\s*total layer number\s*[:=]\s*(\d+)", re.I)
    re_maxz = re.compile(r";\s*max[_ ]?z[_ ]?height\s*[:=]\s*([0-9.+-]+)", re.I)
    re_minz = re.compile(r";\s*(?:z_min|first_layer_height)\s*[:=]\s*([0-9.+-]+)", re.I)
    re_mat   = re.compile(r";\s*filament_type\s*[:=]\s*([a-z0-9_+\-]+)", re.I)
    re_diam_hdr  = re.compile(r";\s*filament_?diameter(?:\[\d+\])?\s*[:=]\s*([0-9.+-]+)", re.I)
    re_noz  = re.compile(r";\s*nozzle_?diameter(?:\[\d+\])?\s*[:=]\s*([0-9.+-]+)", re.I)
    re_obj   = re.compile(r";\s*printing object\s+(.+)", re.I)
    re_tool  = re.compile(r";\s*makerbot_tool_type\s*=\s*(mk13(?:_impla|_experimental)?)", re.I)
    re_raft1 = re.compile(r";\s*type\s*:\s*RAFT", re.I)
    re_raft2 = re.compile(r";\s*raft\s*[:=]\s*(on|true|1)", re.I)
    re_type  = re.compile(r";\s*TYPE\s*:\s*(.+)", re.I)

    re_code = re.compile(r"^([GMT]\d+)", re.I)
    re_word = re.compile(rf"([XYZEF]){FLOAT_RE}", re.I)

    abs_xyz=True; abs_e=True
    x=y=z=None
    e=0.0; e_offset=0.0; a_mm=0.0
    last_f=None
    cur_feature = "UNKNOWN"

    xmin=ymin=xmax=ymax=None

    segments: List[Segment]=[]
    current_poly: List[Tuple[float,float,float,float,Optional[float]]] = []
    current_feature = cur_feature
    poly_z=None; poly_f=None

    travel_buf = {"x":None,"y":None,"z":None,"f":None}

    def close_poly():
        nonlocal current_poly, poly_z, poly_f, current_feature
        if current_poly:
            segments.append(("EX", (current_feature, current_poly)))
        current_poly=[]; poly_z=None; poly_f=None

    def flush_travel_if_any():
        nonlocal travel_buf
        if any(v is not None for v in travel_buf.values()):
            segments.append(("TR", (travel_buf["x"], travel_buf["y"], travel_buf["z"], travel_buf["f"])))
            travel_buf={"x":None,"y":None,"z":None,"f":None}

    with gpath.open("r", encoding="utf-8", errors="ignore") as fh:
        for raw in fh:
            s=raw.strip()

            m=re_type.match(s)
            if m:
                cur_feature = m.group(1).strip().upper()
                if current_poly and cur_feature != current_feature:
                    close_poly()
                    current_feature = cur_feature
                else:
                    current_feature = cur_feature

            m=re_time.search(s)
            if m and H.duration_s==0.0:
                try: H.duration_s=_parse_time_s(m.group(1))
                except: pass
            m=re_layers.search(s)
            if m and H.total_layers is None:
                try: H.total_layers=int(m.group(1))
                except: pass
            m=re_maxz.search(s)
            if m:
                try: H.max_z=max(H.max_z, float(m.group(1)))
                except: pass
            m=re_minz.search(s)
            if m and H.min_z==0.0:
                try: H.min_z=float(m.group(1))
                except: pass
            m=re_mat.search(s)
            if m and not H.material:
                H.material=m.group(1).strip().lower()
            m=re_diam_hdr.search(s)
            if m:
                try: H.filament_diam=float(m.group(1))
                except: pass
            m=re_noz.search(s)
            if m:
                try: H.nozzle_diam=float(m.group(1))
                except: pass
            m=re_obj.search(s)
            if m and H.object_name is None:
                rawname=m.group(1).strip()
                rawname=re.split(r"\s+(?:id:|copy\s+\d+)", rawname)[0]
                rawname=re.sub(r"\.(stl|obj|3mf)$","", rawname, flags=re.I)
                H.object_name=os.path.basename(rawname)
            m=re_tool.search(s)
            if m: H.tool_type=m.group(1).lower()
            if re_raft1.search(s) or re_raft2.search(s):
                H.base_layer="raft"

            m=re_code.match(s); code = m.group(1).upper() if m else ""
            if code.startswith("M200"):
                dm = re.search(r"[Dd]\s*"+FLOAT_RE, s)
                if dm:
                    try:
                        d=_norm_float(dm.group(1))
                        if d>0: H.filament_diam=d; H.volumetric=True
                        else: H.volumetric=False
                    except: pass
                continue
            if code=="M82": abs_e=True;  continue
            if code=="M83": abs_e=False;  continue
            if code in ("M104","M109"):
                tm=re.search(r"[Ss]\s*(\d+)", s)
                if tm:
                    try: H.extruder_temp=int(tm.group(1))
                    except: pass
            if code=="G90": abs_xyz=True;  continue
            if code=="G91": abs_xyz=False;  continue
            if code.startswith("G92"):
                for k,v in re_word.findall(s):
                    if k.upper()=="E":
                        e_new=_norm_float(v)
                        e_offset += (e_new - e)
                        e=e_new
                continue

            if code not in ("G0","G1"):
                continue

            words=dict((k.upper(), v) for k,v in re_word.findall(s))
            if not words: continue

            x_new=x; y_new=y; z_new=z; f=last_f
            if "X" in words:
                dx=_norm_float(words["X"]); x_new = dx if abs_xyz or x is None else (x + dx)
            if "Y" in words:
                dy=_norm_float(words["Y"]); y_new = dy if abs_xyz or y is None else (y + dy)
            if "Z" in words:
                dz=_norm_float(words["Z"]); z_new = dz if abs_xyz or z is None else (z + dz)
            if "F" in words:
                f=_norm_float(words["F"]) / 60.0
            if "E" in words:
                v=_norm_float(words["E"])
                e_new = v if abs_e else (e + v)
            else:
                e_new = e

            de = (e_new - e) if abs_e else (_norm_float(words["E"]) if "E" in words else 0.0)
            has_xy = ("X" in words) or ("Y" in words)
            is_extrude = ("E" in words) and (de>0.0) and has_xy

            delta_a_mm = 0.0
            if is_extrude:
                if H.volumetric:
                    area = math.pi*(H.filament_diam*0.5)**2
                    if area>0: delta_a_mm = de / area
                else:
                    delta_a_mm = de

            if is_extrude:
                flush_travel_if_any()
                if current_poly and (
                    (poly_z is None or z_new is None or abs((z_new or 0)-(poly_z or 0))>1e-6) or
                    (poly_f is None or (f is not None and abs(f - poly_f)>FEED_TOL))
                ):
                    segments.append(("EX", (current_feature, current_poly)))
                    current_poly=[]; poly_z=None; poly_f=None
                if not current_poly:
                    poly_z = z_new
                    poly_f = f

                if x_new is not None and y_new is not None:
                    xmin = x_new if xmin is None else min(xmin, x_new)
                    xmax = x_new if xmax is None else max(xmax, x_new)
                    ymin = y_new if ymin is None else min(ymin, y_new)
                    ymax = y_new if ymax is None else max(ymax, y_new)
                if z_new is not None:
                    H.max_z = max(H.max_z, z_new)
                    if H.min_z==0.0: H.min_z = z_new

                a_mm += delta_a_mm
                current_poly.append((x_new, y_new, (z_new if z_new is not None else (poly_z or 0.0)), a_mm, (f if f is not None else poly_f)))
            else:
                if current_poly:
                    segments.append(("EX", (current_feature, current_poly)))
                    current_poly=[]; poly_z=None; poly_f=None
                if has_xy or ("Z" in words) or ("F" in words):
                    if x_new is not None: travel_buf["x"]=x_new
                    if y_new is not None: travel_buf["y"]=y_new
                    if z_new is not None: travel_buf["z"]=z_new
                    if f is not None:     travel_buf["f"]=f

            x,y,z,e = x_new, y_new, z_new, e_new
            if f is not None: last_f=f

    if current_poly:
        segments.append(("EX", (current_feature, current_poly)))
    if any(v is not None for v in travel_buf.values()):
        segments.append(("TR", (travel_buf["x"], travel_buf["y"], travel_buf["z"], travel_buf["f"])))

    H.material = (H.material or DEFAULT_MATERIAL).lower()
    return Parsed(segments=segments, header=H, bbox_raw_xy=(xmin,xmax,ymin,ymax))

# ---------- Transform & Toolpath (adaptiv) ----------
def _build_with_eps(parsed: Parsed, eps_nonsurface: float, eps_surface: float):
    H=parsed.header
    xmin,xmax,ymin,ymax = parsed.bbox_raw_xy
    needs_shift=False
    if xmin is not None and xmax is not None and ymin is not None and ymax is not None:
        needs_shift = (xmin >= -1.0 and ymin >= -1.0 and xmax <= BED_X+1.0 and ymax <= BED_Y+1.0)
    sx = BED_X/2.0 if needs_shift else 0.0
    sy = BED_Y/2.0 if needs_shift else 0.0

    toolpath=[]
    bxmin=bxmax=bymin=bymax=None
    last_out_x=None; last_out_y=None
    filament_mm_total = 0.0

    for kind, payload in parsed.segments:
        if kind=="EX":
            feature, points = payload
            if not points: continue
            feature_up = (feature or "").upper()
            is_surface = (feature_up in SURFACE_TYPES)
            eps = eps_surface if is_surface else eps_nonsurface
            simp = points if (len(points)<=2 or eps<=0.0) else _rdp_xy(points, eps)
            for (px,py,pz,pa,pf) in simp:
                x = round(px - sx, ROUND_XY) if px is not None else None
                y = round(py - sy, ROUND_XY) if py is not None else None
                z = round(pz, ROUND_Z)       if pz is not None else None
                a = round(pa, ROUND_E)
                params={}
                if x is not None: params["x"]=x
                if y is not None: params["y"]=y
                if z is not None: params["z"]=z
                params["a"]=a
                if pf is not None: params["feedrate"]=round(pf,0)
                toolpath.append({"function":"move","parameters":params})
                if x is not None:
                    bxmin = x if bxmin is None else min(bxmin, x)
                    bxmax = x if bxmax is None else max(bxmax, x)
                if y is not None:
                    bymin = y if bymin is None else min(bymin, y)
                    bymax = y if bymax is None else max(bymax, y)
                last_out_x = x if x is not None else last_out_x
                last_out_y = y if y is not None else last_out_y
                filament_mm_total = max(filament_mm_total, pa)
        else:
            (tx,ty,tz,tf)=payload
            emit = True
            if tx is not None or ty is not None:
                if last_out_x is not None and last_out_y is not None and tx is not None and ty is not None:
                    dxy = math.hypot((tx - sx) - last_out_x, (ty - sy) - last_out_y)
                    if dxy < TRAVEL_MIN_DXY:
                        emit = False
            if emit:
                params={}
                if tx is not None: params["x"]=round(tx - sx, ROUND_XY)
                if ty is not None: params["y"]=round(ty - sy, ROUND_XY)
                if tz is not None: params["z"]=round(tz, ROUND_Z)
                if tf is not None: params["feedrate"]=round(tf,0)
                if params:
                    toolpath.append({"function":"move","parameters":params})
                    if "x" in params: last_out_x = params["x"]
                    if "y" in params: last_out_y = params["y"]

    if bxmin is None:
        bxmin=bxmax=bymin=bymax=0.0
    bbox_xy = {"x_min":bxmin,"x_max":bxmax,"y_min":bymin,"y_max":bymax}
    return toolpath, bbox_xy, filament_mm_total, len(toolpath)

def transform_and_build_adaptive(parsed: Parsed):
    H=parsed.header
    base_str = os.environ.get("ORCA_MB_RDP_EPS_BASE", "auto").strip().lower()
    if base_str == "auto":
        eps_nonsurface = max(0.05, 0.2 * max(0.1, H.nozzle_diam or 0.4))
    else:
        try: eps_nonsurface = float(base_str)
        except: eps_nonsurface = max(0.05, 0.2 * max(0.1, H.nozzle_diam or 0.4))
    eps_surface = 0.0 if MODE == "fuzzy" else 0.005

    cur_eps = eps_nonsurface
    best = None
    while True:
        toolpath, bbox_xy, filament_mm_total, ncmd = _build_with_eps(parsed, cur_eps, eps_surface)
        best = (toolpath, bbox_xy, filament_mm_total, ncmd, cur_eps)
        if ncmd <= MAX_COMMANDS_TARGET or cur_eps >= RDP_EPS_MAX:
            break
        cur_eps = min(RDP_EPS_MAX, cur_eps * 1.10)
    return best

# ---------- meta.json ----------
def build_meta(H, bbox_xy: dict, filament_mm_total: float, total_cmds: int):
    area = math.pi*(H.filament_diam*0.5)**2
    vol_mm3 = filament_mm_total * area
    rho = DENSITY.get(H.material.lower(), 1.24)
    mass_g = vol_mm3/1000.0 * rho

    meta = {
        "bot_type": "z18_6",
        "bounding_box": {
            "x_max": float(round(bbox_xy["x_max"], ROUND_XY)),
            "x_min": float(round(bbox_xy["x_min"], ROUND_XY)),
            "y_max": float(round(bbox_xy["y_max"], ROUND_XY)),
            "y_min": float(round(bbox_xy["y_min"], ROUND_XY)),
            "z_max": float(round(max(H.max_z, H.min_z), ROUND_Z)),
            "z_min": float(round(H.min_z, ROUND_Z))
        },
        "chamber_temperature": 0,
        "commanded_duration_s": H.duration_s,
        "duration_s": H.duration_s,
        **({"extruder_temperature": H.extruder_temp, "extruder_temperatures":[H.extruder_temp]} if H.extruder_temp else {}),
        "extrusion_distance_mm": filament_mm_total,
        "extrusion_distances_mm": [filament_mm_total],
        "extrusion_mass_g": mass_g,
        "extrusion_masses_g": [mass_g],
        "grue_git_commit_hash": "fdd251c",
        "grue_version": "7.18.3",
        "libthing_git_commit_hash": "fc3552c",
        "libthing_version": "5.29.1",
        "material": H.material,
        "materials": [H.material],
        "miracle_config": {
            "_bot":"z18_6",
            "_extruders":[H.tool_type or DEFAULT_TOOLTYPE],
            "_materials":[H.material],
            "version":"1.2.0",
            "gaggles":{
                "instance0":{
                    "_baseLayer": ("raft" if H.base_layer=="raft" else "none"),
                    "_printMode":"balanced",
                    "_supportType":"none"
                }
            }
        },
        "model_counts":[{"count":1,"name":"instance0"}],
        "num_tool_changes": 0,
        **({"num_z_layers": int(H.total_layers), "num_z_transitions": int(H.total_layers)} if H.total_layers is not None else {}),
        "platform_temperature": 0,
        "preferences": {"instance0":{"machineBounds": MB_PREF_BOUNDS, "printMode":"balanced"}},
        "sliceconfig_git_commit_hash":"fdd251c",
        "sliceconfig_version":"7.18.3",
        "tool_type": H.tool_type or DEFAULT_TOOLTYPE,
        "tool_types": [H.tool_type or DEFAULT_TOOLTYPE],
        "total_commands": total_cmds,
        "uuid": os.urandom(16).hex(),
        "version": "1.2.0",
    }
    return meta

# ---------- ZIP schreiben ----------
def build_zip(gcode_path: Path, meta: dict, toolpath: List[dict], base_name: Optional[str]):
    out_name = (base_name if base_name else gcode_path.stem) + ".makerbot"
    out_path = gcode_path.parent / out_name
    with zipfile.ZipFile(str(out_path), mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("meta.json", json.dumps(meta, indent=3, ensure_ascii=False))
        z.writestr("print.jsontoolpath", json.dumps(toolpath, separators=(",",":"), ensure_ascii=False))
        for t in THUMBS:
            p = WATCH_DIR / t
            if p.exists():
                z.write(str(p), arcname=t)
    print(str(out_path))
    return out_path

def derive_basename_from_header(gcode_path: Path) -> Optional[str]:
    try:
        with gcode_path.open("r", encoding="utf-8", errors="ignore") as fh:
            for _ in range(400):
                s=fh.readline()
                if not s: break
                m=re.match(r";\s*printing object\s+(.+)", s, re.I)
                if m:
                    raw=m.group(1).strip()
                    raw=re.split(r"\s+(?:id:|copy\s+\d+)", raw)[0]
                    raw=re.sub(r"\.(stl|obj|3mf|gcode)$","", raw, flags=re.I)
                    base=os.path.basename(raw)
                    base=re.sub(r"[^\w\-.]+","_", base).strip("._")
                    return base or None
    except Exception:
        pass
    return None

# ---------- Main ----------
def main(argv):
    gpath=None
    for tok in argv[1:][::-1]:
        if not tok or tok.startswith("--"): continue
        t=tok.strip().strip('"').strip("'")
        if not t: continue
        if t.lower().endswith(".gcode") or Path(t).exists():
            gpath=Path(t); break
    if gpath is None:
        gpath=_latest_gcode(WATCH_DIR)
        if not gpath:
            time.sleep(NO_GCODE_MSG_DELAY_S)
            print("No gcode file found"); return 2
    if not gpath.exists():
        print(f"[ERROR] G-code not found: {gpath}", file=sys.stderr); return 2

    _sleep_stable(gpath, WAIT_AFTER_WRITE_S)

    parsed = parse_gcode(gpath)
    toolpath, bbox_xy, filament_mm_total, ncmd, used_eps = transform_and_build_adaptive(parsed)
    meta = build_meta(parsed.header, bbox_xy, filament_mm_total, ncmd)

    base = derive_basename_from_header(gpath) or gpath.stem
    build_zip(gpath, meta, toolpath, base)
    return 0

if __name__=="__main__":
    sys.exit(main(sys.argv))
