import sys
import os
from pathlib import Path
import numpy as np

sys.path.insert(0, r"E:\creacion-mods\enigma-dynamo")
sys.path.insert(0, r"E:\creacion-mods\enigma-dynamo\pipeline")
sys.path.insert(0, r"E:\creacion-mods\enigma-dynamo\tools")
from coords import blender_to_dmx, blender_dir_to_dmx, uv_blender_to_dmx
import datamodel as dm

JOINTS_PER_VERTEX = 4

def _mesh_parts(d):
    model = d.root["model"]
    dag = next(c for c in model["children"] if c.type == "DmeDag")
    mesh = dag["shape"]
    return model, dag, mesh, mesh["currentState"]

def generate_multimat_dmx(template: Path, npz: Path, out: Path) -> None:
    d = dm.load(str(template))
    model, dag, mesh, vd = _mesh_parts(d)
    joint_index = {j.name: i for i, j in enumerate(model["jointList"])}
    data = np.load(npz)
    bones, values = data["weight_bones"], data["weight_values"]
    missing = sorted({b for row in bones for b in row if b and b not in joint_index})
    if missing:
        raise ValueError(f"Huesos no presentes en jointList: {missing}")

    pos = blender_to_dmx(data["positions"])
    nrm = blender_dir_to_dmx(data["normals"])
    tan = np.array(data["tangents"], dtype=float)
    tan[:, :3] = blender_dir_to_dmx(tan[:, :3])
    uvs = uv_blender_to_dmx(data["uvs"])
    n = len(pos)

    blend_idx, blend_w = [], []
    for row_b, row_w in zip(bones, values):
        for b, w in zip(row_b[:JOINTS_PER_VERTEX], row_w[:JOINTS_PER_VERTEX]):
            blend_idx.append(joint_index[b] if b else 0)
            blend_w.append(float(w) if b else 0.0)

    seq = list(range(n))
    vd["jointCount"] = JOINTS_PER_VERTEX
    vd["position$0"] = dm.make_array([dm.Vector3(p) for p in pos.tolist()], dm.Vector3)
    vd["normal$0"] = dm.make_array([dm.Vector3(p) for p in nrm.tolist()], dm.Vector3)
    vd["tangent$0"] = dm.make_array([dm.Vector4(p) for p in tan.tolist()], dm.Vector4)
    vd["texcoord$0"] = dm.make_array([dm.Vector2(p) for p in uvs.tolist()], dm.Vector2)
    for key in ("position$0", "normal$0", "tangent$0", "texcoord$0"):
        vd[key + "Indices"] = dm.make_array(seq, int)
    vd["blendindices$0"] = dm.make_array(blend_idx, int)
    vd["blendweights$0"] = dm.make_array(blend_w, float)

    tris = data["tris"]
    tri_mats = data["tri_materials"]
    mat_names = data["material_names"]

    face_sets = []
    for idx, mat_name in enumerate(mat_names):
        mask = (tri_mats == idx)
        part_tris = tris[mask]
        if len(part_tris) == 0:
            continue
        flat = []
        for a, b, c in part_tris.tolist():
            flat += [int(a), int(b), int(c), -1]
        
        fs = dm.Element(d, f"faceset_{idx}", "DmeFaceSet")
        mat = dm.Element(d, f"material_{idx}", "DmeMaterial")
        mat["mtlName"] = str(mat_name)
        fs["material"] = mat
        fs["faces"] = dm.make_array(flat, int)
        face_sets.append(fs)
        print(f"FaceSet {idx} [{mat_name}]: {len(part_tris)} tris")

    mesh["faceSets"] = dm.make_array(face_sets, dm.Element)
    mesh["baseStates"] = dm.make_array([vd], dm.Element)
    dag.name = "windrunner_classic"

    out.parent.mkdir(parents=True, exist_ok=True)
    d.write(str(out), "binary", 9)
    print(f"[EXITO] DMX multi-material generado en {out} ({os.path.getsize(out):,} bytes)")

if __name__ == "__main__":
    base_dir = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock")
    template_dmx = base_dir / r"extracted\archer\models\heroes_staging\archer\archer_body.dmx"
    npz_path = base_dir / r"extracted\windrunner_classic_mesh.npz"
    out_dmx = base_dir / r"extracted\archer_windrunner_body.dmx"
    generate_multimat_dmx(template_dmx, npz_path, out_dmx)
