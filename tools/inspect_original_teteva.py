import datamodel as dm

d = dm.load(r'extracted\archer_teteva.dmx')
c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
vd = c['shape']['currentState']
model = d.root['model']
joints = [j.name for j in model['jointList']]
print("Joints in teteva:")
for i, j in enumerate(joints):
    print(f"  {i}: {j}")

indices = vd['blendindices$0']
weights = vd['blendweights$0']
pos = vd['position$0']
print(f"Total vertices in teteva: {len(pos)}")
for i in [0, len(pos)//4, len(pos)//2, 3*len(pos)//4, len(pos)-1]:
    j_idx = indices[i*4]
    w = weights[i*4]
    p = pos[i]
    print(f"Vert {i:2d}: pos=({p[0]:.1f}, {p[1]:.1f}, {p[2]:.1f}), joint={joints[j_idx]} (w={w:.2f})")

