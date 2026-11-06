import sys
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
bone_names = info['bones']
weights = info['weights']
pos = np.array(info['positions'])

# Check distribution of weights along Z (height of bow)
z_vals = pos[:, 2]
for z_cut in range(-30, 35, 10):
    mask = (z_vals >= z_cut) & (z_vals < z_cut + 10)
    if np.any(mask):
        sub_bones = [b for row in np.array(bone_names)[mask] for b in row if b]
        unique, counts = np.unique(sub_bones, return_counts=True)
        top3 = sorted(zip(unique, counts), key=lambda x: x[1], reverse=True)[:3]
        print(f"Z in [{z_cut:3d}, {z_cut+10:3d}]:", top3)

