import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo\tools')
import datamodel as dm
import numpy as np

d = dm.load(r'extracted\archer\models\heroes_staging\archer\archer_body.dmx')
vd = d.root['model']['children'][122]['shape']['currentState']
pos = np.array([list(p) for p in vd['position$0']])

print("Archer body positions in DMX:")
print(f"X range: {pos[:,0].min():.2f} to {pos[:,0].max():.2f}")
print(f"Y range: {pos[:,1].min():.2f} to {pos[:,1].max():.2f}")
print(f"Z range: {pos[:,2].min():.2f} to {pos[:,2].max():.2f}")

