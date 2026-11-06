import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
uvs = np.array(info['uvs'])
print(f"DMX UVs: U=[{uvs[:,0].min():.4f}, {uvs[:,0].max():.4f}], V=[{uvs[:,1].min():.4f}, {uvs[:,1].max():.4f}]")
print(f"Sample DMX UV: {uvs[0]}")

