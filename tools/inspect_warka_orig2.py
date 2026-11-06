import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
root = dm.root
for k in root:
    print(k, type(root[k]))

# Find joints or vertex groups in DMX
def find_elements(elem, depth=0):
    if depth > 4:
        return
    for k, v in elem.items():
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], datamodel.Element):
            print("  "*depth + f"{k}: list of {len(v)} elements ({v[0].type})")
            if k in ['joints', 'jointWeights', 'transforms']:
                names = [e.name for e in v if hasattr(e, 'name')]
                print("  "*depth + f"  Sample names: {names[:10]}")
        elif isinstance(v, datamodel.Element):
            print("  "*depth + f"{k}: Element ({v.type})")
            find_elements(v, depth+1)

find_elements(root)

