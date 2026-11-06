import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
print("Materials in warka3:", info['materials'])
pos = info['positions']
print(f"Positions: {len(pos)} verts")
print(f"  X: {pos[:,0].min():.2f} to {pos[:,0].max():.2f}")
print(f"  Y: {pos[:,1].min():.2f} to {pos[:,1].max():.2f}")
print(f"  Z: {pos[:,2].min():.2f} to {pos[:,2].max():.2f}")
print(f"Tris: {len(info['tris'])}")
