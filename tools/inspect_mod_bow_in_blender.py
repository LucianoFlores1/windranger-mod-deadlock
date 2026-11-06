import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Archer
bpy.ops.import_scene.gltf(filepath=r"extracted\gltf\archer.glb")
arc_arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
b_hand = arc_arm.data.bones['weapon_hand_L']
print(f"Archer weapon_hand_L head: {arc_arm.matrix_world @ b_hand.head_local}")
print(f"Archer weapon_hand_L tail: {arc_arm.matrix_world @ b_hand.tail_local}")

# 2. Bow from modder
info = read_dmx_mesh(Path(r'extracted\archer_bow1.dmx'))
pos = dmx_to_blender(info['positions'])
me = bpy.data.meshes.new("mod_bow")
me.from_pydata(pos.tolist(), [], info['tris'].tolist())
me.update()
obj = bpy.data.objects.new("mod_bow", me)
bpy.context.scene.collection.objects.link(obj)

xs = [v.co.x for v in me.vertices]
ys = [v.co.y for v in me.vertices]
zs = [v.co.z for v in me.vertices]
print(f"Modder bow in Blender:")
print(f"  X: [{min(xs):.2f}, {max(xs):.2f}]")
print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}]")
print(f"  Z: [{min(zs):.2f}, {max(zs):.2f}]")
print(f"  Center: [{(min(xs)+max(xs))/2:.2f}, {(min(ys)+max(ys))/2:.2f}, {(min(zs)+max(zs))/2:.2f}]")

