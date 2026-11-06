import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = dmx_to_blender(info['positions'])
print("Total vertices:", len(pos))
print("X span:", pos[:, 0].min(), "to", pos[:, 0].max())
print("Y span:", pos[:, 1].min(), "to", pos[:, 1].max())
print("Z span:", pos[:, 2].min(), "to", pos[:, 2].max())

# Where are vertices weighted to hand_R or hand_L?
bones = info['bones']
weights = info['weights']
hand_r_verts = [pos[i] for i, (b_row, w_row) in enumerate(zip(bones, weights)) if any('hand_r' in b.lower() and w > 0.1 for b, w in zip(b_row, w_row))]
hand_l_verts = [pos[i] for i, (b_row, w_row) in enumerate(zip(bones, weights)) if any('hand_l' in b.lower() and w > 0.1 for b, w in zip(b_row, w_row))]
print(f"hand_R verts: {len(hand_r_verts)}")
if hand_r_verts:
    hr = np.array(hand_r_verts)
    print("hand_R X:", hr[:, 0].min(), "to", hr[:, 0].max())
    print("hand_R Y:", hr[:, 1].min(), "to", hr[:, 1].max())
    print("hand_R Z:", hr[:, 2].min(), "to", hr[:, 2].max())
print(f"hand_L verts: {len(hand_l_verts)}")
if hand_l_verts:
    hl = np.array(hand_l_verts)
    print("hand_L X:", hl[:, 0].min(), "to", hl[:, 0].max())
    print("hand_L Y:", hl[:, 1].min(), "to", hl[:, 1].max())
    print("hand_L Z:", hl[:, 2].min(), "to", hl[:, 2].max())

