import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
head_glb = os.path.join(wr_dir, "windrunner_head.glb")
bpy.ops.import_scene.gltf(filepath=head_glb)
h_mesh = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
h_pos = np.array([v.co for v in h_mesh.data.vertices]) * 0.5471

# Find the lowest 10% Z vertices (the tip of her hair / ponytail)
lowest_z_mask = h_pos[:, 2] < (h_pos[:, 2].min() + 0.1)
ponytail_pos = h_pos[lowest_z_mask]
print("Ponytail (lowest Z of hair) Y range:", ponytail_pos[:, 1].min(), "to", ponytail_pos[:, 1].max(), "mean:", np.mean(ponytail_pos[:, 1]))

# Find the face / eyes / nose in windrunner_head.glb:
highest_z = h_pos[:, 2].max()
top_head = h_pos[h_pos[:, 2] > (highest_z - 0.1)]
print("Top of head Y range:", top_head[:, 1].min(), "to", top_head[:, 1].max(), "mean:", np.mean(top_head[:, 1]))

# What about the cape? windrunner_cape.glb
cape_glb = os.path.join(wr_dir, "windrunner_cape.glb")
bpy.ops.import_scene.gltf(filepath=cape_glb)
c_mesh = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o != h_mesh][0]
c_pos = np.array([v.co for v in c_mesh.data.vertices]) * 0.5471
print("Cape mesh Y range:", c_pos[:, 1].min(), "to", c_pos[:, 1].max(), "mean:", np.mean(c_pos[:, 1]))

