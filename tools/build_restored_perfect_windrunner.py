import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import bpy
import numpy as np
import os
import math
from mathutils import Matrix, Vector
import datamodel as dm

INCH = 0.0254
JOINTS_PER_VERTEX = 4

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

def read_dmx_mesh(path):
    d = dm.load(str(path))
    model = d.root['model']
    c = next(c for c in model['children'] if c.type == 'DmeDag')
    shape = c['shape']
    vd = shape['currentState']
    joint_list = [j.name for j in model['jointList']]

    positions = np.array(vd['position$0'])
    k = vd.get('jointCount', 4)
    indices = np.array(vd['blendindices$0']).reshape(-1, k)
    weights = np.array(vd['blendweights$0']).reshape(-1, k)
    n_verts = len(positions)

    vert_bones = []
    vert_weights = []
    for vi in range(n_verts):
        b_names = []
        b_weights = []
        for j in range(k):
            w = float(weights[vi, j])
            j_idx = int(indices[vi, j])
            b_names.append(joint_list[j_idx] if w > 0.0001 else '')
            b_weights.append(w)
        vert_bones.append(b_names)
        vert_weights.append(b_weights)

    tris = []
    for fs in shape.get('faceSets', []):
        cur = []
        for i in fs['faces']:
            if i == -1:
                tris += [[cur[0], cur[j], cur[j + 1]] for j in range(1, len(cur) - 1)]
                cur = []
            else:
                cur.append(i)

    return {
        'positions': positions,
        'bones': vert_bones,
        'weights': vert_weights,
        'tris': np.array(tris)
    }

def export_dmx(obj, out_path, template_path):
    me = obj.data
    me.calc_loop_triangles()
    me.calc_tangents(uvmap=me.uv_layers.active.name)
    mw = obj.matrix_world
    m3 = mw.to_3x3()
    nmat = m3.inverted().transposed()
    uv_data = me.uv_layers.active.data
    corner_normals = me.corner_normals

    group_names = {g.index: g.name for g in obj.vertex_groups}

    vert_weights = []
    for v in me.vertices:
        ws = sorted(((g.weight, group_names[g.group]) for g in v.groups if g.weight > 1e-4), reverse=True)[:4]
        total = sum(w for w, _ in ws)
        names = [n for _, n in ws] + [""] * (4 - len(ws))
        vals = [w / total if total > 0 else 0.0 for w, _ in ws] + [0.0] * (4 - len(ws))
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
    mat_names = [m.name.split('.')[0] + ('.vmat' if '.vmat' in m.name else '') for m in obj.data.materials]

    d = dm.load(str(template_path))
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

    n_verts = len(pos_list)
    blend_indices = []
    blend_weights = []
    for b_row, w_row in zip(wb_list, wv_list):
        for b, w in zip(b_row, w_row):
            blend_indices.append(joint_index.get(b, 7)) # fallback pelvis
            blend_weights.append(float(w))

    seq = list(range(n_verts))
    vd["jointCount"] = JOINTS_PER_VERTEX
    vd["position$0"] = dm.make_array([dm.Vector3(p) for p in dmx_pos.tolist()], dm.Vector3)
    vd["normal$0"] = dm.make_array([dm.Vector3(p) for p in dmx_nrm.tolist()], dm.Vector3)
    vd["tangent$0"] = dm.make_array([dm.Vector4(p) for p in dmx_tan.tolist()], dm.Vector4)
    vd["texcoord$0"] = dm.make_array([dm.Vector2(p) for p in dmx_uv.tolist()], dm.Vector2)
    for key in ("position$0", "normal$0", "tangent$0", "texcoord$0"):
        vd[key + "Indices"] = dm.make_array(seq, int)
    vd["blendindices$0"] = dm.make_array(blend_indices, int)
    vd["blendweights$0"] = dm.make_array(blend_weights, float)

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

    d.write(str(out_path), "binary", 9)
    print(f"[OK] Exported {out_path} ({out_path.stat().st_size:,} bytes, {n_verts} verts, {len(tris)} tris)")

