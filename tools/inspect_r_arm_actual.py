import bpy
import os
import sys

sys.path.append(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\tools")
import build_restored_perfect_windrunner as wr

# Let's run build_body() but stop before export to inspect body_main
wr.build_body()

# body_main is in bpy.data.objects
body = bpy.data.objects.get("archer_warka3") or bpy.data.objects.get("classic_body_main")
print("\n=== INSPECTING RIGHT ARM VERTICES ===")
arm_verts = [v for v in body.data.vertices if v.co.x < -0.22]
print(f"Total vertices on right arm (X < -0.22): {len(arm_verts)}")

spines_found = 0
for v in arm_verts:
    bad = []
    for g in v.groups:
        gname = body.vertex_groups[g.group].name
        if any(b in gname for b in ['spine', 'pelvis', 'clavicle_L', 'head', 'neck', 'leg']):
            if g.weight > 0.005:
                bad.append((gname, round(g.weight, 3)))
    if bad:
        spines_found += 1
        if spines_found <= 20:
            print(f"Vert {v.index} at ({v.co.x:.3f}, {v.co.y:.3f}, {v.co.z:.3f}): {bad}")

print(f"\nTOTAL VERTICES ON RIGHT ARM WITH SPINE/TORSO WEIGHTS: {spines_found} / {len(arm_verts)}")
