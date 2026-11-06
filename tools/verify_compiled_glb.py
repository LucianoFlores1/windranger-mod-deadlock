import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"extracted\verify_archer.glb")

meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
armatures = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE']

print(f"Total meshes: {len(meshes)}, total armatures: {len(armatures)}")

for m in meshes:
    verts = m.data.vertices
    xs = [v.co.x for v in verts]
    ys = [v.co.y for v in verts]
    zs = [v.co.z for v in verts]
    mats = [mat.name for mat in m.data.materials if mat]
    vgs = len(m.vertex_groups)
    print(f"Mesh '{m.name}': {len(verts)} verts, {len(m.data.polygons)} tris/polys, {vgs} vertex groups, mats: {mats}")
    print(f"   Bounds X: [{min(xs):.3f}, {max(xs):.3f}]")
    print(f"   Bounds Y: [{min(ys):.3f}, {max(ys):.3f}]")
    print(f"   Bounds Z: [{min(zs):.3f}, {max(zs):.3f}] (height span: {max(zs)-min(zs):.3f}m)")

# Save blend for visual inspection
bpy.ops.wm.save_as_mainfile(filepath=r"extracted\verify_archer\verify_archer.blend")
print("Saved blend file to extracted/verify_archer/verify_archer.blend")
