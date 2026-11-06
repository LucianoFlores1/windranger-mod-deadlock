import sys
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender
import numpy as np

# Load archer_respawn_countdown_idle.dmx or check animation bones
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

# How is the Arcana left arm weighted in archer_warka3_orig.dmx?
for vi in range(len(pos)):
    p = pos[vi]
    # left arm region
    if p[0] > 0.25 and 1.0 < p[2] < 1.4:
        for b, w in zip(bones[vi], weights[vi]):
            if w > 0.5:
                # print some samples
                if vi % 100 == 0:
                    print(f"Vert {vi}: pos=[{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}], bone={b} (w={w:.2f})")

