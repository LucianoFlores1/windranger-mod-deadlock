import sys
import os
import math
from mathutils import Matrix, Vector
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
import datamodel as dm
from pathlib import Path
import bpy
import numpy as np

JOINTS_PER_VERTEX = 4
INCH = 0.0254

def dmx_to_blender(v):
    v = np.asarray(v, dtype=float)
    return np.stack([-v[..., 0], -v[..., 1], v[..., 2]], axis=-1) * INCH

def blender_dir_to_dmx(v):
    v = np.asarray(v, dtype=float)
    return np.stack([-v[..., 0], -v[..., 1], v[..., 2]], axis=-1)

def blender_to_dmx(v):
    return blender_dir_to_dmx(v) / INCH

def uv_blender_to_dmx(uv):
    uv = np.asarray(uv, dtype=float)
    return np.stack([uv[..., 0], 1.0 - uv[..., 1]], axis=-1)

def build_bow():
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 1. Load ref bow for weight transfer
    bow_template_path = Path(r'extracted\archer_bow1_orig.dmx')
    info = read_dmx_mesh(bow_template_path)
    ref_pos = dmx_to_blender(info['positions'])

    me_ref = bpy.data.meshes.new("ref_mesh")
    me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
    me_ref.update()
    ref_bow = bpy.data.objects.new("ref_bow", me_ref)
    bpy.context.scene.collection.objects.link(ref_bow)

    bone_names = info['bones']
    weights = info['weights']
    for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
        for b_name, w in zip(b_row, w_row):
            if w > 0.001 and b_name:
                vg = ref_bow.vertex_groups.get(b_name) or ref_bow.vertex_groups.new(name=b_name)
                vg.add([vi], float(w), 'REPLACE')

    ref_center = np.mean(ref_pos, axis=0)
    ref_span = np.ptp(ref_pos, axis=0)
    print(f"Ref bow loaded: {len(me_ref.vertices)} verts, {len(ref_bow.vertex_groups)} groups.")
    print(f"Ref bow bounds: X=[{ref_pos[:,0].min():.2f}, {ref_pos[:,0].max():.2f}], Y=[{ref_pos[:,1].min():.2f}, {ref_pos[:,1].max():.2f}], Z=[{ref_pos[:,2].min():.2f}, {ref_pos[:,2].max():.2f}]")

    # 2. Import classic Windrunner bow
    wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
    bow_glb = os.path.join(wr_dir, "windrunner_bow.glb")
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=bow_glb)
    new_objs = set(bpy.context.scene.objects) - before

    classic_bow = None
    for o in new_objs:
        if o.type == 'MESH':
            classic_bow = o
        elif o.type == 'ARMATURE':
            bpy.data.objects.remove(o)

    if not classic_bow:
        raise RuntimeError("No mesh found in windrunner_bow.glb")

    # Clean classic bow
    if classic_bow.data.shape_keys:
        for kb in list(classic_bow.data.shape_keys.key_blocks):
            classic_bow.shape_key_remove(kb)
    classic_bow.vertex_groups.clear()
    classic_bow.modifiers.clear()

    # Rotate classic bow around Y by -90 degrees so length (+X) aligns to +Z, and curve (+Y) stays +Y
    rot_mat = Matrix.Rotation(math.radians(-90), 4, 'Y')
    classic_bow.data.transform(rot_mat)

    # Scale to match ref_bow vertical span
    verts = np.array([v.co for v in classic_bow.data.vertices])
    c_span = np.ptp(verts, axis=0)
    scale_factor = ref_span[2] / c_span[2]
    scale_mat = Matrix.Diagonal((scale_factor, scale_factor, scale_factor, 1.0))
    classic_bow.data.transform(scale_mat)

    # Translate to match ref center
    cur_center = np.mean([v.co for v in classic_bow.data.vertices], axis=0)
    diff = ref_center - cur_center
    trans_mat = Matrix.Translation(Vector(diff.tolist()))
    classic_bow.data.transform(trans_mat)

    verts_final = np.array([v.co for v in classic_bow.data.vertices])
    print(f"Fitted Classic bow bounds: X=[{verts_final[:,0].min():.2f}, {verts_final[:,0].max():.2f}], Y=[{verts_final[:,1].min():.2f}, {verts_final[:,1].max():.2f}], Z=[{verts_final[:,2].min():.2f}, {verts_final[:,2].max():.2f}]")

    # Material
    mat_bow = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_bow.vmat")
    classic_bow.data.materials.clear()
    classic_bow.data.materials.append(mat_bow)

    # 3. Transfer weights from ref_bow
    mod = classic_bow.modifiers.new("DataTransfer", "DATA_TRANSFER")
    mod.object = ref_bow
    mod.use_vert_data = True
    mod.data_types_verts = {'VGROUP_WEIGHTS'}
    mod.vert_mapping = 'NEAREST'
    bpy.context.view_layer.objects.active = classic_bow
    bpy.ops.object.datalayout_transfer(modifier=mod.name)
    bpy.ops.object.modifier_apply(modifier=mod.name)

    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    unweighted = [v.index for v in classic_bow.data.vertices if not any(g.weight > 0.001 for g in v.groups)]
    print(f"Classic bow: {len(classic_bow.data.vertices)} vertices, unweighted: {len(unweighted)}")
    if unweighted:
        vg_root = classic_bow.vertex_groups.get("weapon_hand_L") or classic_bow.vertex_groups.new(name="weapon_hand_L")
        for vi in unweighted:
            vg_root.add([vi], 1.0, 'REPLACE')

    # Verify bone weights on top and bottom tips
    group_names = {g.index: g.name for g in classic_bow.vertex_groups}
    top_v = max(classic_bow.data.vertices, key=lambda v: v.co.z)
    print(f"Bow top tip (Z={top_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in top_v.groups if g.weight > 0.01])

    bot_v = min(classic_bow.data.vertices, key=lambda v: v.co.z)
    print(f"Bow bottom tip (Z={bot_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in bot_v.groups if g.weight > 0.01])

    mid_v = min(classic_bow.data.vertices, key=lambda v: abs(v.co.z - ref_center[2]))
    print(f"Bow grip (Z={mid_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in mid_v.groups if g.weight > 0.01])

    # 4. Extract mesh data
    me = classic_bow.data
    me.calc_loop_triangles()
    me.calc_tangents(uvmap=me.uv_layers.active.name)
    mw = classic_bow.matrix_world
    m3 = mw.to_3x3()
    nmat = m3.inverted().transposed()
    uv_data = me.uv_layers.active.data
    corner_normals = me.corner_normals

    vert_weights = []
    for v_idx, v in enumerate(me.vertices):
        ws = sorted(((g.weight, group_names[g.group]) for g in v.groups if g.weight > 1e-4), reverse=True)[:4]
        total = sum(w for w, _ in ws)
        names = [n for _, n in ws] + [""] * (4 - len(ws))
        vals = [w / total for w, _ in ws] + [0.0] * (4 - len(ws))
        vert_weights.append((names, vals))

    key_to_idx, loop_to_idx = {}, {}
    pos_list, nrm_list, tan_list, uv_list, wb_list, wv_list = [], [], [], [], [], []
    for li, loop in enumerate(me.loops):
        vi = loop.vertex_index
        n = (nmat @ corner_normals[li].vector).normalized()
        u = uv_data[li].uv
        key = (vi, round(u[0], 6), round(u[1], 6), round(n.x, 4), round(n.y, 4), round(n.z, 4))
        idx = key_to_idx.get(key)
        if idx is None:
            idx = key_to_idx[key] = len(pos_list)
            pos_list.append(tuple(mw @ me.vertices[vi].co))
            nrm_list.append(tuple(n))
            t = (m3 @ loop.tangent).normalized()
            tan_list.append((t.x, t.y, t.z, loop.bitangent_sign))
            uv_list.append((u[0], u[1]))
            wb_list.append(vert_weights[vi][0])
            wv_list.append(vert_weights[vi][1])
        loop_to_idx[li] = idx

    tris = [[loop_to_idx[l] for l in t.loops] for t in me.loop_triangles]

    # 5. Write to DMX using bow template
    d = dm.load(str(bow_template_path))
    model = d.root['model']
    joint_index = {j.name: i for i, j in enumerate(model['jointList'])}
    c = next(c for c in model['children'] if c.type == 'DmeDag')
    shape = c['shape']
    vd = shape['currentState']

    dmx_pos = blender_to_dmx(pos_list)
    dmx_nrm = blender_dir_to_dmx(nrm_list)
    dmx_tan = np.array(tan_list, dtype=float)
    dmx_tan[:, :3] = blender_dir_to_dmx(dmx_tan[:, :3])
    dmx_uv = uv_blender_to_dmx(uv_list)
    n = len(dmx_pos)

    blend_idx, blend_w = [], []
    for row_b, row_w in zip(wb_list, wv_list):
        for b, w in zip(row_b[:JOINTS_PER_VERTEX], row_w[:JOINTS_PER_VERTEX]):
            blend_idx.append(joint_index[b] if (b and b in joint_index) else 0)
            blend_w.append(float(w) if (b and b in joint_index) else 0.0)

    seq = list(range(n))
    vd["jointCount"] = JOINTS_PER_VERTEX
    vd["position$0"] = dm.make_array([dm.Vector3(p) for p in dmx_pos.tolist()], dm.Vector3)
    vd["normal$0"] = dm.make_array([dm.Vector3(p) for p in dmx_nrm.tolist()], dm.Vector3)
    vd["tangent$0"] = dm.make_array([dm.Vector4(p) for p in dmx_tan.tolist()], dm.Vector4)
    vd["texcoord$0"] = dm.make_array([dm.Vector2(p) for p in dmx_uv.tolist()], dm.Vector2)
    for key in ("position$0", "normal$0", "tangent$0", "texcoord$0"):
        vd[key + "Indices"] = dm.make_array(seq, int)
    vd["blendindices$0"] = dm.make_array(blend_idx, int)
    vd["blendweights$0"] = dm.make_array(blend_w, float)

    # FaceSet for bow
    flat = []
    for a, b, c in tris:
        flat += [int(a), int(b), int(c), -1]
    fs = dm.Element(d, "faceset_0", "DmeFaceSet")
    mat_elem = dm.Element(d, "material_0", "DmeMaterial")
    mat_elem["mtlName"] = "models/heroes_staging/archer/materials/windranger_arcana_bow.vmat"
    fs["material"] = mat_elem
    fs["faces"] = dm.make_array(flat, int)

    shape["faceSets"] = dm.make_array([fs], dm.Element)
    shape["baseStates"] = dm.make_array([vd], dm.Element)

    out_dmx = Path(r"extracted\archer_bow1.dmx")
    d.write(str(out_dmx), "binary", 9)
    print(f"[EXITO] DMX archer_bow1 escrito: {out_dmx} ({out_dmx.stat().st_size:,} bytes)")

if __name__ == "__main__":
    build_bow()
