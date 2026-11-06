import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"extracted\verify_archer.glb")

meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
print(f"Total meshes in compiled model: {len(meshes)}")

for m in meshes:
    verts = np.array([v.co for v in m.data.vertices])
    print(f"Mesh: {m.name}")
    print(f"  Verts: {len(verts)}, Polys: {len(m.data.polygons)}")
    print(f"  X: [{verts[:,0].min():.3f}, {verts[:,0].max():.3f}] (span: {verts[:,0].max()-verts[:,0].min():.3f}m)")
    print(f"  Y: [{verts[:,1].min():.3f}, {verts[:,1].max():.3f}] (span: {verts[:,1].max()-verts[:,1].min():.3f}m)")
    print(f"  Z: [{verts[:,2].min():.3f}, {verts[:,2].max():.3f}] (span: {verts[:,2].max()-verts[:,2].min():.3f}m)")

# Check warka orientation:
warka = next(m for m in meshes if 'warka' in m.name.lower())
w_verts = np.array([v.co for v in warka.data.vertices])
feet = w_verts[w_verts[:,2] < 0.1]
print(f"Warka feet Y range: [{feet[:,1].min():.3f}, {feet[:,1].max():.3f}] (toes at min Y: {feet[:,1].min():.3f})")

# Check bow orientation:
bow = next(m for m in meshes if 'bow' in m.name.lower() and 'teteva' not in m.name.lower() and 'arrow' not in m.name.lower())
b_verts = np.array([v.co for v in bow.data.vertices])
print(f"Bow Z range: [{b_verts[:,2].min():.3f}, {b_verts[:,2].max():.3f}] (height: {b_verts[:,2].max()-b_verts[:,2].min():.3f}m)")

bpy.ops.wm.save_as_mainfile(filepath=r"extracted\verify_archer_scene.blend")
print("Saved blend to extracted/verify_archer_scene.blend")

