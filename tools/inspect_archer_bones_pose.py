import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")

arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)
if arm:
    print(f"Armature: {arm.name}, bones: {len(arm.data.bones)}")
    for b in arm.data.bones:
        if b.name in ["head", "neck_0", "spine_2", "pelvis", "arm_upper_L", "arm_lower_L", "hand_L", "leg_upper_L", "leg_lower_L", "ankle_L", "ball_L", "leg_upper_R", "leg_lower_R", "ankle_R", "ball_R", "weaponHier_JNT"]:
            head = b.head_local
            tail = b.tail_local
            print(f"  {b.name:15}: head=({head.x:.3f}, {head.y:.3f}, {head.z:.3f}), tail=({tail.x:.3f}, {tail.y:.3f}, {tail.z:.3f})")

