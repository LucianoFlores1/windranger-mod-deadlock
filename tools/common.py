import sys
import bpy

def script_args():
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(path))
    new = [o for o in bpy.data.objects if o not in before]
    arms = [o for o in new if o.type == "ARMATURE"]
    if len(arms) != 1:
        raise RuntimeError(f"Se esperaba 1 armature en {path}, hay {len(arms)}")
    meshes = [o for o in new if o.type == "MESH" and o.find_armature() == arms[0]]
    return arms[0], meshes

def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)
