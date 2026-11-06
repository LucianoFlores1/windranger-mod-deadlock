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

bpy.ops.object.select_all(action='DESELECT')
for m in objs:
    m.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
bpy.ops.object.join()
joined = bpy.context.view_layer.objects.active

pts = np.array([v.co for v in joined.data.vertices])

# Strict hand check: 0.85 < Z < 1.25
hand_L_mask = (pts[:,0] > 0.45) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)
print("Hand L (X > 0.45, 0.85 < Z < 1.25):", np.sum(hand_L_mask))

hand_R_mask = (pts[:,0] < -0.45) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)
print("Hand R (X < -0.45, 0.85 < Z < 1.25):", np.sum(hand_R_mask))

# Legs check: Z < 0.80
leg_mask = pts[:,2] < 0.80
print("Legs (Z < 0.80) X range:", pts[leg_mask, 0].min(), pts[leg_mask, 0].max())

