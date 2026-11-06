import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)
scale = 0.5471

arms = [o for o in bpy.context.scene.objects if 'arms' in o.name.lower()][0]
wrist_L_group = arms.vertex_groups.get('wrist_L')
if wrist_L_group:
    wrist_verts = [v.co * scale for v in arms.data.vertices if any(g.group == wrist_L_group.index and g.weight > 0.1 for g in v.groups)]
    wrist_pts = np.array(wrist_verts)
    print("wrist_L verts count:", len(wrist_pts))
    print(f"wrist_L X: [{wrist_pts[:,0].min():.2f}, {wrist_pts[:,0].max():.2f}], Z: [{wrist_pts[:,2].min():.2f}, {wrist_pts[:,2].max():.2f}]")

wrist_R_group = arms.vertex_groups.get('wrist_R')
if wrist_R_group:
    wrist_verts_R = [v.co * scale for v in arms.data.vertices if any(g.group == wrist_R_group.index and g.weight > 0.1 for g in v.groups)]
    wrist_pts_R = np.array(wrist_verts_R)
    print("wrist_R verts count:", len(wrist_pts_R))
    print(f"wrist_R X: [{wrist_pts_R[:,0].min():.2f}, {wrist_pts_R[:,0].max():.2f}], Z: [{wrist_pts_R[:,2].min():.2f}, {wrist_pts_R[:,2].max():.2f}]")