def build_bow():
    print("\n=== STEP 1: BUILDING CLASSIC BOW ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    bow_template_path = Path(r'extracted\archer_bow1_orig.dmx')
    info = read_dmx_mesh(bow_template_path)
    ref_pos = dmx_to_blender(info['positions'])
    ref_center = np.mean(ref_pos, axis=0)
    ref_span = np.ptp(ref_pos, axis=0)

    # Reference object for DataTransfer
    me_ref = bpy.data.meshes.new("ref_mesh")
    me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
    me_ref.update()
    ref_bow = bpy.data.objects.new("ref_bow", me_ref)
    bpy.context.scene.collection.objects.link(ref_bow)

    for vi, (b_row, w_row) in enumerate(zip(info['bones'], info['weights'])):
        for b_name, w in zip(b_row, w_row):
            if w > 0.001 and b_name:
                vg = ref_bow.vertex_groups.get(b_name) or ref_bow.vertex_groups.new(name=b_name)
                vg.add([vi], float(w), 'REPLACE')

    # Import classic bow
    wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
    bow_glb = os.path.join(wr_dir, "windrunner_bow.glb")
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=bow_glb)
    classic_bow = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')

    if classic_bow.data.shape_keys:
        for kb in list(classic_bow.data.shape_keys.key_blocks):
            classic_bow.shape_key_remove(kb)
    classic_bow.vertex_groups.clear()
    classic_bow.modifiers.clear()

    rot_mat = Matrix.Rotation(math.radians(-90), 4, 'Y')
    classic_bow.data.transform(rot_mat)

    c_pos = np.array([v.co for v in classic_bow.data.vertices])
    scale_factor = ref_span[2] / np.ptp(c_pos[:, 2])
    scale_mat = Matrix.Diagonal((scale_factor, scale_factor, scale_factor, 1.0))
    classic_bow.data.transform(scale_mat)

    c_center = np.mean([v.co for v in classic_bow.data.vertices], axis=0)
    diff = ref_center - c_center
    trans_mat = Matrix.Translation(Vector(diff.tolist()))
    classic_bow.data.transform(trans_mat)

    mat_bow = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_bow.vmat")
    classic_bow.data.materials.clear()
    classic_bow.data.materials.append(mat_bow)

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
    if unweighted:
        vg_root = classic_bow.vertex_groups.get("weapon_hand_L") or classic_bow.vertex_groups.new(name="weapon_hand_L")
        for vi in unweighted:
            vg_root.add([vi], 1.0, 'REPLACE')

    out_bow = Path(r'extracted\archer_bow1.dmx')
    export_dmx(classic_bow, out_bow, bow_template_path)

    bow_d = read_dmx_mesh(out_bow)
    bow_pos_dmx = np.array(bow_d['positions'])
    top_tip = max(bow_pos_dmx, key=lambda p: p[2])
    bot_tip = min(bow_pos_dmx, key=lambda p: p[2])
    print(f"Classic Bow Tips (DMX coords): top={top_tip}, bot={bot_tip}")
    return top_tip, bot_tip

def build_teteva(top_tip, bot_tip):
    print("\n=== STEP 2: BUILDING CLEAN BOWSTRING ===")
    d = dm.load(r'extracted\archer_teteva.dmx')
    c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
    vd = c['shape']['currentState']
    model = d.root['model']
    joint_index = {j.name: i for i, j in enumerate(model['jointList'])}
    upper_idx = joint_index.get('upperLimb_1', joint_index.get('upperLimb_end', 0))
    lower_idx = joint_index.get('lowerLimb_1', joint_index.get('lowerLimb_end', 0))

    n_verts = len(vd['position$0']) # 32 vertices
    new_pos = []
    blend_idx = []
    blend_w = []

    for i in range(n_verts):
        frac = i / (n_verts - 1)
        p = (1.0 - frac) * bot_tip + frac * top_tip
        new_pos.append(dm.Vector3(p.tolist()))
        if frac > 0.5:
            blend_idx += [upper_idx, 0, 0, 0]
            blend_w += [1.0, 0.0, 0.0, 0.0]
        else:
            blend_idx += [lower_idx, 0, 0, 0]
            blend_w += [1.0, 0.0, 0.0, 0.0]

    vd['position$0'] = dm.make_array(new_pos, dm.Vector3)
    vd['blendindices$0'] = dm.make_array(blend_idx, int)
    vd['blendweights$0'] = dm.make_array(blend_w, float)

    out_teteva = Path(r'extracted\archer_teteva.dmx')
    d.write(str(out_teteva), "binary", 9)
    print(f"[OK] Clean teteva written: {out_teteva} ({out_teteva.stat().st_size:,} bytes)")

