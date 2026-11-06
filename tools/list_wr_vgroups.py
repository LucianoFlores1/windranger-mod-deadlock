import bpy
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

gltf_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_gltf = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

bpy.ops.import_scene.gltf(filepath=base_gltf)
parts = ["windrunner_head.glb", "windrunner_cape.glb", "windrunner_shoulderpads.glb", "windrunner_quiver.glb", "windrunner_bow.glb"]
for p in parts:
    path = os.path.join(gltf_dir, p)
    if os.path.exists(path):
        bpy.ops.import_scene.gltf(filepath=path)

all_vgroups = set()
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        for vg in obj.vertex_groups:
            all_vgroups.add(vg.name)

print("All vertex groups in Windrunner pieces:")
for vg in sorted(all_vgroups):
    print("  ", vg)
