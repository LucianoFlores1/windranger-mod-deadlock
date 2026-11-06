import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, '.')
from tools.build_restored_perfect_windrunner import read_dmx_mesh, dmx_to_blender

# 1. Inspect quiver in archer_warka3.dmx
info = read_dmx_mesh(Path(r'extracted\archer_warka3.dmx'))
pos = dmx_to_blender(info['positions'])
bones = info['bones']
weights = info['weights']

quiver_verts = []
for i, (b_row, w_row) in enumerate(zip(bones, weights)):
    for b, w in zip(b_row, w_row):
        if any(k in b for k in ['quiver', 'spine_2']) and w > 0.5:
            # check if vert is in quiver area
            quiver_verts.append((pos[i], b, w))

print("Total quiver/spine_2 verts in warka3:", len(quiver_verts))

# 2. Inspect original Dota 2 quiver: windrunner_quiver.glb
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_quiver.glb"))
q_obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
q_pts = np.array([v.co for v in q_obj.data.vertices]) * 0.5471
print("Dota 2 quiver original bounds (scaled):")
print(f"  X: [{q_pts[:,0].min():.2f}, {q_pts[:,0].max():.2f}]")
print(f"  Y: [{q_pts[:,1].min():.2f}, {q_pts[:,1].max():.2f}]")
print(f"  Z: [{q_pts[:,2].min():.2f}, {q_pts[:,2].max():.2f}]")

# What bones did Dota 2 quiver have?
print("Dota 2 quiver vertex groups:", [g.name for g in q_obj.vertex_groups])

