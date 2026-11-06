import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
import datamodel as dm
import numpy as np

d = dm.load(r'extracted\archer_warka3_orig.dmx')
c = next(c for c in d.root['model']['children'] if c.type == 'DmeDag')
shape = c['shape']
pos = np.array([list(p) for p in shape['currentState']['position$0']]) * 0.0254

for i, fs in enumerate(shape['faceSets']):
    m_name = fs['material']['mtlName']
    faces = list(fs['faces'])
    # Extract unique vertex indices in this faceset
    v_indices = set(idx for idx in faces if idx != -1)
    fs_pos = pos[list(v_indices)]
    print(f"FaceSet {i}: {m_name}")
    print(f"  Verts: {len(v_indices)}, Tris: {len(faces)//4}")
    print(f"  X: [{fs_pos[:,0].min():.2f}, {fs_pos[:,0].max():.2f}], Y: [{fs_pos[:,1].min():.2f}, {fs_pos[:,1].max():.2f}], Z: [{fs_pos[:,2].min():.2f}, {fs_pos[:,2].max():.2f}]")

