import bpy
import numpy as np
import os
import math
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_bow.glb"))

c_bow = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
bpy.ops.object.select_all(action='DESELECT')
c_bow.select_set(True)
bpy.context.view_layer.objects.active = c_bow

# Remove armatures
for o in list(bpy.context.scene.objects):
    if o.type == 'ARMATURE':
        bpy.data.objects.remove(o)

c_bow.rotation_euler = (0, math.radians(-90), 0)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

verts = np.array([v.co for v in c_bow.data.vertices])
span = np.ptp(verts, axis=0)
print(f"Classic bow span after rot Y=-90 & apply: {span}")

