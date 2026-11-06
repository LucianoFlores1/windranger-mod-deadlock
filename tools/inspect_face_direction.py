import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = np.array(info['positions']) * 0.0254

# Head vertices: Z between 1.8 and 2.1
head_mask = (pos[:,2] > 1.8) & (pos[:,2] < 2.1)
head_pos = pos[head_mask]

# Let's find extreme Y on head:
print("Head vertices count:", len(head_pos))
print(f"Head Y min: {head_pos[:,1].min():.3f}, max: {head_pos[:,1].max():.3f}")

# Find bone weights on head vertices:
bones = [info['bones'][i] for i in range(len(pos)) if head_mask[i]]
weights = [info['weights'][i] for i in range(len(pos)) if head_mask[i]]

# Which side has face bones / hair bones?
# Let's find vertices with highest Y vs lowest Y:
max_y_verts = head_pos[head_pos[:,1] > (head_pos[:,1].max() - 0.05)]
min_y_verts = head_pos[head_pos[:,1] < (head_pos[:,1].min() + 0.05)]

print(f"Points at max Y (Y ~ {head_pos[:,1].max():.3f}): count={len(max_y_verts)}, avg Z={np.mean(max_y_verts[:,2]):.3f}")
print(f"Points at min Y (Y ~ {head_pos[:,1].min():.3f}): count={len(min_y_verts)}, avg Z={np.mean(min_y_verts[:,2]):.3f}")

# Also check feet: where are the toes?
# Feet vertices: Z < 0.1
feet_mask = pos[:,2] < 0.1
feet_pos = pos[feet_mask]
print(f"Feet Y min: {feet_pos[:,1].min():.3f}, max: {feet_pos[:,1].max():.3f}")

# In archer.vnmskel:
# We know ball_L (toes) is at Y = -0.142!
# ankle_L (heel/ankle) is at Y = +0.060!
# Therefore:
# -Y IS FORWARD (TOES)!
# +Y IS BACKWARD (HEEL / BACK)!

