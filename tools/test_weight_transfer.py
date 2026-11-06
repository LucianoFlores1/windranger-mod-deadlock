import sys
import os
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load Archer Armature
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
arc_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')

# 2. Load warka3 as reference object with weights
info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = dmx_to_blender(info['positions'])
me_ref = bpy.data.meshes.new("ref_mesh")
me_ref.from_pydata(pos.tolist(), [], info['tris'].tolist())
me_ref.update()
ref_obj = bpy.data.objects.new("ref_warka", me_ref)
bpy.context.scene.collection.objects.link(ref_obj)

# Create vertex groups on ref_obj from info['bones'] and info['weights']
bone_names = info['bones']
weights = info['weights']
for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
    for b_name, w in zip(b_row, w_row):
        if w > 0.001 and b_name:
            vg = ref_obj.vertex_groups.get(b_name) or ref_obj.vertex_groups.new(name=b_name)
            vg.add([vi], float(w), 'REPLACE')

print(f"Reference object created with {len(ref_obj.vertex_groups)} vertex groups.")

# 3. Import classic Windrunner parts
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

parts = [
    (base_glb, "windranger_base"),
    (os.path.join(wr_dir, "windrunner_head.glb"), "windrunner_hair"),
    (os.path.join(wr_dir, "windrunner_cape.glb"), "windrunner_cape"),
    (os.path.join(wr_dir, "windrunner_shoulderpads.glb"), "windrunner_shoulders"),
    (os.path.join(wr_dir, "windrunner_quiver.glb"), "windrunner_quiver"),
]

classic_meshes = []
for fpath, label in parts:
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
            classic_meshes.append(o)
        elif o.type == 'ARMATURE' and o != arc_arm:
            bpy.data.objects.remove(o)

# Scale all classic meshes to match ref_obj
scale = 0.5471
for m in classic_meshes:
    m.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Join classic meshes
bpy.ops.object.select_all(action='DESELECT')
for m in classic_meshes:
    m.select_set(True)
bpy.context.view_layer.objects.active = classic_meshes[0]
bpy.ops.object.join()
joined = bpy.context.view_layer.objects.active
joined.name = "classic_windrunner_body"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

print(f"Joined classic mesh: {len(joined.data.vertices)} vertices, {len(joined.data.polygons)} polygons.")

# 4. Transfer weights from ref_obj to joined
mod = joined.modifiers.new("DataTransfer", "DATA_TRANSFER")
mod.object = ref_obj
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'NEAREST'
bpy.context.view_layer.objects.active = joined
bpy.ops.object.datalayout_transfer(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)

# Limit total to 4 bones and normalize
bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)

# Verify weights
unweighted = []
for v in joined.data.vertices:
    total_w = sum(g.weight for g in v.groups if g.weight > 0.001)
    if total_w < 0.001:
        unweighted.append(v.index)

print(f"Unweighted vertices after transfer: {len(unweighted)}")
print(f"Vertex groups on joined: {len(joined.vertex_groups)}")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_transfer.blend")
print("Saved to extracted/test_transfer.blend")
