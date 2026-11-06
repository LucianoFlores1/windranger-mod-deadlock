import bpy
import numpy as np
import os
import sys
import math
from mathutils import Matrix, Vector

sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender, blender_to_dmx, blender_dir_to_dmx, uv_blender_to_dmx
import datamodel as dm
from pathlib import Path

INCH = 0.0254
JOINTS_PER_VERTEX = 4

def run_pipeline():
    print("=== STARTING PERFECT WINDRUNNER PIPELINE ===")

    # =========================================================================
    # 1. BUILD BOW (VERTICAL, RIGID WOODEN RECURVE BOW)
    # =========================================================================
    print("\n--- 1. BUILDING VERTICAL CLASSIC BOW ---")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    bow_template_path = Path(r'extracted\archer_bow1_orig.dmx')
    info = read_dmx_mesh(bow_template_path)
    ref_pos = dmx_to_blender(info['positions'])
    ref_center = np.mean(ref_pos, axis=0)
    ref_span = np.ptp(ref_pos, axis=0)

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

    # The original proven rotation that keeps the bow vertical:
    rot_mat = Matrix.Rotation(math.radians(-90), 4, 'Y')
    classic_bow.data.transform(rot_mat)

    # Scale to match ref_bow vertical span
    c_pos = np.array([v.co for v in classic_bow.data.vertices])
    scale_factor = ref_span[2] / np.ptp(c_pos[:, 2])
    scale_mat = Matrix.Diagonal((scale_factor, scale_factor, scale_factor, 1.0))
    classic_bow.data.transform(scale_mat)

    # Translate to match ref center
    c_center = np.mean([v.co for v in classic_bow.data.vertices], axis=0)
    diff = ref_center - c_center
    trans_mat = Matrix.Translation(Vector(diff.tolist()))
    classic_bow.data.transform(trans_mat)

    # Material
    mat_bow = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_bow.vmat")
    classic_bow.data.materials.clear()
    classic_bow.data.materials.append(mat_bow)

    # Rig the classic wooden bow:
    # In Dota 2, it's a solid wooden bow attached to the left wrist.
    # We weight 100% to weapon_hand_L so it stays rigid, clean, and never twists when shooting!
    vg_bow = classic_bow.vertex_groups.new(name="weapon_hand_L")
    for v in classic_bow.data.vertices:
        vg_bow.add([v.index], 1.0, 'REPLACE')

    fitted_bow_pos = np.array([v.co for v in classic_bow.data.vertices])
    bow_top_tip = max(fitted_bow_pos, key=lambda p: p[2])
    bow_bot_tip = min(fitted_bow_pos, key=lambda p: p[2])
    print(f"Classic bow bounds: X=[{fitted_bow_pos[:,0].min():.2f}, {fitted_bow_pos[:,0].max():.2f}], Z=[{fitted_bow_pos[:,2].min():.2f}, {fitted_bow_pos[:,2].max():.2f}]")
    print(f"Bow top tip: {bow_top_tip}, bot tip: {bow_bot_tip}")

    out_bow_dmx = Path(r'extracted\archer_bow1.dmx')
    _export_dmx(classic_bow, out_bow_dmx, bow_template_path)
    print(f"[OK] archer_bow1.dmx written: {out_bow_dmx.stat().st_size:,} bytes")

    # =========================================================================
    # 2. BUILD BOWSTRING (archer_teteva.dmx)
    # =========================================================================
    print("\n--- 2. BUILDING CLEAN BOWSTRING ---")
    d_tet = dm.load(r'extracted\archer_teteva.dmx')
    c_tet = next(c for c in d_tet.root['model']['children'] if c.type == 'DmeDag')
    vd_tet = c_tet['shape']['currentState']
    model_tet = d_tet.root['model']
    joint_index = {j.name: i for i, j in enumerate(model_tet['jointList'])}
    upper_idx = joint_index.get('upperLimb_1', joint_index.get('upperLimb_end', 0))
    lower_idx = joint_index.get('lowerLimb_1', joint_index.get('lowerLimb_end', 0))

    top_tip_dmx = blender_to_dmx(bow_top_tip)
    bot_tip_dmx = blender_to_dmx(bow_bot_tip)

    n_verts = len(vd_tet['position$0']) # 32 vertices
    new_pos = []
    blend_idx = []
    blend_w = []

    for i in range(n_verts):
        frac = i / (n_verts - 1)
        p = (1.0 - frac) * bot_tip_dmx + frac * top_tip_dmx
        new_pos.append(dm.Vector3(p.tolist()))

        if frac > 0.5:
            blend_idx += [upper_idx, 0, 0, 0]
        else:
            blend_idx += [lower_idx, 0, 0, 0]
        blend_w += [1.0, 0.0, 0.0, 0.0]

    vd_tet['position$0'] = dm.make_array(new_pos, dm.Vector3)
    vd_tet['blendindices$0'] = dm.make_array(blend_idx, int)
    vd_tet['blendweights$0'] = dm.make_array(blend_w, float)

    out_teteva = Path(r'extracted\archer_teteva.dmx')
    d_tet.write(str(out_teteva), "binary", 9)
    print(f"[OK] archer_teteva.dmx written: {out_teteva.stat().st_size:,} bytes")

    # =========================================================================
    # 3. BUILD CHARACTER BODY (archer_warka3.dmx)
    # =========================================================================
    print("\n--- 3. BUILDING WARKA3 WITH SAFE ISOLATED RIGGING ---")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Load reference warka for base body transfer
    warka_template_path = Path(r'extracted\archer_warka3_orig.dmx')
    info_warka = read_dmx_mesh(warka_template_path)
    ref_pos_w = dmx_to_blender(info_warka['positions'])

    me_ref_w = bpy.data.meshes.new("ref_warka_mesh")
    me_ref_w.from_pydata(ref_pos_w.tolist(), [], info_warka['tris'].tolist())
    me_ref_w.update()
    ref_warka = bpy.data.objects.new("ref_warka", me_ref_w)
    bpy.context.scene.collection.objects.link(ref_warka)

    for vi, (b_row, w_row) in enumerate(zip(info_warka['bones'], info_warka['weights'])):
        for b_name, w in zip(b_row, w_row):
            if w > 0.001 and b_name:
                vg = ref_warka.vertex_groups.get(b_name) or ref_warka.vertex_groups.new(name=b_name)
                vg.add([vi], float(w), 'REPLACE')

    # Materials
    mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
    mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
    mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")

    scale = 0.5471

    # Part A: Base Body (torso, arms, legs)
    base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=base_glb)
    base_objs = [o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH' and 'icosphere' not in o.name.lower()]

    for o in base_objs:
        o.scale = (scale, scale, scale)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        if o.data.shape_keys:
            for kb in list(o.data.shape_keys.key_blocks):
                o.shape_key_remove(kb)
        o.vertex_groups.clear()
        o.modifiers.clear()
        o.data.materials.clear()
        o.data.materials.append(mat_base)

    bpy.ops.object.select_all(action='DESELECT')
    for o in base_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = base_objs[0]
    bpy.ops.object.join()
    base_mesh = bpy.context.view_layer.objects.active
    base_mesh.name = "classic_base_body"

    # Transfer body weights from ref_warka
    mod_b = base_mesh.modifiers.new("DataTransfer", "DATA_TRANSFER")
    mod_b.object = ref_warka
    mod_b.use_vert_data = True
    mod_b.data_types_verts = {'VGROUP_WEIGHTS'}
    mod_b.vert_mapping = 'NEAREST'
    bpy.context.view_layer.objects.active = base_mesh
    bpy.ops.object.datalayout_transfer(modifier=mod_b.name)
    bpy.ops.object.modifier_apply(modifier=mod_b.name)

    # Clean up hands strictly within the hand bounding box (0.80 < Z < 1.40):
    vg_hand_L = base_mesh.vertex_groups.get("hand_L") or base_mesh.vertex_groups.new(name="hand_L")
    vg_hand_R = base_mesh.vertex_groups.get("hand_R") or base_mesh.vertex_groups.new(name="hand_R")

    left_clean, right_clean = 0, 0
    for v in base_mesh.data.vertices:
        # STRICT check: Must be in arm/hand height (0.80 < Z < 1.40) so LEGS ARE NEVER TOUCHED!
        if 0.80 < v.co.z < 1.40:
            if v.co.x > 0.42:
                # Left hand (bow grip)
                left_clean += 1
                for g in list(v.groups):
                    base_mesh.vertex_groups[g.group].remove([v.index])
                vg_hand_L.add([v.index], 1.0, 'REPLACE')
            elif v.co.x < -0.42:
                # Right hand (drawing hand)
                right_clean += 1
                for g in list(v.groups):
                    base_mesh.vertex_groups[g.group].remove([v.index])
                vg_hand_R.add([v.index], 1.0, 'REPLACE')

    print(f"Hand cleanup complete: {left_clean} left verts -> hand_L, {right_clean} right verts -> hand_R. 0 leg verts affected!")

    # Part B: Head / Hair
    head_glb = os.path.join(wr_dir, "windrunner_head.glb")
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=head_glb)
    head_mesh = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')
    head_mesh.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = head_mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    head_mesh.vertex_groups.clear()
    head_mesh.modifiers.clear()
    head_mesh.data.materials.clear()
    head_mesh.data.materials.append(mat_hair)

    vg_head = head_mesh.vertex_groups.new(name="head")
    for v in head_mesh.data.vertices:
        vg_head.add([v.index], 1.0, 'REPLACE')

    # Part C: Shoulderpads (Clean 0% head/neck rigging!)
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
            # Left shoulderpad
            factor = max(0.0, min(1.0, (v.co.x - 0.10) / 0.30))
            w_arm = factor * 0.40
            w_clav = 1.0 - w_arm
            vg_clav_L.add([v.index], w_clav, 'REPLACE')
            vg_arm_L.add([v.index], w_arm, 'REPLACE')
        else:
            # Right shoulder strap
            factor = max(0.0, min(1.0, (-v.co.x - 0.10) / 0.20))
            w_arm = factor * 0.30
            w_clav = 1.0 - w_arm
            vg_clav_R.add([v.index], w_clav, 'REPLACE')
            vg_arm_R.add([v.index], w_arm, 'REPLACE')
    print("Shoulderpads rigged cleanly with ZERO head/neck weights!")

    # Part D: Quiver
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

    # Attach quiver firmly to spine_2 (upper back) with subtle quiver_jiggle bounce:
    vg_sp2 = quiver_mesh.vertex_groups.new(name="spine_2")
    vg_qj = quiver_mesh.vertex_groups.new(name="quiver_jiggle")
    for v in quiver_mesh.data.vertices:
        vg_sp2.add([v.index], 0.70, 'REPLACE')
        vg_qj.add([v.index], 0.30, 'REPLACE')
    print("Quiver rigged to upper back (spine_2 + gentle quiver_jiggle)!")

    # Part E: Cape (Subtle natural cloth movement!)
    cape_glb = os.path.join(wr_dir, "windrunner_cape.glb")
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=cape_glb)
    cape_mesh = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')
    cape_mesh.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = cape_mesh
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    cape_mesh.vertex_groups.clear()
    cape_mesh.modifiers.clear()
    cape_mesh.data.materials.clear()
    cape_mesh.data.materials.append(mat_cape)

    # Natural spine & hip cloth gradient:
    # Top collar: spine_3
    # Upper back: spine_2
    # Mid back: spine_1
    # Lower cape: pelvis (gives natural sway with character locomotion without breaking!)
    vg_cape_sp3 = cape_mesh.vertex_groups.new(name="spine_3")
    vg_cape_sp2 = cape_mesh.vertex_groups.new(name="spine_2")
    vg_cape_sp1 = cape_mesh.vertex_groups.new(name="spine_1")
    vg_cape_pelvis = cape_mesh.vertex_groups.new(name="pelvis")

    for v in cape_mesh.data.vertices:
        z = v.co.z
        if z > 1.50:
            vg_cape_sp3.add([v.index], 1.0, 'REPLACE')
        elif z > 1.25:
            f = (z - 1.25) / 0.25
            vg_cape_sp3.add([v.index], f, 'REPLACE')
            vg_cape_sp2.add([v.index], 1.0 - f, 'REPLACE')
        elif z > 1.00:
            f = (z - 1.00) / 0.25
            vg_cape_sp2.add([v.index], f, 'REPLACE')
            vg_cape_sp1.add([v.index], 1.0 - f, 'REPLACE')
        else:
            # Lower flowing tail: blends to pelvis so it sways with hip bobbing and running
            f = max(0.0, min(1.0, (1.00 - z) / 0.40))
            vg_cape_sp1.add([v.index], 1.0 - f * 0.70, 'REPLACE')
            vg_cape_pelvis.add([v.index], f * 0.70, 'REPLACE')

    print("Cape rigged with smooth spine-to-pelvis locomotion gradient!")

    # Join all 5 parts together
    all_parts = [base_mesh, head_mesh, shoulder_mesh, quiver_mesh, cape_mesh]
    bpy.ops.object.select_all(action='DESELECT')
    for p in all_parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = base_mesh
    bpy.ops.object.join()
    final_warka = bpy.context.view_layer.objects.active
    final_warka.name = "classic_windrunner_body"

    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    out_warka_dmx = Path(r'extracted\archer_warka3.dmx')
    _export_dmx(final_warka, out_warka_dmx, warka_template_path)
    print(f"[OK] archer_warka3.dmx written: {out_warka_dmx.stat().st_size:,} bytes")
    print("=== PIPELINE FINISHED SUCCESSFULLY ===")

def _export_dmx(obj, out_path, template_path):
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
    d.write(str(out_path), "binary", 9)

if __name__ == "__main__":
    run_pipeline()

