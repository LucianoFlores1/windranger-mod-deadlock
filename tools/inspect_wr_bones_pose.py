import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb")

arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)
if arm:
    print(f"Armature: {arm.name}, bones: {len(arm.data.bones)}")
    for b in arm.data.bones:
        name_lower = b.name.lower()
        if any(k in name_lower for k in ["head", "pelvis", "root", "foot", "toe", "ankle", "thigh", "hand", "clavicle", "spine"]):
            head = b.head_local
            print(f"  {b.name:20}: head=({head.x:.3f}, {head.y:.3f}, {head.z:.3f})")

