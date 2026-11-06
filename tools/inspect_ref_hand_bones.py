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

# Left hand is around X > 0.4, Right hand is around X < -0.4
r_hand_indices = [i for i, p in enumerate(pos) if p[0] < -0.40 and 0.70 < p[2] < 1.35]
l_hand_indices = [i for i, p in enumerate(pos) if p[0] > 0.40 and 0.70 < p[2] < 1.35]

print(f"Ref R hand: {len(r_hand_indices)} vertices")
print(f"Ref L hand: {len(l_hand_indices)} vertices")

# Count bone influences in R hand
r_bones = {}
for i in r_hand_indices:
    for b, w in zip(bones[i], weights[i]):
        if w > 0.01:
            r_bones[b] = r_bones.get(b, 0) + 1

print("\nRef R hand bones:")
for b, count in sorted(r_bones.items(), key=lambda x: -x[1]):
    print(f"  {b}: {count}")

# Now let's check Classic Windrunner hands
# In classic windrunner, where are the hand vertices?

