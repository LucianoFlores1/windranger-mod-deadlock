import bpy
import numpy as np
import os
import math
from mathutils import Vector
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

ref_center = np.mean(pos_bow, axis=0)
ref_span = np.ptp(pos_bow, axis=0)
print(f"Ref bow center: {ref_center}")
print(f"Ref bow span:   {ref_span}")

# 2. Classic bow
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_bow.glb"))
c_bow = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ref_obj)

# Clean
if c_bow.data.shape_keys:
    for kb in list(c_bow.data.shape_keys.key_blocks):
        c_bow.shape_key_remove(kb)
c_bow.vertex_groups.clear()
c_bow.modifiers.clear()

# Try rotation (0, -90 deg, 0)
c_bow.rotation_euler = (0, math.radians(-90), 0)
bpy.context.view_layer.objects.active = c_bow
bpy.ops.object.transform_apply(rotation=True)

# Check span
verts = np.array([v.co for v in c_bow.data.vertices])
c_span = np.ptp(verts, axis=0)
print(f"Classic bow span after rot Y=-90: {c_span}")

# Scale factor: ref Z span / classic Z span
scale_factor = ref_span[2] / c_span[2]
print(f"Scale factor: {scale_factor:.4f}")
c_bow.scale = (scale_factor, scale_factor, scale_factor)
bpy.ops.object.transform_apply(scale=True)

# Center alignment
cur_center = np.mean([v.co for v in c_bow.data.vertices], axis=0)
c_bow.location += Vector((ref_center - cur_center).tolist())
bpy.ops.object.transform_apply(location=True)

verts_final = np.array([v.co for v in c_bow.data.vertices])
print("Fitted classic bow bounds:")
print(f"  X: {verts_final[:,0].min():.3f} to {verts_final[:,0].max():.3f}")
print(f"  Y: {verts_final[:,1].min():.3f} to {verts_final[:,1].max():.3f}")
print(f"  Z: {verts_final[:,2].min():.3f} to {verts_final[:,2].max():.3f}")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_direct_bow_fit.blend")
print("Saved blend to extracted/test_direct_bow_fit.blend")

