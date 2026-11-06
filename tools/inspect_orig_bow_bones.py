import sys
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh

info = read_dmx_mesh(Path(r'extracted\archer_bow1_orig.dmx'))
bone_names = info['bones']
weights = info['weights']
pos = info['positions']

# Find unique bones in bow
unique_bones = set()
for b_row in bone_names:
    for b in b_row:
        if b:
            unique_bones.add(b)
print("Bones used in archer_bow1_orig:", sorted(unique_bones))

# Top vertices vs bottom vertices
top_vi = max(range(len(pos)), key=lambda i: pos[i][2])
bot_vi = min(range(len(pos)), key=lambda i: pos[i][2])
mid_vi = min(range(len(pos)), key=lambda i: abs(pos[i][2]))
print(f"Top vert (Z={pos[top_vi][2]:.1f}):", list(zip(bone_names[top_vi], weights[top_vi])))
print(f"Mid vert (Z={pos[mid_vi][2]:.1f}):", list(zip(bone_names[mid_vi], weights[mid_vi])))
print(f"Bot vert (Z={pos[bot_vi][2]:.1f}):", list(zip(bone_names[bot_vi], weights[bot_vi])))

