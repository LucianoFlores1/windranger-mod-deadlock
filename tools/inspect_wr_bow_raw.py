import bpy
import numpy as np
import os

bpy.ops.wm.read_factory_settings(use_empty=True)
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_bow.glb"))

bow_obj = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
bow_arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)

print("Bow mesh:", bow_obj.name)
verts = np.array([v.co for v in bow_obj.data.vertices])
print(f"Mesh bounds: X=[{verts[:,0].min():.2f}, {verts[:,0].max():.2f}], Y=[{verts[:,1].min():.2f}, {verts[:,1].max():.2f}], Z=[{verts[:,2].min():.2f}, {verts[:,2].max():.2f}]")

if bow_arm:
    print(f"Bow armature: {bow_arm.name}, bones: {len(bow_arm.data.bones)}")
    for b in bow_arm.data.bones:
        h = b.head_local
        t = b.tail_local
        print(f"  {b.name:20}: head=({h.x:.2f}, {h.y:.2f}, {h.z:.2f}), tail=({t.x:.2f}, {t.y:.2f}, {t.z:.2f})")

