import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.test_refined_rig import base_mesh

pts = np.array([v.co for v in base_mesh.data.vertices])
l_forearm_mask = (pts[:,0] > 0.28) & (pts[:,0] <= 0.48) & (pts[:,2] > 0.85) & (pts[:,2] < 1.35)
l_forearm_indices = np.where(l_forearm_mask)[0]

forearm_bones = set()
for vi in l_forearm_indices:
    v = base_mesh.data.vertices[vi]
    for g in v.groups:
        if g.weight > 0.05:
            forearm_bones.add(base_mesh.vertex_groups[g.group].name)

print("Left forearm bones after DataTransfer:", sorted(forearm_bones))

