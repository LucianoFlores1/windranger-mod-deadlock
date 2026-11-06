import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

print("=== CHECKING LEGS IN ARCHER_WARKA3.DMX ===")
# Legs are Z < 1.0
leg_indices = [i for i, p in enumerate(pos) if p[2] < 1.0]
print(f"Total leg/lower verts (Z < 1.0): {len(leg_indices)}")

leg_bone_counts = {}
for i in leg_indices:
    for b, w in zip(bones[i], weights[i]):
        if w > 0.01:
            leg_bone_counts[b] = leg_bone_counts.get(b, 0) + 1

for b, c in sorted(leg_bone_counts.items(), key=lambda x: -x[1]):
    print(f"  {b}: {c} vertices")

