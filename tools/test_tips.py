import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

bow_info = read_dmx_mesh(Path('extracted/archer_bow1.dmx'))
bow_pos = np.array(bow_info['positions'])
top_tip = max(bow_pos, key=lambda p: p[2])
bot_tip = min(bow_pos, key=lambda p: p[2])
print('Top tip:', top_tip)
print('Bot tip:', bot_tip)
print('Bow Z span:', bow_pos[:,2].min(), 'to', bow_pos[:,2].max())
print('Bow Y span:', bow_pos[:,1].min(), 'to', bow_pos[:,1].max())
print('Bow X span:', bow_pos[:,0].min(), 'to', bow_pos[:,0].max())

