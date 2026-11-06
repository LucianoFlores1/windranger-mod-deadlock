import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

for bname in ['clavicle_L', 'arm_upper_L', 'clavicle_R', 'arm_upper_R', 'neck_0', 'head']:
    b_verts = [pos[i] for i, (b_row, w_row) in enumerate(zip(bones, weights)) if any(bname == b and w > 0.1 for b, w in zip(b_row, w_row))]
    if b_verts:
        bv = np.array(b_verts)
        print(f"{bname:12s} ({len(bv):4d} verts): X=[{bv[:,0].min():.2f}, {bv[:,0].max():.2f}], Y=[{bv[:,1].min():.2f}, {bv[:,1].max():.2f}], Z=[{bv[:,2].min():.2f}, {bv[:,2].max():.2f}]")

