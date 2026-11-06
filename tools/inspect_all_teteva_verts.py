import datamodel as dm

d = dm.load(r'extracted\archer_teteva.dmx')
c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
vd = c['shape']['currentState']
model = d.root['model']
joints = [j.name for j in model['jointList']]

indices = vd['blendindices$0']
weights = vd['blendweights$0']
pos = vd['position$0']

print("All 32 vertices in original teteva:")
for i in range(len(pos)):
    j_list = []
    for k in range(4):
        idx = indices[i*4 + k]
        w = weights[i*4 + k]
        if w > 0.01:
            j_list.append(f"{joints[idx]}:{w:.2f}")
    p = pos[i]
    print(f"v{i:2d}: Z={p[2]:+6.1f}, Y={p[1]:+6.1f}, X={p[0]:+6.1f} | {' '.join(j_list)}")

