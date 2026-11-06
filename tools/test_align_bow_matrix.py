import bpy
import numpy as np
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
from mathutils import Matrix, Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Orig bow in Blender space
info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])
ref_center = np.mean(ref_pos, axis=0)

# Landmarks in orig bow
ref_top = max(ref_pos, key=lambda p: p[2])
ref_bot = min(ref_pos, key=lambda p: p[2])
# The grip/center is where weapon_hand_L is centered
# or the belly of the curve
print(f"Ref Top: {ref_top}")
print(f"Ref Bot: {ref_bot}")
print(f"Ref Center: {ref_center}")

# 2. Classic bow
glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_bow.glb"
bpy.ops.import_scene.gltf(filepath=glb)
bow = next(o for o in bpy.data.objects if o.type == 'MESH')
c_pos = np.array([v.co for v in bow.data.vertices])

c_top = max(c_pos, key=lambda p: p[0]) # length is along X
c_bot = min(c_pos, key=lambda p: p[0])
c_center = np.mean(c_pos, axis=0)
print(f"Classic Top (max X): {c_top}")
print(f"Classic Bot (min X): {c_bot}")
print(f"Classic Center: {c_center}")

# Let's check which way the curve points in classic bow vs ref bow:
# In classic bow, curve is along +Y:
print("Classic max Y vertex:", max(c_pos, key=lambda p: p[1]))
# In ref bow:
print("Ref bow X span:", ref_pos[:, 0].min(), "to", ref_pos[:, 0].max())
print("Ref bow Y span:", ref_pos[:, 1].min(), "to", ref_pos[:, 1].max())

