import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)

arms = [o for o in bpy.context.scene.objects if 'arms' in o.name.lower()][0]
print("Arms vertex groups count:", len(arms.vertex_groups))
for g in arms.vertex_groups:
    verts = [v for v in arms.data.vertices if any(vg.group == g.index and vg.weight > 0.05 for vg in v.groups)]
    if len(verts) > 0 and any(k in g.name for k in ['bicep', 'elbow', 'wrist', 'clavicle', 'hand', 'mid', 'thumb', 'ring']):
        print(f"  {g.name:20s}: {len(verts)} vertices")

