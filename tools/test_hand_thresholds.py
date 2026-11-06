import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)
scale = 0.5471

objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and 'icosphere' not in o.name.lower()]
for m in objs:
    m.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Join
bpy.ops.object.select_all(action='DESELECT')
for m in objs:
    m.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
bpy.ops.object.join()
joined = bpy.context.view_layer.objects.active

pts = np.array([v.co for v in joined.data.vertices])
print("Joined base mesh:")
print("X > 0.40 count:", np.sum(pts[:,0] > 0.40))
print("X > 0.45 count:", np.sum(pts[:,0] > 0.45))
print("X > 0.48 count:", np.sum(pts[:,0] > 0.48))
print("X < -0.40 count:", np.sum(pts[:,0] < -0.40))
print("X < -0.45 count:", np.sum(pts[:,0] < -0.45))
print("X < -0.48 count:", np.sum(pts[:,0] < -0.48))

# Check Z range of X > 0.40
mask_L = pts[:,0] > 0.40
print(f"Left hand (X > 0.40): Z in [{pts[mask_L, 2].min():.2f}, {pts[mask_L, 2].max():.2f}]")
mask_R = pts[:,0] < -0.40
print(f"Right hand (X < -0.40): Z in [{pts[mask_R, 2].min():.2f}, {pts[mask_R, 2].max():.2f}]")

