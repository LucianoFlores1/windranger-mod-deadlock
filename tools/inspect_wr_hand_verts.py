import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)

# Find arms mesh
arms_mesh = [o for o in bpy.context.scene.objects if 'arms' in o.name.lower()][0]
# How many vertices are in the left hand (X > 0.40)?
hand_verts = [v for v in arms_mesh.data.vertices if v.co.x * 0.5471 > 0.45]
print(f"Total left hand vertices in Dota 2 Windrunner: {len(hand_verts)}")

# What vertex groups did Dota 2 Windrunner have originally?
print("Original vertex groups in windrunner arms:")
for g in arms_mesh.vertex_groups:
    print(" ", g.name)

