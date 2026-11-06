import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import numpy as np

for name in ['archer_teteva.dmx', 'archer_arrowb2.dmx']:
    info = read_dmx_mesh(Path(f'extracted/{name}'))
    raw_pos = np.array(info['positions'])
    # In DMX space (inches)
    print(f"=== {name} ===")
    print(f"  Raw DMX pos: X=[{raw_pos[:,0].min():.2f}, {raw_pos[:,0].max():.2f}], Y=[{raw_pos[:,1].min():.2f}, {raw_pos[:,1].max():.2f}], Z=[{raw_pos[:,2].min():.2f}, {raw_pos[:,2].max():.2f}]")
    # In Blender space (-X, -Y, Z) * 0.0254
    b_pos = np.stack([-raw_pos[:,0], -raw_pos[:,1], raw_pos[:,2]], axis=-1) * 0.0254
    print(f"  Blender pos: X=[{b_pos[:,0].min():.2f}, {b_pos[:,0].max():.2f}], Y=[{b_pos[:,1].min():.2f}, {b_pos[:,1].max():.2f}], Z=[{b_pos[:,2].min():.2f}, {b_pos[:,2].max():.2f}]")
    
    # Active bones
    active = set()
    for b_row, w_row in zip(info['bones'], info['weights']):
        for b, w in zip(b_row, w_row):
            if w > 0.01 and b:
                active.add(b)
    print(f"  Bones: {active}")

