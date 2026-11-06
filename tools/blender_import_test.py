import bpy
import os

# Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

gltf_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_gltf = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"
archer_gltf = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\archer.glb"

print("Importing Windrunner Base GLB...")
bpy.ops.import_scene.gltf(filepath=base_gltf)
wr_objects = list(bpy.context.scene.objects)
print(f"Windrunner base objects ({len(wr_objects)}):")
for obj in wr_objects:
    print(f"  {obj.name} (type: {obj.type})")

parts = ["windrunner_head.glb", "windrunner_cape.glb", "windrunner_shoulderpads.glb", "windrunner_quiver.glb", "windrunner_bow.glb"]
for p in parts:
    path = os.path.join(gltf_dir, p)
    if os.path.exists(path):
        print(f"Importing {p}...")
        bpy.ops.import_scene.gltf(filepath=path)

print(f"\nTotal scene objects after parts import: {len(bpy.context.scene.objects)}")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"  Mesh: {obj.name}, verts: {len(obj.data.vertices)}")
