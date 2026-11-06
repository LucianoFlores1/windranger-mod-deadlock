import sys
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

# Find all vertices weighted to hand_L and hand_R
hl_verts = []
hr_verts = []
for i, (b_row, w_row) in enumerate(zip(bones, weights)):
    for b, w in zip(b_row, w_row):
        if 'hand_L' in b and w > 0.3:
            hl_verts.append(pos[i])
        if 'hand_R' in b and w > 0.3:
            hr_verts.append(pos[i])

hl = np.array(hl_verts)
hr = np.array(hr_verts)
print(f"hand_L verts: {len(hl)}")
print(f"  X: [{hl[:,0].min():.2f}, {hl[:,0].max():.2f}]")
print(f"  Y: [{hl[:,1].min():.2f}, {hl[:,1].max():.2f}]")
print(f"  Z: [{hl[:,2].min():.2f}, {hl[:,2].max():.2f}]")

print(f"hand_R verts: {len(hr)}")
print(f"  X: [{hr[:,0].min():.2f}, {hr[:,0].max():.2f}]")
print(f"  Y: [{hr[:,1].min():.2f}, {hr[:,1].max():.2f}]")
print(f"  Z: [{hr[:,2].min():.2f}, {hr[:,2].max():.2f}]")

# Are there any other vertices weighted to arm_lower_L, arm_upper_L?
for arm_b in ['arm_upper_L', 'arm_lower_L', 'arm_upper_R', 'arm_lower_R']:
    v_list = []
    for i, (b_row, w_row) in enumerate(zip(bones, weights)):
        for b, w in zip(b_row, w_row):
            if arm_b in b and w > 0.3:
                v_list.append(pos[i])
    if v_list:
        v_arr = np.array(v_list)
        print(f"{arm_b} verts: {len(v_arr)}, X: [{v_arr[:,0].min():.2f}, {v_arr[:,0].max():.2f}], Z: [{v_arr[:,2].min():.2f}, {v_arr[:,2].max():.2f}]")

