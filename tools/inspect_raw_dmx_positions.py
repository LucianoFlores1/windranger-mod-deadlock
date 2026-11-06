import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
pos = np.array(info['positions'])
print("Raw DMX positions (inches):")
print("  X:", pos[:,0].min(), pos[:,0].max())
print("  Y:", pos[:,1].min(), pos[:,1].max())
print("  Z:", pos[:,2].min(), pos[:,2].max())

