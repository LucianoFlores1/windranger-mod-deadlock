import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender

bpy.ops.wm.read_factory_settings(use_empty=True)
scale = 0.5471
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

# Load ref warka
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
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

# Materials
mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")

# 1. Shoulderpads (Separate)
sh_glb = os.path.join(wr_dir, "windrunner_shoulderpads.glb")
before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=sh_glb)
shoulder_mesh = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')
shoulder_mesh.scale = (scale, scale, scale)
bpy.context.view_layer.objects.active = shoulder_mesh
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
shoulder_mesh.vertex_groups.clear()
shoulder_mesh.data.materials.clear()
shoulder_mesh.data.materials.append(mat_shoulders)

vg_clav_L = shoulder_mesh.vertex_groups.new(name="clavicle_L")
vg_arm_L = shoulder_mesh.vertex_groups.new(name="arm_upper_L")
vg_clav_R = shoulder_mesh.vertex_groups.new(name="clavicle_R")
vg_arm_R = shoulder_mesh.vertex_groups.new(name="arm_upper_R")

for v in shoulder_mesh.data.vertices:
    if v.co.x > 0.0:
        factor = max(0.0, min(1.0, (v.co.x - 0.10) / 0.30))
        w_arm = factor * 0.30
        vg_clav_L.add([v.index], 1.0 - w_arm, 'REPLACE')
        vg_arm_L.add([v.index], w_arm, 'REPLACE')
    else:
        factor = max(0.0, min(1.0, (-v.co.x - 0.10) / 0.20))
        w_arm = factor * 0.30
        vg_clav_R.add([v.index], 1.0 - w_arm, 'REPLACE')
        vg_arm_R.add([v.index], w_arm, 'REPLACE')

# 2. Quiver (Separate - 100% spine_2 so it NEVER rotates with head/neck/arm!)
quiv_glb = os.path.join(wr_dir, "windrunner_quiver.glb")
before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=quiv_glb)
quiver_mesh = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'MESH')
quiver_mesh.scale = (scale, scale, scale)
bpy.context.view_layer.objects.active = quiver_mesh
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
quiver_mesh.vertex_groups.clear()
quiver_mesh.data.materials.clear()
quiver_mesh.data.materials.append(mat_quiver)

vg_q_sp2 = quiver_mesh.vertex_groups.new(name="spine_2")
for v in quiver_mesh.data.vertices:
    vg_q_sp2.add([v.index], 1.0, 'REPLACE')

# 3. Base body, Hair, Cape
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

# DataTransfer
mod = body_main.modifiers.new("DataTransfer", "DATA_TRANSFER")
mod.object = ref_warka
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'NEAREST'
bpy.context.view_layer.objects.active = body_main
bpy.ops.object.datalayout_transfer(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)

# Post-transfer cleanup:
group_map = {g.name: g for g in body_main.vertex_groups}
vg_cR = group_map.get('clavicle_R') or body_main.vertex_groups.new(name='clavicle_R')
vg_auR = group_map.get('arm_upper_R') or body_main.vertex_groups.new(name='arm_upper_R')
vg_cL = group_map.get('clavicle_L') or body_main.vertex_groups.new(name='clavicle_L')
vg_auL = group_map.get('arm_upper_L') or body_main.vertex_groups.new(name='arm_upper_L')
vg_hL = group_map.get('hand_L') or body_main.vertex_groups.new(name='hand_L')
vg_hR = group_map.get('hand_R') or body_main.vertex_groups.new(name='hand_R')

# Fix Right Shoulder (remove spine_0, spine_1, clavicle_L, head, neck_0)
r_sh_fixed = 0
for v in body_main.data.vertices:
    if v.co.x < -0.15 and v.co.z > 1.25:
        removed = 0.0
        for g_entry in list(v.groups):
            g_name = body_main.vertex_groups[g_entry.group].name
            if g_name in ['spine_0', 'spine_1', 'clavicle_L', 'head', 'neck_0']:
                removed += g_entry.weight
                body_main.vertex_groups[g_entry.group].remove([v.index])
        if removed > 0.01:
            r_sh_fixed += 1
            target = vg_cR if v.co.x > -0.28 else vg_auR
            try: cur = target.weight(v.index)
            except: cur = 0.0
            target.add([v.index], cur + removed, 'REPLACE')
print(f"Right shoulder verts cleaned: {r_sh_fixed}")

# Fix Left Shoulder (remove spine_0, spine_1, clavicle_R, head, neck_0)
l_sh_fixed = 0
for v in body_main.data.vertices:
    if v.co.x > 0.15 and v.co.z > 1.25:
        removed = 0.0
        for g_entry in list(v.groups):
            g_name = body_main.vertex_groups[g_entry.group].name
            if g_name in ['spine_0', 'spine_1', 'clavicle_R', 'head', 'neck_0']:
                removed += g_entry.weight
                body_main.vertex_groups[g_entry.group].remove([v.index])
        if removed > 0.01:
            l_sh_fixed += 1
            target = vg_cL if v.co.x < 0.28 else vg_auL
            try: cur = target.weight(v.index)
            except: cur = 0.0
            target.add([v.index], cur + removed, 'REPLACE')
print(f"Left shoulder verts cleaned: {l_sh_fixed}")

# Clean Hands (ONLY X > 0.48 or X < -0.48, so FOREARMS ARE UNTOUCHED!)
l_h_fixed = 0
for v in body_main.data.vertices:
    if v.co.x > 0.48 and 0.85 < v.co.z < 1.25:
        meta_w = 0.0
        for g_entry in list(v.groups):
            g_name = body_main.vertex_groups[g_entry.group].name
            if 'pinky' in g_name or 'meta' in g_name or 'leg' in g_name:
                meta_w += g_entry.weight
                body_main.vertex_groups[g_entry.group].remove([v.index])
        if meta_w > 0.01:
            l_h_fixed += 1
            try: cur = vg_hL.weight(v.index)
            except: cur = 0.0
            vg_hL.add([v.index], cur + meta_w, 'REPLACE')
print(f"Left hand verts cleaned: {l_h_fixed}")

r_h_fixed = 0
for v in body_main.data.vertices:
    if v.co.x < -0.48 and 0.85 < v.co.z < 1.25:
        meta_w = 0.0
        for g_entry in list(v.groups):
            g_name = body_main.vertex_groups[g_entry.group].name
            if 'pinky' in g_name or 'meta' in g_name or 'leg' in g_name:
                meta_w += g_entry.weight
                body_main.vertex_groups[g_entry.group].remove([v.index])
        if meta_w > 0.01:
            r_h_fixed += 1
            try: cur = vg_hR.weight(v.index)
            except: cur = 0.0
            vg_hR.add([v.index], cur + meta_w, 'REPLACE')
print(f"Right hand verts cleaned: {r_h_fixed}")

# Cape:
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
print(f"Cape vertices updated: {len(cape_verts)}")

# NOW JOIN shoulder_mesh AND quiver_mesh
bpy.ops.object.select_all(action='DESELECT')
shoulder_mesh.select_set(True)
quiver_mesh.select_set(True)
body_main.select_set(True)
bpy.context.view_layer.objects.active = body_main
bpy.ops.object.join()
final_body = bpy.context.view_layer.objects.active
bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)
print("Joined final body with 0 head/neck weights on shoulders and quiver!")

