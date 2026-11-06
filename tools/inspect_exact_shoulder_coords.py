import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
sh_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_shoulderpads.glb"
bpy.ops.import_scene.gltf(filepath=sh_glb)

m = next(o for o in bpy.data.objects if o.type == 'MESH')
pos = np.array([v.co for v in m.data.vertices]) * 0.5471

print("Shoulderpad coordinates:")
print(f"X: [{pos[:,0].min():.4f}, {pos[:,0].max():.4f}]")
print(f"Y: [{pos[:,1].min():.4f}, {pos[:,1].max():.4f}]")
print(f"Z: [{pos[:,2].min():.4f}, {pos[:,2].max():.4f}]")
print("Total vertices in shoulderpad:", len(pos))

