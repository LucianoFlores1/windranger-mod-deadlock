import sys
sys.path.insert(0, "tools")
import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
glb_path = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner.glb"
bpy.ops.import_scene.gltf(filepath=glb_path)

armature = None
mesh = None
for o in bpy.data.objects:
    if o.type == 'ARMATURE':
        armature = o
    elif o.type == 'MESH':
        mesh = o

print("Armature:", armature.name if armature else "None")
print("Mesh:", mesh.name if mesh else "None")
if armature:
    bones = [b.name for b in armature.data.bones]
    print(f"Total bones in Dota 2 Windrunner: {len(bones)}")
    for b in sorted(bones):
        print("  Dota bone:", b)

if mesh:
    print(f"Vertex groups in Dota 2 Windrunner mesh: {len(mesh.vertex_groups)}")
    for vg in sorted([vg.name for vg in mesh.vertex_groups]):
        print("  Dota VG:", vg)

