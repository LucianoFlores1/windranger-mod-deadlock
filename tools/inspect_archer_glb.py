import bpy, os, sys
import numpy as np

bpy.ops.wm.read_factory_settings(use_empty=True)
archer_glb = r'extracted\archer.glb'
bpy.ops.import_scene.gltf(filepath=archer_glb)

print("Objects in archer.glb:")
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        pts = np.array([v.co for v in o.data.vertices])
        print(f"Mesh {o.name:30s}: X=[{pts[:,0].min():+.2f}, {pts[:,0].max():+.2f}], Y=[{pts[:,1].min():+.2f}, {pts[:,1].max():+.2f}], Z=[{pts[:,2].min():+.2f}, {pts[:,2].max():+.2f}]")
    elif o.type == 'ARMATURE':
        print(f"Armature: {o.name}")
        for b in o.data.bones:
            if b.name in ['head', 'hand_L', 'hand_R', 'knee_L', 'knee_R', 'ankle_L', 'pelvis']:
                print(f"  Bone {b.name:15s}: head={b.head}, tail={b.tail}")

