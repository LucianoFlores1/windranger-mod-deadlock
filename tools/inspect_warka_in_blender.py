import sys
import os
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Import Archer
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
arc_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')

# 2. Load warka3
info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
# Convert dmx coords to blender coords:
# dmx_to_blender = (y, -x, z) * 0.0254
from pipeline.coords import dmx_to_blender
blender_pos = dmx_to_blender(info['positions'])

me = bpy.data.meshes.new("warka3_mesh")
me.from_pydata(blender_pos.tolist(), [], info['tris'].tolist())
me.update()

obj = bpy.data.objects.new("warka3", me)
bpy.context.scene.collection.objects.link(obj)

# Check bounds
xs = [v.co.x for v in me.vertices]
ys = [v.co.y for v in me.vertices]
zs = [v.co.z for v in me.vertices]
print(f"Warka3 in Blender:")
print(f"  X: [{min(xs):.2f}, {max(xs):.2f}]")
print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}]")
print(f"  Z: [{min(zs):.2f}, {max(zs):.2f}]")

# Archer bounds
arc_mesh = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o != obj)
axs = [v.co.x for v in arc_mesh.data.vertices]
ays = [v.co.y for v in arc_mesh.data.vertices]
azs = [v.co.z for v in arc_mesh.data.vertices]
print(f"Archer mesh in Blender:")
print(f"  X: [{min(axs):.2f}, {max(axs):.2f}]")
print(f"  Y: [{min(ays):.2f}, {max(ays):.2f}]")
print(f"  Z: [{min(azs):.2f}, {max(azs):.2f}]")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\inspect_warka_blend.blend")
print("Saved to extracted/inspect_warka_blend.blend")

