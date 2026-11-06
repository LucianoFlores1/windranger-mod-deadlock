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
print('Ref warka (Arcana) Y min/max:', ref_pos[:,1].min(), ref_pos[:,1].max(), 'mean Y:', np.mean(ref_pos[:,1]))
print('Ref warka X min/max:', ref_pos[:,0].min(), ref_pos[:,0].max())
print('Ref warka Z min/max:', ref_pos[:,2].min(), ref_pos[:,2].max())

# Where are the nose / face vertices of ref_warka? (Z > 1.6)
head_mask = ref_pos[:, 2] > 1.6
print('Ref warka head Y min/max:', ref_pos[head_mask, 1].min(), ref_pos[head_mask, 1].max())

# Where are the feet of ref_warka? (Z < 0.2)
feet_mask = ref_pos[:, 2] < 0.2
print('Ref warka feet Y min/max:', ref_pos[feet_mask, 1].min(), ref_pos[feet_mask, 1].max())

base_glb = r'E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb'
bpy.ops.import_scene.gltf(filepath=base_glb)
wr_mesh = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
wr_pos = np.array([v.co for v in wr_mesh.data.vertices]) * 0.5471
print('WR base GLB Y min/max:', wr_pos[:,1].min(), wr_pos[:,1].max(), 'mean Y:', np.mean(wr_pos[:,1]))
head_mask_wr = wr_pos[:, 2] > 1.6
if np.any(head_mask_wr):
    print('WR head Y min/max:', wr_pos[head_mask_wr, 1].min(), wr_pos[head_mask_wr, 1].max())
feet_mask_wr = wr_pos[:, 2] < 0.2
if np.any(feet_mask_wr):
    print('WR feet Y min/max:', wr_pos[feet_mask_wr, 1].min(), wr_pos[feet_mask_wr, 1].max())

