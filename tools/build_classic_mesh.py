import bpy
import os
import sys
import numpy as np

base_dir = r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock"
sys.path.insert(0, os.path.join(base_dir, "tools"))
from export_mesh import export_npz

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Import Archer
archer_path = os.path.join(base_dir, r"extracted\gltf\archer.glb")
bpy.ops.import_scene.gltf(filepath=archer_path)
arc_arm = next(obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE')
arc_meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

# 2. Import Windrunner Base and Accessories
wr_dir = os.path.join(base_dir, r"dota2_extracted\models\heroes\windrunner")
wr_base = os.path.join(base_dir, r"extracted\gltf\windrunner\models\heroes\windrunner\windrunner.glb")

before_objs = set(bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=wr_base)
base_objs = set(bpy.context.scene.objects) - before_objs
wr_arm = next(obj for obj in base_objs if obj.type == 'ARMATURE')
wr_base_meshes = [obj for obj in base_objs if obj.type == 'MESH' and obj.name != 'Icosphere']

def bone_world_head(arm, bone_name):
    b = arm.data.bones[bone_name]
    return arm.matrix_world @ b.head_local

arc_pelvis = bone_world_head(arc_arm, "pelvis")
arc_head = bone_world_head(arc_arm, "head")
wr_root = bone_world_head(wr_arm, "root")
wr_head = bone_world_head(wr_arm, "head")

scale_factor = abs(arc_head.z - arc_pelvis.z) / max(0.001, abs(wr_head.z - wr_root.z))
print(f"Scale factor: {scale_factor:.4f}")
wr_arm.scale = wr_arm.scale * scale_factor
bpy.context.view_layer.update()
wr_arm.location += (arc_pelvis - bone_world_head(wr_arm, "root"))
bpy.context.view_layer.update()

for m in wr_base_meshes:
    if m.data.shape_keys:
        for kb in list(m.data.shape_keys.key_blocks):
            m.shape_key_remove(kb)
    for mod in list(m.modifiers):
        if mod.type == 'ARMATURE':
            bpy.context.view_layer.objects.active = m
            bpy.ops.object.modifier_apply(modifier=mod.name)

BONE_MAP = {
    "root": "pelvis",
    "spine2": "spine_1",
    "spine2_helper": "spine_1",
    "spine3": "spine_3",
    "neck1": "neck_0",
    "head": "head",
    "clavicle_L": "clavicle_L",
    "bicep_L": "arm_upper_L",
    "elbow_L": "arm_lower_L",
    "elbow_L_helper": "arm_lower_L",
    "forearm_jnt": "arm_lower_L",
    "forearm_jnt_helper": "arm_lower_L",
    "wrist_L": "hand_L",
    "wrist_L_helper": "hand_L",
    "clavicle_R": "clavicle_R",
    "bicep_R": "arm_upper_R",
    "elbow_R": "arm_lower_R",
    "elbow_R_helper": "arm_lower_R",
    "wrist_R": "hand_R",
    "wrist_R_helper": "hand_R",
    "thumb_0_R": "hand_R",
    "thumb_1_R": "hand_R",
    "mid_0_R": "hand_R",
    "mid_1_R": "hand_R",
    "ring_0_R": "hand_R",
    "ring_1_R": "hand_R",
    "thigh_L": "leg_upper_L",
    "thigh_L_helper": "leg_upper_L",
    "knee_L": "leg_lower_L",
    "knee_L_helper": "leg_lower_L",
    "ankle_L": "ankle_L",
    "ankle_L_helper": "ankle_L",
    "toeBase_L": "ankle_L",
    "toeBase_L_helper": "ankle_L",
    "thigh_R": "leg_upper_R",
    "thigh_R_helper": "leg_upper_R",
    "knee_R": "leg_lower_R",
    "knee_R_helper": "leg_lower_R",
    "ankle_R": "ankle_R",
    "ankle_R_helper": "ankle_R",
    "toeBase_R": "ankle_R",
    "toeBase_R_helper": "ankle_R",
}

for m in wr_base_meshes:
    acc = {}
    nverts = len(m.data.vertices)
    for g in list(m.vertex_groups):
        target = BONE_MAP.get(g.name)
        if not target:
            # Match heuristics
            if "arm" in g.name.lower() or "bicep" in g.name.lower():
                target = "arm_upper_L" if "_L" in g.name else "arm_upper_R"
            elif "elbow" in g.name.lower() or "forearm" in g.name.lower():
                target = "arm_lower_L" if "_L" in g.name else "arm_lower_R"
            elif "wrist" in g.name.lower() or "hand" in g.name.lower() or "finger" in g.name.lower() or "thumb" in g.name.lower() or "mid" in g.name.lower() or "ring" in g.name.lower():
                target = "hand_L" if "_L" in g.name else "hand_R"
            elif "thigh" in g.name.lower():
                target = "leg_upper_L" if "_L" in g.name else "leg_upper_R"
            elif "knee" in g.name.lower():
                target = "leg_lower_L" if "_L" in g.name else "leg_lower_R"
            elif "ankle" in g.name.lower() or "toe" in g.name.lower():
                target = "ankle_L" if "_L" in g.name else "ankle_R"
            elif "head" in g.name.lower() or "neck" in g.name.lower():
                target = "head"
            elif "spine" in g.name.lower():
                target = "spine_2"
            else:
                target = "spine_1"
        arr = acc.setdefault(target, np.zeros(nverts))
        for v in m.data.vertices:
            for vg in v.groups:
                if vg.group == g.index:
                    arr[v.index] += vg.weight
    m.vertex_groups.clear()
    for name, arr in acc.items():
        vg = m.vertex_groups.new(name=name)
        for i in np.nonzero(arr > 1e-4)[0]:
            vg.add([int(i)], float(arr[i]), "REPLACE")

mat_base = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_base.vmat")
mat_hair = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_hair.vmat")
mat_cape = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_head.vmat")
mat_shoulders = bpy.data.materials.new(name="models/heroes_staging/grey_talon/materials/windranger_arcana_armor_style1.vmat")
mat_quiver = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_arrow.vmat")
mat_bow = bpy.data.materials.new(name="models/heroes_staging/archer/materials/windranger_arcana_bow.vmat")

for m in wr_base_meshes:
    m.data.materials.clear()
    m.data.materials.append(mat_base)

part_assignments = [
    ("windrunner_head.glb", "head", mat_hair),
    ("windrunner_cape.glb", "spine_3", mat_cape),
    ("windrunner_shoulderpads.glb", "spine_3", mat_shoulders),
    ("windrunner_quiver.glb", "quiver", mat_quiver),
    ("windrunner_bow.glb", "weaponHier_JNT", mat_bow),
]

all_pieces = list(wr_base_meshes)
for fname, target_bone, part_mat in part_assignments:
    fpath = os.path.join(wr_dir, fname)
    if not os.path.exists(fpath):
        continue
    curr_before = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=fpath)
    new_m = next(o for o in set(bpy.context.scene.objects) - curr_before if o.type == 'MESH')
    new_m.scale = new_m.scale * scale_factor
    new_m.location += (arc_pelvis - bone_world_head(wr_arm, "root"))
    bpy.context.view_layer.objects.active = new_m
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    new_m.data.materials.clear()
    new_m.data.materials.append(part_mat)
    
    vg = new_m.vertex_groups.new(name=target_bone)
    all_indices = list(range(len(new_m.data.vertices)))
    vg.add(all_indices, 1.0, "REPLACE")
    all_pieces.append(new_m)

