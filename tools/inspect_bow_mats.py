import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_bow1_orig.dmx")
root = dm.root
print("Root:", root.name)

# Find materials
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
print("Materials in archer_bow1_orig.dmx:", mats)

