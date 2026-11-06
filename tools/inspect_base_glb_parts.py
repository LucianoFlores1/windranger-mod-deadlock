import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)

for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        pts = np.array([v.co for v in o.data.vertices])
        print(f"Mesh: {o.name}")
        print(f"  Verts: {len(pts)}")
        print(f"  X bounds: [{pts[:,0].min():.2f}, {pts[:,0].max():.2f}]")
        print(f"  Y bounds: [{pts[:,1].min():.2f}, {pts[:,1].max():.2f}]")
        print(f"  Z bounds: [{pts[:,2].min():.2f}, {pts[:,2].max():.2f}]")

