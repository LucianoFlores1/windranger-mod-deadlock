import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender

info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

# Find vertices in right shoulder / upper arm
r_shoulder = []
for i in range(len(pos)):
    p = pos[i]
    if -0.45 < p[0] < -0.10 and 1.30 < p[2] < 1.80 and -0.20 < p[1] < 0.20:
        b_list = [(bones[i][k], weights[i][k]) for k in range(4) if weights[i][k] > 0.05]
        r_shoulder.append((p, b_list))

print(f"Right shoulder/arm vertices: {len(r_shoulder)}")
r_bones = set()
for p, b_list in r_shoulder:
    for b, w in b_list:
        r_bones.add(b)
print("Bones on right shoulder:", sorted(r_bones))

# Print any vertices that have head, neck, or weird bones
weird = []
for p, b_list in r_shoulder:
    for b, w in b_list:
        if any(bad in b for bad in ['head', 'neck', 'spine_0', 'pelvis', 'hand_L', 'arm_upper_L', 'clavicle_L']):
            weird.append((p, b_list))
            break

print(f"Weird bone vertices in right shoulder: {len(weird)}")
for p, b_list in weird[:10]:
    print(f"  Pos: [{p[0]:+.2f}, {p[1]:+.2f}, {p[2]:+.2f}] -> {b_list}")