def build_body():
    print("\n=== STEP 3: BUILDING PERFECT WINDRUNNER BODY ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    warka_template_path = Path(r'extracted\archer_warka3_orig.dmx')
    info = read_dmx_mesh(warka_template_path)
    ref_pos = dmx_to_blender(info['positions'])

    me_ref = bpy.data.meshes.new("ref_mesh")
    me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
    me_ref.update()
    ref_warka = bpy.data.objects.new("ref_warka", me_ref)
    bpy.context.scene.collection.objects.link(ref_warka)

    for vi, (b_row, w_row) in enumerate(zip(info['bones'], info['weights'])):
        for b_name, w in zip(b_row, w_row):
            if w > 0.001 and b_name:
                vg = ref_warka.vertex_groups.get(b_name) or ref_warka.vertex_groups.new(name=b_name)
                vg.add([vi], float(w), 'REPLACE')

    print(f"Ref warka loaded: {len(me_ref.vertices)} verts, {len(ref_warka.vertex_groups)} groups.")

    # Materials
    mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
    mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
    mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    # Correct classic shoulderpad material: matches cape and green leather!
    mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")

    scale = 0.5471
    wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
    base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

    # Part A: Shoulderpads (Independent clean rigging to clavicle & upper arm with 0% head/neck!)
    sh_glb = os.path.join(wr_dir, "windrunner_shoulderpads.glb")
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=sh_glb)
    shoulder_mesh = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')
    shoulder_mesh.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = shoulder_mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    shoulder_mesh.vertex_groups.clear()
    shoulder_mesh.modifiers.clear()
    shoulder_mesh.data.materials.clear()
    shoulder_mesh.data.materials.append(mat_shoulders)

    vg_clav_L = shoulder_mesh.vertex_groups.new(name="clavicle_L")
    vg_arm_L = shoulder_mesh.vertex_groups.new(name="arm_upper_L")
    vg_clav_R = shoulder_mesh.vertex_groups.new(name="clavicle_R")
    vg_arm_R = shoulder_mesh.vertex_groups.new(name="arm_upper_R")

    for v in shoulder_mesh.data.vertices:
        if v.co.x > 0.0:
            # Left shoulderpad (+X in Blender)
            factor = max(0.0, min(1.0, (v.co.x - 0.10) / 0.30))
            w_arm = factor * 0.30
            vg_clav_L.add([v.index], 1.0 - w_arm, 'REPLACE')
            vg_arm_L.add([v.index], w_arm, 'REPLACE')
        else:
            # Right strap (-X in Blender)
            factor = max(0.0, min(1.0, (-v.co.x - 0.10) / 0.20))
            w_arm = factor * 0.30
            vg_clav_R.add([v.index], 1.0 - w_arm, 'REPLACE')
            vg_arm_R.add([v.index], w_arm, 'REPLACE')
    print("[OK] Shoulderpad rigged independently with classic green leather material & 0 head/neck weights!")

    # Part B: Quiver (Separate - 100% spine_2 so it is anchored to upper back and NEVER rotates with head or arm!)
    quiv_glb = os.path.join(wr_dir, "windrunner_quiver.glb")
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=quiv_glb)
    quiver_mesh = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')
    quiver_mesh.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = quiver_mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    quiver_mesh.vertex_groups.clear()
    quiver_mesh.modifiers.clear()
    quiver_mesh.data.materials.clear()
    quiver_mesh.data.materials.append(mat_quiver)

    vg_q_sp2 = quiver_mesh.vertex_groups.new(name="spine_2")
    for v in quiver_mesh.data.vertices:
        vg_q_sp2.add([v.index], 1.0, 'REPLACE')
    print("[OK] Quiver rigged solidly to upper back (spine_2) with 0 head/neck/arm weights!")

    # Part C: Base body, Hair, Cape
    other_parts = [
        (base_glb, mat_base, "base"),
        (os.path.join(wr_dir, "windrunner_head.glb"), mat_hair, "hair"),
        (os.path.join(wr_dir, "windrunner_cape.glb"), mat_cape, "cape"),
    ]

    imported_objs = []
    cape_mesh = None

    for fpath, part_mat, tag in other_parts:
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
                imported_objs.append(o)
                if tag == "cape":
                    cape_mesh = o
            elif o.type == 'ARMATURE':
                bpy.data.objects.remove(o)

    for m in imported_objs:
        m.scale = (scale, scale, scale)
        bpy.context.view_layer.objects.active = m
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    bpy.ops.object.select_all(action='DESELECT')
    for m in imported_objs:
        m.select_set(True)
    bpy.context.view_layer.objects.active = imported_objs[0]
    bpy.ops.object.join()
    body_main = bpy.context.view_layer.objects.active
    body_main.name = "classic_body_main"
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # DataTransfer from ref_warka (NEAREST)
    mod = body_main.modifiers.new("DataTransfer", "DATA_TRANSFER")
    mod.object = ref_warka
    mod.use_vert_data = True
    mod.data_types_verts = {'VGROUP_WEIGHTS'}
    mod.vert_mapping = 'NEAREST'
    bpy.context.view_layer.objects.active = body_main
    bpy.ops.object.datalayout_transfer(modifier=mod.name)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    print("[OK] DataTransfer applied to body_main.")

    # Post-Transfer Polish
    group_map = {g.name: g for g in body_main.vertex_groups}
    vg_cR = group_map.get('clavicle_R') or body_main.vertex_groups.new(name='clavicle_R')
    vg_auR = group_map.get('arm_upper_R') or body_main.vertex_groups.new(name='arm_upper_R')
    vg_alR = group_map.get('arm_lower_R') or body_main.vertex_groups.new(name='arm_lower_R')
    vg_cL = group_map.get('clavicle_L') or body_main.vertex_groups.new(name='clavicle_L')
    vg_auL = group_map.get('arm_upper_L') or body_main.vertex_groups.new(name='arm_upper_L')
    vg_alL = group_map.get('arm_lower_L') or body_main.vertex_groups.new(name='arm_lower_L')
    vg_hL = group_map.get('hand_L') or body_main.vertex_groups.new(name='hand_L')
    vg_hR = group_map.get('hand_R') or body_main.vertex_groups.new(name='hand_R')

    # 1. Complete Right Arm Cleanup (Fixes ultimate arm deformation & spine/leg/pelvis tearing)
    r_arm_fixed = 0
    for v in body_main.data.vertices:
        if v.co.x < -0.18 and v.co.z > 0.75:
            removed = 0.0
            for g_entry in list(v.groups):
                g_name = body_main.vertex_groups[g_entry.group].name
                # Remove ANY torso, spine, pelvis, head, neck, leg, or opposite side bone from the arm!
                if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_L', 'head', 'neck', 'leg', '_L']):
                    removed += g_entry.weight
                    body_main.vertex_groups[g_entry.group].remove([v.index])
                elif v.co.x <= -0.28 and 'clavicle' in g_name:
                    removed += g_entry.weight
                    body_main.vertex_groups[g_entry.group].remove([v.index])
            if removed > 0.001:
                r_arm_fixed += 1
                if v.co.x < -0.47:
                    target = vg_hR
                elif v.co.x < -0.32:
                    target = vg_alR
                elif v.co.x > -0.26 and v.co.z > 1.25:
                    target = vg_cR
                else:
                    target = vg_auR
                try: cur = target.weight(v.index)
                except: cur = 0.0
                target.add([v.index], cur + removed, 'REPLACE')
    print(f"[OK] Right arm completely cleaned of bad weights: {r_arm_fixed} vertices!")

    # 2. Complete Left Arm Cleanup (Protects left arm, elbow and bow grip)
    l_arm_fixed = 0
    for v in body_main.data.vertices:
        if v.co.x > 0.18 and v.co.z > 0.75:
            removed = 0.0
            for g_entry in list(v.groups):
                g_name = body_main.vertex_groups[g_entry.group].name
                if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_R', 'head', 'neck', 'leg', '_R']):
                    removed += g_entry.weight
                    body_main.vertex_groups[g_entry.group].remove([v.index])
                elif v.co.x >= 0.28 and 'clavicle' in g_name:
                    removed += g_entry.weight
                    body_main.vertex_groups[g_entry.group].remove([v.index])
            if removed > 0.001:
                l_arm_fixed += 1
                if v.co.x > 0.47:
                    target = vg_hL
                elif v.co.x > 0.32:
                    target = vg_alL
                elif v.co.x < 0.26 and v.co.z > 1.25:
                    target = vg_cL
                else:
                    target = vg_auL
                try: cur = target.weight(v.index)
                except: cur = 0.0
                target.add([v.index], cur + removed, 'REPLACE')
    print(f"[OK] Left arm completely cleaned of bad weights: {l_arm_fixed} vertices!")

    # 3. Clean Left Hand (Solid closed fist holding bow grip - consolidate ALL fingers into hand_L!)
    l_h_fixed = 0
    for v in body_main.data.vertices:
        if v.co.x > 0.47 and 0.85 < v.co.z < 1.25:
            finger_w = 0.0
            for g_entry in list(v.groups):
                g_name = body_main.vertex_groups[g_entry.group].name
                if any(k in g_name for k in ['finger', 'thumb', 'index', 'middle', 'ring', 'pinky', 'meta']):
                    finger_w += g_entry.weight
                    body_main.vertex_groups[g_entry.group].remove([v.index])
            if finger_w > 0.001:
                l_h_fixed += 1
                try: cur = vg_hL.weight(v.index)
                except: cur = 0.0
                vg_hL.add([v.index], cur + finger_w, 'REPLACE')
    print(f"[OK] Left hand (bow grip): {l_h_fixed} vertices consolidated into hand_L (solid fist, 0 finger tear!)")

    # 4. Clean Right Hand
    r_h_fixed = 0
    for v in body_main.data.vertices:
        if v.co.x < -0.48 and 0.85 < v.co.z < 1.25:
            meta_w = 0.0
            for g_entry in list(v.groups):
                g_name = body_main.vertex_groups[g_entry.group].name
                if 'pinky' in g_name or 'meta' in g_name:
                    meta_w += g_entry.weight
                    body_main.vertex_groups[g_entry.group].remove([v.index])
            if meta_w > 0.01:
                r_h_fixed += 1
                try: cur = vg_hR.weight(v.index)
                except: cur = 0.0
                vg_hR.add([v.index], cur + meta_w, 'REPLACE')
    print(f"[OK] Right hand verts cleaned (forearm preserved!): {r_h_fixed}")

    # Cape Dynamics:
    cape_mat_idx = None
    for mi, m in enumerate(body_main.data.materials):
        if m == mat_cape:
            cape_mat_idx = mi
            break
    cape_verts = set()
    for poly in body_main.data.polygons:
        if poly.material_index == cape_mat_idx:
            for vi in poly.vertices: cape_verts.add(vi)

    vg_sp3 = group_map.get('spine_3') or body_main.vertex_groups.new(name='spine_3')
    vg_sp2 = group_map.get('spine_2') or body_main.vertex_groups.new(name='spine_2')
    vg_sp1 = group_map.get('spine_1') or body_main.vertex_groups.new(name='spine_1')
    vg_pelvis = group_map.get('pelvis') or body_main.vertex_groups.new(name='pelvis')

    for vi in cape_verts:
        v = body_main.data.vertices[vi]
        for g in list(v.groups):
            g_name = body_main.vertex_groups[g.group].name
            if any(bad in g_name for bad in ['leg', 'ankle', 'arm', 'hand', 'head']):
                body_main.vertex_groups[g.group].remove([vi])
        z = v.co.z
        if z > 1.50: vg_sp3.add([vi], 1.0, 'REPLACE')
        elif z > 1.25:
            f = (z - 1.25) / 0.25
            vg_sp3.add([vi], f, 'REPLACE')
            vg_sp2.add([vi], 1.0 - f, 'REPLACE')
        elif z > 1.00:
            f = (z - 1.00) / 0.25
            vg_sp2.add([vi], f, 'REPLACE')
            vg_sp1.add([vi], 1.0 - f, 'REPLACE')
        else:
            f = max(0.0, min(1.0, (1.00 - z) / 0.40))
            vg_sp1.add([vi], 1.0 - f * 0.60, 'REPLACE')
            vg_pelvis.add([vi], f * 0.60, 'REPLACE')
    print(f"[OK] Cape vertices updated: {len(cape_verts)}")

    # NOW JOIN shoulder_mesh AND quiver_mesh INTO FINAL BODY
    bpy.ops.object.select_all(action='DESELECT')
    shoulder_mesh.select_set(True)
    quiver_mesh.select_set(True)
    body_main.select_set(True)
    bpy.context.view_layer.objects.active = body_main
    bpy.ops.object.join()
    final_body = bpy.context.view_layer.objects.active

    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    out_warka = Path(r'extracted\archer_warka3.dmx')
    export_dmx(final_body, out_warka, warka_template_path)
    print(f"[OK] Final perfect body exported: {out_warka}")

if __name__ == '__main__':
    top_tip, bot_tip = build_bow()
    build_teteva(top_tip, bot_tip)
    build_body()
    print("\n[ALL ASSETS BUILT AND REFINED TO PERFECTION!]")
