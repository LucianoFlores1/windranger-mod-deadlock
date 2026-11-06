import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np
import bpy
import os

info_bow = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
pos_bow = np.array(info_bow['positions']) * 0.0254 # Direct conversion in meters!

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Direct DMX ref bow in Blender
me_ref = bpy.data.meshes.new("ref_bow_direct")
me_ref.from_pydata(pos_bow.tolist(), [], info_bow['tris'].tolist())
me_ref.update()
ref_obj = bpy.data.objects.new("ref_bow_direct", me_ref)
bpy.context.scene.collection.objects.link(ref_obj)

print("Direct ref_bow bounds:")
print(f"  X: {pos_bow[:,0].min():.3f} to {pos_bow[:,0].max():.3f} (span: {pos_bow[:,0].max() - pos_bow[:,0].min():.3f})")
print(f"  Y: {pos_bow[:,1].min():.3f} to {pos_bow[:,1].max():.3f} (span: {pos_bow[:,1].max() - pos_bow[:,1].min():.3f})")
print(f"  Z: {pos_bow[:,2].min():.3f} to {pos_bow[:,2].max():.3f} (span: {pos_bow[:,2].max() - pos_bow[:,2].min():.3f})")

# 2. Classic bow from glb
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_bow.glb"))
c_bow = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ref_obj)
c_verts = np.array([v.co for v in c_bow.data.vertices])
print("Original windrunner_bow.glb bounds:")
print(f"  X: {c_verts[:,0].min():.3f} to {c_verts[:,0].max():.3f} (span: {c_verts[:,0].max() - c_verts[:,0].min():.3f})")
print(f"  Y: {c_verts[:,1].min():.3f} to {c_verts[:,1].max():.3f} (span: {c_verts[:,1].max() - c_verts[:,1].min():.3f})")
print(f"  Z: {c_verts[:,2].min():.3f} to {c_verts[:,2].max():.3f} (span: {c_verts[:,2].max() - c_verts[:,2].min():.3f})")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\compare_bow_direct.blend")
print("Saved blend to extracted/compare_bow_direct.blend")
