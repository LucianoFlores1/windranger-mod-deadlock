import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

orig = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
new_d = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))

o_pos = np.array(orig['positions'])
n_pos = np.array(new_d['positions'])

print("Original DMX bounds (raw values in file):")
print(f"  X: {o_pos[:,0].min():.2f} to {o_pos[:,0].max():.2f} (span: {o_pos[:,0].max()-o_pos[:,0].min():.2f})")
print(f"  Y: {o_pos[:,1].min():.2f} to {o_pos[:,1].max():.2f} (span: {o_pos[:,1].max()-o_pos[:,1].min():.2f})")
print(f"  Z: {o_pos[:,2].min():.2f} to {o_pos[:,2].max():.2f} (span: {o_pos[:,2].max()-o_pos[:,2].min():.2f})")

print("\nNew DMX bounds (raw values in file):")
print(f"  X: {n_pos[:,0].min():.2f} to {n_pos[:,0].max():.2f} (span: {n_pos[:,0].max()-n_pos[:,0].min():.2f})")
print(f"  Y: {n_pos[:,1].min():.2f} to {n_pos[:,1].max():.2f} (span: {n_pos[:,1].max()-n_pos[:,1].min():.2f})")
print(f"  Z: {n_pos[:,2].min():.2f} to {n_pos[:,2].max():.2f} (span: {n_pos[:,2].max()-n_pos[:,2].min():.2f})")

