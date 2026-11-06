import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

info = read_dmx_mesh(Path(r'extracted\archer_bow1.dmx'))
pos = np.array(info['positions']) # Raw DMX inches!

top_v = max(pos, key=lambda p: p[2])
bot_v = min(pos, key=lambda p: p[2])
mid_v = min(pos, key=lambda p: abs(p[2]))

print(f"Fitted bow top tip in DMX: X={top_v[0]:.2f}, Y={top_v[1]:.2f}, Z={top_v[2]:.2f}")
print(f"Fitted bow bot tip in DMX: X={bot_v[0]:.2f}, Y={bot_v[1]:.2f}, Z={bot_v[2]:.2f}")
print(f"Fitted bow grip in DMX:    X={mid_v[0]:.2f}, Y={mid_v[1]:.2f}, Z={mid_v[2]:.2f}")

