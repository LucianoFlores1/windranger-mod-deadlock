import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Archer
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
arc_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
arc_bones = {b.name: b.head_local for b in arc_arm.data.bones}

# 2. Windrunner
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb")
wr_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE' and o != arc_arm)
wr_bones = {b.name: b.head_local for b in wr_arm.data.bones}

print("=== ARCHER KEY BONES ===")
for name in ['pelvis', 'spine_1', 'spine_2', 'spine_3', 'neck_0', 'head', 'arm_upper_L', 'arm_lower_L', 'hand_L', 'leg_upper_L', 'leg_lower_L', 'ankle_L']:
    if name in arc_bones:
        p = arc_bones[name]
        print(f"  {name}: [{p.x:.3f}, {p.y:.3f}, {p.z:.3f}]")

print("\n=== WINDRUNNER KEY BONES ===")
for name in ['root', 'spine1', 'spine2', 'spine3', 'neck1', 'head', 'bicep_L', 'elbow_L', 'wrist_L', 'thigh_L', 'knee_L', 'ankle_L']:
    if name in wr_bones:
        p = wr_bones[name]
        print(f"  {name}: [{p.x:.3f}, {p.y:.3f}, {p.z:.3f}]")

