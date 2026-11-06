import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, 'tools')

bpy.ops.wm.read_factory_settings(use_empty=True)
scale = 0.5471
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

other_parts = [
    (base_glb, "base"),
    (os.path.join(wr_dir, "windrunner_head.glb"), "hair"),
    (os.path.join(wr_dir, "windrunner_cape.glb"), "cape"),
    (os.path.join(wr_dir, "windrunner_quiver.glb"), "quiver"),
]

imported_objs = []
for fpath, tag in other_parts:
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=fpath)
    new_objs = set(bpy.context.scene.objects) - before
    for o in new_objs:
        if o.type == 'MESH' and 'icosphere' not in o.name.lower():
            imported_objs.append(o)
        elif o.type == 'ARMATURE':
            bpy.data.objects.remove(o)

for m in imported_objs:
    m.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.ops.object.select_all(action='DESELECT')
for m in imported_objs:
    m.select_set(True)
bpy.context.view_layer.objects.active = imported_objs[0]
bpy.ops.object.join()
body_main = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

pts = np.array([v.co for v in body_main.data.vertices])
print("body_main vertices:", len(pts))
print("X > 0.40 & 0.85 < Z < 1.25 count:", np.sum((pts[:,0] > 0.40) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)))
print("X > 0.45 & 0.85 < Z < 1.25 count:", np.sum((pts[:,0] > 0.45) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)))
print("X < -0.40 & 0.85 < Z < 1.25 count:", np.sum((pts[:,0] < -0.40) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)))
print("X < -0.45 & 0.85 < Z < 1.25 count:", np.sum((pts[:,0] < -0.45) & (pts[:,2] > 0.85) & (pts[:,2] < 1.25)))

