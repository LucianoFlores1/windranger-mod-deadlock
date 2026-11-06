import bpy
import numpy as np
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
from mathutils import Matrix, Vector
import itertools

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Ref bow
info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])
ref_center = np.mean(ref_pos, axis=0)
ref_top = max(ref_pos, key=lambda p: p[2])
ref_bot = min(ref_pos, key=lambda p: p[2])

# 2. Classic bow
glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner\windrunner_bow.glb"
bpy.ops.import_scene.gltf(filepath=glb)
bow = next(o for o in bpy.data.objects if o.type == 'MESH')
c_pos = np.array([v.co for v in bow.data.vertices])
c_center = np.mean(c_pos, axis=0)

# Shift classic to origin
c_shifted = c_pos - c_center

# Scale factor
ref_span_z = ref_pos[:, 2].max() - ref_pos[:, 2].min()
c_span_x = c_pos[:, 0].max() - c_pos[:, 0].min()
scale = ref_span_z / c_span_x
c_scaled = c_shifted * scale

best_score = float('inf')
best_R = None
best_name = None

# Test standard 90-deg rotation permutations
# Matrix of form R where R has entries in {-1, 0, 1} and det(R) = +1
perms = list(itertools.permutations([0, 1, 2]))
signs = list(itertools.product([-1, 1], repeat=3))

for p in perms:
    for s in signs:
        R = np.zeros((3, 3))
        for row, (col, sign) in enumerate(zip(p, s)):
            R[row, col] = sign
        if np.isclose(np.linalg.det(R), 1.0):
            # Test how well tips align
            # In classic, top is max X, bot is min X
            c_top = c_scaled[np.argmax(c_pos[:, 0])]
            c_bot = c_scaled[np.argmin(c_pos[:, 0])]
            rot_top = R @ c_top
            rot_bot = R @ c_bot
            
            # We want rot_top to have max Z (> 0.5) and rot_bot to have min Z (< -0.5)
            if rot_top[2] > 0.5 and rot_bot[2] < -0.5:
                # Also curve: in ref bow, grip is +X relative to tips!
                # tips - center has X < 0
                tips_x = (rot_top[0] + rot_bot[0]) / 2.0
                # In ref bow:
                ref_tips_x = (ref_top[0] + ref_bot[0]) / 2.0 - ref_center[0]
                # Compare sign of curve
                score = abs(rot_top[2] - (ref_top[2] - ref_center[2])) + abs(rot_bot[2] - (ref_bot[2] - ref_center[2])) + abs(tips_x - ref_tips_x)*2
                print(f"R candidate det={np.linalg.det(R):.0f}, rot_top={rot_top}, tips_x={tips_x:.3f}, ref_tips_x={ref_tips_x:.3f}, score={score:.4f}")
                if score < best_score:
                    best_score = score
                    best_R = R

print("\n=== BEST ROTATION MATRIX ===")
print(best_R)
print("Best score:", best_score)

