import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender

bpy.ops.wm.read_factory_settings(use_empty=True)
scale = 0.5471
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=base_glb)
new_objs = set(bpy.context.scene.objects) - before
arms = [o for o in new_objs if 'arms' in o.name.lower()][0]
arms.scale = (scale, scale, scale)
bpy.context.view_layer.objects.active = arms
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Find wrist_L in original Dota 2 mesh
wrist_L_grp = arms.vertex_groups.get('wrist_L')
wrist_verts = [v for v in arms.data.vertices if any(g.group == wrist_L_grp.index and g.weight > 0.1 for g in v.groups)]
print(f"Original Dota 2 wrist_L vertices count: {len(wrist_verts)}")
pts = np.array([v.co for v in wrist_verts])
print(f"Original wrist_L bounds: X=[{pts[:,0].min():.3f}, {pts[:,0].max():.3f}], Y=[{pts[:,1].min():.3f}, {pts[:,1].max():.3f}], Z=[{pts[:,2].min():.3f}, {pts[:,2].max():.3f}]")

# If we take X > 0.47 & 0.85 < Z < 1.25:
mask = (np.array([v.co[0] for v in arms.data.vertices]) > 0.47) & \
       (np.array([v.co[2] for v in arms.data.vertices]) > 0.85) & \
       (np.array([v.co[2] for v in arms.data.vertices]) < 1.25)
print(f"Vertices matching hand box (X > 0.47): {np.sum(mask)}")

# Are any elbow/bicep vertices in that box?
for vi in np.where(mask)[0]:
    v = arms.data.vertices[vi]
    for g in v.groups:
        g_name = arms.vertex_groups[g.group].name
        if 'elbow' in g_name or 'bicep' in g_name:
            if g.weight > 0.3:
                print(f"Warning: vert {vi} has {g_name} weight {g.weight:.2f}")

