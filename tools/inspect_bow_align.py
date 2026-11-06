import bpy
import os
import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Mod bow
info = read_dmx_mesh(Path(r'extracted\archer_bow1.dmx'))
pos = dmx_to_blender(info['positions'])
me_ref = bpy.data.meshes.new("ref_bow")
me_ref.from_pydata(pos.tolist(), [], info['tris'].tolist())
me_ref.update()
ref_bow = bpy.data.objects.new("ref_bow", me_ref)
bpy.context.scene.collection.objects.link(ref_bow)

bone_names = info['bones']
weights = info['weights']
for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
    for b_name, w in zip(b_row, w_row):
        if w > 0.001 and b_name:
            vg = ref_bow.vertex_groups.get(b_name) or ref_bow.vertex_groups.new(name=b_name)
            vg.add([vi], float(w), 'REPLACE')

print(f"Ref bow: {len(me_ref.vertices)} verts, {len(ref_bow.vertex_groups)} groups.")
ref_xs = [v.co.x for v in me_ref.vertices]
ref_ys = [v.co.y for v in me_ref.vertices]
ref_zs = [v.co.z for v in me_ref.vertices]
print(f"Ref bow bounds: X=[{min(ref_xs):.2f}, {max(ref_xs):.2f}], Y=[{min(ref_ys):.2f}, {max(ref_ys):.2f}], Z=[{min(ref_zs):.2f}, {max(ref_zs):.2f}]")

# 2. Classic bow
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bow_glb = os.path.join(wr_dir, "windrunner_bow.glb")
bpy.ops.import_scene.gltf(filepath=bow_glb)
classic_bow = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o != ref_bow)
classic_xs = [v.co.x for v in classic_bow.data.vertices]
classic_ys = [v.co.y for v in classic_bow.data.vertices]
classic_zs = [v.co.z for v in classic_bow.data.vertices]
print(f"Classic bow raw bounds: X=[{min(classic_xs):.2f}, {max(classic_xs):.2f}], Y=[{min(classic_ys):.2f}, {max(classic_ys):.2f}], Z=[{min(classic_zs):.2f}, {max(classic_zs):.2f}]")

