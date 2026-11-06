import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
import datamodel as dm
from pathlib import Path
import collections

d = dm.load(r'extracted\archer_warka3.dmx')
c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
shape = c['shape']

# Find faceset for shoulders
# In test_warka_correct, FaceSet 3 is models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat
for i, fs in enumerate(shape['faceSets']):
    m_name = fs['material']['mtlName']
    if 'armor_style1' in m_name:
        faces = list(fs['faces'])
        v_indices = set(idx for idx in faces if idx != -1)
        print(f"Shoulderpads faceset {i} ({m_name}): {len(v_indices)} vertices")
        
        info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
        bone_counts = collections.Counter()
        for vi in v_indices:
            for b, w in zip(info['bones'][vi], info['weights'][vi]):
                if w > 0.05 and b:
                    bone_counts[b] += 1
        for b, count in bone_counts.most_common():
            print(f"  {b:25}: {count} vertices")

