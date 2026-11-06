import sys
sys.path.insert(0, "tools")
import datamodel
import numpy as np

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
root = dm.root
mesh = next(c['shape'] for c in root['model']['children'] if c.type == 'DmeDag')
pos = np.array(mesh['currentState']['position$0'])

print("Raw DMX archer_warka3_orig positions:")
print("X span:", pos[:, 0].min(), "to", pos[:, 0].max())
print("Y span:", pos[:, 1].min(), "to", pos[:, 1].max())
print("Z span:", pos[:, 2].min(), "to", pos[:, 2].max())

