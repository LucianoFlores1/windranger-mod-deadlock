import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_teteva.dmx'))
pos = np.array(info['positions'])
print("Teteva 32 verts:")
for i, (p, b, w) in enumerate(zip(pos, info['bones'], info['weights'])):
    print(f"  v{i:2d}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}) bones={list(zip(b, w))}")

