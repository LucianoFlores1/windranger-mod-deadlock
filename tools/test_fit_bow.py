import bpy
import os
import sys
import math
from mathutils import Vector
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Mod bow
info = read_dmx_mesh(Path(r'extracted\archer_bow1.dmx'))
pos = dmx_to_blender(info['positions'])
me_ref = bpy.data.meshes.new("ref_bow")
me_ref.from_pydata(pos.tolist(), [], info['tris'].tolist())
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

ref_center = np.mean(pos, axis=0)

# 2. Classic bow
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bow_glb = os.path.join(wr_dir, "windrunner_bow.glb")
bpy.ops.import_scene.gltf(filepath=bow_glb)
classic_bow = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ref_bow)

# Clean classic bow
if classic_bow.data.shape_keys:
    for kb in list(classic_bow.data.shape_keys.key_blocks):
        classic_bow.shape_key_remove(kb)
classic_bow.vertex_groups.clear()
classic_bow.modifiers.clear()

# Rotate classic bow so length X aligns to Z, and curve Y aligns to X
classic_bow.rotation_euler = (0, math.radians(-90), math.radians(90))
scale_factor = 0.4638
classic_bow.scale = (scale_factor, scale_factor, scale_factor)
bpy.context.view_layer.objects.active = classic_bow
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Move classic bow to ref center
cur_center = np.mean([v.co for v in classic_bow.data.vertices], axis=0)
classic_bow.location += Vector((ref_center - cur_center).tolist())
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

c_xs = [v.co.x for v in classic_bow.data.vertices]
c_ys = [v.co.y for v in classic_bow.data.vertices]
c_zs = [v.co.z for v in classic_bow.data.vertices]
print(f"Fitted Classic bow bounds: X=[{min(c_xs):.2f}, {max(c_xs):.2f}], Y=[{min(c_ys):.2f}, {max(c_ys):.2f}], Z=[{min(c_zs):.2f}, {max(c_zs):.2f}]")

# Transfer weights from ref_bow
mod = classic_bow.modifiers.new("DataTransfer", "DATA_TRANSFER")
mod.object = ref_bow
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'NEAREST'
bpy.context.view_layer.objects.active = classic_bow
bpy.ops.object.datalayout_transfer(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)

# Normalize
bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)

unweighted = [v.index for v in classic_bow.data.vertices if not any(g.weight > 0.001 for g in v.groups)]
print(f"Classic bow unweighted vertices: {len(unweighted)}")
print(f"Classic bow vertex groups: {len(classic_bow.vertex_groups)}")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_fitted_bow.blend")
print("Saved to extracted/test_fitted_bow.blend")
