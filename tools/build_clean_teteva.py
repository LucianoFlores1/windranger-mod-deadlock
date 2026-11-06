import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
import datamodel as dm
from pathlib import Path
import numpy as np

# Load fitted bow tips
bow_info = read_dmx_mesh(Path(r'extracted\archer_bow1.dmx'))
bow_pos = np.array(bow_info['positions'])
top_tip = max(bow_pos, key=lambda p: p[2])
bot_tip = min(bow_pos, key=lambda p: p[2])

print(f"Connecting bowstring between:")
print(f"  Top tip: X={top_tip[0]:.2f}, Y={top_tip[1]:.2f}, Z={top_tip[2]:.2f}")
print(f"  Bot tip: X={bot_tip[0]:.2f}, Y={bot_tip[1]:.2f}, Z={bot_tip[2]:.2f}")

# Load original teteva template
d = dm.load(r'extracted\archer_teteva.dmx')
c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
shape = c['shape']
vd = shape['currentState']

model = d.root['model']
joint_index = {j.name: i for i, j in enumerate(model['jointList'])}
upper_idx = joint_index.get('upperLimb_1', joint_index.get('upperLimb_end', 0))
lower_idx = joint_index.get('lowerLimb_1', joint_index.get('lowerLimb_end', 0))

n_verts = len(vd['position$0']) # 32 vertices
new_pos = []
blend_idx = []
blend_w = []

for i in range(n_verts):
    # Fraction from 0 (bot) to 1 (top)
    frac = i / (n_verts - 1)
    p = (1.0 - frac) * bot_tip + frac * top_tip
    new_pos.append(dm.Vector3(p.tolist()))
    
    # Weights: bottom half to lowerLimb_1, top half to upperLimb_1
    if frac > 0.5:
        # upper
        blend_idx += [upper_idx, 0, 0, 0]
        blend_w += [1.0, 0.0, 0.0, 0.0]
    else:
        # lower
        blend_idx += [lower_idx, 0, 0, 0]
        blend_w += [1.0, 0.0, 0.0, 0.0]

vd['position$0'] = dm.make_array(new_pos, dm.Vector3)
vd['blendindices$0'] = dm.make_array(blend_idx, int)
vd['blendweights$0'] = dm.make_array(blend_w, float)

out_teteva = Path(r'extracted\archer_teteva.dmx')
d.write(str(out_teteva), "binary", 9)
print(f"[OK] Clean teteva written: {out_teteva} ({out_teteva.stat().st_size:,} bytes)")

