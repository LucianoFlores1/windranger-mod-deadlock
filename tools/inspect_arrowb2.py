import sys
sys.path.insert(0, "tools")
import datamodel
import numpy as np

dm = datamodel.load("extracted/archer_arrowb2.dmx")
root = dm.root

mesh = None
def find_mesh(elem):
    global mesh
    if elem.type == 'DmeMesh':
        mesh = elem
        return
    for k, v in elem.items():
        if isinstance(v, datamodel.Element):
            find_mesh(v)
        elif isinstance(v, list):
            for e in v:
                if isinstance(e, datamodel.Element):
                    find_mesh(e)

find_mesh(root['model'])
cs = mesh['currentState']
pos = np.array(cs['position$0'])
print(f"archer_arrowb2 positions ({len(pos)} verts):")
print(f"X: min={pos[:,0].min():.2f}, max={pos[:,0].max():.2f}, span={pos[:,0].ptp():.2f}")
print(f"Y: min={pos[:,1].min():.2f}, max={pos[:,1].max():.2f}, span={pos[:,1].ptp():.2f}")
print(f"Z: min={pos[:,2].min():.2f}, max={pos[:,2].max():.2f}, span={pos[:,2].ptp():.2f}")

# And what material does archer_arrowb2 have?
mats = set()
def find_mats(elem):
    if elem.type == 'DmeMaterial':
        mats.add(elem.name)
    for k, v in elem.items():
        if isinstance(v, datamodel.Element):
            find_mats(v)
        elif isinstance(v, list):
            for e in v:
                if isinstance(e, datamodel.Element):
                    find_mats(e)

find_mats(root)
print("Materials in archer_arrowb2.dmx:", mats)

