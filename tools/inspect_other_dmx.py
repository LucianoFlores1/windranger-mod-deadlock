import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo\tools')
import datamodel as dm
import numpy as np

for name in ['archer_bow1', 'archer_teteva', 'archer_arrowb2']:
    d = dm.load(f'extracted\\{name}.dmx')
    model = d.root['model']
    c = next(c for c in model['children'] if c.type == 'DmeDag')
    shape = c['shape']
    vd = shape['currentState']
    pos = np.array([list(p) for p in vd['position$0']])
    mats = [fs['material']['mtlName'] for fs in shape['faceSets']]
    print(f"{name}: {len(pos)} verts, mats={mats}, Z range={pos[:,2].min():.2f} to {pos[:,2].max():.2f}")

