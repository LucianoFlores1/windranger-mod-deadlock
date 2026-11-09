import bpy
import os
import sys
import numpy as np

sys.path.append(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\tools")
import build_restored_perfect_windrunner as wr

top, bot = wr.build_bow()
wr.build_teteva(top, bot)
wr.build_body()

body = bpy.data.objects.get("archer_warka3") or bpy.data.objects.get("classic_body_main")
group_map = {g.name: g for g in body.vertex_groups}

vg_auR = group_map.get('arm_upper_R')
vg_alR = group_map.get('arm_lower_R') or body.vertex_groups.new(name='arm_lower_R')
vg_hR = group_map.get('hand_R')

# Test Right Arm Strict Cleanup
cleaned_r = 0
for v in body.data.vertices:
    if v.co.x < -0.20 and v.co.z > 0.75:
        removed = 0.0
        for g_entry in list(v.groups):
            g_name = body.vertex_groups[g_entry.group].name
            # Bad bones on right arm
            if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_L', 'head', 'neck', 'leg', '_L']):
                removed += g_entry.weight
                body.vertex_groups[g_entry.group].remove([v.index])
        if removed > 0.001:
            cleaned_r += 1
            if v.co.x < -0.47:
                target = vg_hR
            elif v.co.x < -0.32:
                target = vg_alR
            else:
                target = vg_auR
            try: cur = target.weight(v.index)
            except: cur = 0.0
            target.add([v.index], cur + removed, 'REPLACE')

print(f"\n[RESULT] Right arm vertices cleaned of bad weights: {cleaned_r}")

# Re-check for ANY bad weights on right arm
remaining_bad = 0
for v in body.data.vertices:
    if v.co.x < -0.20 and v.co.z > 0.75:
        for g in v.groups:
            g_name = body.vertex_groups[g.group].name
            if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_L', 'head', 'neck', 'leg', '_L']):
                remaining_bad += 1

print(f"[RESULT] Remaining bad weights on right arm: {remaining_bad}")
