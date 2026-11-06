import bpy
import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load archer.glb (exported directly from Source2Viewer)
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
archer_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
for o in archer_objs:
    print(f"archer.glb obj: {o.name}")
    verts = np.array([v.co for v in o.data.vertices])
    print(f"  X: {verts[:,0].min():.2f} to {verts[:,0].max():.2f}")
    print(f"  Y: {verts[:,1].min():.2f} to {verts[:,1].max():.2f}")
    print(f"  Z: {verts[:,2].min():.2f} to {verts[:,2].max():.2f}")

# 2. Load warka from DMX using dmx_to_blender
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
w_blender = dmx_to_blender(info['positions'])
print(f"dmx_to_blender warka3_orig:")
print(f"  X: {w_blender[:,0].min():.2f} to {w_blender[:,0].max():.2f}")
print(f"  Y: {w_blender[:,1].min():.2f} to {w_blender[:,1].max():.2f}")
print(f"  Z: {w_blender[:,2].min():.2f} to {w_blender[:,2].max():.2f}")

# 3. Load windrunner.glb
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb")
wr_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o not in archer_objs]
for o in wr_objs:
    verts = np.array([v.co for v in o.data.vertices])
    print(f"windrunner.glb obj: {o.name}")
    print(f"  X: {verts[:,0].min():.2f} to {verts[:,0].max():.2f}")
    print(f"  Y: {verts[:,1].min():.2f} to {verts[:,1].max():.2f}")
    print(f"  Z: {verts[:,2].min():.2f} to {verts[:,2].max():.2f}")

