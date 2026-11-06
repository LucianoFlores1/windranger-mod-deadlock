import bpy
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Archer
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
arc_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
arc_bones = {b.name: arc_arm.matrix_world @ b.head_local for b in arc_arm.data.bones}

# 2. Windrunner base
base_glb = r"extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=base_glb)
wr_arm = next(o for o in set(bpy.context.scene.objects) - before if o.type == 'ARMATURE')
wr_bones = {b.name: wr_arm.matrix_world @ b.head_local for b in wr_arm.data.bones}

print(f"Archer head Z: {arc_bones['head'].z:.3f}, ankle_L Z: {arc_bones['ankle_L'].z:.3f}")
print(f"Windrunner head Z: {wr_bones['head'].z:.3f}, ankle_L Z: {wr_bones['ankle_L'].z:.3f}")

arc_height = arc_bones['head'].z - arc_bones['ankle_L'].z
wr_height = wr_bones['head'].z - wr_bones['ankle_L'].z
scale = arc_height / wr_height
print(f"Computed Scale: {scale:.4f}")

# Archer pelvis
arc_pelvis = arc_bones['pelvis']
wr_pelvis = wr_bones['root']
print(f"Archer pelvis: {arc_pelvis}")
print(f"Windrunner root: {wr_pelvis}")

