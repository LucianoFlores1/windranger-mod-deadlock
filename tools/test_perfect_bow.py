import bpy
import numpy as np
import os
import math
from mathutils import Matrix, Vector
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Direct DMX ref bow in Blender (NO AXIS SWAP! Direct * 0.0254)
info_bow = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
pos_bow = np.array(info_bow['positions']) * 0.0254

me_ref = bpy.data.meshes.new("ref_bow_direct")
me_ref.from_pydata(pos_bow.tolist(), [], info_bow['tris'].tolist())
me_ref.update()
ref_obj = bpy.data.objects.new("ref_bow_direct", me_ref)
bpy.context.scene.collection.objects.link(ref_obj)

# Add vertex groups to ref_obj for weight transfer
for vi, (b_row, w_row) in enumerate(zip(info_bow['bones'], info_bow['weights'])):
    for b_name, w in zip(b_row, w_row):
        if w > 0.001 and b_name:
            vg = ref_obj.vertex_groups.get(b_name) or ref_obj.vertex_groups.new(name=b_name)
            vg.add([vi], float(w), 'REPLACE')

ref_center = np.mean(pos_bow, axis=0)
ref_span = np.ptp(pos_bow, axis=0)
print(f"Ref bow bounds: X=[{pos_bow[:,0].min():.2f}, {pos_bow[:,0].max():.2f}], Y=[{pos_bow[:,1].min():.2f}, {pos_bow[:,1].max():.2f}], Z=[{pos_bow[:,2].min():.2f}, {pos_bow[:,2].max():.2f}]")

# 2. Classic bow
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_bow.glb"))
c_bow = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ref_obj)

# Remove armatures
for o in list(bpy.context.scene.objects):
    if o.type == 'ARMATURE':
        bpy.data.objects.remove(o)

# Apply rotation: rot Y=-90 then rot Z=180
rot_mat = Matrix.Rotation(math.radians(180), 4, 'Z') @ Matrix.Rotation(math.radians(-90), 4, 'Y')
c_bow.data.transform(rot_mat)

verts = np.array([v.co for v in c_bow.data.vertices])
c_span = np.ptp(verts, axis=0)
scale_factor = ref_span[2] / c_span[2]
print(f"Scale factor: {scale_factor:.4f}")

# Apply scale
scale_mat = Matrix.Diagonal((scale_factor, scale_factor, scale_factor, 1.0))
c_bow.data.transform(scale_mat)

# Apply translation to match center
cur_center = np.mean([v.co for v in c_bow.data.vertices], axis=0)
diff = ref_center - cur_center
trans_mat = Matrix.Translation(Vector(diff.tolist()))
c_bow.data.transform(trans_mat)

verts_final = np.array([v.co for v in c_bow.data.vertices])
print(f"Classic bow bounds: X=[{verts_final[:,0].min():.2f}, {verts_final[:,0].max():.2f}], Y=[{verts_final[:,1].min():.2f}, {verts_final[:,1].max():.2f}], Z=[{verts_final[:,2].min():.2f}, {verts_final[:,2].max():.2f}]")

# Transfer weights from ref_obj
mod = c_bow.modifiers.new("DataTransfer", "DATA_TRANSFER")
mod.object = ref_obj
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'NEAREST'
bpy.context.view_layer.objects.active = c_bow
bpy.ops.object.datalayout_transfer(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)

# Normalize
bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)

unweighted = [v.index for v in c_bow.data.vertices if not any(g.weight > 0.001 for g in v.groups)]
print(f"Unweighted vertices: {len(unweighted)}")
print(f"Bow vertex groups: {len(c_bow.vertex_groups)}")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_perfect_bow.blend")
print("Saved blend to extracted/test_perfect_bow.blend")

