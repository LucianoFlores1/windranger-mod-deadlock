import sys
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh

for name in ['archer_bow1.dmx', 'archer_arrowb2.dmx']:
    info = read_dmx_mesh(Path('extracted') / name)
    pos = info['positions']
    print(f"=== {name} ===")
    print(f"  Verts: {len(pos)}")
    print(f"  Materials: {info.get('materials', [])}")
    bones = set()
    for row in info['bones']:
        for b in row:
            if b: bones.add(b)
    print(f"  Bones: {sorted(bones)}")
