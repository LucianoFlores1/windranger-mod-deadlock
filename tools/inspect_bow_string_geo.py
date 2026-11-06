import bpy
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"dota2_extracted\models\heroes\windrunner\windrunner_bow.glb")
m = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
verts = np.array([v.co for v in m.data.vertices])

# In windrunner_bow, the bow is along X (-1.84 to +1.89)
# Are there thin long polygons connecting the tips?
print(f"Total polygons in bow: {len(m.data.polygons)}")
# Let's check long edges:
long_edges = []
for e in m.data.edges:
    v1 = verts[e.vertices[0]]
    v2 = verts[e.vertices[1]]
    length = np.linalg.norm(v1 - v2)
    if length > 1.0:
        long_edges.append((length, e.vertices[0], e.vertices[1]))

print(f"Long edges (>1m): {len(long_edges)}")
for l, v1, v2 in long_edges:
    print(f"  Length: {l:.2f}m between verts {v1} and {v2}")

