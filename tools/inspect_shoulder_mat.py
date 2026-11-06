import bpy, os, sys

bpy.ops.wm.read_factory_settings(use_empty=True)
wr_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted\models\heroes\windrunner"
bpy.ops.import_scene.gltf(filepath=os.path.join(wr_dir, "windrunner_shoulderpads.glb"))

for m in bpy.data.materials:
    print("Material on shoulderpads:", m.name)
    if m.use_nodes:
        for node in m.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                print("  Texture image:", node.image.name, node.image.filepath)

