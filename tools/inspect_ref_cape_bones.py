import bpy, os, sys
import numpy as np
from pathlib import Path

# Run build_classic_warka up to the point of inspecting cape weights
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh

warka_info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
bone_names = warka_info['bones']
weights = warka_info['weights']

# What bones exist on the back/cape of the Arcana reference?
# In ref, where Z is between 0.5 and 1.5 and Y is negative (Blender -Y is back, or is +Y back?)
# Let's check!
print("Ref warka back vertices bones:")
pos = np.array(warka_info['positions'])
# In DMX, +Y is front or back?
# Let's check spine bones
for i, (b_row, w_row) in enumerate(zip(bone_names, weights)):
    for b, w in zip(b_row, w_row):
        if any(h in b for h in ['hair_L', 'hair_R']) and w > 0.3:
            print(f"Vert {i}: pos={pos[i]}, bone={b}:{w:.2f}")
            break

