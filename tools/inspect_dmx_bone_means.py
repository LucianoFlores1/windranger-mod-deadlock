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

def get_bone_mean(name):
    verts = [pos[vi] for vi, (b_row, w_row) in enumerate(zip(bones, weights)) if any(b == name and w > 0.3 for b, w in zip(b_row, w_row))]
    if verts:
        return np.mean(verts, axis=0)
    return None

for b in ['pelvis', 'spine_0', 'spine_1', 'spine_2', 'spine_3', 'neck_0', 'head', 'ball_L', 'ball_R', 'ankle_L', 'ankle_R', 'hand_L', 'hand_R']:
    m = get_bone_mean(b)
    if m is not None:
        print(f"{b:12}: X={m[0]:.3f}, Y={m[1]:.3f}, Z={m[2]:.3f}")

