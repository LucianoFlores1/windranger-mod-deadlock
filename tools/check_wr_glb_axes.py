import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)

# Find meshes: windranger_base_arms, windranger_legs, etc.
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        pts = np.array([v.co for v in o.data.vertices]) * 0.5471
        print(f"Object {o.name:35s}:")
        print(f"  X = [{pts[:,0].min():+.3f}, {pts[:,0].max():+.3f}]")
        print(f"  Y = [{pts[:,1].min():+.3f}, {pts[:,1].max():+.3f}]")
        print(f"  Z = [{pts[:,2].min():+.3f}, {pts[:,2].max():+.3f}]")

