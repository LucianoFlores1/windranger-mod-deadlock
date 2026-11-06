import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\archer.glb")

arm = next(obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE')
bones = [b.name for b in arm.data.bones]
print(f"Archer total bones: {len(bones)}")
print("Archer bones list:")
for b in sorted(bones):
    if any(k in b.lower() for k in ['pelvis', 'spine', 'head', 'neck', 'arm', 'hand', 'leg', 'thigh', 'knee', 'ankle', 'clavicle', 'weapon']):
        print("  ", b)
