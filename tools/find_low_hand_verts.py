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

print("=== INSPECTING LOW VERTICES WITH HAND WEIGHTS ===")
for i, p in enumerate(pos):
    if p[2] < 1.0:
        for b, w in zip(bones[i], weights[i]):
            if 'hand' in b.lower() and w > 0.01:
                print(f"Vert {i}: pos=({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}), bone={b}, w={w:.2f}")
                break

