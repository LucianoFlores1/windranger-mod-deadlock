import bpy
import os

wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
base_glb = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb"

for fname in [base_glb, "windrunner_head.glb", "windrunner_cape.glb", "windrunner_shoulderpads.glb", "windrunner_quiver.glb", "windrunner_bow.glb"]:
    fpath = os.path.join(wr_dir, fname) if not os.path.isabs(fname) else fname
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=fpath)
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for m in meshes:
        xs = [v.co.x for v in m.data.vertices]
        ys = [v.co.y for v in m.data.vertices]
        zs = [v.co.z for v in m.data.vertices]
        print(f"{os.path.basename(fname)} - {m.name}:")
        print(f"   X: [{min(xs):.2f}, {max(xs):.2f}], Y: [{min(ys):.2f}, {max(ys):.2f}], Z: [{min(zs):.2f}, {max(zs):.2f}]")

