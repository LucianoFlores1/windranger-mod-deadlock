import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import collections
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = np.array(info['positions']) * 0.0254

# In Blender space: pos = (-X, -Y, Z)
b_pos = np.stack([-pos[:,0], -pos[:,1], pos[:,2]], axis=-1)

# Hand L vertices: b_pos[:,0] > 0.4 and b_pos[:,2] between 0.8 and 1.3
hand_L_indices = [i for i, p in enumerate(b_pos) if p[0] > 0.45 and 0.8 < p[2] < 1.3]
# Hand R vertices: b_pos[:,0] < -0.4 and b_pos[:,2] between 0.8 and 1.3
hand_R_indices = [i for i, p in enumerate(b_pos) if p[0] < -0.45 and 0.8 < p[2] < 1.3]

print(f"Hand L vertices: {len(hand_L_indices)}")
hand_L_bones = collections.Counter()
for vi in hand_L_indices:
    for b, w in zip(info['bones'][vi], info['weights'][vi]):
        if w > 0.05 and b:
            hand_L_bones[b] += 1
for b, c in hand_L_bones.most_common():
    print(f"  {b:25}: {c}")

print(f"\nHand R vertices: {len(hand_R_indices)}")
hand_R_bones = collections.Counter()
for vi in hand_R_indices:
    for b, w in zip(info['bones'][vi], info['weights'][vi]):
        if w > 0.05 and b:
            hand_R_bones[b] += 1
for b, c in hand_R_bones.most_common():
    print(f"  {b:25}: {c}")

