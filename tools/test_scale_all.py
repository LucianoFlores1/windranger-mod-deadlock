import bpy
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Archer
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
arc_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
arc_mesh = next(o for o in bpy.context.scene.objects if o.type == 'MESH')

# 2. Windrunner parts (excluding bow for now)
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

parts = [base_glb, "windrunner_head.glb", "windrunner_cape.glb", "windrunner_shoulderpads.glb", "windrunner_quiver.glb"]

scale = 0.5471
wr_meshes = []

for p in parts:
    fpath = os.path.join(wr_dir, p) if not os.path.isabs(p) else p
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=fpath)
    new_objs = set(bpy.context.scene.objects) - before
    for o in new_objs:
        if o.type == 'MESH' and o.name != 'Icosphere':
            wr_meshes.append(o)
        elif o.type == 'ARMATURE' and o != arc_arm:
            # remove extra armatures
            bpy.data.objects.remove(o)

# Apply scale to all meshes
for m in wr_meshes:
    m.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Get combined bounds
all_xs = [v.co.x for m in wr_meshes for v in m.data.vertices]
all_ys = [v.co.y for m in wr_meshes for v in m.data.vertices]
all_zs = [v.co.z for m in wr_meshes for v in m.data.vertices]

print(f"Combined Windrunner body+clothes (5 pieces):")
print(f"  Total meshes: {len(wr_meshes)}")
print(f"  Total vertices: {len(all_xs)}")
print(f"  X: [{min(all_xs):.2f}, {max(all_xs):.2f}]")
print(f"  Y: [{min(all_ys):.2f}, {max(all_ys):.2f}]")
print(f"  Z: [{min(all_zs):.2f}, {max(all_zs):.2f}]")

axs = [v.co.x for v in arc_mesh.data.vertices]
ays = [v.co.y for v in arc_mesh.data.vertices]
azs = [v.co.z for v in arc_mesh.data.vertices]
print(f"Archer mesh:")
print(f"  X: [{min(axs):.2f}, {max(axs):.2f}]")
print(f"  Y: [{min(ays):.2f}, {max(ays):.2f}]")
print(f"  Z: [{min(azs):.2f}, {max(azs):.2f}]")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_fitted_windrunner.blend")
print("Saved to extracted/test_fitted_windrunner.blend")

