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

def build_warka():
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 1. Reference mesh
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

    # 2. Materials
    mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
    mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
    mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")

    # 3. Import classic parts
    wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
    base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

    parts = [
        (base_glb, mat_base, "base"),
        (os.path.join(wr_dir, "windrunner_head.glb"), mat_hair, "hair"),
        (os.path.join(wr_dir, "windrunner_cape.glb"), mat_cape, "cape"),
        (os.path.join(wr_dir, "windrunner_shoulderpads.glb"), mat_shoulders, "shoulders"),
        (os.path.join(wr_dir, "windrunner_quiver.glb"), mat_quiver, "quiver"),
    ]

    scale = 0.5471
    classic_meshes = []
    shoulder_mesh = None

    for fpath, part_mat, tag in parts:
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
                if tag == "shoulders":
                    shoulder_mesh = o
            elif o.type == 'ARMATURE':
                bpy.data.objects.remove(o)

    # Scale uniformly
    for m in classic_meshes:
        m.scale = (scale, scale, scale)
        bpy.context.view_layer.objects.active = m
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Rig shoulderpads independently to clavicle_L and arm_upper_L!
    # In Dota 2, shoulderpads are mostly clavicle_L (60%) and arm_upper_L (40%)
    if shoulder_mesh:
        vg_clav = shoulder_mesh.vertex_groups.new(name="clavicle_L")
        vg_arm = shoulder_mesh.vertex_groups.new(name="arm_upper_L")
        for v in shoulder_mesh.data.vertices:
            # If vertex is closer to the body/neck: more clavicle
            # If vertex is further out on the shoulder (+X): more arm_upper
            # In Blender, left shoulder is +X (X between 0.15 and 0.45)
            factor = (v.co.x - 0.15) / 0.30
            factor = max(0.0, min(1.0, factor))
            w_arm = factor * 0.5
            w_clav = 1.0 - w_arm
            vg_clav.add([v.index], w_clav, 'REPLACE')
            vg_arm.add([v.index], w_arm, 'REPLACE')
        print(f"Shoulderpad rigged cleanly to clavicle_L and arm_upper_L (0 head/neck weights!)")

    # Join
    bpy.ops.object.select_all(action='DESELECT')
    for m in classic_meshes:
        m.select_set(True)
    bpy.context.view_layer.objects.active = classic_meshes[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = "classic_windrunner_body"
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Transfer weights from ref_obj (only for vertices that don't have weights yet!)
    # To do this safely:
    # We use DATA_TRANSFER on joined, then we fix up hands and shoulders!
    mod = joined.modifiers.new("DataTransfer", "DATA_TRANSFER")
    mod.object = ref_obj
    mod.use_vert_data = True
    mod.data_types_verts = {'VGROUP_WEIGHTS'}
    mod.vert_mapping = 'NEAREST'
    bpy.context.view_layer.objects.active = joined
    bpy.ops.object.datalayout_transfer(modifier=mod.name)
    bpy.ops.object.modifier_apply(modifier=mod.name)

    # Now apply Post-Transfer Fixes:
    # Fix 1: Shoulderpad vertices (belonging to mat_shoulders / Z in [1.5, 1.9], X in [0.08, 0.45])
    # Remove head, neck_0, arm_lower_L
    forbidden_shoulder = ['head', 'neck_0', 'arm_lower_L', 'arm_lower_R', 'spine_3']
    group_map = {g.name: g for g in joined.vertex_groups}

    for v in joined.data.vertices:
        # If vertex is in the left shoulder region
        if 0.10 < v.co.x < 0.45 and 1.50 < v.co.z < 1.95 and -0.15 < v.co.y < 0.20:
            removed_weight = 0.0
            for fn in forbidden_shoulder:
                if fn in group_map:
                    try:
                        w = group_map[fn].weight(v.index)
                        if w > 0:
                            removed_weight += w
                            group_map[fn].remove([v.index])
                    except:
                        pass
            if removed_weight > 0.01:
                # Add removed weight to clavicle_L
                if 'clavicle_L' in group_map:
                    try:
                        cur_w = group_map['clavicle_L'].weight(v.index)
                    except:
                        cur_w = 0.0
                    group_map['clavicle_L'].add([v.index], cur_w + removed_weight, 'REPLACE')

        # Fix 2: Right Hand vertices (-X < -0.45, Z between 0.8 and 1.3)
        # Any weight on pinky bones or meta bones -> hand_R
        if v.co.x < -0.45 and 0.80 < v.co.z < 1.30:
            pinky_w = 0.0
            for g_entry in list(v.groups):
                g_name = joined.vertex_groups[g_entry.group].name
                if 'pinky' in g_name or 'meta' in g_name:
                    pinky_w += g_entry.weight
                    joined.vertex_groups[g_entry.group].remove([v.index])
            if pinky_w > 0.01:
                if 'hand_R' in group_map:
                    try:
                        cur_h = group_map['hand_R'].weight(v.index)
                    except:
                        cur_h = 0.0
                    group_map['hand_R'].add([v.index], cur_h + pinky_w, 'REPLACE')

        # Fix 3: Left Hand vertices (+X > 0.45, Z between 0.8 and 1.3)
        # Any weight on pinky bones or meta bones -> hand_L
        if v.co.x > 0.45 and 0.80 < v.co.z < 1.30:
            meta_w = 0.0
            for g_entry in list(v.groups):
                g_name = joined.vertex_groups[g_entry.group].name
                if 'pinky' in g_name or 'meta' in g_name:
                    meta_w += g_entry.weight
                    joined.vertex_groups[g_entry.group].remove([v.index])
            if meta_w > 0.01:
                if 'hand_L' in group_map:
                    try:
                        cur_h = group_map['hand_L'].weight(v.index)
                    except:
                        cur_h = 0.0
                    group_map['hand_L'].add([v.index], cur_h + meta_w, 'REPLACE')

    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    # Verify shoulder and hands after fixes:
    group_names = {g.index: g.name for g in joined.vertex_groups}
    r_hand_v = min([v for v in joined.data.vertices if v.co.x < -0.45], key=lambda v: v.co.x)
    print(f"Right hand tip (-X={r_hand_v.co.x:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in r_hand_v.groups if g.weight > 0.01])

    l_hand_v = max([v for v in joined.data.vertices if v.co.x > 0.45], key=lambda v: v.co.x)
    print(f"Left hand tip (+X={l_hand_v.co.x:.2f}):", [(group_names[g.group], round(g.weight, 3)) for g in l_hand_v.groups if g.weight > 0.01])

    # Extract mesh data and write DMX
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

    # Write DMX
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
    print(f"[EXITO] DMX archer_warka3 con hombro y manos pulidos escrito: {out_dmx} ({out_dmx.stat().st_size:,} bytes)")

if __name__ == "__main__":
    build_warka()

