import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = np.array(info['positions'])
print("Raw DMX pos bounds (inches?):")
print(f"  DMX 0 (X): {pos[:,0].min():.2f} to {pos[:,0].max():.2f}")
print(f"  DMX 1 (Y): {pos[:,1].min():.2f} to {pos[:,1].max():.2f}")
print(f"  DMX 2 (Z): {pos[:,2].min():.2f} to {pos[:,2].max():.2f}")

