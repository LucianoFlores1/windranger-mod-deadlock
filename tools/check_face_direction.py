import bpy, os, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pipeline.coords import dmx_to_blender

bpy.ops.wm.read_factory_settings(use_empty=True)
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
ref_pos = dmx_to_blender(info['positions'])

# Find which bone is pelvis, spine_3, head in ref_warka
bone_names = info['bones']
weights = info['weights']
head_verts = []
for vi, (b_row, w_row) in enumerate(zip(bone_names, weights)):
    for b_name, w in zip(b_row, w_row):
        if 'head' in b_name and w > 0.8:
            head_verts.append(ref_pos[vi])
head_verts = np.array(head_verts)
print("Ref warka 'head' bone verts count:", len(head_verts))
print("Ref warka head Y range:", head_verts[:, 1].min(), "to", head_verts[:, 1].max(), "mean:", np.mean(head_verts[:, 1]))

# Now let's check Dota 2 Windrunner's head mesh or face
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
head_glb = os.path.join(wr_dir, "windrunner_head.glb")
bpy.ops.import_scene.gltf(filepath=head_glb)
h_mesh = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
h_pos = np.array([v.co for v in h_mesh.data.vertices]) * 0.5471
print("WR head mesh Y range:", h_pos[:, 1].min(), "to", h_pos[:, 1].max(), "mean:", np.mean(h_pos[:, 1]))

# Where is the nose / face of Windrunner in windrunner_head.glb?
# Nose has highest or lowest Y? Let's check max vs min Y of the face
print("WR head mesh bounds:")
print("  X:", h_pos[:, 0].min(), h_pos[:, 0].max())
print("  Y:", h_pos[:, 1].min(), h_pos[:, 1].max())
print("  Z:", h_pos[:, 2].min(), h_pos[:, 2].max())

