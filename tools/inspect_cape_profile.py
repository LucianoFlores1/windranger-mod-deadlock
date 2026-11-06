import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
cape_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_cape.glb"
bpy.ops.import_scene.gltf(filepath=cape_glb)

cape = next(o for o in bpy.data.objects if o.type == 'MESH')
pos = np.array([v.co for v in cape.data.vertices]) * 0.5471

print(f"Cape vertices: {len(pos)}")
print(f"X (lateral): [{pos[:,0].min():.2f}, {pos[:,0].max():.2f}]")
print(f"Y (front-back): [{pos[:,1].min():.2f}, {pos[:,1].max():.2f}]")
print(f"Z (height): [{pos[:,2].min():.2f}, {pos[:,2].max():.2f}]")

# Height profile of cape:
# Top collar/shoulders: Z > 1.45
# Mid back: Z in [1.0, 1.45]
# Lower cape / legs: Z < 1.0
top_verts = np.sum(pos[:, 2] > 1.45)
mid_verts = np.sum((pos[:, 2] <= 1.45) & (pos[:, 2] > 0.90))
bot_verts = np.sum(pos[:, 2] <= 0.90)
print(f"Cape vertical distribution: Top={top_verts}, Mid={mid_verts}, Bot={bot_verts}")

