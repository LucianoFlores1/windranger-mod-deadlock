import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo\tools')
import datamodel as dm
import numpy as np

d = dm.load(r'extracted\archer_warka3.dmx')
print("Root keys:", d.root.keys())
model = d.root['model']
dags = [c for c in model['children'] if c.type == 'DmeDag']
print(f"Total DmeDag: {len(dags)}")
for i, c in enumerate(dags):
    shape = c.get('shape')
    if shape:
        vd = shape['currentState']
        pos = np.array([list(p) for p in vd['position$0']])
        mats = [fs['material']['mtlName'] for fs in shape['faceSets']]
        print(f"Mesh {i} '{c.name}': {len(pos)} verts, mats={mats}")
        print(f"   X: {pos[:,0].min():.2f} to {pos[:,0].max():.2f}")
        print(f"   Y: {pos[:,1].min():.2f} to {pos[:,1].max():.2f}")
        print(f"   Z: {pos[:,2].min():.2f} to {pos[:,2].max():.2f}")

