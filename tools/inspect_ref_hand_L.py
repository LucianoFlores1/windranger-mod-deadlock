import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])
bone_names = info['bones']
weights = info['weights']

hl_verts = []
for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
    for b_name, w in zip(b_row, w_row):
        if b_name == 'hand_L':
            hl_verts.append((ref_pos[vi], w))

print("Total hand_L verts in ref_warka:", len(hl_verts))
pts = np.array([p for p, w in hl_verts])
print("hand_L X bounds:", pts[:,0].min(), pts[:,0].max())
print("hand_L Y bounds:", pts[:,1].min(), pts[:,1].max())
print("hand_L Z bounds:", pts[:,2].min(), pts[:,2].max())

