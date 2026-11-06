import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
pos = np.array(info['positions']) * 0.0254
bones = info['bones']
weights = info['weights']

# Collect unique bones that have non-zero weight
active_bones = {}
for b_row, w_row in zip(bones, weights):
    for b, w in zip(b_row, w_row):
        if w > 0.01 and b:
            active_bones[b] = active_bones.get(b, 0) + 1

print(f"Active bones in bow ({len(active_bones)}):")
for b, count in active_bones.items():
    print(f"  {b:25}: {count} verts")

# Find average position of vertices for each bone
for b in active_bones:
    b_verts = []
    for vi, (b_row, w_row) in enumerate(zip(bones, weights)):
        for bn, w in zip(b_row, w_row):
            if bn == b and w > 0.5:
                b_verts.append(pos[vi])
    if b_verts:
        b_pos = np.mean(b_verts, axis=0)
        print(f"  Bone {b:20} center: X={b_pos[0]:.2f}, Y={b_pos[1]:.2f}, Z={b_pos[2]:.2f}")
