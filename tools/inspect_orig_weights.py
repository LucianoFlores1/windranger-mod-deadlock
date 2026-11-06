import sys
sys.path.insert(0, "tools")
import datamodel

dm = datamodel.load("extracted/archer_warka3_orig.dmx")
root = dm.root
joints = [j.name for j in root['skeleton']['jointList']]

# Find mesh in model
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
print("Mesh name:", mesh.name if mesh else "None")

# Inspect vertex weights
joint_weights = mesh.get("jointWeights")
print("Joint weights type:", type(joint_weights))

# Let's count how many non-zero weights each joint has across all vertices!
joint_counts = {}
for j in joints:
    joint_counts[j] = 0

# Check vertex data
# In DMX, jointWeights has weight data
# Or vertexData has jointIndices and jointWeights
vdata = mesh.get("vertexData")
print("VertexData type:", type(vdata))
if vdata:
    for f in vdata.get("vertexFormat", []):
        print("  Format field:", f)
    indices = vdata.get("jointIndices", [])
    weights = vdata.get("jointWeights", [])
    print(f"Indices len: {len(indices)}, Weights len: {len(weights)}")
    
    # Check which joints have weights
    used_joints = set()
    for idx_tuple in indices:
        for idx in idx_tuple:
            if idx < len(joints):
                used_joints.add(joints[idx])
    print(f"Used joints count: {len(used_joints)}")
    print("Used joints in orig warka3:")
    for j in sorted(used_joints):
        print("  ", j)

