import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
root = dm.root
joints = [j.name for j in root['skeleton']['jointList']]

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
print("currentState keys:", list(cs.keys()))
joint_indices = cs.get('jointIndices', [])
print(f"jointIndices len: {len(joint_indices)}")

used_joints = set()
for t in joint_indices:
    if isinstance(t, (list, tuple)):
        for idx in t:
            if idx < len(joints):
                used_joints.add(joints[idx])
    elif isinstance(t, int):
        if t < len(joints):
            used_joints.add(joints[t])

print("Total used joints:", len(used_joints))
for j in sorted(used_joints):
    print("  ", j)

