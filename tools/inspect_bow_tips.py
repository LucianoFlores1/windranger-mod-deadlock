import bpy
import numpy as np
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_bow.glb"))
bow_obj = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
verts = np.array([v.co for v in bow_obj.data.vertices])

# In windrunner_bow, the bow grip is around X=0.
# The curve goes towards +Y.
print("Points at +X (tip):", verts[verts[:,0] > 1.7])
print("Points at -X (tip):", verts[verts[:,0] < -1.7])
print("Points near center X~0:", verts[np.abs(verts[:,0]) < 0.1][:5])

