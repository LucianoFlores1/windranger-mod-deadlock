"""Encaje de las articulaciones de Enigma sobre las de Dynamo (numpy puro, sin bpy)."""
import numpy as np
from bone_map import BONE_MAP

WAIST = ["Root_0"] + [f"base0_{i}" for i in range(6)] + ["Spine_0"]
CHEST = ["Spine_1", "Spine_3"]
TORSO = WAIST + CHEST
REGIONS = ("arms", "chest", "waist", "clav")
HEAD = ["Head_0", "Head_1"]
FINGERS = ("thumb", "index", "mid", "ring")

def _rot_between(a, b):
    a = a / np.linalg.norm(a); b = b / np.linalg.norm(b)
    v = np.cross(a, b); c = float(a @ b)
    if c < -1 + 1e-9:
        axis = np.cross(a, [1.0, 0, 0])
        if np.linalg.norm(axis) < 1e-6:
            axis = np.cross(a, [0, 1.0, 0])
        axis /= np.linalg.norm(axis)
        return 2 * np.outer(axis, axis) - np.eye(3)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx / (1 + c)

def _affine(L, src, dst):
    M = np.eye(4); M[:3, :3] = L; M[:3, 3] = dst - L @ src
    return M

def segment_transform(e0, e1, d0, d1, thickness=1.0):
    a, b = e1 - e0, d1 - d0
    u = a / np.linalg.norm(a)
    s_len = np.linalg.norm(b) / np.linalg.norm(a)
    S = thickness * np.eye(3) + (s_len - thickness) * np.outer(u, u)
    return _affine(_rot_between(a, b) @ S, e0, d0)

def rigid_transform(e_dir, d_dir, e_pivot, d_pivot):
    return _affine(_rot_between(e_dir, d_dir), e_pivot, d_pivot)

def horizontal_scale(center, k):
    L = np.diag([k, k, 1.0])
    c = np.array([center[0], center[1], 0.0])
    return _affine(L, c, c)

def translation(dx, dy, dz):
    M = np.eye(4)
    M[:3, 3] = [dx, dy, dz]
    return M

def build_bone_transforms(eni, dyn, thickness, neck_drop=0.0, head_lift=0.0, region_thickness=None):
    """region_thickness: dict opcional {"arms","chest","waist","clav"} -> grosor por región;
    las regiones ausentes (o None) usan `thickness`."""
    missing = [b for b in BONE_MAP if b not in eni]
    if missing:
        raise ValueError(f"Faltan articulaciones de Enigma: {missing}")
    rt = dict(region_thickness or {})
    unknown = set(rt) - set(REGIONS)
    if unknown:
        raise ValueError(f"Regiones de grosor desconocidas: {sorted(unknown)}")
    k = {r: float(rt.get(r, thickness)) for r in REGIONS}
    mats = {}
    waist = horizontal_scale(dyn["spine_0"], k["waist"])
    chest = horizontal_scale(dyn["spine_0"], k["chest"])
    for b in WAIST:
        mats[b] = waist
    mats["Spine_1"] = chest
    mats["Spine_3"] = translation(0, 0, -neck_drop) @ chest
    for b in HEAD:
        mats[b] = translation(0, 0, head_lift)
    for s in ("L", "R"):
        e = lambda n: eni[f"{n}_{s}"]
        d = lambda n: dyn[f"{n}_{s}"]
        clav = segment_transform(e("clavicle"), e("bicep"), d("clavicle"), d("arm_upper"), k["clav"])
        clav = translation(0, 0, -neck_drop / 2) @ clav
        upper = segment_transform(e("bicep"), e("elbow"), d("arm_upper"), d("arm_lower"), k["arms"])
        lower = segment_transform(e("elbow"), e("wrist"), d("arm_lower"), d("hand"), k["arms"])
        hand = rigid_transform(e("wrist") - e("elbow"), d("hand") - d("arm_lower"), e("wrist"), d("hand"))
        mats[f"clavicle_{s}"] = clav
        mats[f"deltoid_{s}"] = mats[f"bicep_{s}"] = upper
        mats[f"elbow_{s}"] = mats[f"wrist_helper_{s}"] = lower
        mats[f"wrist_{s}"] = hand
        for f in FINGERS:
            for i in range(3):
                mats[f"{f}_{i}_{s}"] = hand
    return {b: mats[b] for b in BONE_MAP}

def apply_lbs(points, weights, mats):
    P = np.c_[points, np.ones(len(points))]
    wsum = weights.sum(1)
    out = np.einsum("vb,bij,vj->vi", weights, mats, P)[:, :3]
    ok = wsum > 1e-8
    out[ok] /= wsum[ok, None]
    out[~ok] = points[~ok]
    return out

def apply_lbs_normals(normals, weights, mats):
    N = np.linalg.inv(mats[:, :3, :3]).transpose(0, 2, 1)
    out = np.einsum("lb,bij,lj->li", weights, N, normals)
    bad = np.linalg.norm(out, axis=1) < 1e-8
    out[bad] = normals[bad]
    return out / np.linalg.norm(out, axis=1, keepdims=True)
