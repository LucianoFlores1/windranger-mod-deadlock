import bpy
import numpy as np
import os
import sys
sys.path.insert(0, 'tools')
sys.path.insert(0, r'E:\creacion-mods\enigma-dynamo')
from pipeline.write_dmx import read_dmx_mesh
from pathlib import Path

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Load ref warka with DIRECT conversion (pos * 0.0254)
info = read_dmx_mesh(Path(r'extracted\archer_warka3_orig.dmx'))
ref_pos = np.array(info['positions']) * 0.0254

me_ref = bpy.data.meshes.new("ref_mesh")
me_ref.from_pydata(ref_pos.tolist(), [], info['tris'].tolist())
me_ref.update()
ref_obj = bpy.data.objects.new("ref_warka_direct", me_ref)
bpy.context.scene.collection.objects.link(ref_obj)

print("Direct ref_warka bounds:")
print(f"  X: {ref_pos[:,0].min():.3f} to {ref_pos[:,0].max():.3f}")
print(f"  Y: {ref_pos[:,1].min():.3f} to {ref_pos[:,1].max():.3f}")
print(f"  Z: {ref_pos[:,2].min():.3f} to {ref_pos[:,2].max():.3f}")

# 2. Load classic Windrunner body from glb
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

parts = [
    base_glb,
    os.path.join(wr_dir, "windrunner_head.glb"),
    os.path.join(wr_dir, "windrunner_cape.glb"),
    os.path.join(wr_dir, "windrunner_shoulderpads.glb"),
    os.path.join(wr_dir, "windrunner_quiver.glb"),
]

classic_meshes = []
for fpath in parts:
    before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=fpath)
    new_objs = set(bpy.context.scene.objects) - before
    for o in new_objs:
        if o.type == 'MESH' and 'icosphere' not in o.name.lower():
            if o.data.shape_keys:
                for kb in list(o.data.shape_keys.key_blocks):
                    o.shape_key_remove(kb)
            o.vertex_groups.clear()
            o.modifiers.clear()
            classic_meshes.append(o)
        elif o.type == 'ARMATURE':
            bpy.data.objects.remove(o)

# Join classic meshes
bpy.ops.object.select_all(action='DESELECT')
for m in classic_meshes:
    m.select_set(True)
bpy.context.view_layer.objects.active = classic_meshes[0]
bpy.ops.object.join()
joined = bpy.context.view_layer.objects.active
joined.name = "classic_wr_raw"

c_verts = np.array([v.co for v in joined.data.vertices])
print("Classic Windrunner raw bounds:")
print(f"  X: {c_verts[:,0].min():.3f} to {c_verts[:,0].max():.3f}")
print(f"  Y: {c_verts[:,1].min():.3f} to {c_verts[:,1].max():.3f}")
print(f"  Z: {c_verts[:,2].min():.3f} to {c_verts[:,2].max():.3f}")

# Face/head check:
# Top 5% of vertices in Z:
ref_head_verts = ref_pos[ref_pos[:,2] > (ref_pos[:,2].max() - 0.2)]
ref_head_center = np.mean(ref_head_verts, axis=0)
print(f"Ref head center: X={ref_head_center[0]:.3f}, Y={ref_head_center[1]:.3f}, Z={ref_head_center[2]:.3f}")

c_head_verts = c_verts[c_verts[:,2] > (c_verts[:,2].max() - 0.3)]
c_head_center = np.mean(c_head_verts, axis=0)
print(f"Classic head center: X={c_head_center[0]:.3f}, Y={c_head_center[1]:.3f}, Z={c_head_center[2]:.3f}")

# Check toes (bottom 5% in Z):
ref_feet = ref_pos[ref_pos[:,2] < (ref_pos[:,2].min() + 0.1)]
print(f"Ref feet Y range: {ref_feet[:,1].min():.3f} to {ref_feet[:,1].max():.3f}")

c_feet = c_verts[c_verts[:,2] < (c_verts[:,2].min() + 0.1)]
print(f"Classic feet Y range: {c_feet[:,1].min():.3f} to {c_feet[:,1].max():.3f}")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\test_direct_warka.blend")
print("Saved blend to extracted/test_direct_warka.blend")
