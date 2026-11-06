import sys
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh

warka_info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
bone_names = warka_info['bones']
weights = warka_info['weights']

hair_count = 0
for b_row, w_row in zip(bone_names, weights):
    for b, w in zip(b_row, w_row):
        if 'hair' in b and w > 0.01:
            hair_count += 1
            print(f"Hair bone: {b}, weight: {w}")

print(f"Total hair bone weights: {hair_count}")

