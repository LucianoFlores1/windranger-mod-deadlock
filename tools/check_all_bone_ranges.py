import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender

bpy.ops.wm.read_factory_settings(use_empty=True)
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])
bone_names = info['bones']
weights = info['weights']

# Group vertices by bone
bone_verts = {}
for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
    for b_name, w in zip(b_row, w_row):
        if w > 0.6:
            bone_verts.setdefault(b_name, []).append(ref_pos[vi])

for b in sorted(bone_verts.keys()):
    pts = np.array(bone_verts[b])
    print(f"Bone {b:20s}: X = [{pts[:,0].min():+.3f}, {pts[:,0].max():+.3f}], Y = [{pts[:,1].min():+.3f}, {pts[:,1].max():+.3f}], Z = [{pts[:,2].min():+.3f}, {pts[:,2].max():+.3f}]")

