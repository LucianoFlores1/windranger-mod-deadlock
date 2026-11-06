import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
bpy.ops.import_scene.gltf(filepath=base_glb)

arms = next(o for o in bpy.data.objects if 'arms' in o.name.lower())
pos = np.array([v.co for v in arms.data.vertices]) * 0.5471

# In arms: Left hand is max X, Right hand is min X
# Let's find vertices with |X| > 0.40 and Z between 0.8 and 1.4
l_hand = [p for p in pos if p[0] > 0.40 and 0.80 < p[2] < 1.40]
r_hand = [p for p in pos if p[0] < -0.40 and 0.80 < p[2] < 1.40]
print(f"Arms mesh: {len(pos)} verts")
print(f"Left hand verts (|X| > 0.40, 0.8 < Z < 1.4): {len(l_hand)}")
print(f"Right hand verts (|X| < -0.40, 0.8 < Z < 1.4): {len(r_hand)}")

# Check if ANY vertex in the other meshes (legs, torso) has |X| > 0.40 and 0.8 < Z < 1.4:
for o in bpy.data.objects:
    if o.type == 'MESH' and 'arms' not in o.name.lower() and 'icosphere' not in o.name.lower():
        p = np.array([v.co for v in o.data.vertices]) * 0.5471
        bad = [v for v in p if abs(v[0]) > 0.40 and 0.80 < v[2] < 1.40]
        print(f"Mesh {o.name}: {len(bad)} verts in hand box")

