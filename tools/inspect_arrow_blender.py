import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_arrowb2.dmx'))
arrow_pos = dmx_to_blender(info['positions'])
print("Arrow bounds in Blender:")
print("X:", arrow_pos[:, 0].min(), "to", arrow_pos[:, 0].max())
print("Y:", arrow_pos[:, 1].min(), "to", arrow_pos[:, 1].max())
print("Z:", arrow_pos[:, 2].min(), "to", arrow_pos[:, 2].max())

