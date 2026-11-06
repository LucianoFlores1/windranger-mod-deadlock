import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb")
arms = next(o for o in bpy.context.scene.objects if 'arms' in o.name.lower())
verts = np.array([v.co for v in arms.data.vertices])

# Right hand: X < -0.6
r_hand_verts = [i for i, v in enumerate(verts) if v[0] < -0.8]
print(f"Windrunner right hand verts: {len(r_hand_verts)}")
for vi in r_hand_verts[:10]:
    v = arms.data.vertices[vi]
    print(f"  v{vi}: {[(arms.vertex_groups[g.group].name, round(g.weight, 2)) for g in v.groups]}")

