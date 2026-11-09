import bpy
import os
import sys

sys.path.append(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\tools")
import build_restored_perfect_windrunner as wr

top, bot = wr.build_bow()
wr.build_teteva(top, bot)
wr.build_body()

body = bpy.data.objects.get("archer_warka3") or bpy.data.objects.get("classic_body_main")
group_map = {g.name: g for g in body.vertex_groups}

vg_auL = group_map.get('arm_upper_L')
vg_alL = group_map.get('arm_lower_L') or body.vertex_groups.new(name='arm_lower_L')
vg_hL = group_map.get('hand_L')

cleaned_l = 0
for v in body.data.vertices:
    if v.co.x > 0.20 and v.co.z > 0.75:
        removed = 0.0
        for g_entry in list(v.groups):
            g_name = body.vertex_groups[g_entry.group].name
            if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_R', 'head', 'neck', 'leg', '_R']):
                removed += g_entry.weight
                body.vertex_groups[g_entry.group].remove([v.index])
        if removed > 0.001:
            cleaned_l += 1
            if v.co.x > 0.47:
                target = vg_hL
            elif v.co.x > 0.32:
                target = vg_alL
            else:
                target = vg_auL
            try: cur = target.weight(v.index)
            except: cur = 0.0
            target.add([v.index], cur + removed, 'REPLACE')

print(f"\n[RESULT] Left arm vertices cleaned of bad weights: {cleaned_l}")

remaining_bad_l = 0
for v in body.data.vertices:
    if v.co.x > 0.20 and v.co.z > 0.75:
        for g in v.groups:
            g_name = body.vertex_groups[g.group].name
            if any(bad in g_name for bad in ['spine', 'pelvis', 'clavicle_R', 'head', 'neck', 'leg', '_R']):
                remaining_bad_l += 1

print(f"[RESULT] Remaining bad weights on left arm: {remaining_bad_l}")
