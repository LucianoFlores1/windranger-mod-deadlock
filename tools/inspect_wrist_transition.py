import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
bpy.ops.import_scene.gltf(filepath=base_glb)

arms = [o for o in bpy.context.scene.objects if 'arms' in o.name.lower()][0]
wrist_L_grp = arms.vertex_groups.get('wrist_L')
elbow_L_grp = arms.vertex_groups.get('elbow_L')
wrist_helper = arms.vertex_groups.get('wrist_L_helper')

print("Wrist vertices inspection:")
for vi in range(len(arms.data.vertices)):
    v = arms.data.vertices[vi]
    w_wrist = 0.0
    w_elbow = 0.0
    w_helper = 0.0
    for g in v.groups:
        if g.group == wrist_L_grp.index: w_wrist = g.weight
        elif elbow_L_grp and g.group == elbow_L_grp.index: w_elbow = g.weight
        elif wrist_helper and g.group == wrist_helper.index: w_helper = g.weight
    if w_wrist > 0.01:
        if w_elbow > 0.01:
            print(f"  v{vi} (X={v.co.x*0.5471:.3f}): wrist={w_wrist:.2f}, elbow={w_elbow:.2f}, helper={w_helper:.2f}")

