import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_bow1.dmx'))
bones = info['bones']
weights = info['weights']
pos = info['positions']

bone_counts = {}
for i in range(len(pos)):
    for b, w in zip(bones[i], weights[i]):
        if w > 0.01:
            bone_counts[b] = bone_counts.get(b, 0) + 1

print("Bones in archer_bow1.dmx:")
for b, c in sorted(bone_counts.items(), key=lambda x: -x[1]):
    print(f"  {b}: {c} vertices")

