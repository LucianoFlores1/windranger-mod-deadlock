import bpy
import os

gltf_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
parts = ["windrunner_head.glb", "windrunner_cape.glb", "windrunner_shoulderpads.glb", "windrunner_quiver.glb", "windrunner_bow.glb"]

for p in parts:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(gltf_dir, p))
    mesh = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
    arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)
    vgs = [vg.name for vg in mesh.vertex_groups]
    print(f"Part {p}: mesh={mesh.name}, arm={arm.name if arm else 'None'}, vgs={vgs[:5]}")
