import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
raw_pos = np.array(info['positions'])
# Transform with (-X, -Y, Z) * 0.0254
pos = np.stack([-raw_pos[:,0], -raw_pos[:,1], raw_pos[:,2]], axis=-1) * 0.0254
bones = info['bones']
weights = info['weights']

print("Transformed Bow bounds in Blender space:")
print(f"  X: {pos[:,0].min():.3f} to {pos[:,0].max():.3f}")
print(f"  Y: {pos[:,1].min():.3f} to {pos[:,1].max():.3f}")
print(f"  Z: {pos[:,2].min():.3f} to {pos[:,2].max():.3f}")

def get_bone_mean(name):
    verts = [pos[vi] for vi, (b_row, w_row) in enumerate(zip(bones, weights)) if any(b == name and w > 0.3 for b, w in zip(b_row, w_row))]
    if verts:
        return np.mean(verts, axis=0)
    return None

for b in ['weapon_hand_L', 'upperLimb_0', 'upperLimb_1', 'upperLimb_end', 'lowerLimb_0', 'lowerLimb_1', 'lowerLimb_end']:
    m = get_bone_mean(b)
    if m is not None:
        print(f"  {b:20}: X={m[0]:.3f}, Y={m[1]:.3f}, Z={m[2]:.3f}")

