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

# Shoulderpad is on the left side: X > 0.10, Z > 1.50
shoulder_verts = []
for i, p in enumerate(pos):
    # In Blender coords: X is lateral (arms)! Left shoulder is X > 0.10, Z > 1.50
    if p[0] > 0.10 and p[2] > 1.50:
        shoulder_verts.append(i)

print(f"Found {len(shoulder_verts)} shoulder vertices")
bone_counts = {}
for i in shoulder_verts:
    for b, w in zip(bones[i], weights[i]):
        if w > 0.01:
            bone_counts[b] = bone_counts.get(b, 0) + 1

print("\nBones affecting shoulderpad in compiled archer_warka3.dmx:")
for b, c in sorted(bone_counts.items(), key=lambda x: -x[1]):
    print(f"  {b}: {c} vertices")

