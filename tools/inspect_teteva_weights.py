import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_teteva.dmx")
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
b_indices = cs.get('blendindices$0', [])
b_weights = cs.get('blendweights$0', [])

joint_vertex_counts = {j: 0 for j in joints}
for i in range(0, len(b_indices), 4):
    for k in range(4):
        if i + k < len(b_indices) and i + k < len(b_weights):
            w = b_weights[i + k]
            idx = b_indices[i + k]
            if w > 0.001 and idx < len(joints):
                joint_vertex_counts[joints[idx]] += 1

print("\n--- Non-zero weighted joints in archer_teteva: ---")
for j, count in sorted(joint_vertex_counts.items(), key=lambda x: -x[1]):
    if count > 0:
        print(f"  {j}: {count} vertices")

