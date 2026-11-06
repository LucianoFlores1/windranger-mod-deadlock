import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
quiv_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_quiver.glb"
bpy.ops.import_scene.gltf(filepath=quiv_glb)

for o in bpy.data.objects:
    if o.type == 'MESH':
        pos = np.array([v.co for v in o.data.vertices]) * 0.5471
        print(f"Mesh {o.name}: {len(pos)} verts, X=[{pos[:,0].min():.2f}, {pos[:,0].max():.2f}], Y=[{pos[:,1].min():.2f}, {pos[:,1].max():.2f}], Z=[{pos[:,2].min():.2f}, {pos[:,2].max():.2f}]")

