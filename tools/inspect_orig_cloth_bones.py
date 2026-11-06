import sys
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh

info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
bone_names = info['bones']
unique_bones = set()
for row in bone_names:
    for b in row:
        if b:
            unique_bones.add(b)

print("All bones in archer_warka3_orig:")
for b in sorted(unique_bones):
    if any(k in b.lower() for k in ['cape', 'cloth', 'coat', 'hair', 'skirt', 'quiver', 'spine', 'pelvis']):
        print(" ", b)