bpy.ops.object.select_all(action="DESELECT")
for m in all_pieces:
    m.select_set(True)
bpy.context.view_layer.objects.active = all_pieces[0]
bpy.ops.object.join()
joined = bpy.context.view_layer.objects.active
joined.name = "windrunner_classic_body"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Guarantee every vertex has at least one valid group weight
vg_spine = joined.vertex_groups.get("spine_2") or joined.vertex_groups.new(name="spine_2")
for v in joined.data.vertices:
    total_w = sum(g.weight for g in v.groups if g.weight > 1e-4)
    if total_w < 1e-4:
        vg_spine.add([v.index], 1.0, "REPLACE")

bpy.ops.object.vertex_group_limit_total(group_select_mode="ALL", limit=4)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)

unweighted = [v.index for v in joined.data.vertices if not [g for g in v.groups if g.weight > 1e-4]]
print(f"Unweighted vertices after assignment: {len(unweighted)}")

joined.parent = arc_arm
joined.matrix_parent_inverse = arc_arm.matrix_world.inverted()
joined.modifiers.new("Armature", "ARMATURE").object = arc_arm

for m in arc_meshes:
    bpy.data.objects.remove(m)
bpy.data.objects.remove(wr_arm)

out_npz = os.path.join(base_dir, r"extracted\windrunner_classic_mesh.npz")
n_verts = export_npz(joined, arc_arm, out_npz)
print(f"[EXITO] Malla clasica exportada a {out_npz} ({n_verts} vertices).")

out_blend = os.path.join(base_dir, r"extracted\windrunner_on_archer.blend")
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print(f"[EXITO] Guardado en {out_blend}")
