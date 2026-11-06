import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"dota2_extracted\models\heroes\windrunner\windrunner_shoulderpads.glb")
m = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)
print(f"Mesh: {m.name}, verts: {len(m.data.vertices)}")
if arm:
    print(f"Armature bones: {[b.name for b in arm.data.bones]}")
print(f"Vertex groups on mesh: {[g.name for g in m.vertex_groups]}")

