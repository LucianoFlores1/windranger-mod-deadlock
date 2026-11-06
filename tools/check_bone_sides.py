import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = np.array(info['positions']) * 0.0254
bones = info['bones']
weights = info['weights']

ankle_L_verts = []
ankle_R_verts = []

for vi, (b_row, w_row) in enumerate(zip(bones, weights)):
    for b, w in zip(b_row, w_row):
        if w > 0.5:
            if b == 'ankle_L':
                ankle_L_verts.append(pos[vi])
            elif b == 'ankle_R':
                ankle_R_verts.append(pos[vi])

ankle_L_verts = np.array(ankle_L_verts)
ankle_R_verts = np.array(ankle_R_verts)

print(f"ankle_L verts ({len(ankle_L_verts)}): X mean = {np.mean(ankle_L_verts[:,0]):.3f}")
print(f"ankle_R verts ({len(ankle_R_verts)}): X mean = {np.mean(ankle_R_verts[:,0]):.3f}")

hand_L_verts = [pos[vi] for vi, (b_row, w_row) in enumerate(zip(bones, weights)) if any(b == 'hand_L' and w > 0.5 for b, w in zip(b_row, w_row))]
hand_R_verts = [pos[vi] for vi, (b_row, w_row) in enumerate(zip(bones, weights)) if any(b == 'hand_R' and w > 0.5 for b, w in zip(b_row, w_row))]
print(f"hand_L verts ({len(hand_L_verts)}): X mean = {np.mean(hand_L_verts, axis=0)[0]:.3f}")
print(f"hand_R verts ({len(hand_R_verts)}): X mean = {np.mean(hand_R_verts, axis=0)[0]:.3f}")

