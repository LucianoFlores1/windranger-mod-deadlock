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

# Import base
before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=base_glb)
new_objs = set(bpy.context.scene.objects) - before
base_parts = [o for o in new_objs if o.type == 'MESH' and 'icosphere' not in o.name.lower()]
for m in base_parts:
    m.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    m.vertex_groups.clear()

bpy.ops.object.select_all(action='DESELECT')
for m in base_parts:
    m.select_set(True)
bpy.context.view_layer.objects.active = base_parts[0]
bpy.ops.object.join()
base_mesh = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# DataTransfer
mod = base_mesh.modifiers.new("DataTransfer", "DATA_TRANSFER")
mod.object = ref_warka
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'NEAREST'
bpy.context.view_layer.objects.active = base_mesh
bpy.ops.object.datalayout_transfer(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)

# Now check right shoulder vertices on base_mesh
pts = np.array([v.co for v in base_mesh.data.vertices])
r_sh_mask = (pts[:,0] < -0.15) & (pts[:,2] > 1.25)
print("Right shoulder verts in base_mesh:", np.sum(r_sh_mask))

# Check left shoulder verts in base_mesh
l_sh_mask = (pts[:,0] > 0.15) & (pts[:,2] > 1.25)
print("Left shoulder verts in base_mesh:", np.sum(l_sh_mask))

# Check wrist bounds
l_wrist_mask = (pts[:,0] > 0.48) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)
print("Left hand (X > 0.48):", np.sum(l_wrist_mask))
r_wrist_mask = (pts[:,0] < -0.48) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)
print("Right hand (X < -0.48):", np.sum(r_wrist_mask))

# Forearms:
l_forearm_mask = (pts[:,0] > 0.28) & (pts[:,0] <= 0.48) & (pts[:,2] > 0.85) & (pts[:,2] < 1.35)
print("Left forearm (0.28 < X <= 0.48):", np.sum(l_forearm_mask))
r_forearm_mask = (pts[:,0] < -0.28) & (pts[:,0] >= -0.48) & (pts[:,2] > 0.85) & (pts[:,2] < 1.35)
print("Right forearm (-0.48 <= X < -0.28):", np.sum(r_forearm_mask))

