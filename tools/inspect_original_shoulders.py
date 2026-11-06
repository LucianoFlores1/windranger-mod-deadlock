import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path
import collections

info = read_dmx_mesh(Path(r'extracted\windrunner_shoulderpads_windranger_shoulders.dmx'))
bone_counts = collections.Counter()
for b_row, w_row in zip(info['bones'], info['weights']):
    for b, w in zip(b_row, w_row):
        if w > 0.05 and b:
            bone_counts[b] += 1

print("Original Dota 2 bone weights on shoulderpads:")
for b, c in bone_counts.most_common():
    print(f"  {b:25}: {c} vertices")

