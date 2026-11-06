import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
bpy.ops.import_scene.gltf(filepath=base_glb)

arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
print(f"Total bones in windrunner: {len(arm.data.bones)}")
for b in arm.data.bones:
    print(f"  {b.name} (parent: {b.parent.name if b.parent else 'None'})")

