import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info_bow = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
pos_bow = np.array(info_bow['positions'])
print("Raw Bow DMX pos bounds (inches):")
print(f"  DMX 0 (X): {pos_bow[:,0].min():.2f} to {pos_bow[:,0].max():.2f}")
print(f"  DMX 1 (Y): {pos_bow[:,1].min():.2f} to {pos_bow[:,1].max():.2f}")
print(f"  DMX 2 (Z): {pos_bow[:,2].min():.2f} to {pos_bow[:,2].max():.2f}")
print("In meters (pos * 0.0254):")
print(f"  X: {pos_bow[:,0].min()*0.0254:.2f} to {pos_bow[:,0].max()*0.0254:.2f}")
print(f"  Y: {pos_bow[:,1].min()*0.0254:.2f} to {pos_bow[:,1].max()*0.0254:.2f}")
print(f"  Z: {pos_bow[:,2].min()*0.0254:.2f} to {pos_bow[:,2].max()*0.0254:.2f}")

