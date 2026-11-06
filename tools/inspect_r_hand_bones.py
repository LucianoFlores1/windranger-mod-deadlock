import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender

bpy.ops.wm.read_factory_settings(use_empty=True)
scale = 0.5471
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

# Load ref
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])
me_ref = bpy.data.meshes.new("ref_mesh")
me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
me_ref.update()
ref_warka = bpy.data.objects.new("ref_warka", me_ref)
bpy.context.scene.collection.objects.link(ref_warka)
for vi, (b_row, w_row) in enumerate(zip(info['bones'], info['weights'])):
    for b_name, w in zip(b_row, w_row):
        if w > 0.001 and b_name:
            vg = ref_warka.vertex_groups.get(b_name) or ref_warka.vertex_groups.new(name=b_name)
            vg.add([vi], float(w), 'REPLACE')

other_parts = [
    (base_glb, "base"),
    (os.path.join(wr_dir, "windrunner_head.glb"), "hair"),
    (os.path.join(wr_dir, "windrunner_cape.glb"), "cape"),
    (os.path.join(wr_dir, "windrunner_quiver.glb"), "quiver"),
]

imported_objs = []
for fpath, tag in other_parts:
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=fpath)
    new_objs = set(bpy.context.scene.objects) - before
    for o in new_objs:
        if o.type == 'MESH' and 'icosphere' not in o.name.lower():
            imported_objs.append(o)
        elif o.type == 'ARMATURE':
            bpy.data.objects.remove(o)

for m in imported_objs:
    m.scale = (scale, scale, scale)
    bpy.context.view_layer.objects.active = m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bpy.ops.object.select_all(action='DESELECT')
for m in imported_objs:
    m.select_set(True)
bpy.context.view_layer.objects.active = imported_objs[0]
bpy.ops.object.join()
body_main = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# DataTransfer
mod = body_main.modifiers.new("DataTransfer", "DATA_TRANSFER")
mod.object = ref_warka
mod.use_vert_data = True
mod.data_types_verts = {'VGROUP_WEIGHTS'}
mod.vert_mapping = 'NEAREST'
bpy.context.view_layer.objects.active = body_main
bpy.ops.object.datalayout_transfer(modifier=mod.name)
bpy.ops.object.modifier_apply(modifier=mod.name)

# Inspect right hand vertices groups
r_groups = set()
for v in body_main.data.vertices:
    if v.co.x < -0.45 and 0.85 < v.co.z < 1.25:
        for g in v.groups:
            if g.weight > 0.05:
                r_groups.add(body_main.vertex_groups[g.group].name)

print("Bones on right hand (X < -0.45, 0.85 < Z < 1.25):", sorted(r_groups))
