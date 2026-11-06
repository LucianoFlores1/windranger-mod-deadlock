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

def build_fixed_assets():
    print("=== STARTING COMPLETE FIX PIPELINE ===")
    
    # -------------------------------------------------------------
    # PART 1: FIX BOW (archer_bow1.dmx)
    # -------------------------------------------------------------
    print("\n--- 1. BUILDING CLEANLY ALIGNED BOW ---")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Load ref bow
    bow_template_path = Path(r'extracted\archer_bow1_orig.dmx')
    info = read_dmx_mesh(bow_template_path)
    ref_pos = dmx_to_blender(info['positions'])
    ref_center = np.mean(ref_pos, axis=0)
    ref_span = np.ptp(ref_pos, axis=0)

    me_ref = bpy.data.meshes.new("ref_bow_mesh")
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

    # Clean classic bow
    if classic_bow.data.shape_keys:
        for kb in list(classic_bow.data.shape_keys.key_blocks):
            classic_bow.shape_key_remove(kb)
    classic_bow.vertex_groups.clear()
    classic_bow.modifiers.clear()

    # Apply the mathematically optimal rotation matrix:
    # X -> Z, Y -> -X, Z -> -Y
    rot_mat = Matrix([
        [ 0.0, -1.0,  0.0, 0.0],
        [ 0.0,  0.0, -1.0, 0.0],
        [ 1.0,  0.0,  0.0, 0.0],
        [ 0.0,  0.0,  0.0, 1.0]
    ])
    classic_bow.data.transform(rot_mat)

    # Scale to match ref_bow vertical span
    c_pos = np.array([v.co for v in classic_bow.data.vertices])
    c_span_z = np.ptp(c_pos[:, 2])
    scale_factor = ref_span[2] / c_span_z
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

    # Transfer weights from ref_bow
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

    # Save fitted bow vertices for teteva calculation
    fitted_bow_pos = np.array([v.co for v in classic_bow.data.vertices])
    bow_top_tip = max(fitted_bow_pos, key=lambda p: p[2])
    bow_bot_tip = min(fitted_bow_pos, key=lambda p: p[2])
    print(f"Bow fitted: top tip={bow_top_tip}, bot tip={bow_bot_tip}")

    # Export archer_bow1.dmx
    out_bow_dmx = Path(r'extracted\archer_bow1.dmx')
    _export_dmx(classic_bow, out_bow_dmx, bow_template_path)
    print(f"[OK] archer_bow1.dmx written: {out_bow_dmx.stat().st_size:,} bytes")

    # -------------------------------------------------------------
    # PART 2: FIX BOWSTRING (archer_teteva.dmx)
    # -------------------------------------------------------------
    print("\n--- 2. BUILDING DYNAMIC BOWSTRING ---")
    d_tet = dm.load(r'extracted\archer_teteva.dmx')
    c_tet = next(c for c in d_tet.root['model']['children'] if c.type == 'DmeDag')
    vd_tet = c_tet['shape']['currentState']
    model_tet = d_tet.root['model']
    joint_index = {j.name: i for i, j in enumerate(model_tet['jointList'])}
    upper_idx = joint_index.get('upperLimb_1', joint_index.get('upperLimb_end', 0))
    lower_idx = joint_index.get('lowerLimb_1', joint_index.get('lowerLimb_end', 0))
    string_idx = joint_index.get('bow_string', 0)

    # Convert bow tips to DMX coords
    top_tip_dmx = blender_to_dmx(bow_top_tip)
    bot_tip_dmx = blender_to_dmx(bow_bot_tip)
    
    # Grip / rest point of bowstring (near handle)
    mid_bow_dmx = (top_tip_dmx + bot_tip_dmx) / 2.0
    # In DMX, string pulls slightly back toward -Y (or toward bow_string bone)

    n_verts = len(vd_tet['position$0']) # 32 vertices
    new_pos = []
    blend_idx = []
    blend_w = []

    for i in range(n_verts):
        frac = i / (n_verts - 1)
        # Position along the bow tips
        p = (1.0 - frac) * bot_tip_dmx + frac * top_tip_dmx
        new_pos.append(dm.Vector3(p.tolist()))

        # Weighting:
        # Extreme ends: 100% limb tips
        # Center (near frac=0.5): blend smoothly with bow_string bone!
        center_dist = abs(frac - 0.5) * 2.0 # 0 at center, 1 at ends
        string_weight = max(0.0, 1.0 - center_dist**1.5) * 0.70 # up to 70% to bow_string in center

        if frac > 0.5:
            limb_idx = upper_idx
        else:
            limb_idx = lower_idx

        limb_weight = 1.0 - string_weight
        blend_idx += [limb_idx, string_idx, 0, 0]
        blend_w += [float(limb_weight), float(string_weight), 0.0, 0.0]

    vd_tet['position$0'] = dm.make_array(new_pos, dm.Vector3)
    vd_tet['blendindices$0'] = dm.make_array(blend_idx, int)
    vd_tet['blendweights$0'] = dm.make_array(blend_w, float)

    out_teteva = Path(r'extracted\archer_teteva.dmx')
    d_tet.write(str(out_teteva), "binary", 9)
    print(f"[OK] archer_teteva.dmx written: {out_teteva.stat().st_size:,} bytes")

    # -------------------------------------------------------------
    # PART 3: FIX WARKA (BODY, CAPE, SHOULDERPAD, HANDS)
    # -------------------------------------------------------------
    print("\n--- 3. BUILDING WARKA3 WITH CLEAN RIGGING & CLOTH PHYSICS ---")
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Reference warka
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

    # Load base mesh
    base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=base_glb)
    base_objs = [o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH' and 'icosphere' not in o.name.lower()]

    # Join base body parts together first
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

    # CLEAN UP HANDS & FINGERS ON BASE BODY:
    # In Blender: X is lateral (arms)! Left hand is X > 0.40, Right hand is X < -0.40
    vg_hand_L = base_mesh.vertex_groups.get("hand_L") or base_mesh.vertex_groups.new(name="hand_L")
    vg_hand_R = base_mesh.vertex_groups.get("hand_R") or base_mesh.vertex_groups.new(name="hand_R")

    left_hand_count = 0
    right_hand_count = 0
    for v in base_mesh.data.vertices:
        # Left Hand (grip holding the bow): 100% clean to hand_L
        if v.co.x > 0.42:
            left_hand_count += 1
            for g in list(v.groups):
                base_mesh.vertex_groups[g.group].remove([v.index])
            vg_hand_L.add([v.index], 1.0, 'REPLACE')

        # Right Hand (drawing string): 100% clean to hand_R
        elif v.co.x < -0.42:
            right_hand_count += 1
            for g in list(v.groups):
                base_mesh.vertex_groups[g.group].remove([v.index])
            vg_hand_R.add([v.index], 1.0, 'REPLACE')

    print(f"Cleaned hands: {left_hand_count} left hand verts -> hand_L, {right_hand_count} right hand verts -> hand_R (0 collapsed fingers!)")

    # Load Head (Hair)
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

    # Hair / Ponytail dynamic rigging:
    # Head base to head bone; ponytail tip to hair_L_0..2 and hair_R_0..2 (Deadlock jiggle bones!)
    vg_head = head_mesh.vertex_groups.new(name="head")
    vg_hair_L = head_mesh.vertex_groups.new(name="hair_L_0")
    vg_hair_R = head_mesh.vertex_groups.new(name="hair_R_0")
    for v in head_mesh.data.vertices:
        # Ponytail hangs backward (-Y in Blender, or Y < -0.05)
        if v.co.y < -0.05 and v.co.z < 1.95:
            # Ponytail jiggle
            vg_head.add([v.index], 0.3, 'REPLACE')
            vg_hair_L.add([v.index], 0.35, 'REPLACE')
            vg_hair_R.add([v.index], 0.35, 'REPLACE')
        else:
            vg_head.add([v.index], 1.0, 'REPLACE')

    # Load Shoulderpads
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

    # Shoulderpad clean rigging:
    # 0% head, 0% neck! Only clavicle_L and arm_upper_L
    vg_clav_L = shoulder_mesh.vertex_groups.new(name="clavicle_L")
    vg_arm_L = shoulder_mesh.vertex_groups.new(name="arm_upper_L")
    for v in shoulder_mesh.data.vertices:
        # Left shoulder: X from 0.12 to 0.40
        factor = (v.co.x - 0.12) / 0.28
        factor = max(0.0, min(1.0, factor))
        w_arm = factor * 0.45
        w_clav = 1.0 - w_arm
        vg_clav_L.add([v.index], w_clav, 'REPLACE')
        vg_arm_L.add([v.index], w_arm, 'REPLACE')
    print("Shoulderpad rigged cleanly (100% clavicle_L / arm_upper_L, 0% head/neck!)")

    # Load Quiver
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

    # Quiver rigging:
    # Upper strap to spine_2, quiver body to quiver_jiggle (Deadlock's native jiggle bone!)
    vg_spine2 = quiver_mesh.vertex_groups.new(name="spine_2")
    vg_quiv_jig = quiver_mesh.vertex_groups.new(name="quiver_jiggle")
    for v in quiver_mesh.data.vertices:
        vg_spine2.add([v.index], 0.35, 'REPLACE')
        vg_quiv_jig.add([v.index], 0.65, 'REPLACE')
    print("Quiver rigged with Deadlock quiver_jiggle physics bone!")

    # Load Cape (The cloth movement fix!)
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

    # Cape Cloth Rigging:
    # - Top collar (Z > 1.45): spine_3 (70%), neck_0 (30%)
    # - Upper back (1.20 < Z <= 1.45): spine_2 (60%), spine_3 (40%)
    # - Mid back (0.95 < Z <= 1.20): spine_1 (40%), pelvis (40%), spine_2 (20%)
    # - Lower cape (Z <= 0.95):
    #     Left fold (X > 0.05): leg_upper_L (40%), pelvis (60%) -> sways with left leg!
    #     Right fold (X < -0.05): leg_upper_R (40%), pelvis (60%) -> sways with right leg!
    #     Center fold (|X| <= 0.05): pelvis (70%), spine_0 (30%)
    vg_sp3 = cape_mesh.vertex_groups.new(name="spine_3")
    vg_sp2 = cape_mesh.vertex_groups.new(name="spine_2")
    vg_sp1 = cape_mesh.vertex_groups.new(name="spine_1")
    vg_sp0 = cape_mesh.vertex_groups.new(name="spine_0")
    vg_pelvis = cape_mesh.vertex_groups.new(name="pelvis")
    vg_leg_L = cape_mesh.vertex_groups.new(name="leg_upper_L")
    vg_leg_R = cape_mesh.vertex_groups.new(name="leg_upper_R")
    vg_neck = cape_mesh.vertex_groups.new(name="neck_0")

    for v in cape_mesh.data.vertices:
        z = v.co.z
        x = v.co.x
        if z > 1.45:
            # Collar
            vg_sp3.add([v.index], 0.70, 'REPLACE')
            vg_neck.add([v.index], 0.30, 'REPLACE')
        elif z > 1.20:
            # Upper back
            f = (z - 1.20) / 0.25
            vg_sp3.add([v.index], 0.40 + 0.30 * f, 'REPLACE')
            vg_sp2.add([v.index], 0.60 - 0.30 * f, 'REPLACE')
        elif z > 0.95:
            # Mid back
            vg_sp2.add([v.index], 0.30, 'REPLACE')
            vg_sp1.add([v.index], 0.40, 'REPLACE')
            vg_pelvis.add([v.index], 0.30, 'REPLACE')
        else:
            # Lower flowing cape
            f_bot = max(0.0, min(1.0, (0.95 - z) / 0.50))
            leg_weight = 0.20 + 0.25 * f_bot # up to 45% leg sway at tip
            pelvis_weight = 1.0 - leg_weight
            if x > 0.03:
                vg_leg_L.add([v.index], leg_weight, 'REPLACE')
                vg_pelvis.add([v.index], pelvis_weight, 'REPLACE')
            elif x < -0.03:
                vg_leg_R.add([v.index], leg_weight, 'REPLACE')
                vg_pelvis.add([v.index], pelvis_weight, 'REPLACE')
            else:
                vg_pelvis.add([v.index], 0.70, 'REPLACE')
                vg_sp0.add([v.index], 0.30, 'REPLACE')
    print("Cape rigged with dynamic leg-sway & multi-spine cloth blending!")

    # JOIN ALL PARTS
    all_meshes = [base_mesh, head_mesh, shoulder_mesh, quiver_mesh, cape_mesh]
    bpy.ops.object.select_all(action='DESELECT')
    for m in all_meshes:
        m.select_set(True)
    bpy.context.view_layer.objects.active = base_mesh
    bpy.ops.object.join()
    final_warka = bpy.context.view_layer.objects.active
    final_warka.name = "classic_windrunner_final"

    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)

    out_warka_dmx = Path(r'extracted\archer_warka3.dmx')
    _export_dmx(final_warka, out_warka_dmx, warka_template_path)
    print(f"[OK] archer_warka3.dmx written: {out_warka_dmx.stat().st_size:,} bytes")
    print("=== PIPELINE COMPLETE ===")

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

    # Write DMX
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
    build_fixed_assets()
