import bpy
from pathlib import Path

# Open or build to inspect
# Let's inspect tools/inspect_r_arm_bones.py
blend_path = Path(r"extracted\test_fitted_windrunner.blend")
if blend_path.exists():
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    
    obj = bpy.data.objects.get("windrunner_fitted") or bpy.data.objects.get("warka") or bpy.data.objects.get("body_main")
    if obj:
        print(f"Inspecting object: {obj.name}, verts: {len(obj.data.vertices)}")
        # Check right arm vertices: X < -0.18, 0.8 < Z < 1.4
        bad_count = 0
        for v in obj.data.vertices:
            if v.co.x < -0.18 and 0.8 < v.co.z < 1.4:
                bad_groups = []
                for g in v.groups:
                    g_name = obj.vertex_groups[g.group].name
                    if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_L', 'head', 'neck', 'leg']):
                        if g.weight > 0.01:
                            bad_groups.append((g_name, round(g.weight, 3)))
                if bad_groups:
                    bad_count += 1
                    if bad_count <= 15:
                        print(f"Vert {v.index} at ({v.co.x:.2f}, {v.co.y:.2f}, {v.co.z:.2f}) has bad groups: {bad_groups}")
        print(f"Total verts on right arm with torso/spine weights: {bad_count}")
    else:
        print("Object not found in blend file, objects:", [o.name for o in bpy.data.objects])
else:
    print("Blend file not found")
