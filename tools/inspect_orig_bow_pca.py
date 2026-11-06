import bpy
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load ref bow
info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])
print("Orig bow in Blender coords:")
print(f"X: [{ref_pos[:,0].min():.4f}, {ref_pos[:,0].max():.4f}]")
print(f"Y: [{ref_pos[:,1].min():.4f}, {ref_pos[:,1].max():.4f}]")
print(f"Z: [{ref_pos[:,2].min():.4f}, {ref_pos[:,2].max():.4f}]")

# Find top tip, bot tip, grip in orig bow
top_tip = max(ref_pos, key=lambda p: p[2])
bot_tip = min(ref_pos, key=lambda p: p[2])
print(f"Orig top tip: ({top_tip[0]:.4f}, {top_tip[1]:.4f}, {top_tip[2]:.4f})")
print(f"Orig bot tip: ({bot_tip[0]:.4f}, {bot_tip[1]:.4f}, {bot_tip[2]:.4f})")

# Check PCA or principal axis of bow
center = np.mean(ref_pos, axis=0)
diff = ref_pos - center
cov = np.cov(diff.T)
eigvals, eigvecs = np.linalg.eigh(cov)
# Major axis is eigvecs[:, 2]
print("Major axis (length of bow):", eigvecs[:, 2])
print("Second axis (curve of bow):", eigvecs[:, 1])
print("Normal axis (thickness):", eigvecs[:, 0])

