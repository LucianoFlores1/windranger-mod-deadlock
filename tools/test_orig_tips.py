import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

orig_info = read_dmx_mesh(Path('extracted/archer_bow1_orig.dmx'))
orig_pos = np.array(orig_info['positions'])
print("ORIG Bow Z span:", orig_pos[:,2].min(), 'to', orig_pos[:,2].max())
print("ORIG Bow Y span:", orig_pos[:,1].min(), 'to', orig_pos[:,1].max())
print("ORIG Bow X span:", orig_pos[:,0].min(), 'to', orig_pos[:,0].max())

top_orig = max(orig_pos, key=lambda p: p[2])
bot_orig = min(orig_pos, key=lambda p: p[2])
print("ORIG Top tip:", top_orig)
print("ORIG Bot tip:", bot_orig)

