import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)
scale = 0.5471

arms = [o for o in bpy.context.scene.objects if 'arms' in o.name.lower()][0]
pts = np.array([v.co for v in arms.data.vertices]) * scale

print("Scaled arms X min/max:", pts[:,0].min(), pts[:,0].max())
print("Scaled arms Y min/max:", pts[:,1].min(), pts[:,1].max())
print("Scaled arms Z min/max:", pts[:,2].min(), pts[:,2].max())

# Where are the hand vertices? (lowest/outermost parts)
left_hand = pts[pts[:, 0] > 0.20]
print("Left arm/hand (X > 0.20) Z range:", left_hand[:, 2].min(), left_hand[:, 2].max())
right_hand = pts[pts[:, 0] < -0.20]
print("Right arm/hand (X < -0.20) Z range:", right_hand[:, 2].min(), right_hand[:, 2].max())

