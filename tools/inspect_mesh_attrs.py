import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
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
for k in mesh:
    print(k, type(mesh[k]))

