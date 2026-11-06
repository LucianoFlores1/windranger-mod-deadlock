import bpy
import numpy as np
import os
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
import datamodel as dm
from pathlib import Path

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

def test_warka():
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 1. Load reference warka3 for weight transfer
    warka_template_path = Path(r'extracted\archer_warka3_orig.dmx')
    info = read_dmx_mesh(warka_template_path)
    ref_pos = dmx_to_blender(info['positions'])

    me_ref = bpy.data.meshes.new("ref_mesh")
    me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
    me_ref.update()
    ref_obj = bpy.data.objects.new("ref_warka", me_ref)
    bpy.context.scene.collection.objects.link(ref_obj)

    bone_names = info['bones']
    weights = info['weights']
    for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
        for b_name, w in zip(b_row, w_row):
            if w > 0.001 and b_name:
                vg = ref_obj.vertex_groups.get(b_name) or ref_obj.vertex_groups.new(name=b_name)
                vg.add([vi], float(w), 'REPLACE')

    print(f"Ref warka loaded: {len(me_ref.vertices)} verts, {len(ref_obj.vertex_groups)} groups.")
    ref_min = np.min(ref_pos, axis=0)
    ref_max = np.max(ref_pos, axis=0)
    print(f"Ref bounds: X=[{ref_min[0]:.2f}, {ref_max[0]:.2f}], Y=[{ref_min[1]:.2f}, {ref_max[1]:.2f}], Z=[{ref_min[2]:.2f}, {ref_max[2]:.2f}]")

    # 2. Materials definition
    mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
    mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
    mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat")
    mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")

    # 3. Import classic Windrunner parts
    wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
    base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

    parts = [
        (base_glb, mat_base),
        (os.path.join(wr_dir, "windrunner_head.glb"), mat_hair),
        (os.path.join(wr_dir, "windrunner_cape.glb"), mat_cape),
        (os.path.join(wr_dir, "windrunner_shoulderpads.glb"), mat_shoulders),
        (os.path.join(wr_dir, "windrunner_quiver.glb"), mat_quiver),
    ]

    scale = 0.5471
    classic_meshes = []
    for fpath, part_mat in parts:
        before = set(bpy.context.scene.objects)
        bpy.ops.import_scene.gltf(filepath=fpath)
        new_objs = set(bpy.context.scene.objects) - before
        for o in new_objs:
            if o.type == 'MESH' and 'icosphere' not in o.name.lower():
                if o.data.shape_keys:
                    for kb in list(o.data.shape_keys.key_blocks):
                        o.shape_key_remove(kb)
                o.vertex_groups.clear()
                o.modifiers.clear()
                o.data.materials.clear()
                o.data.materials.append(part_mat)
                classic_meshes.append(o)
            elif o.type == 'ARMATURE':
                bpy.data.objects.remove(o)

    # Scale uniformly around (0,0,0)
    for m in classic_meshes:
        m.scale = (scale, scale, scale)
        bpy.context.view_layer.objects.active = m
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Join into one unified mesh
    bpy.ops.object.select_all(action='DESELECT')
    for m in classic_meshes:
        m.select_set(True)
    bpy.context.view_layer.objects.active = classic_meshes[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = "classic_windrunner_body"
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    c_verts = np.array([v.co for v in joined.data.vertices])
    c_min = np.min(c_verts, axis=0)
    c_max = np.max(c_verts, axis=0)
    print(f"Classic bounds after scale: X=[{c_min[0]:.2f}, {c_max[0]:.2f}], Y=[{c_min[1]:.2f}, {c_max[1]:.2f}], Z=[{c_min[2]:.2f}, {c_max[2]:.2f}]")

    # 4. Transfer weights from ref_obj
    mod = joined.modifiers.new("DataTransfer", "DATA_TRANSFER")
    mod.object = ref_obj
    mod.use_vert_data = True
    mod.data_types_verts = {'VGROUP_WEIGHTS'}
    mod.vert_mapping = 'NEAREST'
    bpy.context.view_layer.objects.active = joined
    bpy.ops.object.datalayout_transfer(modifier=mod.name)
    bpy.ops.object.modifier_apply(modifier=mod.name)

    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    unweighted = [v.index for v in joined.data.vertices if not any(g.weight > 0.001 for g in v.groups)]
    print(f"Joined mesh: {len(joined.data.vertices)} vertices, unweighted: {len(unweighted)}")
    if unweighted:
        vg_pelvis = joined.vertex_groups.get("pelvis") or joined.vertex_groups.new(name="pelvis")
        for vi in unweighted:
            vg_pelvis.add([vi], 1.0, 'REPLACE')

    # Verify bone assignments on key points:
    group_names = {g.index: g.name for g in joined.vertex_groups}
    top_v = max(joined.data.vertices, key=lambda v: v.co.z)
    print(f"Head top (Z={top_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in top_v.groups if g.weight > 0.01])

    l_foot_v = min([v for v in joined.data.vertices if v.co.x > 0.1], key=lambda v: v.co.z)
    print(f"Left foot (+X={l_foot_v.co.x:.2f}, Z={l_foot_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in l_foot_v.groups if g.weight > 0.01])

    r_foot_v = min([v for v in joined.data.vertices if v.co.x < -0.1], key=lambda v: v.co.z)
    print(f"Right foot (-X={r_foot_v.co.x:.2f}, Z={r_foot_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in r_foot_v.groups if g.weight > 0.01])

    l_hand_v = max([v for v in joined.data.vertices if v.co.x > 0.3], key=lambda v: v.co.x)
    print(f"Left hand (+X={l_hand_v.co.x:.2f}, Z={l_hand_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in l_hand_v.groups if g.weight > 0.01])

    r_hand_v = min([v for v in joined.data.vertices if v.co.x < -0.3], key=lambda v: v.co.x)
    print(f"Right hand (-X={r_hand_v.co.x:.2f}, Z={r_hand_v.co.z:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in r_hand_v.groups if g.weight > 0.01])

    # 5. Extract mesh data
    me = joined.data
    me.calc_loop_triangles()
    me.calc_tangents(uvmap=me.uv_layers.active.name)
    mw = joined.matrix_world
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
    tri_mats = [t.material_index for t in me.loop_triangles]
    mat_names = [m.name for m in joined.data.materials]

    # 6. Write to DMX using warka template
    d = dm.load(str(warka_template_path))
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

    # FaceSets per material
    tris_arr = np.array(tris, dtype=np.int32)
    tri_mats_arr = np.array(tri_mats, dtype=np.int32)
    face_sets = []
    for m_idx, m_name in enumerate(mat_names):
        m_tris = tris_arr[tri_mats_arr == m_idx]
        if len(m_tris) == 0:
            continue
        flat = []
        for a, b, c in m_tris.tolist():
            flat += [int(a), int(b), int(c), -1]
        fs = dm.Element(d, f"faceset_{m_idx}", "DmeFaceSet")
        mat_elem = dm.Element(d, f"material_{m_idx}", "DmeMaterial")
        mat_elem["mtlName"] = m_name
        fs["material"] = mat_elem
        fs["faces"] = dm.make_array(flat, int)
        face_sets.append(fs)
        print(f"FaceSet {m_idx} ({m_name}): {len(m_tris)} tris")

    shape["faceSets"] = dm.make_array(face_sets, dm.Element)
    shape["baseStates"] = dm.make_array([vd], dm.Element)

    out_dmx = Path(r"extracted\archer_warka3.dmx")
    d.write(str(out_dmx), "binary", 9)
    print(f"[EXITO] DMX archer_warka3 escrito: {out_dmx} ({out_dmx.stat().st_size:,} bytes)")

if __name__ == "__main__":
    test_warka()

