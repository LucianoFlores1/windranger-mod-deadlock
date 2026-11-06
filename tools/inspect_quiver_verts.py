import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender

info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

# Material for quiver was mat_quiver = windranger_arcana_arrow.vmat
# FaceSet 3
# Let's find vertices with Y > 0.15 and Z > 1.4
quiver_verts = []
for i in range(len(pos)):
    p = pos[i]
    if 0.18 < p[1] < 0.40 and 1.40 < p[2] < 2.10 and abs(p[0]) < 0.55:
        # Check bone weights
        b_list = [(bones[i][k], weights[i][k]) for k in range(4) if weights[i][k] > 0.05]
        quiver_verts.append((p, b_list))

print(f"Candidate quiver verts: {len(quiver_verts)}")
unique_bones = set()
for p, b_list in quiver_verts:
    for b, w in b_list:
        unique_bones.add(b)
print("Bones on quiver:", sorted(unique_bones))

# Print first 10
for p, b_list in quiver_verts[:10]:
    print(f"  Pos: [{p[0]:+.2f}, {p[1]:+.2f}, {p[2]:+.2f}] -> {b_list}")

