import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_bow.glb"
bpy.ops.import_scene.gltf(filepath=glb)

bow = next(o for o in bpy.data.objects if o.type == 'MESH')
pos = np.array([v.co for v in bow.data.vertices])

center = np.mean(pos, axis=0)
diff = pos - center
cov = np.cov(diff.T)
eigvals, eigvecs = np.linalg.eigh(cov)

print("Classic bow raw bounds:")
print(f"X: [{pos[:,0].min():.4f}, {pos[:,0].max():.4f}]")
print(f"Y: [{pos[:,1].min():.4f}, {pos[:,1].max():.4f}]")
print(f"Z: [{pos[:,2].min():.4f}, {pos[:,2].max():.4f}]")
print("Major axis (length of bow):", eigvecs[:, 2])
print("Second axis (curve of bow):", eigvecs[:, 1])
print("Normal axis (thickness):", eigvecs[:, 0])

