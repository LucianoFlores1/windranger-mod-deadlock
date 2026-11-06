import sys
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo\tools')
import datamodel as dm
import numpy as np

d = dm.load(r'extracted\archer_arrowb2.dmx')
model = d.root['model']
c = next(c for c in model['children'] if c.type == 'DmeDag')
vd = c['shape']['currentState']
joint_list = [j.name for j in model['jointList']]
bi = np.array(vd['blendindices$0']).reshape(-1, vd['jointCount'])
bw = np.array(vd['blendweights$0']).reshape(-1, vd['jointCount'])

bones = set()
for row_i, row_w in zip(bi, bw):
    for idx, w in zip(row_i, row_w):
        if w > 0.001:
            bones.add(joint_list[idx])
print("Arrow/Quiver bones:", bones)

