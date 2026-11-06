import bpy, os, sys
from pathlib import Path
sys.path.insert(0, 'tools')

bpy.ops.wm.read_factory_settings(use_empty=True)
base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
before = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=base_glb)
new_objs = set(bpy.context.scene.objects) - before
mesh_objs = [o for o in new_objs if o.type == 'MESH' and 'icosphere' not in o.name.lower()]
print("Mesh objs from base_glb:", [o.name for o in mesh_objs])
for o in mesh_objs:
    print(o.name, "vertex count:", len(o.data.vertices))

