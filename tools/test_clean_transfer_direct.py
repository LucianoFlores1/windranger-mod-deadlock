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

def test_transfer():
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 1. Load ref warka with DIRECT conversion (pos * 0.0254)
    warka_template_path = Path(r'extracted\archer_warka3_orig.dmx')
    info = read_dmx_mesh(warka_template_path)
    ref_pos = np.array(info['positions']) * INCH

    me_ref = bpy.data.meshes.new("ref_mesh")
    me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
    me_ref.update()
    ref_obj = bpy.data.objects.new("ref_warka_direct", me_ref)
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

    # 2. Materials
    mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
    mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
    mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
    mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat")
    mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")

    # 3. Load classic Windrunner parts
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

    # Scale uniformly
    for m in classic_meshes:
        m.scale = (scale, scale, scale)
        bpy.context.view_layer.objects.active = m
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Join
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

    # 4. Transfer weights from ref_obj directly
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

    bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_direct_transfer.blend")
    print("Saved to extracted/test_direct_transfer.blend")

    # Let's inspect weights of some key vertices (head, hand_L, leg_lower_L, ankle_L)
    group_names = {g.index: g.name for g in joined.vertex_groups}
    # Head vertex (high Z):
    top_v = max(joined.data.vertices, key=lambda v: v.co.z)
    top_w = [(group_names[g.group], g.weight) for g in top_v.groups if g.weight > 0.01]
    print(f"Top vertex (head, Z={top_v.co.z:.2f}) bones:", top_w)

    # Left foot vertex (low Z, positive X):
    l_foot_v = min([v for v in joined.data.vertices if v.co.x > 0.1], key=lambda v: v.co.z)
    l_foot_w = [(group_names[g.group], g.weight) for g in l_foot_v.groups if g.weight > 0.01]
    print(f"Left foot vertex (Z={l_foot_v.co.z:.2f}, X={l_foot_v.co.x:.2f}) bones:", l_foot_w)

    # Right foot vertex (low Z, negative X):
    r_foot_v = min([v for v in joined.data.vertices if v.co.x < -0.1], key=lambda v: v.co.z)
    r_foot_w = [(group_names[g.group], g.weight) for g in r_foot_v.groups if g.weight > 0.01]
    print(f"Right foot vertex (Z={r_foot_v.co.z:.2f}, X={r_foot_v.co.x:.2f}) bones:", r_foot_w)

    # Left hand vertex (positive X, Z~1.2):
    l_hand_v = max([v for v in joined.data.vertices if v.co.x > 0.3], key=lambda v: v.co.x)
    l_hand_w = [(group_names[g.group], g.weight) for g in l_hand_v.groups if g.weight > 0.01]
    print(f"Left hand vertex (X={l_hand_v.co.x:.2f}, Z={l_hand_v.co.z:.2f}) bones:", l_hand_w)

if __name__ == "__main__":
    test_transfer()

